"""Official Meta Instagram Graph API (v27.0) Resumable Reels Publisher.

Used automatically by publish_all.py when IG_USER_ID and IG_ACCESS_TOKEN are configured in .env,
the episode duration is within the Graph API Reels-tab ceiling (5s..90s), and UI-only AI disclosure
is not required. Episodes above 90s or requiring UI toggles dispatch through Meta Business Suite.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH_API_VERSION = "v22.0"


def _load_ig_credentials() -> tuple[str, str]:
    """Read IG_USER_ID and IG_ACCESS_TOKEN from environment or .env without printing secrets."""
    ig_user_id = os.environ.get("IG_USER_ID", "").strip()
    ig_token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    env_file = REPO_ROOT / ".env"
    if env_file.exists() and (not ig_user_id or not ig_token):
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "IG_USER_ID" and not ig_user_id:
                ig_user_id = v
            elif k == "IG_ACCESS_TOKEN" and not ig_token:
                ig_token = v
    return ig_user_id, ig_token


def has_ig_graph_ready() -> bool:
    uid, tok = _load_ig_credentials()
    return bool(uid and tok)


def upload_reel_graph_api(video_path: Path, caption: str, timeout_s: int = 300) -> dict[str, Any]:
    """Publish an Instagram Reel via official Resumable Upload protocol (rupload.facebook.com)."""
    ig_user_id, access_token = _load_ig_credentials()
    if not ig_user_id or not access_token:
        raise RuntimeError("IG_USER_ID e IG_ACCESS_TOKEN ausentes no ambiente/.env.")

    file_size = video_path.stat().st_size

    # Step 1: Initialize resumable REELS container
    init_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_user_id}/media"
    init_payload = urllib.parse.urlencode(
        {
            "upload_type": "resumable",
            "media_type": "REELS",
            "caption": caption[:2200],
            "share_to_feed": "true",
            "access_token": access_token,
        }
    ).encode("utf-8")
    init_req = urllib.request.Request(init_url, data=init_payload, method="POST")
    with urllib.request.urlopen(init_req, timeout=30) as resp:
        init_data = json.loads(resp.read().decode("utf-8"))

    container_id = init_data["id"]
    upload_uri = init_data["uri"]

    # Step 2: Upload raw MP4 bytes to rupload.facebook.com
    video_bytes = video_path.read_bytes()
    up_req = urllib.request.Request(
        upload_uri,
        data=video_bytes,
        method="POST",
        headers={
            "Authorization": f"OAuth {access_token}",
            "offset": "0",
            "file_size": str(file_size),
            "Content-Type": "application/octet-stream",
        },
    )
    with urllib.request.urlopen(up_req, timeout=240) as up_resp:
        json.loads(up_resp.read().decode("utf-8"))

    # Step 3: Poll container status_code until FINISHED
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        st_url = (
            f"https://graph.facebook.com/{GRAPH_API_VERSION}/{container_id}"
            f"?fields=status_code,status&access_token={urllib.parse.quote(access_token)}"
        )
        with urllib.request.urlopen(st_url, timeout=20) as st_resp:
            st_data = json.loads(st_resp.read().decode("utf-8"))
        code = st_data.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise RuntimeError(f"Instagram Graph API retornou ERROR no container {container_id}: {st_data.get('status')}")
        time.sleep(5.0)
    else:
        raise TimeoutError(f"Timeout aguardando processamento do Reel {container_id} na Graph API.")

    # Step 4: Publish container and fetch permalink
    pub_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_user_id}/media_publish"
    pub_payload = urllib.parse.urlencode(
        {"creation_id": container_id, "access_token": access_token}
    ).encode("utf-8")
    pub_req = urllib.request.Request(pub_url, data=pub_payload, method="POST")
    with urllib.request.urlopen(pub_req, timeout=30) as pub_resp:
        pub_data = json.loads(pub_resp.read().decode("utf-8"))

    media_id = pub_data["id"]
    perm_url = (
        f"https://graph.facebook.com/{GRAPH_API_VERSION}/{media_id}"
        f"?fields=permalink&access_token={urllib.parse.quote(access_token)}"
    )
    permalink = ""
    try:
        with urllib.request.urlopen(perm_url, timeout=15) as perm_resp:
            permalink = json.loads(perm_resp.read().decode("utf-8")).get("permalink", "")
    except Exception:
        permalink = f"https://www.instagram.com/reel/{media_id}/"

    return {"platform": "instagram", "method": "graph_api", "published": True, "id": media_id, "url": permalink}
