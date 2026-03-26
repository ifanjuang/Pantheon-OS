"""Génère le HTML de l'interface de configuration."""


def render_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OS Projet — Configuration</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- CodeMirror 6 -->
  <script type="module">
    import { EditorView, basicSetup } from 'https://esm.sh/codemirror@6.0.1';
    import { StreamLanguage } from 'https://esm.sh/@codemirror/language@6.10.6';
    import { yaml } from 'https://esm.sh/@codemirror/legacy-modes@6.4.2/mode/yaml';
    import { oneDark } from 'https://esm.sh/@codemirror/theme-one-dark@6.1.2';

    // ── État ────────────────────────────────────────────────────
    let editor = null;
    let currentModule = null;
    let dirty = false;

    // ── JWT (stocké en sessionStorage après login) ───────────────
    function getToken() { return sessionStorage.getItem('token') || ''; }
    function headers() {
      return { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + getToken() };
    }

    // ── Initialiser CodeMirror ───────────────────────────────────
    function initEditor(content) {
      const container = document.getElementById('editor-container');
      container.innerHTML = '';
      editor = new EditorView({
        doc: content,
        extensions: [
          basicSetup,
          StreamLanguage.define(yaml),
          oneDark,
          EditorView.updateListener.of(update => {
            if (update.docChanged) { dirty = true; updateSaveBtn(); }
          }),
          EditorView.theme({ '&': { height: '100%', fontSize: '13px' } }),
        ],
        parent: container,
      });
    }

    function getEditorContent() {
      return editor ? editor.state.doc.toString() : '';
    }

    function setEditorContent(content) {
      if (!editor) { initEditor(content); return; }
      editor.dispatch({
        changes: { from: 0, to: editor.state.doc.length, insert: content }
      });
      dirty = false;
      updateSaveBtn();
    }

    // ── UI helpers ───────────────────────────────────────────────
    function toast(msg, type = 'success') {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.className = `fixed bottom-4 right-4 px-4 py-2 rounded shadow-lg text-white text-sm transition-opacity
        ${type === 'success' ? 'bg-green-600' : 'bg-red-600'}`;
      t.style.opacity = '1';
      setTimeout(() => { t.style.opacity = '0'; }, 3000);
    }

    function updateSaveBtn() {
      const btn = document.getElementById('btn-save');
      if (!btn) return;
      btn.disabled = !dirty;
      btn.className = dirty
        ? 'px-4 py-2 rounded text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white cursor-pointer'
        : 'px-4 py-2 rounded text-sm font-medium bg-gray-600 text-gray-400 cursor-not-allowed';
    }

    function setTitle(name) {
      document.getElementById('editor-title').textContent = name === '__modules__'
        ? 'modules.yaml — Registre global'
        : `modules/${name}/config.yaml`;
    }

    // ── Login ────────────────────────────────────────────────────
    async function login(email, password) {
      const r = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!r.ok) throw new Error('Identifiants invalides');
      const data = await r.json();
      sessionStorage.setItem('token', data.access_token);
    }

    // ── Charger liste modules ────────────────────────────────────
    async function loadModules() {
      const r = await fetch('/admin/modules', { headers: headers() });
      if (r.status === 401) { showLogin(); return; }
      const modules = await r.json();
      renderModuleList(modules);
    }

    function renderModuleList(modules) {
      const list = document.getElementById('module-list');
      list.innerHTML = '';

      // Entrée spéciale modules.yaml
      list.appendChild(makeItem({
        name: '__modules__',
        enabled: true,
        has_config: true,
        description: 'Registre global des modules',
      }));

      modules.forEach(m => list.appendChild(makeItem(m)));
    }

    function makeItem(m) {
      const div = document.createElement('div');
      const isSpecial = m.name === '__modules__';
      div.className = `flex items-center gap-2 px-3 py-2 rounded cursor-pointer hover:bg-gray-700
        ${currentModule === m.name ? 'bg-gray-700 border-l-2 border-blue-400' : ''}`;

      // Toggle switch (sauf modules.yaml)
      if (!isSpecial) {
        const toggle = document.createElement('button');
        toggle.title = m.enabled ? 'Désactiver' : 'Activer';
        toggle.className = `w-8 h-4 rounded-full transition-colors flex-shrink-0
          ${m.enabled ? 'bg-green-500' : 'bg-gray-500'}`;
        toggle.addEventListener('click', async (e) => {
          e.stopPropagation();
          await toggleModule(m.name, !m.enabled);
        });
        div.appendChild(toggle);
      } else {
        const icon = document.createElement('span');
        icon.textContent = '⚙';
        icon.className = 'text-blue-400 text-xs flex-shrink-0 w-8 text-center';
        div.appendChild(icon);
      }

      const label = document.createElement('div');
      label.className = 'min-w-0';
      label.innerHTML = `
        <div class="text-sm font-medium text-gray-100 truncate">${isSpecial ? 'modules.yaml' : m.name}</div>
        ${m.description ? `<div class="text-xs text-gray-400 truncate">${m.description}</div>` : ''}
      `;
      div.appendChild(label);

      if (m.has_config || isSpecial) {
        div.addEventListener('click', () => selectModule(m.name));
      } else {
        div.title = 'Pas de config.yaml';
        label.querySelector('div').className += ' text-gray-500';
      }

      div.id = `item-${m.name}`;
      return div;
    }

    async function toggleModule(name, enabled) {
      const r = await fetch(`/admin/modules/${name}/toggle`, {
        method: 'POST',
        headers: headers(),
        body: JSON.stringify({ enabled }),
      });
      if (r.ok) {
        toast(`Module '${name}' ${enabled ? 'activé' : 'désactivé'}`);
        await loadModules();
      } else {
        toast('Erreur lors du toggle', 'error');
      }
    }

    // ── Charger config d'un module ───────────────────────────────
    async function selectModule(name) {
      currentModule = name;

      // Highlight
      document.querySelectorAll('#module-list > div').forEach(el => {
        el.classList.remove('bg-gray-700', 'border-l-2', 'border-blue-400');
      });
      const item = document.getElementById(`item-${name}`);
      if (item) item.classList.add('bg-gray-700', 'border-l-2', 'border-blue-400');

      const url = name === '__modules__' ? '/admin/config/modules' : `/admin/config/${name}`;
      const r = await fetch(url, { headers: headers() });
      if (!r.ok) { toast('Erreur chargement config', 'error'); return; }
      const data = await r.json();

      setTitle(name);
      setEditorContent(data.content || '');
      dirty = false;
      updateSaveBtn();

      document.getElementById('editor-panel').classList.remove('hidden');
    }

    // ── Sauvegarder ──────────────────────────────────────────────
    async function saveConfig() {
      if (!currentModule || !dirty) return;
      const content = getEditorContent();
      const url = currentModule === '__modules__'
        ? '/admin/config/modules'
        : `/admin/config/${currentModule}`;
      const r = await fetch(url, {
        method: 'PUT',
        headers: headers(),
        body: JSON.stringify({ content }),
      });
      const data = await r.json();
      if (r.ok) {
        toast('Configuration sauvegardée ✓');
        dirty = false;
        updateSaveBtn();
        if (currentModule === '__modules__') await loadModules();
      } else {
        toast(data.detail || 'Erreur sauvegarde', 'error');
      }
    }

    // ── Login form ───────────────────────────────────────────────
    function showLogin() {
      document.getElementById('login-overlay').classList.remove('hidden');
    }

    function hideLogin() {
      document.getElementById('login-overlay').classList.add('hidden');
    }

    // ── Init ─────────────────────────────────────────────────────
    window.addEventListener('DOMContentLoaded', async () => {
      if (!getToken()) { showLogin(); return; }
      await loadModules();

      document.getElementById('btn-save').addEventListener('click', saveConfig);

      document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        try {
          await login(email, password);
          hideLogin();
          await loadModules();
        } catch (err) {
          document.getElementById('login-error').textContent = err.message;
        }
      });

      document.getElementById('btn-logout').addEventListener('click', () => {
        sessionStorage.removeItem('token');
        showLogin();
      });

      // Raccourci clavier Ctrl+S / Cmd+S
      document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
          e.preventDefault();
          saveConfig();
        }
      });
    });
  </script>
  <style>
    .cm-editor { height: 100%; }
    .cm-scroller { overflow: auto; height: 100%; }
  </style>
</head>
<body class="bg-gray-900 text-gray-100 h-screen flex flex-col overflow-hidden">

  <!-- Header -->
  <header class="bg-gray-800 border-b border-gray-700 px-4 py-3 flex items-center justify-between flex-shrink-0">
    <div class="flex items-center gap-3">
      <span class="text-blue-400 font-bold text-lg">OS Projet</span>
      <span class="text-gray-500 text-sm">/ Configuration</span>
    </div>
    <div class="flex items-center gap-3">
      <button id="btn-save" disabled
        class="px-4 py-2 rounded text-sm font-medium bg-gray-600 text-gray-400 cursor-not-allowed">
        Sauvegarder <span class="text-xs opacity-60 ml-1">Ctrl+S</span>
      </button>
      <button id="btn-logout"
        class="px-3 py-2 rounded text-sm text-gray-400 hover:text-gray-200 hover:bg-gray-700">
        Déconnexion
      </button>
    </div>
  </header>

  <!-- Main -->
  <div class="flex flex-1 overflow-hidden">

    <!-- Sidebar modules -->
    <aside class="w-64 bg-gray-800 border-r border-gray-700 flex flex-col flex-shrink-0">
      <div class="px-3 py-3 border-b border-gray-700">
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Modules</p>
        <p class="text-xs text-gray-500 mt-1">Cliquer pour éditer la config</p>
      </div>
      <div id="module-list" class="flex-1 overflow-y-auto py-2 space-y-0.5 px-1">
        <div class="text-gray-500 text-sm px-3 py-2">Chargement…</div>
      </div>
    </aside>

    <!-- Éditeur -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Placeholder quand rien n'est sélectionné -->
      <div id="editor-panel" class="hidden flex-1 flex flex-col overflow-hidden">
        <div class="bg-gray-800 border-b border-gray-700 px-4 py-2 flex items-center justify-between flex-shrink-0">
          <span id="editor-title" class="text-sm font-mono text-gray-300"></span>
          <span class="text-xs text-gray-500">YAML</span>
        </div>
        <div id="editor-container" class="flex-1 overflow-hidden"></div>
      </div>

      <div id="editor-placeholder" class="flex-1 flex items-center justify-center text-gray-600">
        <div class="text-center">
          <div class="text-4xl mb-3">⚙️</div>
          <p class="text-lg font-medium text-gray-500">Sélectionner un module</p>
          <p class="text-sm mt-1">Cliquer sur un module dans la liste pour éditer sa configuration</p>
        </div>
      </div>
    </main>
  </div>

  <!-- Toast -->
  <div id="toast" class="fixed bottom-4 right-4 px-4 py-2 rounded shadow-lg text-white text-sm opacity-0 transition-opacity bg-green-600 pointer-events-none"></div>

  <!-- Login overlay -->
  <div id="login-overlay" class="hidden fixed inset-0 bg-gray-900 bg-opacity-95 flex items-center justify-center z-50">
    <div class="bg-gray-800 border border-gray-700 rounded-xl p-8 w-full max-w-sm shadow-2xl">
      <h2 class="text-xl font-bold mb-1 text-gray-100">OS Projet</h2>
      <p class="text-sm text-gray-400 mb-6">Connexion administrateur</p>
      <form id="login-form" class="space-y-4">
        <div>
          <label class="block text-xs text-gray-400 mb-1">Email</label>
          <input id="login-email" type="email" autocomplete="email"
            class="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-sm text-gray-100 focus:outline-none focus:border-blue-500"
            placeholder="admin@agence.fr" required>
        </div>
        <div>
          <label class="block text-xs text-gray-400 mb-1">Mot de passe</label>
          <input id="login-password" type="password" autocomplete="current-password"
            class="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-sm text-gray-100 focus:outline-none focus:border-blue-500"
            required>
        </div>
        <p id="login-error" class="text-red-400 text-xs min-h-[1rem]"></p>
        <button type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white rounded py-2 text-sm font-medium transition-colors">
          Connexion
        </button>
      </form>
    </div>
  </div>

  <script type="module">
    // Afficher l'éditeur quand un module est sélectionné, cacher le placeholder
    const observer = new MutationObserver(() => {
      const panel = document.getElementById('editor-panel');
      const placeholder = document.getElementById('editor-placeholder');
      if (panel && placeholder) {
        const hidden = panel.classList.contains('hidden');
        placeholder.style.display = hidden ? 'flex' : 'none';
      }
    });
    const panel = document.getElementById('editor-panel');
    if (panel) observer.observe(panel, { attributes: true });
  </script>

</body>
</html>"""
