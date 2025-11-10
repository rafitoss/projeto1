/* ========================================
   🌙 Tema Escuro Persistente
======================================== */
const htmlEl = document.documentElement;
const toggleBtn = document.getElementById("toggleDark");
if (toggleBtn) {
  if (localStorage.getItem("tema") === "dark") htmlEl.classList.add("dark");
  toggleBtn.addEventListener("click", () => {
    htmlEl.classList.toggle("dark");
    localStorage.setItem("tema", htmlEl.classList.contains("dark") ? "dark" : "light");
  });
}

/* ========================================
   🔐 LOGIN E LOGOUT
======================================== */
const loginForm = document.getElementById("loginForm");
const logoutBtn = document.getElementById("logoutBtn");

if (loginForm) {
  loginForm.addEventListener("submit", async e => {
    e.preventDefault();
    const usuario = document.getElementById("usuario").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const msg = document.getElementById("loginMsg");

    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, senha }),
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("logado", "true");
      msg.textContent = "Login realizado com sucesso!";
      msg.className = "text-green-600";
      setTimeout(() => (window.location.href = "menu.html"), 800);
    } else {
      msg.textContent = data.error || "Falha no login.";
      msg.className = "text-red-600";
    }
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    await fetch("/api/logout", { method: "POST" });
    localStorage.removeItem("logado");
    window.location.href = "index.html";
  });
}

/* ========================================
   💾 Queries / ⚙️ Processos - Placeholder
======================================== */
const queryContainer = document.getElementById("queryContainer");
const processoContainer = document.getElementById("processoContainer");

if (queryContainer) {
  queryContainer.innerHTML = `
    <button id="btnNovaQuery" class="btn-primary">➕ Nova Query</button>
    <div id="listaQueries" class="text-center text-gray-500 mt-4">Carregando...</div>
  `;
}

if (processoContainer) {
  processoContainer.innerHTML = `
    <button id="btnNovoProc" class="btn-primary">➕ Novo Processo</button>
    <div id="listaProcessos" class="text-center text-gray-500 mt-4">Carregando...</div>
  `;
}
