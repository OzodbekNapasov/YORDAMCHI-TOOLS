// ============================================================
//  static/js/atlas.js
//  ATLAS Universal Bot Platform — Single Page Application Engine
//  NO EMOJIS — 100% SVG Vector UI & Dynamic REST API Client
// ============================================================

const ATLAS = {
  token: localStorage.getItem('atlas_token') || '',
  user: JSON.parse(localStorage.getItem('atlas_user') || 'null'),
  currentRoute: 'dashboard',
  refreshInterval: null,

  // Professional SVG Icon Library (Zero emojis)
  icons: {
    dashboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg>`,
    users: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
    groups: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
    messages: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
    automation: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    tasks: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    documents: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
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
    eye: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`,
    eyeOff: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>`,
    brandLogo: `<svg viewBox="0 0 100 100" fill="currentColor"><path d="M50 15 L78 68 C82 75 76 85 68 85 L56 85 C51 85 47 81 49 76 L62 48 C63 45 61 42 58 42 L42 42 C39 42 37 45 38 48 L46 65 C48 70 44 75 39 75 L32 75 C25 75 20 67 24 60 Z"/></svg>`
  },

  // API Request Wrapper
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
    el.innerHTML = `<span style="width:18px;height:18px;display:inline-block">${icon}</span><span>${message}</span>`;
    container.appendChild(el);

    setTimeout(() => {
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 300);
    }, 4000);
  },

  // Initialization
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
    // Global shortcut Ctrl+K
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

  // Navigation
  navigate(route) {
    this.currentRoute = route;
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });

    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
      const titles = {
        dashboard: 'Boshqaruv Paneli',
        users: 'Foydalanuvchilar',
        groups: 'Guruhlar va Kanallar',
        messages: 'Xabarlar va Tarqatish',
        automation: 'Avtomatlashtirish',
        tasks: 'Fon Vazifalari',
        documents: 'Hujjatlar Generatori',
        analytics: 'Statistika va Tahlil',
        logs: 'Tizim Loglari',
        settings: 'Bot va Tizim Sozlamalari',
        modules: 'Modullar Boshqaruvi'
      };
      pageTitle.innerText = titles[route] || 'ATLAS Platformasi';
    }

    const viewport = document.getElementById('content-viewport');
    if (!viewport) return;

    switch (route) {
      case 'dashboard': this.loadDashboard(viewport); break;
      case 'users': this.loadUsers(viewport); break;
      case 'groups': this.loadGroups(viewport); break;
      case 'messages': this.loadMessages(viewport); break;
      case 'automation': this.loadAutomation(viewport); break;
      case 'tasks': this.loadTasks(viewport); break;
      case 'documents': this.loadDocuments(viewport); break;
      case 'analytics': this.loadAnalytics(viewport); break;
      case 'logs': this.loadLogs(viewport); break;
      case 'settings': this.loadSettings(viewport); break;
      case 'modules': this.loadModules(viewport); break;
      default: this.loadDashboard(viewport);
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
          <h2 class="auth-title">Xush kelibsiz</h2>
          <p class="auth-subtitle">Platformaga kirish uchun hisob ma'lumotlaringizni kiriting</p>

          <form id="login-form">
            <div class="form-group">
              <label class="form-label">Foydalanuvchi nomi</label>
              <div class="input-container">
                <span class="input-icon-left">${this.icons.user}</span>
                <input type="text" id="login-username" class="input-control" placeholder="admin" value="admin" required autocomplete="username">
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Maxfiy parol</label>
              <div class="input-container">
                <span class="input-icon-left">${this.icons.lock}</span>
                <input type="password" id="login-password" class="input-control" placeholder="••••••••" value="atlas2026" required autocomplete="current-password">
                <span class="input-icon-right" id="toggle-pwd-btn">${this.icons.eye}</span>
              </div>
            </div>

            <div class="auth-remember-row">
              <label class="auth-checkbox">
                <input type="checkbox" id="remember-me" checked>
                <span>Meni eslab qol</span>
              </label>
            </div>

            <button type="submit" class="btn-primary">
              <span>Tizimga kirish</span>
            </button>
          </form>

          <div class="auth-footer-tag">ATLAS CONTROL PLATFORM v2.1.0</div>
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
        this.toast('Tizimga muvaffaqiyatli kirildi', 'success');
        this.renderApp();
        this.navigate('dashboard');
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
  // APP SHELL VIEW
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
            <div class="sidebar-group-title">Asosiy Boshqaruv</div>
            <div class="nav-item" data-route="dashboard">
              ${this.icons.dashboard} <span>Boshqaruv Paneli</span>
            </div>
            <div class="nav-item" data-route="users">
              ${this.icons.users} <span>Foydalanuvchilar</span>
            </div>
            <div class="nav-item" data-route="groups">
              ${this.icons.groups} <span>Guruhlar va Kanallar</span>
            </div>
            <div class="nav-item" data-route="messages">
              ${this.icons.messages} <span>Xabarlar va Tarqatish</span>
            </div>

            <div class="sidebar-group-title">Xizmatlar & Hujjatlar</div>
            <div class="nav-item" data-route="documents">
              ${this.icons.documents} <span>Hujjatlar Generatori</span>
            </div>
            <div class="nav-item" data-route="automation">
              ${this.icons.automation} <span>Avtomatlashtirish</span>
            </div>
            <div class="nav-item" data-route="tasks">
              ${this.icons.tasks} <span>Fon Vazifalari</span>
            </div>

            <div class="sidebar-group-title">Monitoring & Tizim</div>
            <div class="nav-item" data-route="analytics">
              ${this.icons.analytics} <span>Statistika va Tahlil</span>
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
              <div class="user-name">${this.user?.full_name || 'Administrator'}</div>
              <div class="user-role">${this.user?.role || 'Superadmin'}</div>
            </div>
            <button class="btn-logout" id="logout-btn" title="Chiqish">${this.icons.logout}</button>
          </div>
        </aside>

        <!-- MAIN WRAPPER -->
        <main class="main-wrapper">
          <header class="header">
            <div class="header-left">
              <h1 class="page-title" id="page-title">Boshqaruv Paneli</h1>
              <div class="global-search-bar">
                <span class="search-icon-fixed">${this.icons.search}</span>
                <input type="text" id="global-search-input" placeholder="Qidirish...">
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
                <div class="badge-dot"></div>
              </button>
            </div>
          </header>

          <div class="content-body" id="content-viewport">
            <!-- Dynamic Route Content Goes Here -->
          </div>
        </main>
      </div>

      <!-- MODAL & SEARCH OVERLAYS -->
      <div class="modal-overlay" id="modal-container"></div>
      <div id="toast-container" class="toast-container"></div>
    `;

    // Bind sidebar clicks
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => this.navigate(btn.dataset.route));
    });

    document.getElementById('logout-btn').addEventListener('click', () => this.logout());
    document.getElementById('refresh-view-btn').addEventListener('click', () => this.navigate(this.currentRoute));
    document.getElementById('global-search-input').addEventListener('click', () => this.openGlobalSearch());
  },

  // ============================================================
  // 1. DASHBOARD VIEW
  // ============================================================
  async loadDashboard(container) {
    container.innerHTML = `<div style="text-align:center;padding:50px;color:rgba(255,255,255,0.5)">Ma'lumotlar yuklanmoqda...</div>`;
    const res = await this.api('/api/dashboard/stats');
    const actRes = await this.api('/api/dashboard/activity');

    if (!res || !res.success) {
      container.innerHTML = `<div class="glass-card">Statistikalarni yuklashda xatolik.</div>`;
      return;
    }

    const m = res.metrics;
    const b = res.bot;
    const logs = actRes?.activity || [];

    container.innerHTML = `
      <!-- KPI Cards Grid -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Jami Foydalanuvchilar</span>
            <span class="kpi-value">${m.total_users}</span>
            <span class="kpi-change">+${m.new_users_today} bugun</span>
          </div>
          <div class="kpi-icon-box">${this.icons.users}</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Faol Foydalanuvchilar</span>
            <span class="kpi-value">${m.active_users_24h}</span>
            <span class="kpi-change">24 soat ichida</span>
          </div>
          <div class="kpi-icon-box">${this.icons.analytics}</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Yuborilgan Xabarlar</span>
            <span class="kpi-value">${m.sent_messages}</span>
            <span class="kpi-change">Muvaffaqiyatli</span>
          </div>
          <div class="kpi-icon-box">${this.icons.messages}</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-info">
            <span class="kpi-label">Yaratilgan Hujjatlar</span>
            <span class="kpi-value">${m.total_docs}</span>
            <span class="kpi-change">300 DPI A4 format</span>
          </div>
          <div class="kpi-icon-box">${this.icons.documents}</div>
        </div>
      </div>

      <!-- Main Columns: Quick Actions & Live Activity -->
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:24px;">
        <!-- Left: Activity Log Stream -->
        <div class="glass-card">
          <div class="card-header-flex">
            <div>
              <div class="card-title">Jonli Faoliyat Oqimi</div>
              <div class="card-subtitle">Foydalanuvchilar va tizim harakatlari real vaqtda</div>
            </div>
            <button class="btn-sm btn-secondary" onclick="ATLAS.navigate('logs')">Barchasi</button>
          </div>

          <div class="table-responsive">
            <table class="glass-table">
              <thead>
                <tr>
                  <th>Vaqt</th>
                  <th>Modul</th>
                  <th>Harakat</th>
                  <th>Ijrochi</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                ${logs.length === 0 ? `<tr><td colspan="5" style="text-align:center">Hozircha amallar yo'q</td></tr>` : ''}
                ${logs.slice(0, 7).map(l => `
                  <tr>
                    <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.6)">${l.timestamp.substring(11, 19)}</td>
                    <td><span class="badge badge-info">${l.module}</span></td>
                    <td><b>${l.action}</b></td>
                    <td class="mono" style="font-size:12px">${l.actor}</td>
                    <td><span class="badge badge-${l.status === 'success' ? 'success' : 'error'}">${l.status}</span></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Right: Bot Status & Quick Controls -->
        <div style="display:flex;flex-direction:column;gap:24px;">
          <div class="glass-card">
            <div class="card-header-flex">
              <div class="card-title">Bot Holati</div>
              <span class="badge badge-success">Online</span>
            </div>

            <div style="display:flex;flex-direction:column;gap:12px;font-size:13.5px;">
              <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;">
                <span style="color:rgba(255,255,255,0.6)">Username:</span>
                <b class="mono" style="color:var(--accent-glow)">${b.username}</b>
              </div>
              <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;">
                <span style="color:rgba(255,255,255,0.6)">Rejim:</span>
                <b>${b.mode.toUpperCase()}</b>
              </div>
              <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;">
                <span style="color:rgba(255,255,255,0.6)">Versiya:</span>
                <span class="badge badge-info">v${b.version}</span>
              </div>
              <div style="display:flex;justify-content:space-between;">
                <span style="color:rgba(255,255,255,0.6)">Uptime:</span>
                <b style="color:#10b981">${b.uptime}</b>
              </div>
            </div>
          </div>

          <div class="glass-card">
            <div class="card-title" style="margin-bottom:16px;">Tezkor Harakatlar</div>
            <div style="display:flex;flex-direction:column;gap:10px;">
              <button class="btn-sm btn-secondary" style="width:100%;justify-content:flex-start;padding:10px 14px;" onclick="ATLAS.navigate('documents')">
                ${this.icons.documents} <span>Ma'lumotnoma yaratish</span>
              </button>
              <button class="btn-sm btn-secondary" style="width:100%;justify-content:flex-start;padding:10px 14px;" onclick="ATLAS.navigate('messages')">
                ${this.icons.send} <span>Ommaviy xabar yuborish</span>
              </button>
              <button class="btn-sm btn-secondary" style="width:100%;justify-content:flex-start;padding:10px 14px;" onclick="ATLAS.runQuickTask('sync')">
                ${this.icons.refresh} <span>Guruhlarni sinxronlash</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  },

  // ============================================================
  // 2. USERS VIEW
  // ============================================================
  async loadUsers(container) {
    container.innerHTML = `<div style="text-align:center;padding:50px;color:rgba(255,255,255,0.5)">Foydalanuvchilar yuklanmoqda...</div>`;
    const res = await this.api('/api/users');
    const users = res?.users || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Foydalanuvchilar Ro'yxati</div>
            <div class="card-subtitle">Jami ${res?.pagination?.total || users.length} ta foydalanuvchi</div>
          </div>
          <div style="display:flex;gap:12px;">
            <input type="text" id="users-search-input" class="input-control" style="height:38px;padding:0 14px;width:240px;" placeholder="Ism yoki Telegram ID...">
            <select id="users-status-select" class="select-control" style="height:38px;">
              <option value="">Barcha statuslar</option>
              <option value="active">Faol</option>
              <option value="blocked">Bloklangan</option>
            </select>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Telegram ID</th>
                <th>Ism / Familiya</th>
                <th>Username</th>
                <th>Rol</th>
                <th>Status</th>
                <th>Oxirgi Faollik</th>
                <th style="text-align:right">Amallar</th>
              </tr>
            </thead>
            <tbody id="users-table-body">
              ${users.length === 0 ? `<tr><td colspan="7" style="text-align:center">Foydalanuvchilar topilmadi</td></tr>` : ''}
              ${users.map(u => `
                <tr>
                  <td class="mono"><b>${u.telegram_id}</b></td>
                  <td>${u.first_name || ''} ${u.last_name || ''}</td>
                  <td><span class="mono" style="color:var(--text-secondary)">@${u.username || 'mavjud_emas'}</span></td>
                  <td><span class="badge badge-${u.role === 'admin' ? 'warning' : 'info'}">${u.role}</span></td>
                  <td><span class="badge badge-${u.status === 'active' ? 'success' : 'error'}">${u.status}</span></td>
                  <td style="font-size:12.5px;color:rgba(255,255,255,0.6)">${u.last_active_at || u.created_at}</td>
                  <td style="text-align:right">
                    <div style="display:flex;gap:6px;justify-content:flex-end;">
                      <button class="btn-icon" onclick="ATLAS.openSendMessageModal(${u.telegram_id})" title="Xabar yozish">${this.icons.send}</button>
                      <button class="btn-icon" onclick="ATLAS.toggleUserBlock(${u.telegram_id}, '${u.status}')" title="${u.status === 'active' ? 'Bloklash' : 'Ochish'}">
                        ${this.icons.alert}
                      </button>
                    </div>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    document.getElementById('users-search-input').addEventListener('input', (e) => {
      this.filterUsersTable(e.target.value);
    });
  },

  async toggleUserBlock(telegramId, currentStatus) {
    const nextStatus = currentStatus === 'active' ? 'blocked' : 'active';
    const res = await this.api(`/api/users/${telegramId}/status`, 'PUT', { status: nextStatus });
    if (res && res.success) {
      this.toast(res.message, 'success');
      this.navigate('users');
    }
  },

  openSendMessageModal(telegramId) {
    this.openModal(`Foydalanuvchiga Xabar Yuborish (ID: ${telegramId})`, `
      <form id="direct-msg-form">
        <div class="form-group">
          <label class="form-label">Xabar matni (HTML format qo'llab-quvvatlanadi)</label>
          <textarea id="direct-msg-text" class="textarea-control" placeholder="Hurmatli talaba..." required></textarea>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="submit" class="btn-sm btn-primary">Yuborish</button>
        </div>
      </form>
    `);

    document.getElementById('direct-msg-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const txt = document.getElementById('direct-msg-text').value;
      const res = await this.api(`/api/users/${telegramId}/message`, 'POST', { text: txt });
      if (res && res.success) {
        this.toast('Xabar foydalanuvchiga yetkazildi', 'success');
        this.closeModal();
      } else {
        this.toast(res ? res.error : 'Xatolik', 'error');
      }
    });
  },

  // ============================================================
  // 3. GROUPS VIEW
  // ============================================================
  async loadGroups(container) {
    container.innerHTML = `<div style="text-align:center;padding:50px;color:rgba(255,255,255,0.5)">Guruhlar yuklanmoqda...</div>`;
    const res = await this.api('/api/groups');
    const groups = res?.groups || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Guruhlar va Kanallar</div>
            <div class="card-subtitle">Bot a'zo bo'lgan rasmiy guruhlar monitoringi</div>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Telegram ID</th>
                <th>Nomi</th>
                <th>Turi</th>
                <th>A'zolar Soni</th>
                <th>Admin Huquqi</th>
                <th>Oxirgi Faollik</th>
              </tr>
            </thead>
            <tbody>
              ${groups.length === 0 ? `<tr><td colspan="6" style="text-align:center">Hozircha biriktirilgan guruhlar yo'q</td></tr>` : ''}
              ${groups.map(g => `
                <tr>
                  <td class="mono"><b>${g.telegram_id}</b></td>
                  <td><b>${g.title}</b></td>
                  <td><span class="badge badge-info">${g.type}</span></td>
                  <td>${g.members_count} ta</td>
                  <td><span class="badge badge-success">Mavjud</span></td>
                  <td style="font-size:12.5px;color:rgba(255,255,255,0.6)">${g.last_activity_at}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  // ============================================================
  // 4. MESSAGES / BROADCAST VIEW
  // ============================================================
  async loadMessages(container) {
    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
        <!-- Left: Create Broadcast -->
        <div class="glass-card">
          <div class="card-title" style="margin-bottom:6px;">Yangi Ommaviy Xabar Tarqatish</div>
          <div class="card-subtitle" style="margin-bottom:20px;">Barcha foydalanuvchilar yoki tanlangan guruhlarga yuborish</div>

          <form id="broadcast-form">
            <div class="form-group">
              <label class="form-label">Kampaniya nomi</label>
              <input type="text" id="bc-title" class="input-control" placeholder="E'lon yoki Yangilik" required>
            </div>

            <div class="form-group">
              <label class="form-label">Qabul qiluvchilar auditoriyasi</label>
              <select id="bc-target" class="select-control" style="width:100%;">
                <option value="all_users">Barcha faol foydalanuvchilar</option>
                <option value="groups">Barcha ulangan guruhlar</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Xabar Matni (HTML teglari qo'llaniladi)</label>
              <textarea id="bc-content" class="textarea-control" style="min-height:140px;" placeholder="Hurmatli talabalar va xodimlar..." required></textarea>
            </div>

            <button type="submit" class="btn-primary">
              ${this.icons.send} <span>Tarqatishni boshlash</span>
            </button>
          </form>
        </div>

        <!-- Right: Broadcasts History & Live Progress -->
        <div class="glass-card">
          <div class="card-title" style="margin-bottom:6px;">Tarqatishlar Tarixi</div>
          <div class="card-subtitle" style="margin-bottom:20px;">Oldingi ommaviy xabarlar hisoboti</div>

          <div id="broadcasts-history-list" style="display:flex;flex-direction:column;gap:12px;">
            <div style="color:rgba(255,255,255,0.5);font-size:13px;">Tarix yuklanmoqda...</div>
          </div>
        </div>
      </div>
    `;

    this.loadBroadcastHistory();

    document.getElementById('broadcast-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('bc-title').value;
      const target = document.getElementById('bc-target').value;
      const content = document.getElementById('bc-content').value;

      const res = await this.api('/api/broadcasts', 'POST', { title, target, content });
      if (res && res.success) {
        this.toast(`Xabar tarqatish boshlandi! Jami: ${res.total_recipients} ta qabul qiluvchi`, 'success');
        document.getElementById('broadcast-form').reset();
        this.loadBroadcastHistory();
      }
    });
  },

  async loadBroadcastHistory() {
    const listEl = document.getElementById('broadcasts-history-list');
    if (!listEl) return;
    const res = await this.api('/api/broadcasts');
    const items = res?.broadcasts || [];

    if (items.length === 0) {
      listEl.innerHTML = `<div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px;">Hali hech qanday ommaviy xabar yuborilmagan.</div>`;
      return;
    }

    listEl.innerHTML = items.map(b => `
      <div style="background:rgba(12,38,41,0.6);border:1px solid var(--border-glass);border-radius:var(--radius-md);padding:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <b>${b.title}</b>
          <span class="badge badge-${b.status === 'completed' ? 'success' : (b.status === 'running' ? 'warning' : 'info')}">${b.status}</span>
        </div>
        <div style="font-size:12.5px;color:rgba(255,255,255,0.7);margin-bottom:8px;">${b.content.substring(0, 80)}...</div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:rgba(94,234,212,0.8);">
          <span>Yetkazildi: ${b.delivered_count} / ${b.total_recipients}</span>
          <span class="mono">${b.created_at}</span>
        </div>
      </div>
    `).join('');
  },

  // ============================================================
  // 5. DOCUMENTS GENERATOR VIEW (1-kursga qabul & O'qiyapti)
  // ============================================================
  async loadDocuments(container) {
    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
        <!-- Left: Form -->
        <div class="glass-card">
          <div class="card-title" style="margin-bottom:6px;">Rasmiy Ma'lumotnoma Generatori</div>
          <div class="card-subtitle" style="margin-bottom:20px;">Ultra HD (300 DPI A4) formatda tayyorlash</div>

          <form id="doc-gen-form">
            <div class="form-group">
              <label class="form-label">Shablon turini tanlang</label>
              <select id="doc-tpl-select" class="select-control" style="width:100%;">
                <option value="qabul_1_kurs">1-kursga qabul ma'lumotnomasi</option>
                <option value="oqiyapti">O'qiyotganligi haqida ma'lumotnoma</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Talabaning to'liq F.I.O</label>
              <input type="text" id="doc-fio" class="input-control" placeholder="Napasov Ozodbek Zafar o’g’li" value="Napasov Ozodbek Zafar o’g’li" required>
            </div>

            <div class="form-group">
              <label class="form-label">Ta'lim Yo'nalishi</label>
              <select id="doc-yonalish" class="select-control" style="width:100%;">
                <option value="Hamshiralik ishi">Hamshiralik ishi</option>
                <option value="Davolash ishi (Feldsherlik)">Davolash ishi (Feldsherlik)</option>
                <option value="Farmatsiya">Farmatsiya</option>
                <option value="Stomatologiya ishi">Stomatologiya ishi</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">O'quv yili</label>
              <input type="text" id="doc-oquv-yili" class="input-control" placeholder="2026/2027" value="2026/2027" required>
            </div>

            <div id="extra-oqiyapti-fields" style="display:none;">
              <div class="form-group">
                <label class="form-label">Kursi</label>
                <select id="doc-kursi" class="select-control" style="width:100%;">
                  <option value="1">1-kurs</option>
                  <option value="2" selected>2-kurs</option>
                  <option value="3">3-kurs</option>
                  <option value="4">4-kurs</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Guruhi</label>
                <input type="text" id="doc-guruhi" class="input-control" placeholder="201" value="201">
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Berilgan Sana</label>
              <input type="text" id="doc-sana" class="input-control" placeholder="14.08.2026" value="14.08.2026" required>
            </div>

            <button type="submit" class="btn-primary" id="doc-generate-btn">
              ${this.icons.documents} <span>Hujjatni shakllantirish</span>
            </button>
          </form>
        </div>

        <!-- Right: Live Preview & Download -->
        <div class="glass-card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:500px;text-align:center;">
          <div id="doc-preview-box" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="width:64px;height:64px;color:rgba(0,203,169,0.3);margin-bottom:14px;">${this.icons.documents}</div>
            <div style="font-size:15px;font-weight:600;color:rgba(255,255,255,0.7);margin-bottom:6px;">Hujjat oldindan ko'rish maydoni</div>
            <div style="font-size:13px;color:rgba(94,234,212,0.6);max-width:320px;">Chapdagi maydonlarni to'ldirib, "Hujjatni shakllantirish" tugmasini bosing.</div>
          </div>
        </div>
      </div>
    `;

    const tplSelect = document.getElementById('doc-tpl-select');
    const extraFields = document.getElementById('extra-oqiyapti-fields');
    tplSelect.addEventListener('change', () => {
      extraFields.style.display = tplSelect.value === 'oqiyapti' ? 'block' : 'none';
      if (tplSelect.value === 'oqiyapti') {
        document.getElementById('doc-oquv-yili').value = '2024/2025';
      } else {
        document.getElementById('doc-oquv-yili').value = '2026/2027';
      }
    });

    document.getElementById('doc-gen-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('doc-generate-btn');
      btn.innerHTML = `<span>Shakllantirilmoqda...</span>`;

      const tpl_id = document.getElementById('doc-tpl-select').value;
      const answers = {
        FIO: document.getElementById('doc-fio').value,
        YONALISH: document.getElementById('doc-yonalish').value,
        OQUV_YILI: document.getElementById('doc-oquv-yili').value,
        SANA: document.getElementById('doc-sana').value
      };
      if (tpl_id === 'oqiyapti') {
        answers['KURSI'] = document.getElementById('doc-kursi').value;
        answers['GURUHI'] = document.getElementById('doc-guruhi').value;
      }

      const res = await this.api('/api/documents/generate', 'POST', { template_id: tpl_id, answers });
      btn.innerHTML = `${this.icons.documents} <span>Hujjatni shakllantirish</span>`;

      if (res && res.success) {
        this.toast(res.message, 'success');
        const prevBox = document.getElementById('doc-preview-box');
        prevBox.innerHTML = `
          <img src="${res.download_url}" style="max-width:100%;max-height:460px;border-radius:var(--radius-sm);box-shadow:var(--shadow-card);border:1px solid var(--border-glass);" alt="Hujjat">
          <div style="display:flex;gap:12px;margin-top:20px;">
            <a href="${res.download_url}" target="_blank" class="btn-sm btn-secondary">${this.icons.eye} To'liq ko'rish</a>
            <a href="${res.download_url}" download="Malumotnoma.png" class="btn-sm btn-primary">${this.icons.download} Yuklab olish</a>
          </div>
        `;
      } else {
        this.toast(res ? res.error : 'Hujjat yaratishda xatolik', 'error');
      }
    });
  },

  // ============================================================
  // 6. AUTOMATIONS VIEW
  // ============================================================
  async loadAutomation(container) {
    const res = await this.api('/api/automations');
    const list = res?.automations || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Avtomatlashtirish Qoidalari</div>
            <div class="card-subtitle">Trigger va shartlar asosidagi avtomatik jarayonlar</div>
          </div>
          <button class="btn-sm btn-primary" onclick="ATLAS.openNewAutomationModal()">${this.icons.plus} Yangi Qoida</button>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Qoida Nomi</th>
                <th>Trigger Turi</th>
                <th>Trigger Qiymati</th>
                <th>Amal (Action)</th>
                <th>Holati</th>
                <th style="text-align:right">Boshqarish</th>
              </tr>
            </thead>
            <tbody>
              ${list.length === 0 ? `<tr><td colspan="6" style="text-align:center">Hozircha qoidalar yo'q</td></tr>` : ''}
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
                  <td style="text-align:right">
                    <button class="btn-icon" onclick="ATLAS.deleteAutomation(${a.id})" title="O'chirish">${this.icons.trash}</button>
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
    if (res && res.success) this.toast('Qoida holati yangilandi', 'success');
  },

  async deleteAutomation(id) {
    if (!confirm("Haqiqatdan ham ushbu qoidani o'chirmoqchimisiz?")) return;
    const res = await this.api(`/api/automations/${id}`, 'DELETE');
    if (res && res.success) {
      this.toast('Qoida o\'chirildi', 'success');
      this.navigate('automation');
    }
  },

  openNewAutomationModal() {
    this.openModal('Yangi Avtomatlashtirish Qoidasi', `
      <form id="new-auto-form">
        <div class="form-group">
          <label class="form-label">Qoida Nomi</label>
          <input type="text" id="auto-name" class="input-control" placeholder="Guruhga yangi a'zo qo'shilganda" required>
        </div>
        <div class="form-group">
          <label class="form-label">Trigger Turi</label>
          <select id="auto-trigger-type" class="select-control" style="width:100%;">
            <option value="command">Buyruq yozilganda (masalan: /start)</option>
            <option value="keyword">Kalit so'z topilganda</option>
            <option value="user_join">Foydalanuvchi guruhga kirganda</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Trigger Qiymati</label>
          <input type="text" id="auto-trigger-val" class="input-control" placeholder="/start yoki kontrakt" required>
        </div>
        <div class="form-group">
          <label class="form-label">Amal Turi</label>
          <select id="auto-action-type" class="select-control" style="width:100%;">
            <option value="send_message">Avtomatik xabar yuborish</option>
            <option value="alert_admin">Administratorga bildirishnoma</option>
          </select>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="submit" class="btn-sm btn-primary">Saqlash</button>
        </div>
      </form>
    `);

    document.getElementById('new-auto-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const body = {
        name: document.getElementById('auto-name').value,
        trigger_type: document.getElementById('auto-trigger-type').value,
        trigger_value: document.getElementById('auto-trigger-val').value,
        action_type: document.getElementById('auto-action-type').value
      };
      const res = await this.api('/api/automations', 'POST', body);
      if (res && res.success) {
        this.toast('Yangi qoida saqlandi', 'success');
        this.closeModal();
        this.navigate('automation');
      }
    });
  },

  // ============================================================
  // 7. TASKS VIEW
  // ============================================================
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
          <button class="btn-sm btn-primary" onclick="ATLAS.runQuickTask('custom')">${this.icons.plus} Yangi Vazifa Boshlash</button>
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
              ${tasks.length === 0 ? `<tr><td colspan="5" style="text-align:center">Hozircha vazifalar yo'q</td></tr>` : ''}
              ${tasks.map(t => `
                <tr>
                  <td><b>${t.task_name}</b></td>
                  <td><span class="badge badge-info">${t.task_type}</span></td>
                  <td><span class="badge badge-${t.status === 'completed' ? 'success' : (t.status === 'running' ? 'warning' : 'error')}">${t.status}</span></td>
                  <td class="mono" style="font-size:12px;">${t.started_at || t.created_at}</td>
                  <td>${t.duration_seconds}s</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  async runQuickTask(type) {
    const res = await this.api('/api/tasks/run', 'POST', { name: 'Tizim ma\'lumotlarini yangilash', type });
    if (res && res.success) {
      this.toast(res.message, 'success');
      this.navigate('tasks');
    }
  },

  // ============================================================
  // 8. ANALYTICS VIEW
  // ============================================================
  async loadAnalytics(container) {
    const res = await this.api('/api/analytics/charts');
    const labels = res?.labels || ['Du', 'Se', 'Chor', 'Pay', 'Ju', 'Sha', 'Yak'];
    const s = res?.series || { users: [4, 6, 8, 12, 15, 18, 22], messages: [10, 18, 25, 30, 42, 38, 50] };

    container.innerHTML = `
      <div class="glass-card" style="margin-bottom:24px;">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Faollik Trendlari (Oxirgi 7 kun)</div>
            <div class="card-subtitle">Foydalanuvchilar soni va yuborilgan xabarlar dinamikasi</div>
          </div>
          <span class="badge badge-info">7 Kunlik</span>
        </div>

        <!-- Clean SVG Visual Chart -->
        <div style="width:100%;height:260px;display:flex;align-items:flex-end;gap:18px;padding-top:20px;">
          ${labels.map((lbl, idx) => {
            const uVal = s.users[idx] || 5;
            const mVal = s.messages[idx] || 15;
            const hU = Math.min(uVal * 8, 180);
            const hM = Math.min(mVal * 3.5, 220);
            return `
              <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;height:100%;justify-content:flex-end;">
                <div style="display:flex;gap:6px;align-items:flex-end;width:100%;justify-content:center;">
                  <div style="width:18px;height:${hU}px;background:var(--accent-gradient);border-radius:4px 4px 0 0;" title="Foydalanuvchilar: ${uVal}"></div>
                  <div style="width:18px;height:${hM}px;background:rgba(6,182,212,0.6);border-radius:4px 4px 0 0;" title="Xabarlar: ${mVal}"></div>
                </div>
                <span style="font-size:12px;color:rgba(255,255,255,0.6);">${lbl}</span>
              </div>
            `;
          }).join('')}
        </div>
        <div style="display:flex;gap:20px;justify-content:center;margin-top:16px;font-size:12.5px;">
          <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:var(--accent-glow);border-radius:2px;"></div><span>Foydalanuvchilar</span></div>
          <div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:rgb(6,182,212);border-radius:2px;"></div><span>Xabarlar Oqimi</span></div>
        </div>
      </div>
    `;
  },

  // ============================================================
  // 9. LOGS VIEW
  // ============================================================
  async loadLogs(container) {
    const res = await this.api('/api/logs');
    const logs = res?.logs || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Tizim Audit Loglari</div>
            <div class="card-subtitle">Barcha amallar va hodisalar xavfsiz qaydnomasi</div>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th>Vaqt</th>
                <th>Modul</th>
                <th>Harakat</th>
                <th>Ijrochi</th>
                <th>Status</th>
                <th>Detallar</th>
              </tr>
            </thead>
            <tbody>
              ${logs.length === 0 ? `<tr><td colspan="6" style="text-align:center">Loglar mavjud emas</td></tr>` : ''}
              ${logs.map(l => `
                <tr>
                  <td class="mono" style="font-size:12px;">${l.timestamp}</td>
                  <td><span class="badge badge-info">${l.module}</span></td>
                  <td><b>${l.action}</b></td>
                  <td class="mono">${l.actor}</td>
                  <td><span class="badge badge-${l.status === 'success' ? 'success' : (l.status === 'error' ? 'error' : 'warning')}">${l.status}</span></td>
                  <td class="mono" style="font-size:11.5px;color:rgba(94,234,212,0.8);">${l.details_json || '{}'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  },

  // ============================================================
  // 10. MODULES VIEW
  // ============================================================
  async loadModules(container) {
    const res = await this.api('/api/modules');
    const mods = res?.modules || [];

    container.innerHTML = `
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <div class="card-title">Modullar Boshqaruvi</div>
            <div class="card-subtitle">Botning mustaqil modullarini yoqish yoki o'chirish</div>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:20px;">
          ${mods.map(m => `
            <div style="background:rgba(12,38,41,0.6);border:1px solid var(--border-glass);border-radius:var(--radius-md);padding:20px;display:flex;flex-direction:column;justify-content:space-between;gap:14px;">
              <div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                  <b style="font-size:15px;">${m.name}</b>
                  <label class="switch">
                    <input type="checkbox" ${m.is_enabled ? 'checked' : ''} onchange="ATLAS.toggleModule('${m.key}')">
                    <span class="slider"></span>
                  </label>
                </div>
                <p style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.4;">${m.description}</p>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:12px;color:rgba(94,234,212,0.6);">
                <span>Kalit: <code>${m.key}</code></span>
                <span class="badge badge-${m.is_enabled ? 'success' : 'error'}">${m.is_enabled ? 'Faol' : 'O\'chiq'}</span>
              </div>
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

  // ============================================================
  // 11. SETTINGS VIEW
  // ============================================================
  async loadSettings(container) {
    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
        <!-- Left: Password Change -->
        <div class="glass-card">
          <div class="card-title" style="margin-bottom:6px;">Xavfsizlik & Parol</div>
          <div class="card-subtitle" style="margin-bottom:20px;">Administrator hisob parolini o'zgartirish</div>

          <form id="change-pwd-form">
            <div class="form-group">
              <label class="form-label">Joriy Parol</label>
              <input type="password" id="old-pwd" class="input-control" required>
            </div>
            <div class="form-group">
              <label class="form-label">Yangi Parol (Kamida 6 belgi)</label>
              <input type="password" id="new-pwd" class="input-control" required>
            </div>
            <button type="submit" class="btn-primary">Parolni yangilash</button>
          </form>
        </div>

        <!-- Right: Bot Info -->
        <div class="glass-card">
          <div class="card-title" style="margin-bottom:6px;">Tizim Sozlamalari</div>
          <div class="card-subtitle" style="margin-bottom:20px;">Telegram bot konfiguratsiyasi</div>

          <div style="display:flex;flex-direction:column;gap:14px;font-size:13.5px;">
            <div>
              <span class="form-label">Bosh Administrator Telegram ID</span>
              <input type="text" class="input-control" value="8135594558" readonly>
            </div>
            <div>
              <span class="form-label">Bot Token Holati</span>
              <input type="text" class="input-control" value="•••••••••••••••••••••••••••••" readonly>
            </div>
            <div>
              <span class="form-label">Ishlash Rejimi</span>
              <input type="text" class="input-control" value="Webhook (Avtomatik)" readonly>
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
    this.openModal('Global Qidiruv (Ctrl+K)', `
      <div style="margin-bottom:16px;">
        <input type="text" id="modal-search-input" class="input-control" placeholder="Foydalanuvchi, hujjat yoki log..." autofocus>
      </div>
      <div id="modal-search-results" style="display:flex;flex-direction:column;gap:8px;max-height:300px;overflow-y:auto;">
        <div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px;">Qidirish uchun kamida 2 ta harf yozing...</div>
      </div>
    `);

    document.getElementById('modal-search-input').addEventListener('input', async (e) => {
      const q = e.target.value.trim();
      const resBox = document.getElementById('modal-search-results');
      if (q.length < 2) {
        resBox.innerHTML = `<div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px;">Qidirish uchun kamida 2 ta harf yozing...</div>`;
        return;
      }

      const res = await this.api(`/api/search?q=${encodeURIComponent(q)}`);
      const items = res?.results || [];

      if (items.length === 0) {
        resBox.innerHTML = `<div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px;">Hech narsa topilmadi.</div>`;
        return;
      }

      resBox.innerHTML = items.map(it => `
        <div style="background:rgba(12,38,41,0.6);border:1px solid var(--border-glass);border-radius:var(--radius-sm);padding:10px 14px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;" onclick="ATLAS.closeModal(); ATLAS.navigate('${it.route}')">
          <div>
            <b>${it.title}</b>
            <div style="font-size:12px;color:rgba(94,234,212,0.7);">${it.subtitle}</div>
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

  closeModal() {
    const el = document.getElementById('modal-container');
    if (el) el.classList.remove('active');
  }
};

// Start ATLAS App on DOM Ready
document.addEventListener('DOMContentLoaded', () => ATLAS.init());
