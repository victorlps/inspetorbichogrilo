(function () {
  const catalogEl = document.getElementById("catalog");
  const searchInput = document.getElementById("search-input");
  const resultCount = document.getElementById("result-count");

  let items = [];

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function render(filterText) {
    const q = (filterText || "").trim().toLowerCase();
    const filtered = items.filter((item) => {
      if (!item.ativo) return false;
      if (!q) return true;
      const haystack = [
        item.codigo,
        item.titulo,
        item.resumo,
        ...(item.tags || []),
      ]
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });

    resultCount.textContent =
      filtered.length === 1
        ? "1 produto verificado encontrado"
        : `${filtered.length} produtos verificados encontrados`;

    if (filtered.length === 0) {
      catalogEl.innerHTML =
        '<div class="empty-state">Nenhum produto encontrado para essa busca. Tente o código do vídeo (ex.: <strong>IBG-001</strong>).</div>';
      return;
    }

    catalogEl.innerHTML = filtered
      .map((item) => {
        const variantsHtml = (item.variacoes || [])
          .map(
            (v) => `
            <a class="variant-btn" href="${escapeHtml(v.url)}" target="_blank" rel="noopener noreferrer nofollow">
              <span class="variant-title">${escapeHtml(v.rotulo)} →</span>
              <span class="variant-meta">${escapeHtml(v.loja)} · ${escapeHtml(v.especificacao)}</span>
            </a>`
          )
          .join("");

        const noteHtml = item.nota_tecnica
          ? `<div class="note-box">🛠️ ${escapeHtml(item.nota_tecnica)}</div>`
          : "";

        return `
          <article class="card" id="${escapeHtml(item.codigo)}">
            <div class="card-header">
              <span class="code-badge">${escapeHtml(item.codigo)}</span>
              ${item.avaliacao ? `<span class="rating">${escapeHtml(item.avaliacao)}</span>` : ""}
            </div>
            <h2>${escapeHtml(item.titulo)}</h2>
            <p class="summary">${escapeHtml(item.resumo)}</p>
            <div class="variants">${variantsHtml}</div>
            ${noteHtml}
          </article>
        `;
      })
      .join("");
  }

  fetch("catalogo.json", { cache: "no-store" })
    .then((res) => res.json())
    .then((data) => {
      items = Array.isArray(data.produtos) ? data.produtos : [];
      const params = new URLSearchParams(window.location.search);
      const initialCode = params.get("c") || "";
      if (initialCode) {
        searchInput.value = initialCode;
      }
      render(searchInput.value);
    })
    .catch(() => {
      catalogEl.innerHTML =
        '<div class="empty-state">Não foi possível carregar o catálogo no momento.</div>';
    });

  searchInput.addEventListener("input", (e) => {
    render(e.target.value);
  });
})();
