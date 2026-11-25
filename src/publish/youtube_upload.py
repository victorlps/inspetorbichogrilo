"""Official YouTube Data API v3 uploader for Inspetor Bicho Grilo Shorts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_CHANNEL_ID = "UCgIp02Q0H3rXsNwL-kDdFbA"  # @inspetorbichogrilo
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def _resolve_oauth_paths() -> tuple[Path, Path]:
    """Resolve client_secrets and token paths from env/.env without logging credentials."""
    secrets_path = os.environ.get("YOUTUBE_CLIENT_SECRETS", "").strip()
    token_path = os.environ.get("YOUTUBE_TOKEN_PATH", "").strip()
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "YOUTUBE_CLIENT_SECRETS" and not secrets_path:
                secrets_path = v
            elif k == "YOUTUBE_TOKEN_PATH" and not token_path:
                token_path = v
    sec = Path(secrets_path) if secrets_path else (REPO_ROOT / ".env.youtube_client_secret.json")
    tok = Path(token_path) if token_path else (REPO_ROOT / ".env.youtube_token.json")
    if not sec.is_absolute():
        sec = REPO_ROOT / sec
    if not tok.is_absolute():
        tok = REPO_ROOT / tok
    return sec, tok


def get_youtube_service() -> Any:
    """Authenticate via OAuth 2.0 desktop flow and return YouTube Data API v3 client."""
    secrets_path, token_path = _resolve_oauth_paths()
    if not secrets_path.exists():
        raise FileNotFoundError(
            f"OAuth client secrets não encontrado em {secrets_path.name}. "
            "Baixe do Google Cloud Console (YouTube Data API v3) e salve como .env.youtube_client_secret.json."
        )

    creds: Credentials | None = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    return build("youtube", "v3", credentials=creds)


def upload_short(
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
    privacy: str = "private",
    contains_synthetic_media: bool = True,
) -> dict[str, Any]:
    """Upload a vertical Short via YouTube Data API v3."""
    if not video_path.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")

    youtube = get_youtube_service()
    ch_resp = youtube.channels().list(part="snippet", mine=True).execute()
    channels = ch_resp.get("items", [])
    active_id = channels[0]["id"] if channels else ""
    active_title = channels[0]["snippet"]["title"] if channels else "desconhecido"
    if active_id != EXPECTED_CHANNEL_ID:
        raise RuntimeError(
            f"Canal OAuth incorreto: '{active_title}' ({active_id}). "
            f"Esperado: 'Inspetor Bicho Grilo' ({EXPECTED_CHANNEL_ID}). "
            "Apague .env.youtube_token.json e selecione o canal Inspetor Bicho Grilo na tela OAuth."
        )
    body: dict[str, Any] = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "28",  # Science & Technology
            "defaultLanguage": "pt-BR",
            "defaultAudioLanguage": "pt-BR",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": contains_synthetic_media,
        },
    }

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload YouTube: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    print(f"OK YouTube upload concluído: https://youtube.com/shorts/{video_id} (status={privacy})")
    return response


def has_youtube_oauth_ready() -> bool:
    """Return True when both OAuth client secret and saved user/channel token exist on disk."""
    sec, tok = _resolve_oauth_paths()
    return sec.exists() and tok.exists()


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload vertical Short to YouTube via Data API v3.")
    parser.add_argument("--auth-only", action="store_true", help="Executa apenas o fluxo OAuth único e valida o canal Inspetor Bicho Grilo.")
    parser.add_argument("--video", type=Path, default=None)
    parser.add_argument("--title", type=str, default="")
    parser.add_argument("--description-file", type=Path, default=None)
    parser.add_argument("--tags", type=str, default="ComoFunciona,Ciencia,Engenharia,InspetorBichoGrilo,Shorts")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--no-synthetic", action="store_true")
    args = parser.parse_args()

    if args.auth_only:
        yt = get_youtube_service()
        ch_resp = yt.channels().list(part="snippet", mine=True).execute()
        items = ch_resp.get("items", [])
        cid = items[0]["id"] if items else ""
        ctitle = items[0]["snippet"]["title"] if items else ""
        if cid != EXPECTED_CHANNEL_ID:
            raise SystemExit(f"Canal OAuth selecionado ({ctitle} / {cid}) difere de {EXPECTED_CHANNEL_ID}.")
        print(json.dumps({"authenticated": True, "channel_id": cid, "title": ctitle}, ensure_ascii=False))
        return

    if not args.video or not args.title or not args.description_file:
        parser.error("--video, --title e --description-file são obrigatórios exceto com --auth-only.")

    desc = args.description_file.read_text(encoding="utf-8")
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    res = upload_short(
        video_path=args.video,
        title=args.title,
        description=desc,
        tags=tags,
        privacy=args.privacy,
        contains_synthetic_media=not args.no_synthetic,
    )
    print(json.dumps({"id": res.get("id"), "privacy": args.privacy}, ensure_ascii=False))


if __name__ == "__main__":
    main()
