// ============================================================
//  static/js/atlas.js
//  ATLAS Universal Bot Platform — Single Page Application Engine
//  Shaxsiy Markaziy Boshqaruv & Hujjatlar Arxiv Tizimi
//  NO EMOJIS — 100% SVG Vector UI & Dynamic REST API Client
// ============================================================

const ATLAS = {
  token: localStorage.getItem('atlas_token') || '',
  user: JSON.parse(localStorage.getItem('atlas_user') || 'null'),
  currentRoute: 'documents', // Asosiy fokus hujjatlar va bot boshqaruvi
  activeDocTab: 'generate',  // 'generate' yoki 'archiv  // Professional SVG Icon Library (Strictly Zero Emojis)
  icons: {
    dashboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg>`,
    documents: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`,
    archive: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/></svg>`,
    users: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
    groups: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
    messages: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
    automation: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    tasks: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    analytics: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
    logs: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>`,
    settings: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`,
    modules: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`,
    search: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
    bell: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`,
    logout: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>`,
    check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="20 6 9 17 4 12"/></svg>`,
    alert: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
    send: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>`,
    download: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
    plus: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
    trash: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>`,
    refresh: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>`,
    user: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
    lock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`,
    eye: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`,
    eyeOff: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>`,
    edit: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>`,
    chevronDown: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="6 9 12 15 18 9"/></svg>`,
    brandLogo: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 15 L78 68 C82 75 76 85 68 85 L56 85 C51 85 47 81 49 76 L62 48 C63 45 61 42 58 42 L42 42 C39 42 37 45 38 48 L46 65 C48 70 44 75 39 75 L32 75 C25 75 20 67 24 60 Z"/></svg>`
  },

  // API Wrapper
  async api(endpoint, method = 'GET', body = null) {
    const headers = { 'Content-Type': 'application/json' };
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

    try {
      const res = await fetch(endpoint, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
      });

      if (res.status === 401 && this.currentRoute !== 'login') {
        this.logout();
        return null;
      }

      return await res.json();
    } catch (err) {
      console.error('API Error:', err);
      this.toast('Server bilan aloqa uzildi', 'error');
      return null;
    }
  },

  // Toast Notification System
  toast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const el = document.createElement('div');
    el.className = `toast toast-${type}`;
    const icon = type === 'success' ? this.icons.check : (type === 'error' ? this.icons.alert : this.icons.bell);
    el.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(el);

    setTimeout(() => {
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 300);
    }, 3500);
  },

  // Init Application
  init() {
    this.bindGlobalEvents();
    if (!this.token || !this.user) {
      this.renderLogin();
    } else {
      this.renderApp();
      this.navigate(this.currentRoute);
    }
  },

  bindGlobalEvents() {
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        this.openGlobalSearch();
      }
      if (e.key === 'Escape') {
        this.closeModal();
      }
    });
  },

  // Router
  navigate(route) {
    this.currentRoute = route;

    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });
    document.querySelectorAll('.nav-sub-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });

    const isDocSubRoute = route.startsWith('doc_');
    const docGroupHeader = document.getElementById('nav-header-docs');
    if (docGroupHeader) {
      docGroupHeader.classList.toggle('active', route === 'documents' || isDocSubRoute);
    }

    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
      const titles = {
        documents: 'Ma\'lumotnomalar & Buyruqlar Arxivi',
        doc_qabul_1_kurs: '1-kursga Qabul Ma\'lumotnomasi',
        doc_oqiyapti: 'O\'qiyotganligi Haqida Ma\'lumotnoma',
        doc_buyruq_akademik_tatil: 'Akademik Ta\'til Berish Buyrug\'i',
        doc_buyruq_qayta_tiklash: 'Akademik Ta\'tildan Qayta Tiklash Buyrug\'i',
        doc_buyruq_guruhdan_guruhga: 'Guruhdan Guruhga O\'tkazish Buyrug\'i',
        doc_buyruq_safidan_chiqarish: 'Talabalar Safidan Chiqarish Buyrug\'i',
        dashboard: 'Boshqaruv Paneli',
        academic_groups: 'O\'quv Guruhlari Boshqaruvi',
        users: 'Foydalanuvchilar Boshqaruvi',
        groups: 'Ulangan Guruhlar va Kanallar',
        messages: 'Xabarlar va Tarqatish',
        automation: 'Avtomatlashtirish',
        tasks: 'Fon Vazifalari',
        analytics: 'Statistika va Tahlil',
        logs: 'Tizim Loglari',
        settings: 'Bot va Tizim Sozlamalari',
        modules: 'Modullar Boshqaruvi'
      };
      pageTitle.innerText = titles[route] || 'ATLAS Boshqaruv Markazi';
    }

    const viewport = document.getElementById('content-viewport');
    if (!viewport) return;

    if (isDocSubRoute) {
      const tpl_id = route.replace('doc_', '');
      this.activeDocTab = 'generate';
      this.loadDocuments(viewport, tpl_id);
    } else {
      switch (route) {
        case 'documents': this.loadDocuments(viewport); break;
        case 'academic_groups': this.loadGroups(viewport, 'academic'); break;
        case 'dashboard': this.loadDashboard(viewport); break;
        case 'users': this.loadUsers(viewport); break;
        case 'groups': this.loadGroups(viewport, 'telegram'); break;
        case 'messages': this.loadMessages(viewport); break;
        case 'automation': this.loadAutomation(viewport); break;
        case 'tasks': this.loadTasks(viewport); break;
        case 'analytics': this.loadAnalytics(viewport); break;
        case 'logs': this.loadLogs(viewport); break;
        case 'settings': this.loadSettings(viewport); break;
        case 'modules': this.loadModules(viewport); break;
        default: this.loadDocuments(viewport);
      }
    }
  },

  // ============================================================
  // AUTH / LOGIN VIEW
  // ============================================================
  renderLogin() {
    const root = document.getElementById('app-root');
    root.innerHTML = `
      <div class="auth-wrapper">
        <div class="auth-card">
          <div class="auth-logo">
            ${this.icons.brandLogo}
            <div class="auth-logo-text">ATLAS</div>
          </div>
          <h2 class="auth-title">Shaxsiy Boshqaruv Markazi</h2>
          <p class="auth-subtitle">Platformaga kirish uchun parolingizni kiriting</p>

          <form id="login-form">
            <div class="form-group">
              <label class="form-label">Foydalanuvchi nomi</label>
              <div class="input-container">
                <span class="input-icon-left">${this.icons.user}</span>
                <input type="text" id="login-username" class="input-control" placeholder="Loginni kiriting" required autocomplete="username">
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Maxfiy parol</label>
              <div class="input-container">
                <span class="input-icon-left">${this.icons.lock}</span>
                <input type="password" id="login-password" class="input-control" placeholder="Parolni kiriting" required autocomplete="current-password">
                <span class="input-icon-right" id="toggle-pwd-btn">${this.icons.eye}</span>
              </div>
            </div>

            <button type="submit" class="btn-primary btn-block" style="margin-top:24px;">
              <span>Tizimga kirish</span>
            </button>
          </form>

          <div style="margin-top:28px;font-size:11px;color:rgba(255,255,255,0.4);letter-spacing:0.08em;">ATLAS PRIVATE CONTROL v2.1.0</div>
        </div>
      </div>
    `;

    document.getElementById('toggle-pwd-btn').addEventListener('click', () => {
      const pwd = document.getElementById('login-password');
      const isPwd = pwd.type === 'password';
      pwd.type = isPwd ? 'text' : 'password';
      document.getElementById('toggle-pwd-btn').innerHTML = isPwd ? this.icons.eyeOff : this.icons.eye;
    });

    document.getElementById('login-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const u = document.getElementById('login-username').value;
      const p = document.getElementById('login-password').value;

      const res = await this.api('/api/auth/login', 'POST', { username: u, password: p });
      if (res && res.success) {
        this.token = res.token;
        this.user = res.user;
        localStorage.setItem('atlas_token', res.token);
        localStorage.setItem('atlas_user', JSON.stringify(res.user));
        this.toast('Muvaffaqiyatli kirdingiz', 'success');
        this.renderApp();
        this.navigate('documents');
      } else {
        this.toast(res ? res.error : 'Login xatosi', 'error');
      }
    });
  },

  logout() {
    this.api('/api/auth/logout', 'POST');
    this.token = '';
    this.user = null;
    localStorage.removeItem('atlas_token');
    localStorage.removeItem('atlas_user');
    this.renderLogin();
  },

  // ============================================================
  // APP SHELL
  // ============================================================
  renderApp() {
    const root = document.getElementById('app-root');
    root.innerHTML = `
      <div class="app-container">
        <!-- SIDEBAR -->
        <aside class="sidebar">
          <div class="sidebar-header">
            <div class="sidebar-logo-icon">${this.icons.brandLogo}</div>
            <div class="sidebar-brand-name">ATLAS</div>
            <div class="sidebar-brand-badge">PRO</div>
          </div>

          <nav class="sidebar-menu">
            <div class="sidebar-group-title">Hujjatlar & Buyruqlar</div>
            
            <!-- Expandable Accordion Menu -->
            <div class="nav-group open" id="nav-group-docs">
              <div class="nav-group-header" id="nav-header-docs">
                ${this.icons.documents} <span>Hujjatlar & Buyruqlar</span>
                <span class="nav-arrow">${this.icons.chevronDown}</span>
              </div>
              <div class="nav-sub-menu">
                <div class="nav-sub-item" data-route="doc_qabul_1_kurs">🎓 1-kursga qabul</div>
                <div class="nav-sub-item" data-route="doc_oqiyapti">📖 O'qiyotganligi haqida</div>
                <div class="nav-sub-item" data-route="doc_buyruq_akademik_tatil">📝 Akademik ta'til</div>
                <div class="nav-sub-item" data-route="doc_buyruq_qayta_tiklash">📝 Qayta tiklash</div>
                <div class="nav-sub-item" data-route="doc_buyruq_guruhdan_guruhga">📝 Guruh almashtirish</div>
                <div class="nav-sub-item" data-route="doc_buyruq_safidan_chiqarish">📝 Safidan chiqarish</div>
                <div class="nav-sub-item" data-route="documents">🗂️ Barcha Arxiv & Tarix</div>
              </div>
            </div>

            <div class="nav-item" data-route="dashboard">
              ${this.icons.dashboard} <span>Boshqaruv Paneli</span>
            </div>

            <div class="sidebar-group-title">O'quv Bo'limi & Bot Nazorati</div>
            <div class="nav-item" data-route="academic_groups">
              ${this.icons.groups} <span>O'quv Guruhlari</span>
            </div>
            <div class="nav-item" data-route="users">
              ${this.icons.users} <span>Foydalanuvchilar</span>
            </div>
            <div class="nav-item" data-route="groups">
              ${this.icons.groups} <span>Telegram Guruhlar</span>
            </div>
            <div class="nav-item" data-route="messages">
              ${this.icons.messages} <span>Xabarlar & E'lonlar</span>
            </div>
            <div class="nav-item" data-route="tasks">
              ${this.icons.tasks} <span>Fon Vazifalari</span>
            </div>
            <div class="nav-item" data-route="automation">
              ${this.icons.automation} <span>Avtomatlashtirish</span>
            </div>

            <div class="sidebar-group-title">Monitoring & Xavfsizlik</div>
            <div class="nav-item" data-route="analytics">
              ${this.icons.analytics} <span>Statistika & Tahlil</span>
            </div>
            <div class="nav-item" data-route="logs">
              ${this.icons.logs} <span>Tizim Loglari</span>
            </div>
            <div class="nav-item" data-route="modules">
              ${this.icons.modules} <span>Modullar</span>
            </div>
            <div class="nav-item" data-route="settings">
              ${this.icons.settings} <span>Sozlamalar</span>
            </div>
          </nav>

          <div class="sidebar-footer">
            <div class="user-avatar-badge">${(this.user?.full_name || 'A').charAt(0)}</div>
            <div class="user-info">
              <div class="user-name">${this.user?.full_name || 'Bosh Administrator'}</div>
              <div class="user-role">Shaxsiy Boshqaruv</div>
            </div>
            <button class="btn-logout" id="logout-btn" title="Chiqish">${this.icons.logout}</button>
          </div>
        </aside>

        <!-- MAIN WRAPPER -->
        <main class="main-wrapper">
          <header class="header">
            <div class="header-left">
              <h1 class="page-title" id="page-title">Ma'lumotnomalar & Hujjatlar Arxivi</h1>
              <div class="global-search-bar">
                <span class="search-icon-fixed">${this.icons.search}</span>
                <input type="text" id="global-search-input" placeholder="Tezkor qidirish...">
                <span class="search-shortcut">Ctrl+K</span>
              </div>
            </div>

            <div class="header-right">
              <div class="bot-live-pill">
                <div class="pulse-circle"></div>
                <span>BOT FAOL</span>
              </div>
              <button class="header-btn" id="refresh-view-btn" title="Yangilash">${this.icons.refresh}</button>
              <button class="header-btn" id="notif-btn" title="Bildirishnomalar">
                ${this.icons.bell}
              </button>
            </div>
          </header>

          <div class="content-body" id="content-viewport"></div>
        </main>
      </div>

      <!-- MODALS & TOAST -->
      <div class="modal-overlay" id="modal-container"></div>
      <div id="toast-container" class="toast-container"></div>
    `;

    // Accordion Toggle
    document.getElementById('nav-header-docs').addEventListener('click', () => {
      document.getElementById('nav-group-docs').classList.toggle('open');
    });

    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => this.navigate(btn.dataset.route));
    });

    document.querySelectorAll('.nav-sub-item').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.navigate(btn.dataset.route);
      });
    });

    document.getElementById('logout-btn').addEventListener('click', () => this.logout());
    document.getElementById('refresh-view-btn').addEventListener('click', () => this.navigate(this.currentRoute));
    document.getElementById('global-search-input').addEventListener('click', () => this.openGlobalSearch());
  },

  // ============================================================
  // 1. DOCUMENTS & PERMANENT ARCHIVE (ASOSIY BO'LIM)
  // ============================================================
  async loadDocuments(container, specificTplId = null) {
    container.innerHTML = `
      <div class="tab-pills-row">
        <button class="tab-pill-btn ${this.activeDocTab === 'generate' ? 'active' : ''}" id="tab-doc-gen">
          ${this.icons.plus} <span>${specificTplId ? 'Hujjatni Shakllantirish' : 'Yangi Hujjat Shakllantirish'}</span>
        </button>
        <button class="tab-pill-btn ${this.activeDocTab === 'archive' ? 'active' : ''}" id="tab-doc-arch">
          ${this.icons.archive} <span>${specificTplId ? 'Ushbu Hujjat Arxivi' : 'Barcha Hujjatlar Arxivi'}</span>
        </button>
      </div>

      <div id="doc-tab-content"></div>
    `;

    document.getElementById('tab-doc-gen').addEventListener('click', () => {
      this.activeDocTab = 'generate';
      this.loadDocuments(container, specificTplId);
    });

    document.getElementById('tab-doc-arch').addEventListener('click', () => {
      this.activeDocTab = 'archive';
      this.loadDocuments(container, specificTplId);
    });

    const contentBox = document.getElementById('doc-tab-content');
    if (this.activeDocTab === 'generate') {
      this.renderDocumentGenerator(contentBox, specificTplId);
    } else {
      this.renderDocumentArchive(contentBox, specificTplId || '');
    }
  },

  renderDocumentGenerator(container, specificTplId = null) {
    const todayStr = new Date().toLocaleDateString('ru-RU');
    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:24px;margin-bottom:24px;">
        <!-- Left: Input Form -->
        <div class="glass-card">
          <div class="card-header-flex">
            <div>
              <div class="card-title">Rasmiy Hujjatlar & Buyruqlar Generatori</div>
              <div class="card-subtitle">Ultra HD (300 DPI A4) rasm va asl Word (.docx) holida bir zumda shakllantirish</div>
            </div>
          </div>

          <form id="doc-gen-form">
            <div class="form-group">
              <label class="form-label">Hujjat / Buyruq Shablonini Tanlang</label>
              <select id="doc-tpl-select" class="select-control">
                <optgroup label="🎓 Ma'lumotnomalar">
                  <option value="qabul_1_kurs" ${specificTplId === 'qabul_1_kurs' ? 'selected' : ''}>🎓 1-kursga qabul ma'lumotnomasi</option>
                  <option value="oqiyapti" ${specificTplId === 'oqiyapti' ? 'selected' : ''}>📖 O'qiyotganligi haqida ma'lumotnoma</option>
                </optgroup>
                <optgroup label="📝 Rasmiy Buyruqlar">
                  <option value="buyruq_akademik_tatil" ${specificTplId === 'buyruq_akademik_tatil' ? 'selected' : ''}>📝 Akademik ta'til berish buyrug'i</option>
                  <option value="buyruq_qayta_tiklash" ${specificTplId === 'buyruq_qayta_tiklash' ? 'selected' : ''}>📝 Akademik ta'tildan qayta tiklash buyrug'i</option>
                  <option value="buyruq_guruhdan_guruhga" ${specificTplId === 'buyruq_guruhdan_guruhga' ? 'selected' : ''}>📝 Guruhdan guruhga o'tkazish buyrug'i</option>
                  <option value="buyruq_safidan_chiqarish" ${specificTplId === 'buyruq_safidan_chiqarish' ? 'selected' : ''}>📝 Talabalar safidan chiqarish buyrug'i</option>
                </optgroup>
              </select>
            </div>

            <!-- Safidan chiqarish asosi -->
            <div class="form-group" id="group-asos-turi" style="display:none;">
              <label class="form-label">Chiqarish Asosi</label>
              <select id="doc-asos-turi" class="select-control">
                <option value="Talaba arizasi">Talaba arizasi asosida (1-asos)</option>
                <option value="Rahbarini bildirgisi">Guruh rahbarining bildirgisi asosida (2-asos)</option>
              </select>
            </div>

            <!-- Buyruq raqami -->
            <div class="form-group" id="group-buyruq-raqami" style="display:none;">
              <label class="form-label">Buyruq Raqami</label>
              <input type="text" id="doc-buyruq-raqami" class="input-control" placeholder="14-B" value="14-B">
            </div>

            <!-- Avvalgi buyruq rekvizitlari -->
            <div id="group-avvalgi-buyruq" style="display:none;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Avvalgi Buyruq Raqami</label>
                  <input type="text" id="doc-avv-raqam" class="input-control" placeholder="14-B" value="14-B">
                </div>
                <div class="form-group">
                  <label class="form-label">Avvalgi Buyruq Sanasi</label>
                  <input type="text" id="doc-avv-sana" class="input-control" placeholder="10.02.2025" value="10.02.2025">
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Talabaning To'liq F.I.O</label>
              <input type="text" id="doc-fio" class="input-control" placeholder="Napasov Ozodbek Zafar o’g’li" value="" required>
            </div>

            <!-- Ta'lim Yo'nalishi -->
            <div class="form-group" id="group-yonalish">
              <label class="form-label">Ta'lim Yo'nalishi</label>
              <select id="doc-yonalish" class="select-control">
                <option value="Hamshiralik ishi">Hamshiralik ishi</option>
                <option value="Davolash ishi (Feldsherlik)">Davolash ishi (Feldsherlik)</option>
                <option value="Farmatsiya">Farmatsiya</option>
                <option value="Stomatologiya ishi">Stomatologiya ishi</option>
              </select>
            </div>

            <!-- O'quv yili -->
            <div class="form-group" id="group-oquv-yili">
              <label class="form-label">O'quv Yili</label>
              <input type="text" id="doc-oquv-yili" class="input-control" placeholder="2026/2027" value="2026/2027">
            </div>

            <!-- Kursi va Guruhi -->
            <div id="group-kurs-guruh" style="display:none;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group" id="subgroup-kurs">
                  <label class="form-label">Bosqich / Kursi</label>
                  <select id="doc-kursi" class="select-control">
                    <option value="1">1-kurs</option>
                    <option value="2" selected>2-kurs</option>
                    <option value="3">3-kurs</option>
                    <option value="4">4-kurs</option>
                  </select>
                </div>
                <div class="form-group" id="subgroup-guruh">
                  <label class="form-label" id="label-guruh">Guruhi</label>
                  <input type="text" id="doc-guruhi" class="input-control" placeholder="204" value="204" list="academic-groups-list">
                </div>
              </div>
            </div>

            <!-- Yangi guruh -->
            <div class="form-group" id="group-yangi-guruh" style="display:none;">
              <label class="form-label">Yangi Guruh (O'tkazilayotgan / Tiklanayotgan)</label>
              <input type="text" id="doc-yangi-guruhi" class="input-control" placeholder="205" value="205" list="academic-groups-list">
            </div>

            <datalist id="academic-groups-list"></datalist>

            <div class="form-group">
              <label class="form-label">Berilgan Sana</label>
              <input type="text" id="doc-sana" class="input-control" placeholder="${todayStr}" value="${todayStr}" required>
            </div>

            <div style="margin-top:22px;">
              <button type="submit" class="btn-primary btn-block" id="doc-generate-btn">
                ${this.icons.documents} <span>Hujjatni shakllantirish va saqlash</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Right: HD Preview Box -->
        <div class="glass-card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:520px;text-align:center;">
          <div id="doc-preview-box" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="margin-bottom:12px;color:rgba(0,203,169,0.4);">${this.icons.documents}</div>
            <div style="font-size:14.5px;font-weight:700;color:#ffffff;margin-bottom:6px;">Hujjat oldindan ko'rish oynasi</div>
            <div style="font-size:12.5px;color:rgba(94,234,212,0.65);max-width:320px;">Maydonlarni to'ldirib, tugmani bosing. Asl Word (.docx) va 300 DPI rasmi shu yerda aks etadi va saqlanadi.</div>
          </div>
        </div>
      </div>

      <!-- Bottom Dedicated Table for this template -->
      <div id="specific-tpl-archive-box"></div>
    `;

    // Load academic groups datalist asynchronously
    this.api('/api/groups/academic').then(res => {
      const gList = res?.groups || [];
      const dlist = document.getElementById('academic-groups-list');
      if (dlist && gList.length > 0) {
        dlist.innerHTML = gList.map(g => `<option value="${g.group_name}">`).join('');
      }
    });

    const tplSelect = document.getElementById('doc-tpl-select');
    const groupAsos = document.getElementById('group-asos-turi');
    const groupBuyruqNum = document.getElementById('group-buyruq-raqami');
    const groupAvvBuyruq = document.getElementById('group-avvalgi-buyruq');
    const groupYonalish = document.getElementById('group-yonalish');
    const groupOquvYili = document.getElementById('group-oquv-yili');
    const groupKursGuruh = document.getElementById('group-kurs-guruh');
    const subgroupKurs = document.getElementById('subgroup-kurs');
    const subgroupGuruh = document.getElementById('subgroup-guruh');
    const labelGuruh = document.getElementById('label-guruh');
    const groupYangiGuruh = document.getElementById('group-yangi-guruh');

    const updateFormVisibility = () => {
      const val = tplSelect.value;
      
      groupAsos.style.display = 'none';
      groupBuyruqNum.style.display = 'none';
      groupAvvBuyruq.style.display = 'none';
      groupYonalish.style.display = 'none';
      groupOquvYili.style.display = 'none';
      groupKursGuruh.style.display = 'none';
      subgroupKurs.style.display = 'none';
      subgroupGuruh.style.display = 'none';
      groupYangiGuruh.style.display = 'none';

      if (val === 'qabul_1_kurs') {
        groupYonalish.style.display = 'block';
        groupOquvYili.style.display = 'block';
        document.getElementById('doc-oquv-yili').value = '2026/2027';
      } else if (val === 'oqiyapti') {
        groupYonalish.style.display = 'block';
        groupOquvYili.style.display = 'block';
        groupKursGuruh.style.display = 'block';
        subgroupKurs.style.display = 'block';
        subgroupGuruh.style.display = 'block';
        labelGuruh.innerText = 'Guruhi';
        document.getElementById('doc-oquv-yili').value = '2024/2025';
      } else if (val === 'buyruq_akademik_tatil') {
        groupBuyruqNum.style.display = 'block';
        groupKursGuruh.style.display = 'block';
        subgroupKurs.style.display = 'block';
        subgroupGuruh.style.display = 'block';
        labelGuruh.innerText = 'Guruhi';
      } else if (val === 'buyruq_qayta_tiklash') {
        groupBuyruqNum.style.display = 'block';
        groupAvvBuyruq.style.display = 'block';
        groupKursGuruh.style.display = 'block';
        subgroupKurs.style.display = 'block';
        subgroupGuruh.style.display = 'block';
        labelGuruh.innerText = 'Avvalgi Guruhi';
        groupYangiGuruh.style.display = 'block';
      } else if (val === 'buyruq_guruhdan_guruhga') {
        groupBuyruqNum.style.display = 'block';
        groupYonalish.style.display = 'block';
        groupKursGuruh.style.display = 'block';
        subgroupGuruh.style.display = 'block';
        labelGuruh.innerText = 'Qaysi guruhdan';
        groupYangiGuruh.style.display = 'block';
      } else if (val === 'buyruq_safidan_chiqarish') {
        groupAsos.style.display = 'block';
        groupBuyruqNum.style.display = 'block';
        groupKursGuruh.style.display = 'block';
        subgroupKurs.style.display = 'block';
        subgroupGuruh.style.display = 'block';
        labelGuruh.innerText = 'Guruhi';
      }

      // Render dedicated archive below
      this.renderDocumentArchive(document.getElementById('specific-tpl-archive-box'), val, true);
    };

    tplSelect.addEventListener('change', updateFormVisibility);
    updateFormVisibility();

    document.getElementById('doc-gen-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('doc-generate-btn');
      btn.innerHTML = `<span>Shakllantirilmoqda...</span>`;

      const tpl_id = tplSelect.value;
      const fio = document.getElementById('doc-fio').value.trim();
      const sana = document.getElementById('doc-sana').value.trim();

      const answers = {
        FIO: fio,
        IFO: fio,
        SANA: sana,
        sanasi: sana
      };

      if (tpl_id === 'qabul_1_kurs') {
        answers['YONALISH'] = document.getElementById('doc-yonalish').value;
        answers['OQUV_YILI'] = document.getElementById('doc-oquv-yili').value;
      } else if (tpl_id === 'oqiyapti') {
        answers['YONALISH'] = document.getElementById('doc-yonalish').value;
        answers['OQUV_YILI'] = document.getElementById('doc-oquv-yili').value;
        answers['KURSI'] = document.getElementById('doc-kursi').value;
        answers['GURUHI'] = document.getElementById('doc-guruhi').value;
      } else if (tpl_id === 'buyruq_akademik_tatil') {
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value;
        answers['kursi'] = document.getElementById('doc-kursi').value;
        answers['guruhi'] = document.getElementById('doc-guruhi').value;
      } else if (tpl_id === 'buyruq_qayta_tiklash') {
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value;
        answers['avvalgi_buyruq_raqami'] = document.getElementById('doc-avv-raqam').value;
        answers['avvalgi_buyruq_sanasi'] = document.getElementById('doc-avv-sana').value;
        answers['kursi'] = document.getElementById('doc-kursi').value;
        answers['avvalgi_guruhi'] = document.getElementById('doc-guruhi').value;
        answers['yangi_guruhi'] = document.getElementById('doc-yangi-guruhi').value;
      } else if (tpl_id === 'buyruq_guruhdan_guruhga') {
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value;
        answers['yonalishi'] = document.getElementById('doc-yonalish').value;
        answers['avvalgi_guruhi'] = document.getElementById('doc-guruhi').value;
        answers['yangi_guruhi'] = document.getElementById('doc-yangi-guruhi').value;
      } else if (tpl_id === 'buyruq_safidan_chiqarish') {
        answers['asos_turi'] = document.getElementById('doc-asos-turi').value;
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value;
        answers['kursi'] = document.getElementById('doc-kursi').value;
        answers['avvalgi_guruhi'] = document.getElementById('doc-guruhi').value;
      }

      const res = await this.api('/api/documents/generate', 'POST', { template_id: tpl_id, answers });
      btn.innerHTML = `${this.icons.documents} <span>Hujjatni shakllantirish va saqlash</span>`;

      if (res && res.success) {
        this.toast(res.message, 'success');
        const prevBox = document.getElementById('doc-preview-box');
        prevBox.innerHTML = `
          <div style="width:100%;display:flex;flex-direction:column;align-items:center;">
            <img src="${res.view_url}" style="max-width:100%;max-height:410px;border-radius:var(--radius-md);box-shadow:var(--shadow-card);border:1px solid var(--border-glass);" alt="Hujjat">
            <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;justify-content:center;">
              <button class="btn-sm btn-secondary" onclick="ATLAS.openImageModal('${res.view_url}', '${fio}', ${res.doc_id})">
                ${this.icons.eye} <span>Katta ko'rish</span>
              </button>
              <button class="btn-sm btn-secondary" onclick="ATLAS.openEditDocModal(${res.doc_id})">
                ${this.icons.edit} <span>Tahrirlash</span>
              </button>
              <a href="${res.download_docx_url || `/api/documents/download_docx/${res.doc_id}`}" class="btn-sm btn-primary" style="background:#2563eb;border-color:#3b82f6;">
                ${this.icons.download} <span>Word (.docx) yuklab olish</span>
              </a>
              <a href="${res.download_url}" class="btn-sm btn-secondary">
                ${this.icons.download} <span>Rasm (.png)</span>
              </a>
              <button class="btn-sm btn-secondary" onclick="ATLAS.resendDocumentToTelegram(${res.doc_id})">
                ${this.icons.send} <span>Telegramga yuborish</span>
              </button>
            </div>
          </div>
        `;
        // Refresh bottom table
        this.renderDocumentArchive(document.getElementById('specific-tpl-archive-box'), tpl_id, true);
      } else {
        this.toast(res ? res.error : 'Hujjat shakllantirishda xatolik', 'error');
      }
    });
  },

  async renderDocumentArchive(container, initialFilter = '', isEmbedded = false) {
    if (!container) return;
    container.innerHTML = `<div style="text-align:center;padding:30px;color:rgba(255,255,255,0.5);">Arxiv yuklanmoqda...</div>`;
    
    let activeFilter = initialFilter;
    const fetchAndRender = async () => {
      const url = activeFilter ? `/api/documents/list?template=${encodeURIComponent(activeFilter)}` : '/api/documents/list';
      const res = await this.api(url);
      const docs = res?.documents || [];

      container.innerHTML = `
        <div class="glass-card">
          <div class="card-header-flex">
            <div>
              <div class="card-title">${isEmbedded ? 'Ushbu Shablon Bo\'yicha Yaratilganlar Tarixi' : 'Hujjatlar & Buyruqlar Arxivi'}</div>
              <div class="card-subtitle">Jami: ${res?.pagination?.total || docs.length} ta hujjat</div>
            </div>
            <div style="display:flex;gap:10px;">
              <input type="text" id="arch-search-input" class="input-control" style="width:240px;height:38px;" placeholder="F.I.O bo'yicha qidirish...">
            </div>
          </div>

          ${!isEmbedded ? `
            <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;">
              <button class="btn-sm ${!activeFilter ? 'btn-primary' : 'btn-secondary'}" data-filter="">Barchasi</button>
              <button class="btn-sm ${activeFilter === 'qabul_1_kurs' ? 'btn-primary' : 'btn-secondary'}" data-filter="qabul_1_kurs">1-kursga qabul</button>
              <button class="btn-sm ${activeFilter === 'oqiyapti' ? 'btn-primary' : 'btn-secondary'}" data-filter="oqiyapti">O'qiyotganligi</button>
              <button class="btn-sm ${activeFilter === 'buyruq_akademik_tatil' ? 'btn-primary' : 'btn-secondary'}" data-filter="buyruq_akademik_tatil">Akademik ta'til</button>
              <button class="btn-sm ${activeFilter === 'buyruq_qayta_tiklash' ? 'btn-primary' : 'btn-secondary'}" data-filter="buyruq_qayta_tiklash">Qayta tiklash</button>
              <button class="btn-sm ${activeFilter === 'buyruq_guruhdan_guruhga' ? 'btn-primary' : 'btn-secondary'}" data-filter="buyruq_guruhdan_guruhga">Guruh almashtirish</button>
              <button class="btn-sm ${activeFilter === 'buyruq_safidan_chiqarish' ? 'btn-primary' : 'btn-secondary'}" data-filter="buyruq_safidan_chiqarish">Safidan chiqarish</button>
            </div>
          ` : ''}

          <div class="table-responsive">
            <table class="glass-table">
              <thead>
                <tr>
                  <th>Vaqt / Sana</th>
                  <th>Talaba F.I.O</th>
                  <th>Turi & Shablon</th>
                  <th>Qo'shimcha Detal</th>
                  <th>Manba</th>
                  <th style="text-align:right">Tahrirlash & Yuklab olish</th>
                </tr>
              </thead>
              <tbody id="archive-table-body">
                ${docs.length === 0 ? `<tr><td colspan="6" style="text-align:center;padding:24px;color:rgba(255,255,255,0.4);">Hozircha saqlangan hujjatlar yo'q</td></tr>` : ''}
                ${docs.map(d => {
                  const p = d.parsed_data || {};
                  const isBuyruq = d.template_id?.includes('buyruq');
                  const badgeCls = isBuyruq ? 'badge-warning' : 'badge-info';
                  return `
                    <tr>
                      <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.6);">${d.created_at}</td>
                      <td><b>${d.recipient_fio}</b></td>
                      <td><span class="badge ${badgeCls}">${d.template_name}</span></td>
                      <td style="font-size:12.5px;color:rgba(94,234,212,0.85);">
                        ${p.buyruq_raqami ? `№ ${p.buyruq_raqami} | ` : ''}
                        ${p.YONALISH || p.yonalishi || ''}
                        ${p.KURSI || p.kursi ? ` (${p.KURSI || p.kursi}-kurs)` : ''}
                        ${p.GURUHI || p.guruhi || p.avvalgi_guruhi ? ` | ${p.GURUHI || p.guruhi || p.avvalgi_guruhi}-guruh` : ''}
                        ${p.yangi_guruhi ? ` ➔ ${p.yangi_guruhi}` : ''}
                      </td>
                      <td><span class="badge badge-${d.created_by === 'web_admin' ? 'success' : 'warning'}">${d.created_by === 'web_admin' ? 'Web Panel' : 'Telegram Bot'}</span></td>
                      <td style="text-align:right;">
                        <div style="display:flex;gap:6px;justify-content:flex-end;">
                          <button class="btn-icon" onclick="ATLAS.openImageModal('/api/documents/view/${d.id}', '${d.recipient_fio}', ${d.id})" title="Katta ko'rish">${this.icons.eye}</button>
                          <button class="btn-icon" onclick="ATLAS.openEditDocModal(${d.id})" title="Tahrirlash" style="color:var(--accent-glow);">${this.icons.edit}</button>
                          <a href="/api/documents/download_docx/${d.id}" class="btn-icon" title="Word (.docx) yuklab olish" style="color:#60a5fa;">${this.icons.download}</a>
                          <a href="/api/documents/download/${d.id}" class="btn-icon" title="Rasm (.png) yuklab olish">${this.icons.download}</a>
                          <button class="btn-icon" onclick="ATLAS.resendDocumentToTelegram(${d.id})" title="Telegramga yuborish">${this.icons.send}</button>
                          <button class="btn-icon" onclick="ATLAS.deleteDocumentFromArchive(${d.id})" title="Arxivdan o'chirish">${this.icons.trash}</button>
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>
      `;

      // Filter button listeners
      container.querySelectorAll('[data-filter]').forEach(b => {
        b.addEventListener('click', () => {
          activeFilter = b.dataset.filter;
          fetchAndRender();
        });
      });

      // Search listener
      const searchInp = document.getElementById('arch-search-input');
      if (searchInp) {
        searchInp.addEventListener('input', async (e) => {
          const q = e.target.value.trim();
          let sUrl = `/api/documents/list?q=${encodeURIComponent(q)}`;
          if (activeFilter) sUrl += `&template=${encodeURIComponent(activeFilter)}`;
          const sRes = await this.api(sUrl);
          const sDocs = sRes?.documents || [];
          const tbody = document.getElementById('archive-table-body');
          if (!tbody) return;
          if (sDocs.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px;color:rgba(255,255,255,0.4);">Hech qanday hujjat topilmadi</td></tr>`;
            return;
          }
          tbody.innerHTML = sDocs.map(d => {
            const p = d.parsed_data || {};
            const isBuyruq = d.template_id?.includes('buyruq');
            const badgeCls = isBuyruq ? 'badge-warning' : 'badge-info';
            return `
              <tr>
                <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.6);">${d.created_at}</td>
                <td><b>${d.recipient_fio}</b></td>
                <td><span class="badge ${badgeCls}">${d.template_name}</span></td>
                <td style="font-size:12.5px;color:rgba(94,234,212,0.85);">
                  ${p.buyruq_raqami ? `№ ${p.buyruq_raqami} | ` : ''}
                  ${p.YONALISH || p.yonalishi || ''}
                  ${p.KURSI || p.kursi ? ` (${p.KURSI || p.kursi}-kurs)` : ''}
                  ${p.GURUHI || p.guruhi || p.avvalgi_guruhi ? ` | ${p.GURUHI || p.guruhi || p.avvalgi_guruhi}-guruh` : ''}
                  ${p.yangi_guruhi ? ` ➔ ${p.yangi_guruhi}` : ''}
                </td>
                <td><span class="badge badge-${d.created_by === 'web_admin' ? 'success' : 'warning'}">${d.created_by === 'web_admin' ? 'Web Panel' : 'Telegram Bot'}</span></td>
                <td style="text-align:right;">
                  <div style="display:flex;gap:6px;justify-content:flex-end;">
                    <button class="btn-icon" onclick="ATLAS.openImageModal('/api/documents/view/${d.id}', '${d.recipient_fio}', ${d.id})" title="Katta ko'rish">${this.icons.eye}</button>
                    <button class="btn-icon" onclick="ATLAS.openEditDocModal(${d.id})" title="Tahrirlash" style="color:var(--accent-glow);">${this.icons.edit}</button>
                    <a href="/api/documents/download_docx/${d.id}" class="btn-icon" title="Word (.docx) yuklab olish" style="color:#60a5fa;">${this.icons.download}</a>
                    <a href="/api/documents/download/${d.id}" class="btn-icon" title="Rasm (.png) yuklab olish">${this.icons.download}</a>
                    <button class="btn-icon" onclick="ATLAS.resendDocumentToTelegram(${d.id})" title="Telegramga yuborish">${this.icons.send}</button>
                    <button class="btn-icon" onclick="ATLAS.deleteDocumentFromArchive(${d.id})" title="Arxivdan o'chirish">${this.icons.trash}</button>
                  </div>
                </td>
              </tr>
            `;
          }).join('');
        });
      }
    };

    fetchAndRender();
  },

  async openEditDocModal(docId) {
    const res = await this.api('/api/documents/list');
    const docs = res?.documents || [];
    const doc = docs.find(d => d.id === docId);
    if (!doc) {
      this.toast('Hujjat ma\'lumotlari topilmadi', 'error');
      return;
    }

    const p = doc.parsed_data || {};
    const tpl_id = doc.template_id;
    const isBuyruq = tpl_id.includes('buyruq');

    this.openModal(`Hujjatni Tahrirlash: ${doc.template_name}`, `
      <form id="edit-doc-form">
        <div class="form-group">
          <label class="form-label">Talabaning To'liq F.I.O</label>
          <input type="text" id="edit-fio" class="input-control" value="${doc.recipient_fio || ''}" required>
        </div>

        ${isBuyruq ? `
          <div class="form-group">
            <label class="form-label">Buyruq Raqami</label>
            <input type="text" id="edit-buyruq-raqami" class="input-control" value="${p.buyruq_raqami || '14-B'}" required>
          </div>
        ` : ''}

        ${tpl_id === 'buyruq_safidan_chiqarish' ? `
          <div class="form-group">
            <label class="form-label">Chiqarish Asosi</label>
            <select id="edit-asos-turi" class="select-control">
              <option value="Talaba arizasi" ${p.asos_turi === 'Talaba arizasi' ? 'selected' : ''}>Talaba arizasi asosida (1-asos)</option>
              <option value="Rahbarini bildirgisi" ${p.asos_turi === 'Rahbarini bildirgisi' ? 'selected' : ''}>Guruh rahbarining bildirgisi asosida (2-asos)</option>
            </select>
          </div>
        ` : ''}

        ${tpl_id === 'buyruq_qayta_tiklash' ? `
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
            <div class="form-group">
              <label class="form-label">Avvalgi Buyruq Raqami</label>
              <input type="text" id="edit-avv-raqam" class="input-control" value="${p.avvalgi_buyruq_raqami || ''}">
            </div>
            <div class="form-group">
              <label class="form-label">Avvalgi Buyruq Sanasi</label>
              <input type="text" id="edit-avv-sana" class="input-control" value="${p.avvalgi_buyruq_sanasi || ''}">
            </div>
          </div>
        ` : ''}

        ${(p.YONALISH || p.yonalishi || tpl_id === 'qabul_1_kurs' || tpl_id === 'oqiyapti' || tpl_id === 'buyruq_guruhdan_guruhga') ? `
          <div class="form-group">
            <label class="form-label">Ta'lim Yo'nalishi</label>
            <input type="text" id="edit-yonalish" class="input-control" value="${p.YONALISH || p.yonalishi || 'Hamshiralik ishi'}">
          </div>
        ` : ''}

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
          ${(p.KURSI || p.kursi) ? `
            <div class="form-group">
              <label class="form-label">Kursi</label>
              <input type="text" id="edit-kursi" class="input-control" value="${p.KURSI || p.kursi || '1'}">
            </div>
          ` : ''}
          ${(p.GURUHI || p.guruhi || p.avvalgi_guruhi) ? `
            <div class="form-group">
              <label class="form-label">${tpl_id === 'buyruq_qayta_tiklash' || tpl_id === 'buyruq_guruhdan_guruhga' ? 'Avvalgi guruhi' : 'Guruhi'}</label>
              <input type="text" id="edit-guruhi" class="input-control" value="${p.GURUHI || p.guruhi || p.avvalgi_guruhi || ''}">
            </div>
          ` : ''}
        </div>

        ${(tpl_id === 'buyruq_qayta_tiklash' || tpl_id === 'buyruq_guruhdan_guruhga') ? `
          <div class="form-group">
            <label class="form-label">Yangi Guruh</label>
            <input type="text" id="edit-yangi-guruhi" class="input-control" value="${p.yangi_guruhi || ''}">
          </div>
        ` : ''}

        <div class="form-group">
          <label class="form-label">Hujjat Sanasi</label>
          <input type="text" id="edit-sana" class="input-control" value="${p.SANA || p.sanasi || ''}" required>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="submit" class="btn-sm btn-primary" id="edit-submit-btn">Saqlash va Yangilash</button>
        </div>
      </form>
    `);

    document.getElementById('edit-doc-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('edit-submit-btn');
      btn.innerText = 'Yangilanmoqda...';

      const fio = document.getElementById('edit-fio').value.trim();
      const sana = document.getElementById('edit-sana').value.trim();
      const answers = {
        ...p,
        FIO: fio,
        IFO: fio,
        SANA: sana,
        sanasi: sana
      };

      const editBuyruq = document.getElementById('edit-buyruq-raqami');
      if (editBuyruq) answers['buyruq_raqami'] = editBuyruq.value.trim();

      const editAsos = document.getElementById('edit-asos-turi');
      if (editAsos) answers['asos_turi'] = editAsos.value;

      const editAvvRaqam = document.getElementById('edit-avv-raqam');
      if (editAvvRaqam) answers['avvalgi_buyruq_raqami'] = editAvvRaqam.value.trim();

      const editAvvSana = document.getElementById('edit-avv-sana');
      if (editAvvSana) answers['avvalgi_buyruq_sanasi'] = editAvvSana.value.trim();

      const editYonalish = document.getElementById('edit-yonalish');
      if (editYonalish) {
        answers['YONALISH'] = editYonalish.value.trim();
        answers['yonalishi'] = editYonalish.value.trim();
      }

      const editKursi = document.getElementById('edit-kursi');
      if (editKursi) {
        answers['KURSI'] = editKursi.value.trim();
        answers['kursi'] = editKursi.value.trim();
      }

      const editGuruhi = document.getElementById('edit-guruhi');
      if (editGuruhi) {
        answers['GURUHI'] = editGuruhi.value.trim();
        answers['guruhi'] = editGuruhi.value.trim();
        answers['avvalgi_guruhi'] = editGuruhi.value.trim();
      }

      const editYangiGuruhi = document.getElementById('edit-yangi-guruhi');
      if (editYangiGuruhi) answers['yangi_guruhi'] = editYangiGuruhi.value.trim();

      const resUpdate = await this.api(`/api/documents/${docId}`, 'PUT', { answers });
      btn.innerText = 'Saqlash va Yangilash';

      if (resUpdate && resUpdate.success) {
        this.toast(resUpdate.message, 'success');
        this.closeModal();
        this.loadDocuments(document.getElementById('content-viewport'));
      } else {
        this.toast(resUpdate ? resUpdate.error : 'Tahrirlashda xatolik', 'error');
      }
    });
  },

  async resendDocumentToTelegram(docId) {
    this.toast('Telegramga yuborilmoqda...', 'info');
    const res = await this.api(`/api/documents/resend/${docId}`, 'POST');
    if (res && res.success) {
      this.toast(res.message, 'success');
    } else {
      this.toast(res ? res.error : 'Telegramga yuborishda xatolik', 'error');
    }
  },

  async deleteDocumentFromArchive(docId) {
    const confirmed = await this.confirm({
      title: "Arxivdan O'chirish",
      message: "Haqiqatdan ham ushbu hujjatni arxivdan butunlay o'chirmoqchimisiz?",
      confirmText: "O'chirish",
      cancelText: "Bekor qilish",
      isDanger: true
    });
    if (!confirmed) return;

    const res = await this.api(`/api/documents/${docId}`, 'DELETE');
    if (res && res.success) {
      this.toast(res.message, 'success');
      this.loadDocuments(document.getElementById('content-viewport'));
    }
  },

  openImageModal(imgUrl, title, docId) {
    const downloadPngUrl = docId ? `/api/documents/download/${docId}` : imgUrl;
    const downloadDocxUrl = docId ? `/api/documents/download_docx/${docId}` : '';
    this.openModalLarge(`${title} — 300 DPI A4 Ko'rinish`, `
      <div style="text-align:center;">
        <img src="${imgUrl}" style="max-width:100%;max-height:75vh;border-radius:var(--radius-sm);box-shadow:var(--shadow-card);border:1px solid var(--border-glass);" alt="${title}">
        <div class="modal-footer" style="justify-content:center;gap:12px;margin-top:16px;">
          <a href="${imgUrl}" target="_blank" class="btn-sm btn-secondary">${this.icons.eye} Yangi oynada ochish</a>
          ${downloadDocxUrl ? `<a href="${downloadDocxUrl}" class="btn-sm btn-primary" style="background:#2563eb;border-color:#3b82f6;">${this.icons.download} Word (.docx) yuklab olish</a>` : ''}
          <a href="${downloadPngUrl}" class="btn-sm btn-secondary">${this.icons.download} Rasm (.png) yuklab olish</a>
        </div>
      </div>
    `);
  },

  // ============================================================
  // 2. O'QUV GURUHLARI & TELEGRAM GURUHLAR (GURUHLAR BO'LIMI)
  // ============================================================
  async loadGroups(container, activeTab = 'academic') {
    container.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(255,255,255,0.5);">Guruhlar yuklanmoqda...</div>`;

    container.innerHTML = `
      <div class="tab-pills-row">
        <button class="tab-pill-btn ${activeTab === 'academic' ? 'active' : ''}" id="tab-grp-academic">
          ${this.icons.groups} <span>🎓 O'quv Guruhlari (Texnikum)</span>
        </button>
        <button class="tab-pill-btn ${activeTab === 'telegram' ? 'active' : ''}" id="tab-grp-telegram">
          ${this.icons.messages} <span>🤖 Ulangan Telegram Guruhlar</span>
        </button>
      </div>

      <div id="groups-tab-content"></div>
    `;

    document.getElementById('tab-grp-academic').addEventListener('click', () => {
      this.loadGroups(container, 'academic');
    });
    document.getElementById('tab-grp-telegram').addEventListener('click', () => {
      this.loadGroups(container, 'telegram');
    });

    const contentBox = document.getElementById('groups-tab-content');
    if (activeTab === 'academic') {
      this.renderAcademicGroups(contentBox);
    } else {
      this.renderTelegramGroups(contentBox);
    }
  },

  async renderAcademicGroups(container) {
    const res = await this.api('/api/groups/academic');
    const groups = res?.groups || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Texnikum O'quv Guruhlari Ro'yxati</div>
            <div class="card-subtitle">Barcha kurslar bo'yicha guruhlar ro'yxati (Jami: ${groups.length} ta)</div>
          </div>
          <div style="display:flex;gap:10px;">
            <input type="text" id="acad-group-search" class="input-control" style="width:220px;height:38px;" placeholder="Guruh nomini qidirish...">
            <button class="btn-sm btn-primary" id="btn-add-academic-groups">
              ${this.icons.plus} <span>Guruh qo'shish</span>
            </button>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>№</th>
                <th>Guruh Nomi</th>
                <th>Bosqich / Kursi</th>
                <th>Qo'shilgan Sana</th>
                <th style="text-align:right">Amallar</th>
              </tr>
            </thead>
            <tbody id="acad-groups-tbody">
              ${groups.length === 0 ? `<tr><td colspan="5" style="text-align:center;padding:24px;color:rgba(255,255,255,0.4);">Hozircha o'quv guruhlari kiritilmagan. Yuqoridagi "Guruh qo'shish" tugmasini bosing.</td></tr>` : ''}
              ${groups.map((g, idx) => `
                <tr>
                  <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.5);">${idx + 1}</td>
                  <td><b>${g.group_name}</b></td>
                  <td><span class="badge badge-info">${g.course_level || 1}-kurs</span></td>
                  <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.6);">${g.created_at || '-'}</td>
                  <td style="text-align:right;">
                    <button class="btn-icon" onclick="ATLAS.deleteAcademicGroup(${g.id})" title="O'chirish">${this.icons.trash}</button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    document.getElementById('btn-add-academic-groups').addEventListener('click', () => {
      this.openBulkAddGroupsModal();
    });

    document.getElementById('acad-group-search').addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      const tbody = document.getElementById('acad-groups-tbody');
      const filtered = groups.filter(g => g.group_name.toLowerCase().includes(q));
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:24px;color:rgba(255,255,255,0.4);">Hech qanday guruh topilmadi</td></tr>`;
        return;
      }
      tbody.innerHTML = filtered.map((g, idx) => `
        <tr>
          <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.5);">${idx + 1}</td>
          <td><b>${g.group_name}</b></td>
          <td><span class="badge badge-info">${g.course_level || 1}-kurs</span></td>
          <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.6);">${g.created_at || '-'}</td>
          <td style="text-align:right;">
            <button class="btn-icon" onclick="ATLAS.deleteAcademicGroup(${g.id})" title="O'chirish">${this.icons.trash}</button>
          </td>
        </tr>
      `).join('');
    });
  },

  openBulkAddGroupsModal() {
    this.openModal("Yangi O'quv Guruhlarini Kiritish", `
      <form id="bulk-groups-form">
        <div class="form-group">
          <label class="form-label">Guruhlar ro'yxati (Har bir abzasda / qatorda bittadan yozing)</label>
          <div style="font-size:12px;color:rgba(94,234,212,0.8);margin-bottom:8px;">
            Masalan:<br>
            <code>101-Hamshiralik<br>102-Hamshiralik<br>201-Davolash<br>204-Stomatologiya</code>
          </div>
          <textarea id="bulk-groups-text" class="textarea-control" style="min-height:160px;font-family:'JetBrains Mono', monospace;" placeholder="101-Hamshiralik&#10;102-Hamshiralik&#10;201-Davolash&#10;204-Stomatologiya" required></textarea>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="submit" class="btn-sm btn-primary" id="save-groups-btn">Guruhlarni Saqlash</button>
        </div>
      </form>
    `);

    document.getElementById('bulk-groups-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const txt = document.getElementById('bulk-groups-text').value;
      const btn = document.getElementById('save-groups-btn');
      btn.innerText = 'Saqlanmoqda...';

      const res = await this.api('/api/groups/academic/bulk', 'POST', { text: txt });
      btn.innerText = 'Guruhlarni Saqlash';

      if (res && res.success) {
        this.toast(res.message, 'success');
        this.closeModal();
        this.loadGroups(document.getElementById('content-viewport'), 'academic');
      } else {
        this.toast(res ? res.error : 'Guruhlar qo\'shishda xatolik', 'error');
      }
    });
  },

  async deleteAcademicGroup(groupId) {
    const confirmed = await this.confirm({
      title: "Guruhni O'chirish",
      message: "Haqiqatdan ham ushbu guruhni ro'yxatdan o'chirmoqchimisiz?",
      confirmText: "O'chirish",
      cancelText: "Bekor qilish",
      isDanger: true
    });
    if (!confirmed) return;

    const res = await this.api(`/api/groups/academic/${groupId}`, 'DELETE');
    if (res && res.success) {
      this.toast(res.message, 'success');
      this.loadGroups(document.getElementById('content-viewport'), 'academic');
    }
  },

  async renderTelegramGroups(container) {
    const res = await this.api('/api/groups');
    const groups = res?.groups || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Ulangan Telegram Guruhlar va Kanallar</div>
            <div class="card-subtitle">Bot a'zo bo'lgan rasmiy guruhlar</div>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Guruh Nomi</th>
                <th>Turi</th>
                <th>A'zolar Soni</th>
                <th>Holat</th>
              </tr>
            </thead>
            <tbody>
              ${groups.length === 0 ? `<tr><td colspan="5" style="text-align:center;">Hozircha guruhlar yo'q</td></tr>` : ''}
              ${groups.map(g => `
                <tr>
                  <td class="mono"><b>${g.telegram_id}</b></td>
                  <td><b>${g.title}</b></td>
                  <td><span class="badge badge-info">${g.type}</span></td>
                  <td>${g.members_count} ta</td>
                  <td><span class="badge badge-success">Faol</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  async loadMessages(container) {
    container.innerHTML = `
      <div class="glass-card" style="max-width:640px;margin:0 auto;">
        <div class="card-title" style="margin-bottom:6px;">Xabar Yuborish & E'lonlar</div>
        <div class="card-subtitle" style="margin-bottom:20px;">Barcha bot foydalanuvchilariga yoki guruhlarga yuborish</div>

        <form id="broadcast-form">
          <div class="form-group">
            <label class="form-label">Xabar / E'lon Sarlavhasi</label>
            <input type="text" id="bc-title" class="input-control" placeholder="E'lon" required>
          </div>

          <div class="form-group">
            <label class="form-label">Kimga yuborilsin?</label>
            <select id="bc-target" class="select-control">
              <option value="all_users">Barcha foydalanuvchilarga</option>
              <option value="groups">Barcha ulangan guruhlarga</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Xabar Matni (HTML teglari ishlaydi)</label>
            <textarea id="bc-content" class="textarea-control" style="min-height:120px;" placeholder="Hurmatli talabalar..." required></textarea>
          </div>

          <button type="submit" class="btn-primary btn-block">
            ${this.icons.send} <span>Yuborishni boshlash</span>
          </button>
        </form>
      </div>
    `;

    document.getElementById('broadcast-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('bc-title').value;
      const target = document.getElementById('bc-target').value;
      const content = document.getElementById('bc-content').value;

      const res = await this.api('/api/broadcasts', 'POST', { title, target, content });
      if (res && res.success) {
        this.toast(`Xabar tarqatilmoqda! (${res.total_recipients} ta qabul qiluvchi)`, 'success');
        document.getElementById('broadcast-form').reset();
      }
    });
  },

  async loadTasks(container) {
    const res = await this.api('/api/tasks');
    const tasks = res?.tasks || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Fon Vazifalari va Jarayonlar</div>
            <div class="card-subtitle">Asinxron bajarilgan amallar jurnali</div>
          </div>
          <button class="btn-sm btn-primary" id="start-task-btn">${this.icons.plus} <span>Yangi Vazifa Boshlash</span></button>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Vazifa Nomi</th>
                <th>Turi</th>
                <th>Status</th>
                <th>Boshlangan Vaqti</th>
                <th>Davomiyligi</th>
              </tr>
            </thead>
            <tbody>
              ${tasks.length === 0 ? `<tr><td colspan="5" style="text-align:center;">Vazifalar yo'q</td></tr>` : ''}
              ${tasks.map(t => `
                <tr>
                  <td><b>${t.task_name}</b></td>
                  <td><span class="badge badge-info">${t.task_type}</span></td>
                  <td><span class="badge badge-${t.status === 'completed' ? 'success' : 'warning'}">${t.status}</span></td>
                  <td class="mono" style="font-size:12px;">${t.started_at || t.created_at}</td>
                  <td>${t.duration_seconds}s</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    document.getElementById('start-task-btn').addEventListener('click', async () => {
      const res = await this.api('/api/tasks/run', 'POST', { name: 'Tizim ma\'lumotlarini yangilash', type: 'sync' });
      if (res && res.success) {
        this.toast(res.message, 'success');
        this.loadTasks(container);
      }
    });
  },

  async loadAutomation(container) {
    const res = await this.api('/api/automations');
    const list = res?.automations || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Avtomatlashtirish Qoidalari</div>
            <div class="card-subtitle">Bot avtomatik javoblari</div>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Qoida Nomi</th>
                <th>Trigger Turi</th>
                <th>Qiymati</th>
                <th>Amal</th>
                <th>Holati</th>
              </tr>
            </thead>
            <tbody>
              ${list.length === 0 ? `<tr><td colspan="5" style="text-align:center;">Qoidalar yo'q</td></tr>` : ''}
              ${list.map(a => `
                <tr>
                  <td><b>${a.name}</b></td>
                  <td><span class="badge badge-info">${a.trigger_type}</span></td>
                  <td class="mono"><code>${a.trigger_value}</code></td>
                  <td>${a.action_type}</td>
                  <td>
                    <label class="switch">
                      <input type="checkbox" ${a.is_active ? 'checked' : ''} onchange="ATLAS.toggleAutomation(${a.id})">
                      <span class="slider"></span>
                    </label>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  async toggleAutomation(id) {
    const res = await this.api(`/api/automations/${id}/toggle`, 'POST');
    if (res && res.success) this.toast('Holat o\'zgartirildi', 'success');
  },

  async loadAnalytics(container) {
    const res = await this.api('/api/analytics/charts');
    const labels = res?.labels || ['Du', 'Se', 'Chor', 'Pay', 'Ju', 'Sha', 'Yak'];
    const s = res?.series || { users: [4, 6, 8, 12, 15, 18, 22], messages: [10, 18, 25, 30, 42, 38, 50] };

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Faollik Trendlari (Oxirgi 7 kun)</div>
            <div class="card-subtitle">Foydalanuvchilar va xabarlar oqimi</div>
          </div>
        </div>

        <div style="width:100%;height:240px;display:flex;align-items:flex-end;gap:18px;padding-top:20px;">
          ${labels.map((lbl, idx) => {
            const uVal = s.users[idx] || 5;
            const mVal = s.messages[idx] || 15;
            const hU = Math.min(uVal * 7, 160);
            const hM = Math.min(mVal * 3, 200);
            return `
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;height:100%;justify-content:flex-end;">
                <div style="display:flex;gap:5px;align-items:flex-end;justify-content:center;">
                  <div style="width:16px;height:${hU}px;background:var(--accent-gradient);border-radius:3px 3px 0 0;" title="Foydalanuvchilar: ${uVal}"></div>
                  <div style="width:16px;height:${hM}px;background:rgba(6,182,212,0.6);border-radius:3px 3px 0 0;" title="Xabarlar: ${mVal}"></div>
                </div>
                <span style="font-size:11.5px;color:rgba(255,255,255,0.6);">${lbl}</span>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  },

  async loadLogs(container) {
    const res = await this.api('/api/logs');
    const logs = res?.logs || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Tizim Audit Loglari</div>
            <div class="card-subtitle">Barcha amallar xavfsiz qaydnomasi</div>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Vaqt</th>
                <th>Modul</th>
                <th>Amal</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              ${logs.length === 0 ? `<tr><td colspan="4" style="text-align:center;">Loglar yo'q</td></tr>` : ''}
              ${logs.map(l => `
                <tr>
                  <td class="mono" style="font-size:12px;">${l.timestamp}</td>
                  <td><span class="badge badge-info">${l.module}</span></td>
                  <td><b>${l.action}</b></td>
                  <td><span class="badge badge-${l.status === 'success' ? 'success' : 'error'}">${l.status}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  async loadModules(container) {
    const res = await this.api('/api/modules');
    const mods = res?.modules || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-title" style="margin-bottom:18px;">Bot Modullari Boshqaruvi</div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:16px;">
          ${mods.map(m => `
            <div style="background:rgba(8,28,30,0.7);border:1px solid var(--border-glass);border-radius:var(--radius-md);padding:16px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <b>${m.name}</b>
                <label class="switch">
                  <input type="checkbox" ${m.is_enabled ? 'checked' : ''} onchange="ATLAS.toggleModule('${m.key}')">
                  <span class="slider"></span>
                </label>
              </div>
              <p style="font-size:12.5px;color:rgba(255,255,255,0.7);">${m.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  async toggleModule(key) {
    const res = await this.api(`/api/modules/${key}/toggle`, 'POST');
    if (res && res.success) this.toast('Modul holati yangilandi', 'success');
  },

  async loadSettings(container) {
    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
        <div class="glass-card">
          <div class="card-title" style="margin-bottom:16px;">Admin Parolini O'zgartirish</div>
          <form id="change-pwd-form">
            <div class="form-group">
              <label class="form-label">Joriy Parol</label>
              <input type="password" id="old-pwd" class="input-control" required>
            </div>
            <div class="form-group">
              <label class="form-label">Yangi Parol</label>
              <input type="password" id="new-pwd" class="input-control" required>
            </div>
            <button type="submit" class="btn-primary btn-block">Saqlash</button>
          </form>
        </div>

        <div class="glass-card">
          <div class="card-title" style="margin-bottom:16px;">Bot Konfiguratsiyasi</div>
          <div style="display:flex;flex-direction:column;gap:12px;font-size:13px;">
            <div>
              <span class="form-label">Bosh Admin Telegram ID</span>
              <input type="text" class="input-control" value="8135594558" readonly>
            </div>
            <div>
              <span class="form-label">Ishlash Rejimi</span>
              <input type="text" class="input-control" value="Shaxsiy Boshqaruv / Webhook" readonly>
            </div>
          </div>
        </div>
      </div>
    `;

    document.getElementById('change-pwd-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const old_password = document.getElementById('old-pwd').value;
      const new_password = document.getElementById('new-pwd').value;
      const res = await this.api('/api/auth/change_password', 'POST', { old_password, new_password });
      if (res && res.success) {
        this.toast(res.message, 'success');
        document.getElementById('change-pwd-form').reset();
      } else {
        this.toast(res ? res.error : 'Xatolik', 'error');
      }
    });
  },

  // ============================================================
  // GLOBAL SEARCH & MODALS
  // ============================================================
  openGlobalSearch() {
    this.openModal('Tezkor Qidiruv (Ctrl+K)', `
      <div style="margin-bottom:14px;">
        <input type="text" id="modal-search-input" class="input-control" placeholder="Hujjat, talaba F.I.O yoki log..." autofocus>
      </div>
      <div id="modal-search-results" style="display:flex;flex-direction:column;gap:8px;max-height:280px;overflow-y:auto;">
        <div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px;">Kamida 2 ta harf yozing...</div>
      </div>
    `);

    document.getElementById('modal-search-input').addEventListener('input', async (e) => {
      const q = e.target.value.trim();
      const resBox = document.getElementById('modal-search-results');
      if (q.length < 2) return;
      const res = await this.api(`/api/search?q=${encodeURIComponent(q)}`);
      const items = res?.results || [];
      if (items.length === 0) {
        resBox.innerHTML = `<div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px;">Hech narsa topilmadi.</div>`;
        return;
      }
      resBox.innerHTML = items.map(it => `
        <div style="background:rgba(10,32,35,0.6);border:1px solid var(--border-glass);border-radius:var(--radius-sm);padding:10px 14px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;" onclick="ATLAS.closeModal(); ATLAS.navigate('${it.route}')">
          <div>
            <b>${it.title}</b>
            <div style="font-size:11.5px;color:rgba(94,234,212,0.7);">${it.subtitle}</div>
          </div>
          <span class="badge badge-info">${it.type}</span>
        </div>
      `).join('');
    });
  },

  openModal(title, contentHtml) {
    const el = document.getElementById('modal-container');
    el.innerHTML = `
      <div class="modal-box">
        <div class="modal-header">
          <div class="card-title">${title}</div>
          <button class="btn-icon" onclick="ATLAS.closeModal()">&times;</button>
        </div>
        <div class="modal-body">${contentHtml}</div>
      </div>
    `;
    el.classList.add('active');
  },

  openModalLarge(title, contentHtml) {
    const el = document.getElementById('modal-container');
    el.innerHTML = `
      <div class="modal-box modal-box-large">
        <div class="modal-header">
          <div class="card-title">${title}</div>
          <button class="btn-icon" onclick="ATLAS.closeModal()">&times;</button>
        </div>
        <div class="modal-body">${contentHtml}</div>
      </div>
    `;
    el.classList.add('active');
  },

  confirm(options = {}) {
    const {
      title = "Tasdiqlash",
      message = "Harakatni tasdiqlaysizmi?",
      confirmText = "Tasdiqlash",
      cancelText = "Bekor qilish",
      isDanger = false
    } = typeof options === 'string' ? { message: options } : options;

    return new Promise((resolve) => {
      const el = document.getElementById('modal-container');
      const confirmBtnClass = isDanger ? 'btn-danger' : 'btn-primary';
      const icon = isDanger ? this.icons.alert : this.icons.check;

      el.innerHTML = `
        <div class="modal-box confirm-dialog-box">
          <div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:16px;">
            <div style="width:42px;height:42px;border-radius:var(--radius-sm);background:${isDanger ? 'rgba(239,68,68,0.15)' : 'rgba(0,203,169,0.15)'};border:1px solid ${isDanger ? 'rgba(239,68,68,0.3)' : 'rgba(0,203,169,0.3)'};display:flex;align-items:center;justify-content:center;color:${isDanger ? '#f87171' : 'var(--accent-glow)'};flex-shrink:0;">
              ${icon}
            </div>
            <div>
              <div class="card-title" style="font-size:16px;margin-bottom:6px;">${title}</div>
              <div style="font-size:13.5px;color:rgba(255,255,255,0.75);line-height:1.45;">${message}</div>
            </div>
          </div>

          <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:22px;">
            <button type="button" class="btn-sm btn-secondary" id="confirm-modal-cancel">${cancelText} (Esc)</button>
            <button type="button" class="btn-sm ${confirmBtnClass}" id="confirm-modal-ok">${confirmText} (Enter)</button>
          </div>
        </div>
      `;
      el.classList.add('active');

      const okBtn = document.getElementById('confirm-modal-ok');
      const cancelBtn = document.getElementById('confirm-modal-cancel');
      if (okBtn) okBtn.focus();

      const cleanup = () => {
        window.removeEventListener('keydown', onKeyDown);
        el.classList.remove('active');
      };

      const onConfirm = () => {
        cleanup();
        resolve(true);
      };

      const onCancel = () => {
        cleanup();
        resolve(false);
      };

      const onKeyDown = (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          onConfirm();
        } else if (e.key === 'Escape') {
          e.preventDefault();
          onCancel();
        }
      };

      if (okBtn) okBtn.addEventListener('click', onConfirm);
      if (cancelBtn) cancelBtn.addEventListener('click', onCancel);
      window.addEventListener('keydown', onKeyDown);
    });
  },

  closeModal() {
    const el = document.getElementById('modal-container');
    if (el) el.classList.remove('active');
  }
};

document.addEventListener('DOMContentLoaded', () => ATLAS.init());
