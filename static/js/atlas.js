// ============================================================
//  static/js/atlas.js
//  ATLAS Universal Bot Platform — Single Page Application Engine
//  Shaxsiy Markaziy Boshqaruv & Hujjatlar Arxiv Tizimi
//  NO EMOJIS — 100% SVG Vector UI & Dynamic REST API Client
// ============================================================

const ATLAS_NAV_LOGO_PNG = 'data:image/png;base64,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';
const ATLAS_ICE_LOGO_PNG = 'data:image/png;base64,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';

const ATLAS = {
  token: localStorage.getItem('atlas_token') || '',
  user: JSON.parse(localStorage.getItem('atlas_user') || 'null'),
  currentRoute: (window.location.hash || '').replace(/^#\/?/, '').trim() || localStorage.getItem('atlas_last_route') || 'hub',
  activeDocTab: 'generate',  // 'generate' yoki 'archive'
  brandLogoPng: ATLAS_ICE_LOGO_PNG,
  icons: {
    dashboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg>`,
    grid: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg>`,
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
    close: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
    menu: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`,
    chevronDown: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="6 9 12 15 18 9"/></svg>`,
    brandLogo: `<img src="${ATLAS_NAV_LOGO_PNG}" style="height:100%;max-width:100%;object-fit:contain;filter:drop-shadow(0 0 10px rgba(56,189,248,0.85));" alt="ATLAS">`,
    folder: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>`,
    calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
    activity: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>`,
    bookOpen: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`,
    home: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
    arrowLeft: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>`,
    arrowRight: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
    upload: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`,
    clipboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>`,
    save: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>`,
    zap: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    mapPin: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
    info: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`,
    fileText: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`,
    package: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`,
    target: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
    dollarSign: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`,
    play: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>`,
    pause: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>`,
    instagram: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>`,
    youtube: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg>`,
    clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    heart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`,
    videoCamera: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>`,
    externalLink: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`
  },

  // SERVICES REGISTRY FOR DYNAMIC SERVICE HUB (MUNDARIJA)
  SERVICES_REGISTRY: [
    {
      id: 'contracts',
      num: '1',
      title: 'KONTRAKTLAR & BAZA',
      subtitle: 'Bank debitorkasi, 1C/Hemis sinxronlash va to\'lovlar monitoringi',
      category: 'Moliya & Hujjatlar',
      color: '#10b981',
      glow: 'rgba(16, 185, 129, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`
    },
    {
      id: 'amaliyot',
      num: '2',
      title: 'MALAKAVIY AMALIYOT',
      subtitle: 'Talabalar amaliyot buyruqlari, korxonalar bazasi va so\'rovnomalar',
      category: 'O\'quv Bo\'limi',
      color: '#0ea5e9',
      glow: 'rgba(14, 165, 233, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`
    },
    {
      id: 'certificates',
      num: '3',
      title: 'MA\'LUMOTNOMALAR',
      subtitle: 'QR-kodli rasmiy o\'qish ma\'lumotnomalari va buyruqlar generatori',
      category: 'Hujjatlar',
      color: '#6366f1',
      glow: 'rgba(99, 102, 241, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7h3v3H7zM14 7h3v3h-3zM7 14h3v3H7zM14 14h3v3h-3z"/></svg>`
    },
    {
      id: 'orders',
      num: '4',
      title: 'RASMIY BUYRUQLAR',
      subtitle: 'Rektorat farmoyishlari, chetlashtirish va tiklash buyruqlari arxivi',
      category: 'Kantselyariya',
      color: '#8b5cf6',
      glow: 'rgba(139, 92, 246, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 12h6M9 16h6"/></svg>`
    },
    {
      id: 'meta_ads',
      num: '5',
      title: 'META ADS MANAGER',
      subtitle: 'Facebook va Instagram reklama hisoblari, lidlar tahlili va kampaniyalar',
      category: 'Marketing',
      color: '#ec4899',
      glow: 'rgba(236, 72, 153, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8a4 4 0 0 0-4 4c0 2 2 4 4 4s4-2 4-4a4 4 0 0 0-4-4z"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/></svg>`
    },
    {
      id: 'instagram',
      num: '6',
      title: 'INSTAGRAM & YT POSTER',
      subtitle: 'Reels va postlarni Telegram kanal va YouTube Shorts\'ga avtomatik joylash',
      category: 'Avtomatizatsiya',
      color: '#f43f5e',
      glow: 'rgba(244, 63, 94, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>`
    },
    {
      id: 'pc_control',
      num: '7',
      title: 'KOMPYUTER BOSHQARUVI',
      subtitle: 'Windows monitoring, ko\'p monitorli skrinshot, veb-kamera, Sunshine va quvvat',
      category: 'Masofaviy Boshqaruv',
      color: '#00f2fe',
      glow: 'rgba(0, 242, 254, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`
    },
    {
      id: 'ai_chat',
      num: '8',
      title: 'AI PC AGENT CHAT',
      subtitle: 'Kompyuterni boshqaruvchi o\'zbek tilidagi aqlli AI suhbatdosh va assistent',
      category: 'Sun\'iy Intellekt',
      color: '#a855f7',
      glow: 'rgba(168, 85, 247, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>`
    },
    {
      id: 'mtf_converter',
      num: '9',
      title: 'MTF & TEST GENERATOR',
      subtitle: 'MyTestX (.mtf / .xml) testlarini 2-ustunli PDF kitobcha, DOCX va online testga o‘girish',
      category: 'O\'quv & Testlar',
      color: '#3b82f6',
      glow: 'rgba(59, 130, 246, 0.45)',
      icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`
    }
  ],

  // API Wrapper
  async api(endpoint, method = 'GET', body = null) {
    const headers = { 'Content-Type': 'application/json' };
    if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

    let targetUrl = endpoint;
    // MTF konvertor uchun agar foydalanuvchi Vercel'da bo'lsa va lokal server (localhost:5005) yoniq bo'lsa, to'g'ridan-to'g'ri lokal kompyuterda 100% tezkor bajarish
    if (endpoint.startsWith('/api/mtf/convert') && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      try {
        const ping = await fetch('http://localhost:5005/api/ping', { method: 'GET', mode: 'cors' }).catch(() => null);
        if (ping && ping.ok) {
          targetUrl = 'http://localhost:5005' + endpoint;
        }
      } catch (e) {}
    }

    try {
      const res = await fetch(targetUrl, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
      });

      if (res.status === 401 && this.currentRoute !== 'login') {
        this.logout();
        return null;
      }

      const json = await res.json().catch(() => null);
      if (!res.ok) {
        return json || { success: false, error: `HTTP ${res.status}: Server xatoligi` };
      }
      return json;
    } catch (err) {
      console.error('API Error:', err);
      return { success: false, error: err.message || 'Server bilan aloqa uzildi' };
    }
  },

  // Universal Authenticated File Downloader
  async downloadFile(url, fallbackFilename = 'hujjat') {
    this.toast('Fayl tayyorlanmoqda va yuklab olinmoqda...', 'info');
    try {
      let fetchUrl = url;
      if (this.token && !fetchUrl.includes('token=')) {
        fetchUrl += (fetchUrl.includes('?') ? '&' : '?') + `token=${encodeURIComponent(this.token)}`;
      }
      
      const headers = {};
      if (this.token) headers['Authorization'] = `Bearer ${this.token}`;

      const res = await fetch(fetchUrl, { headers });
      if (!res.ok) {
        let errText = 'Faylni yuklab olishda xatolik yuz berdi.';
        try {
          const errJson = await res.json();
          if (errJson && errJson.error) errText = errJson.error;
        } catch (_) {}
        this.toast(errText, 'error');
        return;
      }

      const blob = await res.blob();
      let filename = fallbackFilename;
      const disposition = res.headers.get('Content-Disposition');
      if (disposition && disposition.includes('filename=')) {
        const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '').trim();
        }
      }

      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = blobUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(blobUrl);
      }, 500);

      this.toast('Fayl muvaffaqiyatli yuklab olindi!', 'success');
    } catch (err) {
      console.error('Download error:', err);
      this.toast('Yuklab olishda xatolik: ' + err.message, 'error');
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

  showToast(message, type = 'success') {
    return this.toast(message, type);
  },

  // Universal Modal System
  modal({ title, contentHtml, maxWidth = '560px' }) {
    let container = document.getElementById('modal-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'modal-container';
      container.className = 'modal-backdrop';
      document.body.appendChild(container);
    }

    container.innerHTML = `
      <div class="modal-card" style="max-width:${maxWidth};">
        <div class="modal-header">
          <h3 style="margin:0;font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px;">${title}</h3>
          <button class="modal-close" onclick="ATLAS.closeModal()">&times;</button>
        </div>
        <div class="modal-body" style="padding:20px 24px;">
          ${contentHtml}
        </div>
      </div>
    `;
    container.classList.add('active');
  },

  closeModal() {
    const container = document.getElementById('modal-container');
    if (container) {
      container.classList.remove('active');
      container.innerHTML = '';
    }
  },

  // Cyber Action Loader & Live Progress System
  showActionLoader({
    title = "Jarayon Bajarilmoqda...",
    subtitle = "Iltimos kuting, tizim so'rovingizni bajarmoqda",
    icon = null,
    steps = [
      "Fayl ma'lumotlari aniqlanmoqda",
      "HD video serverga yuklab olinmoqda",
      "Kanalga yuborilmoqda",
      "Baza va statistika yangilanmoqda"
    ],
    funFact = "ATLAS tizimi har bir postni eng yuqori HD sifatda kanallarga yetkazadi."
  } = {}) {
    let overlay = document.getElementById('cyber-action-loader-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'cyber-action-loader-overlay';
      overlay.className = 'cyber-action-overlay';
      document.body.appendChild(overlay);
    }

    const defaultIcon = `
      <svg style="width:28px;height:28px;fill:currentColor;" viewBox="0 0 24 24">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
      </svg>
    `;

    const stepsHtml = steps.map((s, idx) => `
      <div class="cyber-step-item ${idx === 0 ? 'active' : ''}" id="cyber-step-${idx}">
        <div class="cyber-step-dot"></div>
        <span>${s}</span>
      </div>
    `).join('');

    overlay.innerHTML = `
      <div class="cyber-action-card">
        <div class="cyber-loader-spinner-box">
          <div class="cyber-loader-glow-ring"></div>
          <div class="cyber-loader-inner-core">
            ${icon || defaultIcon}
          </div>
        </div>
        <div class="cyber-loader-title">${title}</div>
        <div class="cyber-loader-subtitle">${subtitle}</div>
        
        <div class="cyber-loader-bar-wrap">
          <div class="cyber-loader-bar-fill" id="cyber-loader-progress-bar"></div>
        </div>

        <div class="cyber-steps-list">
          ${stepsHtml}
        </div>

        <div class="cyber-fun-fact">${this.icons.info || ''} ${funFact}</div>
      </div>
    `;

    requestAnimationFrame(() => overlay.classList.add('active'));

    if (this._stepInterval) clearInterval(this._stepInterval);
    let currentStep = 0;
    this._stepInterval = setInterval(() => {
      currentStep++;
      if (currentStep < steps.length) {
        const prevEl = document.getElementById(`cyber-step-${currentStep - 1}`);
        const nextEl = document.getElementById(`cyber-step-${currentStep}`);
        if (prevEl) {
          prevEl.classList.remove('active');
          prevEl.classList.add('done');
        }
        if (nextEl) {
          nextEl.classList.add('active');
        }
      }
    }, 1600);
  },

  hideActionLoader() {
    if (this._stepInterval) {
      clearInterval(this._stepInterval);
      this._stepInterval = null;
    }
    const overlay = document.getElementById('cyber-action-loader-overlay');
    if (overlay) {
      overlay.classList.remove('active');
      setTimeout(() => {
        if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
      }, 320);
    }
  },

  confirmModal({ title, message, confirmText = "O'chirish", onConfirm }) {
    this.modal({
      title: `<span style="color:#f87171;">⚠️ ${title || 'Tasdiqlash'}</span>`,
      maxWidth: '440px',
      contentHtml: `
        <p style="font-size:13px;color:rgba(255,255,255,0.8);margin-bottom:20px;line-height:1.5;">
          ${message || "Haqiqatan ham bu amalni bajarmoqchimisiz?"}
        </p>
        <div style="display:flex;justify-content:flex-end;gap:10px;">
          <button type="button" class="btn-secondary btn-sm" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="button" class="btn-danger btn-sm" id="btn-modal-confirm-action" style="background:#ef4444;color:#fff;border:none;padding:6px 16px;font-weight:700;border-radius:var(--radius-sm);cursor:pointer;">
            ${confirmText}
          </button>
        </div>
      `
    });

    document.getElementById('btn-modal-confirm-action')?.addEventListener('click', async () => {
      this.closeModal();
      if (typeof onConfirm === 'function') {
        await onConfirm();
      }
    });
  },

  // Init Application with Strict Server Verification
  async init() {
    this.bindGlobalEvents();
    const hash = (window.location.hash || '').replace(/^#\/?/, '').trim();
    if (hash && ['hub', 'contracts', 'orders', 'certificates', 'amaliyot', 'meta_ads', 'instagram', 'academic_groups', 'groups', 'dashboard', 'analytics', 'logs', 'settings', 'pc_control'].includes(hash)) {
      this.currentRoute = hash;
    } else {
      this.currentRoute = 'hub';
    }

    // 1. Agar token yoki user bo'lmasa, darhol Login oynasini ochish
    if (!this.token || !this.user) {
      this.token = '';
      this.user = null;
      localStorage.removeItem('atlas_token');
      localStorage.removeItem('atlas_user');
      this.renderLogin();
      return;
    }

    // 2. Token mavjud bo'lsa, uni server orqali qat'iy tekshirish
    const root = document.getElementById('app-root');
    if (root) {
      root.innerHTML = `
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;background:#0d1117;color:#fff;font-family:sans-serif;">
          <div class="spinner" style="width:38px;height:38px;border-width:3px;margin-bottom:14px;"></div>
          <div style="font-size:13px;color:rgba(255,255,255,0.6);letter-spacing:0.04em;">Xavfsizlik tekshirilmoqda...</div>
        </div>
      `;
    }

    try {
      const res = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${this.token}` }
      });

      if (!res.ok) {
        this.logout();
        return;
      }

      const data = await res.json();
      if (!data || !data.success || !data.user || data.user.username.toLowerCase() !== 'ozodbek') {
        this.logout();
        return;
      }

      this.user = data.user;
      localStorage.setItem('atlas_user', JSON.stringify(data.user));
      this.renderApp();
      this.startSystemStatusTimer();
      const savedRoute = (window.location.hash || '').replace(/^#\/?/, '').trim() || localStorage.getItem('atlas_last_route') || 'hub';
      this.navigate(savedRoute, true);
    } catch (err) {
      console.error('Auth check error:', err);
      this.logout();
    }
  },

  // Live System Version & Elapsed Time Tracker
  startSystemStatusTimer() {
    if (!this.systemDeployTime) {
      this.systemDeployTime = new Date();
    }

    const updateDisplay = () => {
      const clockEl = document.getElementById('sys-update-clock');
      const elapsedEl = document.getElementById('sys-elapsed-badge');
      if (!clockEl || !elapsedEl) return;

      const d = this.systemDeployTime;
      const day = String(d.getDate()).padStart(2, '0');
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const year = d.getFullYear();
      const hours = String(d.getHours()).padStart(2, '0');
      const minutes = String(d.getMinutes()).padStart(2, '0');
      clockEl.innerText = `${day}.${month}.${year}, ${hours}:${minutes}`;

      const now = new Date();
      const diffSec = Math.floor((now - d) / 1000);
      const diffMin = Math.floor(diffSec / 60);
      const diffHours = Math.floor(diffMin / 60);

      if (diffMin < 1) {
        elapsedEl.innerText = "hozirgina";
        elapsedEl.style.color = "#34d399";
      } else if (diffMin < 60) {
        elapsedEl.innerText = `${diffMin} daqiqa oldin`;
        elapsedEl.style.color = "#5eead4";
      } else {
        elapsedEl.innerText = `${diffHours} soat ${diffMin % 60} daq oldin`;
        elapsedEl.style.color = "#fbbf24";
      }
    };

    updateDisplay();
    if (this._statusTimer) clearInterval(this._statusTimer);
    this._statusTimer = setInterval(updateDisplay, 15000);
  },

  bindGlobalEvents() {
    window.addEventListener('hashchange', () => {
      const hash = (window.location.hash || '').replace(/^#\/?/, '').trim();
      if (hash && hash !== this.currentRoute && this.token && this.user) {
        this.navigate(hash, false);
      }
    });

    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        this.openGlobalSearch();
      }
      if (e.key === 'Escape') {
        this.closeModal();
      }
    });

    // Global interceptor for all platform download links
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href) return;

      if (
        href.startsWith('/api/documents/download') ||
        href.startsWith('/api/contracts/download') ||
        href.startsWith('/api/amaliyot/download') ||
        href.startsWith('/api/amaliyot/survey/sample-excel')
      ) {
        e.preventDefault();
        const downloadName = link.getAttribute('download') || link.getAttribute('title') || 'fayl';
        this.downloadFile(href, downloadName);
      }
    });
  },

  // Router
  navigate(route, updateHash = true) {
    if (!this.token || !this.user) {
      this.renderLogin();
      return;
    }

    route = String(route || '').replace(/^#\/?/, '').trim() || 'hub';
    this.currentRoute = route;
    try {
      localStorage.setItem('atlas_last_route', route);
    } catch (e) {}

    if (updateHash && window.location.hash !== '#/' + route && window.location.hash !== '#' + route) {
      window.location.hash = '#/' + route;
    }

    const appContainer = document.querySelector('.app-container');
    if (appContainer) {
      if (route === 'hub') {
        appContainer.classList.add('hub-mode');
      } else {
        appContainer.classList.remove('hub-mode');
      }
    }

    // Cursor visibility
    const cursor = document.getElementById('hub-custom-cursor');
    const dot = document.getElementById('hub-cursor-dot');
    if (route === 'hub') {
      document.body.classList.add('hub-cursor-active');
      if (cursor) cursor.style.display = 'block';
      if (dot) dot.style.display = 'block';
    } else {
      document.body.classList.remove('hub-cursor-active');
      if (cursor) cursor.style.display = 'none';
      if (dot) dot.style.display = 'none';
    }

    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });
    document.querySelectorAll('.nav-sub-item').forEach(el => {
      el.classList.toggle('active', el.dataset.route === route);
    });

    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
      const titles = {
        hub: 'Mundarija — Barcha Xizmatlar',
        contracts: 'Kontraktlar & Bank Debitorkasi Yangilash',
        orders: 'Rasmiy Buyruqlar Bolimi',
        certificates: "Rasmiy Ma'lumotnomalar Bolimi",
        amaliyot: "Malakaviy Amaliyot Buyruqlari & Rejalari",
        meta_ads: 'Meta Ads Manager Boshqaruv Markazi',
        instagram: "Instagram Postlarini Sinxronlash & AutoPoster",
        academic_groups: "O'quv Guruhlari Boshqaruvi",
        groups: 'Ulangan Telegram Guruhlar',
        dashboard: 'Boshqaruv Paneli',
        users: 'Foydalanuvchilar Boshqaruvi',
        messages: 'Xabarlar va Tarqatish',
        automation: 'Avtomatlashtirish',
        tasks: 'Fon Vazifalari',
        analytics: 'Statistika va Tahlil',
        logs: 'Tizim Loglari',
        settings: 'Bot va Tizim Sozlamalari',
        modules: 'Modullar Boshqaruvi',
        pc_control: 'Kompyuter Boshqaruvi & Realtime Monitoring',
        ai_chat: 'AI PC Agent Chat (Aqlli Assistent)',
        mtf_converter: 'MTF & Test Generator (PDF / DOCX Konvertor)'
      };
      pageTitle.innerText = titles[route] || 'ATLAS Boshqaruv Markazi';
    }

    const viewport = document.getElementById('content-viewport');
    if (!viewport) return;

    if (route === 'hub') {
      this.loadHub(viewport);
      return;
    }

    viewport.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;min-height:300px;"><div class="spinner"></div></div>';

    switch (route) {
      case 'contracts': this.loadContracts(viewport, 'update'); break;
      case 'orders': this.loadOrders(viewport); break;
      case 'certificates': this.loadCertificates(viewport); break;
      case 'amaliyot': this.loadAmaliyot(viewport); break;
      case 'mtf_converter': this.loadMtfConverter(viewport); break;
      case 'meta_ads': this.loadMetaAds(viewport); break;
      case 'instagram': this.loadInstagram(viewport); break;
      case 'academic_groups': this.loadGroups(viewport, 'academic'); break;
      case 'groups': this.loadGroups(viewport, 'telegram'); break;
      case 'dashboard': this.loadDashboard(viewport); break;
      case 'pc_control': this.loadPcControl(viewport); break;
      case 'ai_chat': this.loadAiChat(viewport); break;
      case 'users': this.loadUsers(viewport); break;
      case 'messages': this.loadMessages(viewport); break;
      case 'automation': this.loadAutomation(viewport); break;
      case 'tasks': this.loadTasks(viewport); break;
      case 'analytics': this.loadAnalytics(viewport); break;
      case 'logs': this.loadLogs(viewport); break;
      case 'settings': this.loadSettings(viewport); break;
      case 'modules': this.loadModules(viewport); break;
      default: this.loadHub(viewport);
    }
  },

  // ============================================================
  // SERVICE HUB / MUNDARIJA VIEW (EXACT IMAGE 1 CARD DESIGN)
  // ============================================================
  loadHub(viewport) {
    const services = this.SERVICES_REGISTRY;
    viewport.innerHTML = `
      <div class="hub-page-container">
        <!-- HEADER -->
        <header class="hub-header">
          <div class="hub-brand-block">
            <div style="display:flex;align-items:center;gap:12px;">
              <img src="${ATLAS_NAV_LOGO_PNG}" style="height:34px;max-width:180px;object-fit:contain;filter:drop-shadow(0 0 16px rgba(56,189,248,0.7));" alt="ATLAS">
              <span style="font-size:11px;font-weight:800;padding:2px 8px;border-radius:6px;background:rgba(56,189,248,0.15);color:#38bdf8;border:1px solid rgba(56,189,248,0.3);letter-spacing:0.5px;">MUNDARIJA</span>
            </div>
            <div class="hub-subtitle-text" style="margin-top:4px;">
              Barcha bot xizmatlari va avtomatlashtirish modullari katalogi
            </div>
          </div>

          <div class="hub-header-actions">
            <div style="display:flex;align-items:center;gap:8px;padding:6px 14px;border-radius:10px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);font-size:12px;color:rgba(255,255,255,0.85);">
              <span style="width:7px;height:7px;border-radius:50%;background:#38bdf8;box-shadow:0 0 8px #38bdf8;"></span>
              <span>Administrator: <b style="color:#ffffff;">${this.user?.full_name || 'Ozodbek'}</b></span>
            </div>
            <button class="btn-sm btn-secondary" id="hub-quick-logout" title="Tizimdan chiqish" style="background:rgba(239,68,68,0.12);color:#f87171;border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:6px 14px;display:flex;align-items:center;gap:6px;cursor:pointer;">
              ${this.icons.logout} <span>Chiqish</span>
            </button>
          </div>
        </header>

        <!-- SERVICES GRID -->
        <div class="hub-grid">
          ${services.map(s => `
            <div class="hub-card" data-route="${s.id}" style="--card-color:${s.color};--card-glow:${s.glow};">
              <div class="hub-card-glowing-emblem">
                ${s.icon}
              </div>

              <div class="hub-card-body">
                <div class="hub-card-title">${s.title}</div>
                <div class="hub-card-desc">${s.subtitle}</div>
              </div>
            </div>
          `).join('')}
        </div>

        <!-- FOOTER -->
        <footer class="hub-footer">
          <div>
            ATLAS Universal Engine &bull; Barcha xizmatlar xavfsiz Cloud OAuth2 bilan integratsiyalangan
          </div>
          <div style="font-family:'JetBrains Mono',monospace;">
            Qisqa tugma: <span style="color:#ffffff;">Ctrl + K</span> (Qidiruv) &bull; Versiya: <span style="color:#38bdf8;">v2.5.2</span>
          </div>
        </footer>
      </div>
    `;

    // Initialize custom cursor & hover effects
    this.initHubCursor();

    // Event listeners
    viewport.querySelectorAll('.hub-card').forEach(card => {
      card.addEventListener('click', () => {
        const route = card.dataset.route;
        if (route) {
          this.navigate(route);
        }
      });
    });

    document.getElementById('hub-quick-logout')?.addEventListener('click', () => {
      this.logout();
    });
  },

  // Interactive Circular Glow Follower Cursor for Mundarija Hub
  initHubCursor() {
    let cursor = document.getElementById('hub-custom-cursor');
    let dot = document.getElementById('hub-cursor-dot');
    if (!cursor) {
      cursor = document.createElement('div');
      cursor.id = 'hub-custom-cursor';
      dot = document.createElement('div');
      dot.id = 'hub-cursor-dot';
      document.body.appendChild(cursor);
      document.body.appendChild(dot);

      let mouseX = window.innerWidth / 2;
      let mouseY = window.innerHeight / 2;
      let cursorX = mouseX;
      let cursorY = mouseY;

      window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        if (dot && dot.style.display !== 'none') {
          dot.style.left = mouseX + 'px';
          dot.style.top = mouseY + 'px';
        }
      });

      const animateCursor = () => {
        cursorX += (mouseX - cursorX) * 0.18;
        cursorY += (mouseY - cursorY) * 0.18;
        if (cursor && cursor.style.display !== 'none') {
          cursor.style.left = cursorX + 'px';
          cursor.style.top = cursorY + 'px';
        }
        requestAnimationFrame(animateCursor);
      };
      animateCursor();
    }

    if (this.currentRoute === 'hub') {
      document.body.classList.add('hub-cursor-active');
      cursor.style.display = 'block';
      dot.style.display = 'block';
    } else {
      document.body.classList.remove('hub-cursor-active');
      cursor.style.display = 'none';
      dot.style.display = 'none';
    }

    // Attach dynamic interactive hover glows
    document.querySelectorAll('.hub-card, #hub-quick-logout').forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.classList.add('active-hover');
        const color = el.style.getPropertyValue('--card-color') || '#2ee59d';
        cursor.style.borderColor = color;
        cursor.style.boxShadow = `0 0 26px ${color}`;
        if (dot) dot.style.background = color;
      });
      el.addEventListener('mouseleave', () => {
        cursor.classList.remove('active-hover');
        cursor.style.borderColor = 'rgba(46, 229, 157, 0.85)';
        cursor.style.boxShadow = '0 0 14px rgba(46, 229, 157, 0.4)';
        if (dot) dot.style.background = '#2ee59d';
      });
    });
  },

  // ============================================================
  // AUTH / LOGIN VIEW
  // ============================================================
  renderLogin() {
    const root = document.getElementById('app-root');
    root.innerHTML = `
      <div class="auth-wrapper">
        <div class="auth-card">
          <div class="auth-logo" style="margin-bottom:20px;display:flex;justify-content:center;align-items:center;">
            <img src="${ATLAS_NAV_LOGO_PNG}" style="height:46px;max-width:210px;object-fit:contain;filter:drop-shadow(0 0 20px rgba(56,189,248,0.75));" alt="ATLAS">
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
        this.navigate('hub');
      } else {
        this.toast(res ? res.error : 'Login xatosi', 'error');
      }
    });
  },

  logout() {
    try {
      this.api('/api/auth/logout', 'POST');
    } catch (_) {}
    this.token = '';
    this.user = null;
    localStorage.removeItem('atlas_token');
    localStorage.removeItem('atlas_user');
    sessionStorage.clear();
    document.cookie = "atlas_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    this.renderLogin();
  },

  // ============================================================
  // APP SHELL
  // ============================================================
  renderApp() {
    if (!this.token || !this.user) {
      this.renderLogin();
      return;
    }

    const root = document.getElementById('app-root');
    root.innerHTML = `
      <div class="app-container">
        <!-- SIDEBAR -->
        <aside class="sidebar">
          <div class="sidebar-header" style="display:flex;align-items:center;justify-content:center;padding:16px 14px;position:relative;">
            <div id="btn-sidebar-logo-hub" style="display:flex;align-items:center;justify-content:center;gap:10px;cursor:pointer;" title="Bosh Mundarijaga qaytish">
              <img src="${ATLAS_NAV_LOGO_PNG}" style="height:26px;max-width:145px;object-fit:contain;filter:drop-shadow(0 0 10px rgba(56,189,248,0.7));" alt="ATLAS PRO">
              <div class="sidebar-brand-badge" style="flex-shrink:0;">PRO</div>
            </div>
            <button class="btn-icon mobile-sidebar-close-btn" id="mobile-sidebar-close-btn" title="Menyuni yopish" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,0.75);background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:8px;width:32px;height:32px;align-items:center;justify-content:center;cursor:pointer;">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <nav class="sidebar-menu">
            <div class="sidebar-group-title">Hujjatlar & Amaliyot</div>
            <div class="nav-item" data-route="contracts">
              ${this.icons.creditCard || this.icons.documents} <span>Kontraktlar & Baza</span>
            </div>
            <div class="nav-item" data-route="amaliyot">
              ${this.icons.activity} <span>Malakaviy Amaliyot</span>
            </div>
            <div class="nav-item" data-route="certificates">
              ${this.icons.fileText} <span>Ma'lumotnomalar</span>
            </div>
            <div class="nav-item" data-route="orders">
              ${this.icons.clipboard} <span>Rasmiy Buyruqlar</span>
            </div>
            <div class="nav-item" data-route="mtf_converter">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> <span>MTF & Test PDF</span>
            </div>

            <div class="sidebar-group-title">Marketing & Reklama</div>
            <div class="nav-item" data-route="meta_ads">
              ${this.icons.target || this.icons.zap} <span>Meta Ads Manager</span>
            </div>
            <div class="nav-item" data-route="instagram">
              ${this.icons.instagram} <span>Instagram Sinxronlash</span>
            </div>

            <div class="sidebar-group-title">O'quv Bo'limi & Bot</div>
            <div class="nav-item" data-route="dashboard">
              ${this.icons.dashboard} <span>Boshqaruv Paneli</span>
            </div>

            <div class="sidebar-group-title">Monitoring & Tizim</div>
            <div class="nav-item" data-route="pc_control">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg> <span>Kompyuter Boshqaruvi</span>
            </div>
            <div class="nav-item" data-route="ai_chat">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg> <span>AI Agent Chat</span>
            </div>
            <div class="nav-item" data-route="analytics">
              ${this.icons.analytics} <span>Statistika & Tahlil</span>
            </div>
            <div class="nav-item" data-route="logs">
              ${this.icons.logs} <span>Tizim Loglari</span>
            </div>
            <div class="nav-item" data-route="settings">
              ${this.icons.settings} <span>Sozlamalar</span>
            </div>
          </nav>

          <!-- SYSTEM STATUS & GITHUB BADGE -->
          <div class="system-status-corner">
            <div class="sys-badge-top">
              <div style="display:flex;align-items:center;gap:6px;">
                <span class="sys-live-dot" title="Tizim faol"></span>
                <span class="sys-ver-code">v2.5.2</span>
              </div>
              <a href="https://github.com/OzodbekNapasov/kontrakt-updater" target="_blank" rel="noopener noreferrer" class="github-repo-link" title="GitHub Repozitoriyasini ochish">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
              </a>
            </div>
          </div>

          <div class="sidebar-footer">
            <div style="width:36px;height:36px;border-radius:10px;background:rgba(56,189,248,0.15);border:1.5px solid rgba(56,189,248,0.4);display:flex;align-items:center;justify-content:center;color:#38bdf8;box-shadow:0 0 12px rgba(56,189,248,0.25);flex-shrink:0;">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
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
              <button class="header-btn mobile-menu-toggle" id="mobile-menu-btn" title="Menyu">
                ${this.icons.menu}
              </button>
              <h1 class="page-title" id="page-title">Ma'lumotnomalar & Hujjatlar Arxivi</h1>
              <div class="global-search-bar">
                <span class="search-icon-fixed">${this.icons.search}</span>
                <input type="text" id="global-search-input" placeholder="Tezkor qidirish...">
                <span class="search-shortcut">Ctrl+K</span>
              </div>
            </div>

            <div class="header-right">
              <button class="header-btn" id="refresh-view-btn" title="Yangilash">
                ${this.icons.refresh}
              </button>
            </div>
          </header>

          <div class="content-body" id="content-viewport"></div>
        </main>
      </div>

      <!-- SIDEBAR BACKDROP FOR MOBILE -->
      <div class="sidebar-backdrop" id="sidebar-backdrop"></div>

      <!-- MODALS & TOAST -->
      <div class="modal-overlay" id="modal-container"></div>
      <div id="toast-container" class="toast-container"></div>
    `;

    // Accordion Toggle
    const headerMain = document.getElementById('nav-header-main');
    if (headerMain) {
      headerMain.addEventListener('click', () => {
        document.getElementById('nav-group-main').classList.toggle('open');
      });
    }

    // Logo click to go back to Hub
    document.getElementById('btn-sidebar-logo-hub')?.addEventListener('click', () => this.navigate('hub'));

    // Mobile Menu Toggle & Backdrop
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const sidebarEl = document.querySelector('.sidebar');
    const backdropEl = document.getElementById('sidebar-backdrop');
    if (mobileBtn && sidebarEl && backdropEl) {
      mobileBtn.addEventListener('click', () => {
        sidebarEl.classList.toggle('mobile-open');
        backdropEl.classList.toggle('active');
      });
      backdropEl.addEventListener('click', () => {
        sidebarEl.classList.remove('mobile-open');
        backdropEl.classList.remove('active');
      });
    }

    document.getElementById('mobile-sidebar-close-btn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebarEl?.classList.remove('mobile-open');
      backdropEl?.classList.remove('active');
    });

    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => {
        if (window.innerWidth <= 992 && sidebarEl && backdropEl) {
          sidebarEl.classList.remove('mobile-open');
          backdropEl.classList.remove('active');
        }
        this.navigate(btn.dataset.route);
      });
    });

    document.querySelectorAll('.nav-sub-item').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (window.innerWidth <= 992 && sidebarEl && backdropEl) {
          sidebarEl.classList.remove('mobile-open');
          backdropEl.classList.remove('active');
        }
        this.navigate(btn.dataset.route);
      });
    });

    document.getElementById('logout-btn').addEventListener('click', () => this.logout());
    document.getElementById('refresh-view-btn').addEventListener('click', () => {
      this.systemDeployTime = new Date();
      this.startSystemStatusTimer();
      this.navigate(this.currentRoute);
      this.toast("Tizim va ma'lumotlar yangilandi", "info");
    });
    document.getElementById('global-search-input').addEventListener('click', () => this.openGlobalSearch());
  },

  // ============================================================
  // 1. BUYRUQLAR BO'LIMI (MINIMALISTIK & ZAMONAVIY)
  // ============================================================
  async loadOrders(container, selectedTplId = 'buyruq_akademik_tatil') {
    let currentTpl = selectedTplId;
    let activeTab = this.ordersActiveTab || 'create'; // 'create' | 'by_group' | 'archive'

    const render = () => {
      this.ordersActiveTab = activeTab;
      container.innerHTML = `
        <div class="tab-pills-row">
          <button class="tab-pill-btn ${activeTab === 'create' ? 'active' : ''}" id="tab-orders-create">
            ${this.icons.plus} <span>Yangi Buyruq Shakllantirish</span>
          </button>
          <button class="tab-pill-btn ${activeTab === 'by_group' ? 'active' : ''}" id="tab-orders-by-group">
            ${this.icons.groups} <span>Guruhlar Kesimi Bo'yicha</span>
          </button>
          <button class="tab-pill-btn ${activeTab === 'archive' ? 'active' : ''}" id="tab-orders-archive">
            ${this.icons.archive} <span>Barcha Buyruqlar Arxivi</span>
          </button>
        </div>

        <div id="orders-main-content"></div>
      `;

      document.getElementById('tab-orders-create').addEventListener('click', () => {
        activeTab = 'create';
        this.ordersActiveTab = 'create';
        render();
      });

      document.getElementById('tab-orders-by-group').addEventListener('click', () => {
        activeTab = 'by_group';
        this.ordersActiveTab = 'by_group';
        render();
      });

      document.getElementById('tab-orders-archive').addEventListener('click', () => {
        activeTab = 'archive';
        this.ordersActiveTab = 'archive';
        render();
      });

      const contentBox = document.getElementById('orders-main-content');
      if (activeTab === 'create') {
        contentBox.innerHTML = `
          <!-- 4 Ta Minimalistik Buyruq Tanlash Kartalari -->
          <div class="template-select-grid">
            <div class="template-select-card ${currentTpl === 'buyruq_akademik_tatil' ? 'active' : ''}" data-tpl="buyruq_akademik_tatil">
              <div class="template-card-icon">${this.icons.documents}</div>
              <div class="template-card-body">
                <div class="template-card-title">Akademik ta'til berish</div>
                <div class="template-card-desc">Salomatligi yoki boshqa sababli ta'til berish buyrug'i</div>
              </div>
            </div>

            <div class="template-select-card ${currentTpl === 'buyruq_qayta_tiklash' ? 'active' : ''}" data-tpl="buyruq_qayta_tiklash">
              <div class="template-card-icon">${this.icons.documents}</div>
              <div class="template-card-body">
                <div class="template-card-title">Qayta tiklash</div>
                <div class="template-card-desc">Akademik ta'tildan so'ng o'qishini davom ettirishga tiklash</div>
              </div>
            </div>

            <div class="template-select-card ${currentTpl === 'buyruq_guruhdan_guruhga' ? 'active' : ''}" data-tpl="buyruq_guruhdan_guruhga">
              <div class="template-card-icon">${this.icons.documents}</div>
              <div class="template-card-body">
                <div class="template-card-title">Guruh almashtirish</div>
                <div class="template-card-desc">Talabani bir o'quv guruhidan boshqasiga o'tkazish</div>
              </div>
            </div>

            <div class="template-select-card ${currentTpl === 'buyruq_safidan_chiqarish' ? 'active' : ''}" data-tpl="buyruq_safidan_chiqarish">
              <div class="template-card-icon">${this.icons.documents}</div>
              <div class="template-card-body">
                <div class="template-card-title">Safidan chiqarish</div>
                <div class="template-card-desc">Talaba arizasi yoki guruh rahbari bildirgisi asosida</div>
              </div>
            </div>
          </div>

          <!-- Form Box -->
          <div id="order-form-box"></div>
        `;

        // Card click listeners
        contentBox.querySelectorAll('.template-select-card').forEach(card => {
          card.addEventListener('click', () => {
            currentTpl = card.dataset.tpl;
            render();
          });
        });

        // Render document generator form for this specific template
        this.renderDocumentGenerator(document.getElementById('order-form-box'), currentTpl);
      } else if (activeTab === 'by_group') {
        this.renderOrdersByGroup(contentBox);
      } else {
        // Render all orders in archive
        this.renderDocumentArchive(contentBox, 'all_orders', false);
      }
    };

    render();
  },

  // ============================================================
  // GURUHLAR KESIMI BO'YICHA BUYRUQLAR RO'YXATI VA JAMI HISOBOTI
  // ============================================================
  async renderOrdersByGroup(container) {
    container.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(255,255,255,0.5);">Guruhlar kesimidagi buyruqlar tahlili yuklanmoqda...</div>`;

    const [docsRes, groupsRes] = await Promise.all([
      this.api('/api/documents/list?limit=1000'),
      this.api('/api/groups/academic')
    ]);

    const allDocs = docsRes?.documents || [];
    const studentGroups = groupsRes?.groups || [];

    // Filter only orders
    const orders = allDocs.filter(d => d.template_id && d.template_id.startsWith('buyruq_'));

    // Helper to get group name from order
    const getOrderGroup = (d) => {
      const p = d.parsed_data || {};
      return (p.guruhi || p.GURUHI || p.avvalgi_guruhi || p.guruh || '').trim();
    };

    // Helper to get course from order
    const getOrderCourse = (d) => {
      const p = d.parsed_data || {};
      const grpName = getOrderGroup(d);
      const matchedGrp = studentGroups.find(g => g.group_name === grpName);
      if (matchedGrp && matchedGrp.course_level) return parseInt(matchedGrp.course_level);
      const c = parseInt(p.kursi || p.KURSI);
      if (!isNaN(c) && c > 0) return c;
      if (grpName.startsWith('24-')) return 2;
      if (grpName.startsWith('25-')) return 1;
      return 1;
    };

    let selectedCourse = 'all'; // 'all', 1, 2, 3, 4
    let selectedGroup = 'all';
    let searchQuery = '';

    const renderView = () => {
      // Filter orders based on user selection
      let filteredOrders = orders.filter(d => {
        const grp = getOrderGroup(d);
        const crs = getOrderCourse(d);
        const fio = (d.recipient_fio || '').toLowerCase();
        const bNum = (d.parsed_data?.buyruq_raqami || '').toLowerCase();

        if (selectedCourse !== 'all' && crs !== parseInt(selectedCourse)) return false;
        if (selectedGroup !== 'all' && grp !== selectedGroup) return false;
        if (searchQuery) {
          const q = searchQuery.toLowerCase();
          if (!fio.includes(q) && !bNum.includes(q) && !grp.toLowerCase().includes(q)) return false;
        }
        return true;
      });

      // Statistics calculations
      const totalOrders = orders.length;
      const tatilOrders = orders.filter(o => o.template_id === 'buyruq_akademik_tatil').length;
      const chiqarishOrders = orders.filter(o => o.template_id === 'buyruq_safidan_chiqarish').length;
      const tiklashOrders = orders.filter(o => o.template_id === 'buyruq_qayta_tiklash').length;
      const otkazishOrders = orders.filter(o => o.template_id === 'buyruq_guruhdan_guruhga').length;
      
      const uniqueGroupsWithOrders = new Set(orders.map(o => getOrderGroup(o)).filter(Boolean)).size;

      // Group filtered orders by course and then by group
      const courseGroupsMap = {}; // { 1: { '25-19': [orders] }, 2: { '24-11': [orders] } }

      // Initialize all registered student groups in their courses
      studentGroups.forEach(sg => {
        const crs = sg.course_level || 1;
        if (!courseGroupsMap[crs]) courseGroupsMap[crs] = {};
        if (!courseGroupsMap[crs][sg.group_name]) {
          courseGroupsMap[crs][sg.group_name] = {
            group_info: sg,
            orders: []
          };
        }
      });

      // Place each filtered order into its bucket
      filteredOrders.forEach(ord => {
        const crs = getOrderCourse(ord);
        const grp = getOrderGroup(ord) || 'Noma\'lum guruh';
        if (!courseGroupsMap[crs]) courseGroupsMap[crs] = {};
        if (!courseGroupsMap[crs][grp]) {
          const matched = studentGroups.find(g => g.group_name === grp);
          courseGroupsMap[crs][grp] = {
            group_info: matched || { group_name: grp, rahbar_name: '', course_level: crs },
            orders: []
          };
        }
        courseGroupsMap[crs][grp].orders.push(ord);
      });

      container.innerHTML = `
        <!-- KPI SUMMARY CARDS (JAMI HISOBOTI) -->
        <div class="contract-kpi-grid" style="margin-bottom:24px;">
          <div class="contract-kpi-card" style="border-top:3px solid #38bdf8;">
            <span class="contract-kpi-label">Jami Buyruqlar</span>
            <span class="contract-kpi-val highlight-cyan">${totalOrders} ta</span>
          </div>
          <div class="contract-kpi-card" style="border-top:3px solid #fbbf24;">
            <span class="contract-kpi-label">Akademik Ta'til</span>
            <span class="contract-kpi-val highlight-warn">${tatilOrders} ta</span>
          </div>
          <div class="contract-kpi-card" style="border-top:3px solid #f87171;">
            <span class="contract-kpi-label">Safidan Chiqarish</span>
            <span class="contract-kpi-val" style="color:#f87171;">${chiqarishOrders} ta</span>
          </div>
          <div class="contract-kpi-card" style="border-top:3px solid #34d399;">
            <span class="contract-kpi-label">Tiklash & O'tkazish</span>
            <span class="contract-kpi-val highlight-green">${tiklashOrders + otkazishOrders} ta</span>
          </div>
        </div>

        <!-- FILTERS BAR -->
        <div class="glass-card" style="margin-bottom:24px;padding:16px 20px;">
          <div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;justify-content:space-between;">
            <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
              <span style="font-size:13px;font-weight:700;color:var(--color-text-main);">Kurs filtri:</span>
              <button class="tab-pill-btn ${selectedCourse === 'all' ? 'active' : ''}" data-course-filter="all" style="height:32px;padding:0 12px;font-size:12px;">
                Barchasi
              </button>
              <button class="tab-pill-btn ${selectedCourse == '1' ? 'active' : ''}" data-course-filter="1" style="height:32px;padding:0 12px;font-size:12px;">
                1-kurs
              </button>
              <button class="tab-pill-btn ${selectedCourse == '2' ? 'active' : ''}" data-course-filter="2" style="height:32px;padding:0 12px;font-size:12px;">
                2-kurs
              </button>
              <button class="tab-pill-btn ${selectedCourse == '3' ? 'active' : ''}" data-course-filter="3" style="height:32px;padding:0 12px;font-size:12px;">
                3-kurs
              </button>
            </div>

            <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
              <select id="by-group-select" class="select-control" style="width:200px;height:36px;font-size:12.5px;">
                <option value="all">-- Barcha guruhlar --</option>
                ${studentGroups.map(g => `<option value="${g.group_name}" ${selectedGroup === g.group_name ? 'selected' : ''}>${g.group_name} (${g.course_level || 1}-kurs)</option>`).join('')}
              </select>

              <input type="text" id="by-group-search" class="input-control" style="width:220px;height:36px;font-size:12.5px;" placeholder="F.I.O yoki buyruq №..." value="${searchQuery}">
            </div>
          </div>
        </div>

        <!-- ACCORDIONS / CARDS BY COURSE & GROUP -->
        <div id="orders-grouped-container">
          ${(() => {
            const sortedCourses = Object.keys(courseGroupsMap).map(Number).sort((a, b) => a - b);
            if (sortedCourses.length === 0) {
              return `<div class="glass-card" style="text-align:center;padding:36px;color:rgba(255,255,255,0.4);">Hech qanday guruh yoki buyruq ma'lumotlari topilmadi.</div>`;
            }

            return sortedCourses.map(courseNum => {
              if (selectedCourse !== 'all' && courseNum !== parseInt(selectedCourse)) return '';

              const groupsInCourse = courseGroupsMap[courseNum] || {};
              const groupKeys = Object.keys(groupsInCourse).sort();

              // Calculate total orders in this course
              const courseOrdersCount = Object.values(groupsInCourse).reduce((acc, g) => acc + g.orders.length, 0);

              // If a specific group is selected, only show that group
              const renderedGroupCards = groupKeys.map(grpKey => {
                if (selectedGroup !== 'all' && grpKey !== selectedGroup) return '';
                const gData = groupsInCourse[grpKey];
                const gOrders = gData.orders;
                const gInfo = gData.group_info || {};

                if (gOrders.length === 0 && (selectedGroup !== 'all' || searchQuery)) return '';

                return `
                  <div class="glass-card" style="margin-bottom:18px;border-left:4px solid ${courseNum == 1 ? '#00f0ff' : courseNum == 2 ? '#00ff88' : '#fbbf24'};">
                    <div class="card-header-flex" style="padding-bottom:12px;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.06);">
                      <div>
                        <div style="display:flex;align-items:center;gap:10px;">
                          <h3 style="font-size:16px;font-weight:700;color:#ffffff;margin:0;">Guruh: <span style="color:var(--accent-glow);">${grpKey}</span></h3>
                          <span class="badge ${courseNum == 1 ? 'badge-cyan' : 'badge-success'}">${courseNum}-kurs</span>
                        </div>
                        <div style="font-size:12.5px;color:rgba(255,255,255,0.6);margin-top:4px;">
                          ${gInfo.rahbar_name ? `Guruh rahbari: <b style="color:#38bdf8;">${gInfo.rahbar_name}</b>` : 'Guruh rahbari kiritilmagan'}
                        </div>
                      </div>
                      <div>
                        <span class="badge ${gOrders.length > 0 ? 'badge-warning' : 'badge-secondary'}" style="font-size:12px;">
                          ${gOrders.length} ta buyruq
                        </span>
                      </div>
                    </div>

                    ${gOrders.length === 0 ? `
                      <div style="padding:14px;font-size:12.5px;color:rgba(255,255,255,0.35);font-style:italic;">
                        Ushbu guruh bo'yicha hali rasmiy buyruq shakllantirilmagan.
                      </div>
                    ` : `
                      <div class="table-responsive">
                        <table class="glass-table">
                          <thead>
                            <tr>
                              <th style="width:40px;">№</th>
                              <th>Talaba F.I.O</th>
                              <th>Buyruq Turi</th>
                              <th>Buyruq № va Sanasi</th>
                              <th>Asos / Tafsilot</th>
                              <th style="text-align:right;">Amallar</th>
                            </tr>
                          </thead>
                          <tbody>
                            ${gOrders.map((ord, oIdx) => {
                              const p = ord.parsed_data || {};
                              let typeBadge = 'badge-info';
                              if (ord.template_id === 'buyruq_akademik_tatil') typeBadge = 'badge-warning';
                              else if (ord.template_id === 'buyruq_safidan_chiqarish') typeBadge = 'badge-danger';
                              else if (ord.template_id === 'buyruq_qayta_tiklash') typeBadge = 'badge-success';
                              else if (ord.template_id === 'buyruq_guruhdan_guruhga') typeBadge = 'badge-cyan';

                              return `
                                <tr>
                                  <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.5);">${oIdx + 1}</td>
                                  <td><b style="color:#ffffff;font-size:13.5px;">${ord.recipient_fio}</b></td>
                                  <td><span class="badge ${typeBadge}">${ord.template_name}</span></td>
                                  <td class="mono" style="font-size:12.5px;color:rgba(94,234,212,0.9);">
                                    ${p.buyruq_raqami ? `№ ${p.buyruq_raqami}` : '-'} <br>
                                    <span style="font-size:11px;color:rgba(255,255,255,0.5);">${p.sanasi || p.SANA || ord.created_at}</span>
                                  </td>
                                  <td style="font-size:12px;color:rgba(255,255,255,0.7);">
                                    ${p.asos_turi ? `Asos: <b>${p.asos_turi}</b><br>` : ''}
                                    ${p.yangi_guruhi ? `Yangi guruh: <b style="color:var(--accent-glow);">${p.yangi_guruhi}</b>` : ''}
                                    ${p.yonalishi ? `Yo'nalish: ${p.yonalishi}` : ''}
                                  </td>
                                  <td style="text-align:right;">
                                    <div style="display:flex;gap:5px;justify-content:flex-end;">
                                      <button class="btn-icon" onclick="ATLAS.openImageModal('/api/documents/view/${ord.id}', '${ord.recipient_fio}', ${ord.id})" title="Katta ko'rish">${this.icons.eye}</button>
                                      <a href="/api/documents/download_docx/${ord.id}" class="btn-icon" title="Word (.docx) yuklab olish" style="color:#60a5fa;">${this.icons.download}</a>
                                      <button class="btn-icon" onclick="ATLAS.openEditDocModal(${ord.id})" title="Tahrirlash" style="color:var(--accent-glow);">${this.icons.edit}</button>
                                      <button class="btn-icon" onclick="ATLAS.deleteDocumentFromArchive(${ord.id})" title="O'chirish">${this.icons.trash}</button>
                                    </div>
                                  </td>
                                </tr>
                              `;
                            }).join('')}
                          </tbody>
                        </table>
                      </div>
                    `}
                  </div>
                `;
              }).join('');

              if (!renderedGroupCards.trim()) return '';

              return `
                <div style="margin-bottom:32px;">
                  <!-- COURSE BANNER -->
                  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;padding:12px 18px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:var(--radius-md);">
                    <span style="color:var(--accent-glow);display:inline-flex;align-items:center;">${this.icons.bookOpen}</span>
                    <h2 style="font-size:17px;font-weight:800;color:#ffffff;margin:0;">
                      ${courseNum}-BOSQICH (${courseNum}-KURS) GURUHLARI
                    </h2>
                    <span class="badge ${courseNum == 1 ? 'badge-cyan' : 'badge-success'}" style="margin-left:auto;">
                      Jami ${courseOrdersCount} ta buyruq
                    </span>
                  </div>

                  ${renderedGroupCards}
                </div>
              `;
            }).join('');
          })()}
        </div>
      `;

      // Event listeners for Course pills
      container.querySelectorAll('[data-course-filter]').forEach(b => {
        b.addEventListener('click', () => {
          selectedCourse = b.dataset.courseFilter;
          renderView();
        });
      });

      // Event listener for Group dropdown
      const grpSelect = document.getElementById('by-group-select');
      if (grpSelect) {
        grpSelect.addEventListener('change', (e) => {
          selectedGroup = e.target.value;
          renderView();
        });
      }

      // Event listener for search
      const searchInp = document.getElementById('by-group-search');
      if (searchInp) {
        searchInp.addEventListener('input', (e) => {
          searchQuery = e.target.value;
          renderView();
        });
      }
    };

    renderView();
  },

  // ============================================================
  // 1.5 AMALIYOT BO'LIMI (PAPAKALAR IERARXIYASI & SO'ROVNOMA BOSHQARUVI)
  // ============================================================
  async loadAmaliyot(container) {
    let currentFolderId = null;
    let folderPath = [];
    let childFolders = [];
    let currentFolderInfo = null;
    let semesterSubView = 'survey'; // 'survey' | 'create_order' | 'generate_all' | 'archive'

    let surveyStudents = [];
    let semesterOrders = [];
    let districtDoctors = {
      "Shahrisabz shahar": "O.Norboyev",
      "Kitob tuman": "A.Hasanov",
      "Yakkabog' tuman": "S.B.Jo’rayev",
      "Shahrisabz tuman": "Z.Esanov",
      "Chiroqchi tuman": "Sh.Ro'ziqulov",
      "Qamashi tuman": "Avazov Shuxrat Shukullayevich"
    };
    let standardDistricts = Object.keys(districtDoctors);

    // Fetch standard districts from server
    try {
      const distRes = await this.api('/api/amaliyot/districts');
      if (distRes?.district_doctors) {
        districtDoctors = distRes.district_doctors;
        standardDistricts = distRes.districts || Object.keys(districtDoctors);
      }
    } catch (e) {}

    const folderIcons = {
      root: this.icons.folder,
      year: this.icons.calendar,
      direction: this.icons.activity,
      groups: this.icons.groups,
      semester: this.icons.bookOpen
    };

    const getFolderTypeTitle = (type) => {
      switch (type) {
        case 'year': return "O'quv Yili";
        case 'direction': return "Yo'nalish";
        case 'groups': return "Guruhlar To'plami";
        case 'semester': return "Semestr";
        default: return "Papka";
      }
    };

    const getNextChildType = (parentType) => {
      if (!parentType) return 'year';
      if (parentType === 'year') return 'direction';
      if (parentType === 'direction') return 'groups';
      if (parentType === 'groups') return 'semester';
      return 'groups';
    };

    // Load folder state & data
    const loadFolderData = async (folderId) => {
      currentFolderId = folderId;
      container.innerHTML = `<div style="text-align:center;padding:40px;color:var(--accent-glow);">Yuklanmoqda...</div>`;

      try {
        // 1. Fetch Breadcrumb Path
        if (folderId) {
          const pathRes = await this.api(`/api/amaliyot/folders/path?folder_id=${folderId}`);
          folderPath = pathRes?.path || [];
          currentFolderInfo = folderPath[folderPath.length - 1] || null;
        } else {
          folderPath = [];
          currentFolderInfo = null;
        }

        // 2. If current folder is SEMESTER, load its Survey & Orders
        if (currentFolderInfo && currentFolderInfo.folder_type === 'semester') {
          const [surveyRes, ordersRes] = await Promise.all([
            this.api(`/api/amaliyot/folders/${folderId}/survey`),
            this.api(`/api/amaliyot/folders/${folderId}/orders`)
          ]);
          surveyStudents = surveyRes?.surveys || [];
          semesterOrders = ordersRes?.orders || [];
          renderSemesterDashboard();
          return;
        }

        // 3. Otherwise, load child folders list
        const pQuery = folderId ? `?parent_id=${folderId}` : '';
        const foldersRes = await this.api(`/api/amaliyot/folders${pQuery}`);
        childFolders = foldersRes?.folders || [];
        renderFolderExplorer();
      } catch (err) {
        container.innerHTML = `
          <div class="glass-card" style="padding:24px;text-align:center;">
            <div style="color:var(--status-error);font-size:16px;font-weight:700;margin-bottom:8px;">Xatolik yuz berdi</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:16px;">${err.message}</div>
            <button class="btn-primary" id="btn-retry-folder">Qayta yuklash</button>
          </div>
        `;
        document.getElementById('btn-retry-folder')?.addEventListener('click', () => loadFolderData(folderId));
      }
    };

    // ============================================================
    // VIEW 1: FOLDER EXPLORER (IERARXIK PAPKALAR KO'RINISHI)
    // ============================================================
    const renderFolderExplorer = () => {
      const parentType = currentFolderInfo ? currentFolderInfo.folder_type : null;
      const nextType = getNextChildType(parentType);
      const nextTypeTitle = getFolderTypeTitle(nextType);

      let headerIcon = this.icons.calendar;
      let headerTitle = "O'quv Yillari Bo'limi";
      let headerDesc = "Kerakli o'quv yili papkasini tanlang yoki yangisini oching:";
      if (parentType === 'year') {
        headerIcon = this.icons.activity;
        headerTitle = `${currentFolderInfo.name} — Yo'nalishlar`;
        headerDesc = "Ushbu o'quv yili bo'yicha yo'nalishlar papkalari:";
      } else if (parentType === 'direction') {
        headerIcon = this.icons.groups;
        headerTitle = `${currentFolderInfo.name} — Guruhlar To'plami`;
        headerDesc = "Buyruqlar to'plamini shakllantirish uchun guruhlar papkasini tanlang:";
      } else if (parentType === 'groups') {
        headerIcon = this.icons.bookOpen;
        headerTitle = `${currentFolderInfo.name} — Semestrlar`;
        headerDesc = "Amaliyot o'tash semestrini tanlang:";
      }

      container.innerHTML = `
        <div class="amaliyot-explorer-wrapper">
          <!-- BREADCRUMB BAR -->
          <div class="amaliyot-breadcrumb-bar">
            <div class="amaliyot-breadcrumbs">
              <div class="breadcrumb-node ${!currentFolderId ? 'active' : ''}" data-folder-id="0">
                <span style="display:inline-flex;align-items:center;gap:6px;">${this.icons.home} Asosiy</span>
              </div>
              ${folderPath.map((node, idx) => `
                <span class="breadcrumb-sep">/</span>
                <div class="breadcrumb-node ${idx === folderPath.length - 1 ? 'active' : ''}" data-folder-id="${node.id}">
                  <span style="display:inline-flex;align-items:center;gap:6px;">${folderIcons[node.folder_type] || this.icons.folder} ${node.name}</span>
                </div>
              `).join('')}
            </div>

            <div class="breadcrumb-bar-actions">
              ${folderPath.length > 0 ? `
                <button class="btn-sm btn-secondary" id="btn-folder-back" title="Oldingi papkaga qaytish" style="display:inline-flex;align-items:center;gap:6px;">
                  ${this.icons.arrowLeft} <span>Orqaga</span>
                </button>
              ` : ''}
              <button class="btn-sm btn-primary" id="btn-add-folder" style="display:inline-flex;align-items:center;gap:6px;">
                ${this.icons.plus} <span>Yangi ${nextTypeTitle} Ochish</span>
              </button>
            </div>
          </div>

          <!-- BANNER -->
          <div class="glass-card" style="padding:16px 20px;">
            <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:3px;display:flex;align-items:center;gap:8px;">
              <span style="color:var(--accent-glow);">${headerIcon}</span>
              <span>${headerTitle}</span>
            </div>
            <div style="font-size:12.5px;color:rgba(94,234,212,0.8);">
              ${headerDesc}
            </div>
          </div>

          <!-- FOLDERS GRID -->
          <div class="folders-grid">
            ${childFolders.map(folder => {
              const icon = folderIcons[folder.folder_type] || this.icons.folder;
              let badgeText = '';
              if (folder.folder_type === 'semester') {
                badgeText = `${folder.survey_count || 0} ta talaba | ${folder.orders_count || 0} ta buyruq`;
              } else {
                badgeText = `${folder.children_count || 0} ta ichki papka`;
              }

              let subText = '';
              if (folder.extra_data?.duration) subText = `Ta'lim: ${folder.extra_data.duration}`;
              else if (folder.extra_data?.groups) subText = `Guruhlar: ${folder.extra_data.groups.join(', ')}`;
              else if (folder.extra_data?.start_date) subText = `Muddat: ${folder.extra_data.start_date} - ${folder.extra_data.end_date}`;

              return `
                <div class="folder-card" data-folder-id="${folder.id}">
                  <div class="folder-card-top">
                    <div class="folder-card-icon" style="color:var(--accent-glow);">${icon}</div>
                    <div class="folder-card-actions">
                      <button class="tab-btn-mini btn-edit-folder" data-folder-id="${folder.id}" title="Tahrirlash">${this.icons.edit}</button>
                      <button class="tab-btn-mini danger btn-delete-folder" data-folder-id="${folder.id}" title="O'chirish">${this.icons.trash}</button>
                    </div>
                  </div>
                  <div>
                    <div class="folder-card-title">${folder.name}</div>
                    ${subText ? `<div class="folder-card-desc">${subText}</div>` : ''}
                  </div>
                  <div class="folder-card-footer">
                    <span class="folder-stat-badge">${badgeText}</span>
                    <span style="color:var(--accent-glow);display:inline-flex;align-items:center;">${this.icons.arrowRight}</span>
                  </div>
                </div>
              `;
            }).join('')}

            <!-- Add new folder dashed card -->
            <div class="folder-card folder-card-add-new" id="card-add-new-folder">
              <div style="color:var(--accent-glow);">${this.icons.plus}</div>
              <div style="font-weight:700;color:#ffffff;font-size:13.5px;">+ Yangi ${nextTypeTitle}</div>
              <div style="font-size:11.5px;color:rgba(94,234,212,0.7);">Papka yaratish uchun bosing</div>
            </div>
          </div>
        </div>
      `;

      // Breadcrumb clicks
      container.querySelectorAll('.breadcrumb-node').forEach(el => {
        el.addEventListener('click', () => {
          const fId = parseInt(el.dataset.folderId);
          loadFolderData(fId || null);
        });
      });

      // Back button
      document.getElementById('btn-folder-back')?.addEventListener('click', () => {
        if (folderPath.length > 1) {
          const parentNode = folderPath[folderPath.length - 2];
          loadFolderData(parentNode.id);
        } else {
          loadFolderData(null);
        }
      });

      // Open folder on card click (excluding action buttons)
      container.querySelectorAll('.folder-card:not(.folder-card-add-new)').forEach(card => {
        card.addEventListener('click', (e) => {
          if (e.target.closest('.btn-edit-folder') || e.target.closest('.btn-delete-folder')) return;
          const fId = parseInt(card.dataset.folderId);
          loadFolderData(fId);
        });
      });

      // Add Folder Modals
      const handleOpenAddModal = () => {
        openAddFolderModal(currentFolderId, nextType);
      };
      document.getElementById('btn-add-folder')?.addEventListener('click', handleOpenAddModal);
      document.getElementById('card-add-new-folder')?.addEventListener('click', handleOpenAddModal);

      // Edit Folder
      container.querySelectorAll('.btn-edit-folder').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const fId = parseInt(btn.dataset.folderId);
          const fObj = childFolders.find(f => f.id === fId);
          if (fObj) openEditFolderModal(fObj);
        });
      });

      // Delete Folder
      container.querySelectorAll('.btn-delete-folder').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.stopPropagation();
          const fId = parseInt(btn.dataset.folderId);
          const fObj = childFolders.find(f => f.id === fId);
          if (confirm(`Haqiqatan ham '${fObj?.name}' papkasi va uning barcha ichki ma'lumotlarini o'chirmoqchimisiz?`)) {
            const res = await this.api(`/api/amaliyot/folders/${fId}`, 'DELETE');
            if (res?.success) {
              this.toast("Papka o'chirildi", "success");
              loadFolderData(currentFolderId);
            } else {
              alert(res?.error || "O'chirishda xatolik yuz berdi");
            }
          }
        });
      });
    };

    // ============================================================
    // MODAL: YANGI PAPKA YARATISH (CONTEXT-AWARE)
    // ============================================================
    let cachedAmaliyotTemplates = [];
    const fetchTemplatesList = async () => {
      if (cachedAmaliyotTemplates.length === 0) {
        const res = await this.api('/api/amaliyot/templates', 'GET');
        if (res?.success && res.templates) cachedAmaliyotTemplates = res.templates;
      }
      return cachedAmaliyotTemplates;
    };

    const openAddFolderModal = async (parentId, folderType) => {
      const templates = await fetchTemplatesList();
      let defaultNamePlaceholder = "2025/2026";
      let titleLabel = "O'quv Yili Nomi";
      if (folderType === 'direction') {
        defaultNamePlaceholder = "Hamshiralik ishi (3 yillik)";
        titleLabel = "Yo'nalish Nomi";
      } else if (folderType === 'groups') {
        defaultNamePlaceholder = "201-204 guruhlar";
        titleLabel = "Guruhlar To'plami Nomi";
      } else if (folderType === 'semester') {
        defaultNamePlaceholder = "2-semestr";
        titleLabel = "Semestr Nomi";
      }

      this.openModal(`Yangi ${getFolderTypeTitle(folderType)} Ochish`, `
        <div class="form-group">
          <label class="form-label">${titleLabel}</label>
          <input type="text" id="modal-folder-name" class="input-control" placeholder="Masalan: ${defaultNamePlaceholder}">
        </div>

        ${folderType === 'direction' ? `
          <div class="form-group">
            <label class="form-label">Ta'lim Muddati</label>
            <select id="modal-folder-duration" class="select-control">
              <option value="3 yillik" selected>3 yillik</option>
              <option value="2 yillik">2 yillik</option>
            </select>
          </div>
        ` : ''}

        ${folderType === 'semester' ? `
          <div class="form-group">
            <label class="form-label">Amaliyot Word Shabloni (.docx)</label>
            <select id="modal-folder-template" class="select-control">
              <option value="">⚡ Avtomatik moslash (Yo'nalish va semestrga qarab)</option>
              ${templates.map(t => `<option value="${t.rel_path}">${t.display_name} (${t.filename})</option>`).join('')}
            </select>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div class="form-group">
              <label class="form-label">Bosqich / Kursi</label>
              <select id="modal-folder-kursi" class="select-control">
                <option value="1" selected>1-kurs</option>
                <option value="2">2-kurs</option>
                <option value="3">3-kurs</option>
                <option value="4">4-kurs</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Boshlanish Sanasi</label>
              <input type="text" id="modal-folder-start" class="input-control" value="08.06.2026">
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Tugash Sanasi</label>
            <input type="text" id="modal-folder-end" class="input-control" value="06.07.2026">
          </div>
        ` : ''}
        <div class="modal-footer">
          <button class="btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button class="btn-primary" id="btn-save-modal-folder">Papkani Ochish</button>
        </div>
      `);

      document.getElementById('btn-save-modal-folder').addEventListener('click', async () => {
        const nameVal = document.getElementById('modal-folder-name').value.trim();
        if (!nameVal) {
          alert("Papka nomini kiriting!");
          return;
        }

        const extra = {};
        if (folderType === 'direction') {
          extra.duration = document.getElementById('modal-folder-duration').value;
        } else if (folderType === 'semester') {
          extra.kursi = document.getElementById('modal-folder-kursi').value;
          extra.start_date = document.getElementById('modal-folder-start').value.trim();
          extra.end_date = document.getElementById('modal-folder-end').value.trim();
          const tplVal = document.getElementById('modal-folder-template').value;
          if (tplVal) extra.template_file = tplVal;
        }

        const res = await this.api('/api/amaliyot/folders', 'POST', {
          parent_id: parentId,
          folder_type: folderType,
          name: nameVal,
          extra_data: extra
        });

        if (res?.success) {
          this.closeModal();
          this.toast("Yangi papka muvaffaqiyatli ochildi!", "success");
          loadFolderData(currentFolderId);
        } else {
          alert(res?.error || "Xatolik yuz berdi");
        }
      });
    };

    // Modal: Edit Folder
    const openEditFolderModal = async (fObj) => {
      const templates = await fetchTemplatesList();
      const extra = fObj.extra_data || {};

      this.openModal('Papka Nomini Tahrirlash', `
        <div class="form-group">
          <label class="form-label">Papka Nomi</label>
          <input type="text" id="modal-edit-folder-name" class="input-control" value="${fObj.name}">
        </div>

        ${fObj.folder_type === 'direction' ? `
          <div class="form-group">
            <label class="form-label">Ta'lim Muddati</label>
            <select id="modal-edit-folder-duration" class="select-control">
              <option value="3 yillik" ${extra.duration === '3 yillik' ? 'selected' : ''}>3 yillik</option>
              <option value="2 yillik" ${extra.duration === '2 yillik' ? 'selected' : ''}>2 yillik</option>
            </select>
          </div>
        ` : ''}

        ${fObj.folder_type === 'semester' ? `
          <div class="form-group">
            <label class="form-label">Amaliyot Word Shabloni (.docx)</label>
            <select id="modal-edit-folder-template" class="select-control">
              <option value="">⚡ Avtomatik moslash (Yo'nalish va semestrga qarab)</option>
              ${templates.map(t => `<option value="${t.rel_path}" ${extra.template_file === t.rel_path ? 'selected' : ''}>${t.display_name} (${t.filename})</option>`).join('')}
            </select>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div class="form-group">
              <label class="form-label">Bosqich / Kursi</label>
              <select id="modal-edit-folder-kursi" class="select-control">
                <option value="1" ${extra.kursi === '1' ? 'selected' : ''}>1-kurs</option>
                <option value="2" ${extra.kursi === '2' ? 'selected' : ''}>2-kurs</option>
                <option value="3" ${extra.kursi === '3' ? 'selected' : ''}>3-kurs</option>
                <option value="4" ${extra.kursi === '4' ? 'selected' : ''}>4-kurs</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Boshlanish Sanasi</label>
              <input type="text" id="modal-edit-folder-start" class="input-control" value="${extra.start_date || '08.06.2026'}">
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Tugash Sanasi</label>
            <input type="text" id="modal-edit-folder-end" class="input-control" value="${extra.end_date || '06.07.2026'}">
          </div>
        ` : ''}

        <div class="modal-footer">
          <button class="btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button class="btn-primary" id="btn-save-edit-folder">Saqlash</button>
        </div>
      `);

      document.getElementById('btn-save-edit-folder').addEventListener('click', async () => {
        const nameVal = document.getElementById('modal-edit-folder-name').value.trim();
        if (!nameVal) return;

        const updatedExtra = { ...extra };
        if (fObj.folder_type === 'direction') {
          updatedExtra.duration = document.getElementById('modal-edit-folder-duration').value;
        } else if (fObj.folder_type === 'semester') {
          updatedExtra.kursi = document.getElementById('modal-edit-folder-kursi').value;
          updatedExtra.start_date = document.getElementById('modal-edit-folder-start').value.trim();
          updatedExtra.end_date = document.getElementById('modal-edit-folder-end').value.trim();
          const tplVal = document.getElementById('modal-edit-folder-template').value;
          if (tplVal) updatedExtra.template_file = tplVal;
          else delete updatedExtra.template_file;
        }

        const res = await this.api(`/api/amaliyot/folders/${fObj.id}`, 'PUT', { name: nameVal, extra_data: updatedExtra });
        if (res?.success) {
          this.closeModal();
          this.toast("Papka ma'lumotlari muvaffaqiyatli yangilandi!", "success");
          loadFolderData(currentFolderId);
        } else {
          alert(res?.error || "Xatolik yuz berdi");
        }
      });
    };

    // ============================================================
    // VIEW 2: SEMESTER DASHBOARD (SO'ROVNOMA + BUYRUQ GENERATORI)
    // ============================================================
    const renderSemesterDashboard = () => {
      const fullPathTitle = folderPath.map(p => p.name).join(' > ');
      const extra = currentFolderInfo?.extra_data || {};
      const sDate = extra.start_date || "08.06.2026";
      const eDate = extra.end_date || "06.07.2026";

      // Calculate District Statistics from surveyStudents
      const districtStats = {};
      surveyStudents.forEach(st => {
        const dName = st.tumani || "Shahrisabz shahar";
        districtStats[dName] = (districtStats[dName] || 0) + 1;
      });

      container.innerHTML = `
        <div class="amaliyot-explorer-wrapper">
          <!-- BREADCRUMB BAR -->
          <div class="amaliyot-breadcrumb-bar">
            <div class="amaliyot-breadcrumbs">
              <div class="breadcrumb-node" data-folder-id="0">
                <span style="display:inline-flex;align-items:center;gap:6px;">${this.icons.home} Asosiy</span>
              </div>
              ${folderPath.map((node, idx) => `
                <span class="breadcrumb-sep">/</span>
                <div class="breadcrumb-node ${idx === folderPath.length - 1 ? 'active' : ''}" data-folder-id="${node.id}">
                  <span style="display:inline-flex;align-items:center;gap:6px;">${folderIcons[node.folder_type] || this.icons.folder} ${node.name}</span>
                </div>
              `).join('')}
            </div>

            <div class="breadcrumb-bar-actions">
              <button class="btn-sm btn-secondary" id="btn-semester-back" style="display:inline-flex;align-items:center;gap:6px;">
                ${this.icons.arrowLeft} <span>Guruhlarga qaytish</span>
              </button>
            </div>
          </div>

          <!-- TOP BANNER -->
          <div class="semester-dashboard-header">
            <div>
              <div style="font-size:18px;font-weight:800;color:#ffffff;margin-bottom:4px;display:flex;align-items:center;gap:8px;">
                <span style="color:var(--accent-glow);">${this.icons.bookOpen}</span>
                <span>${currentFolderInfo.name} — Malakaviy Amaliyot Boshqaruvi</span>
              </div>
              <div style="font-size:12.5px;color:rgba(94,234,212,0.9);line-height:1.4;">
                Yo'nalish: <b>${folderPath[1]?.name || 'Hamshiralik'}</b> &nbsp;|&nbsp; 
                To'plam: <b>${folderPath[2]?.name || 'Guruhlar'}</b> &nbsp;|&nbsp; 
                Jami so'rovnomada: <b style="color:#34d399;">${surveyStudents.length} ta talaba</b>
              </div>
            </div>
          </div>

          <!-- SUB VIEW PILLS -->
          <div class="tab-pills-row">
            <button class="tab-pill-btn ${semesterSubView === 'survey' ? 'active' : ''}" id="tab-sub-survey" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.users} <span>O'tkazilgan So'rovnoma (${surveyStudents.length})</span>
            </button>
            <button class="tab-pill-btn ${semesterSubView === 'create_order' ? 'active' : ''}" id="tab-sub-create-order" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.plus} <span>Tuman Buyrug'ini Yaratish</span>
            </button>
            <button class="tab-pill-btn ${semesterSubView === 'generate_all' ? 'active' : ''}" id="tab-sub-generate-all" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.zap} <span>Barcha Tumanlarni Generatsiya Qilish (ZIP)</span>
            </button>
            <button class="tab-pill-btn ${semesterSubView === 'archive' ? 'active' : ''}" id="tab-sub-archive" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.archive} <span>Buyruqlar Arxivi (${semesterOrders.length})</span>
            </button>
          </div>

          <!-- SUB VIEW CONTAINER -->
          <div id="semester-sub-content"></div>
        </div>
      `;

      // Breadcrumb clicks
      container.querySelectorAll('.breadcrumb-node').forEach(el => {
        el.addEventListener('click', () => {
          const fId = parseInt(el.dataset.folderId);
          loadFolderData(fId || null);
        });
      });

      // Back to groups
      document.getElementById('btn-semester-back')?.addEventListener('click', () => {
        if (folderPath.length > 1) {
          loadFolderData(folderPath[folderPath.length - 2].id);
        } else {
          loadFolderData(null);
        }
      });

      // Tab clicks
      document.getElementById('tab-sub-survey').addEventListener('click', () => {
        semesterSubView = 'survey';
        renderSemesterDashboard();
      });
      document.getElementById('tab-sub-create-order').addEventListener('click', () => {
        semesterSubView = 'create_order';
        renderSemesterDashboard();
      });
      document.getElementById('tab-sub-generate-all').addEventListener('click', () => {
        semesterSubView = 'generate_all';
        renderSemesterDashboard();
      });
      document.getElementById('tab-sub-archive').addEventListener('click', () => {
        semesterSubView = 'archive';
        renderSemesterDashboard();
      });

      const subViewport = document.getElementById('semester-sub-content');

      // Render Active Sub-View
      if (semesterSubView === 'survey') {
        renderSurveyTab(subViewport, districtStats);
      } else if (semesterSubView === 'create_order') {
        renderCreateOrderTab(subViewport, districtStats);
      } else if (semesterSubView === 'generate_all') {
        renderGenerateAllTab(subViewport, districtStats);
      } else if (semesterSubView === 'archive') {
        renderArchiveTab(subViewport);
      }
    };

    // ============================================================
    // SUB-VIEW 1: TALABALAR SO'ROVNOMASI (SURVEY TAB)
    // ============================================================
    const renderSurveyTab = (viewport, districtStats) => {
      viewport.innerHTML = `
        <div class="glass-card" style="padding:22px;">
          <!-- Helpful Format Note -->
          <div style="background:rgba(13,92,86,0.25);border:1px dashed rgba(0,203,169,0.4);border-radius:8px;padding:10px 14px;margin-bottom:14px;display:flex;align-items:center;gap:10px;font-size:12px;color:rgba(255,255,255,0.9);">
            <span style="color:#34d399;display:inline-flex;align-items:center;">${this.icons.info}</span>
            <span><b>Eslatma:</b> Excel faylingizda faqat <b>Guruhi</b> va <b>Talabaning F.I.SH</b> bo'lishi kifoya. Amaliyot muddati va sanalari buyruq shakllantirish bosqichida bir martada kiritiladi.</span>
          </div>

          <!-- Toolbar / Actions Bar -->
          <div class="survey-import-bar">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <input type="file" id="survey-excel-file-input" accept=".xlsx, .xls" style="display:none;">
              <button type="button" class="btn-primary btn-sm" id="btn-trigger-excel-upload" style="display:inline-flex;align-items:center;gap:6px;">
                ${this.icons.upload} <span>Excel Fayl Yuklash (Import)</span>
              </button>
              <button type="button" class="btn-secondary btn-sm" id="btn-paste-bulk-survey" style="display:inline-flex;align-items:center;gap:6px;">
                ${this.icons.clipboard} <span>Matndan Nusxalash</span>
              </button>
            </div>
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <button type="button" class="btn-secondary btn-sm" id="btn-add-survey-row" style="display:inline-flex;align-items:center;gap:6px;">
                ${this.icons.plus} <span>Qator Qo'shish</span>
              </button>
              <button type="button" class="btn-primary btn-sm" id="btn-save-all-survey" style="display:inline-flex;align-items:center;gap:6px;">
                ${this.icons.save} <span>So'rovnomani Saqlash</span>
              </button>
            </div>
          </div>

          <!-- District Stats Chips -->
          <div style="font-size:12.5px;font-weight:700;color:rgba(255,255,255,0.9);margin-bottom:6px;display:flex;align-items:center;gap:6px;">
            <span style="color:var(--accent-glow);">${this.icons.mapPin}</span>
            <span>Tumanlar bo'yicha taqsimot statistikasi:</span>
          </div>
          <div class="district-stats-row" id="district-stats-chips-container">
            ${Object.keys(districtStats).length > 0 ? Object.entries(districtStats).map(([dName, cnt]) => `
              <div class="district-stat-chip">
                <span>${dName}:</span>
                <span class="district-stat-count">${cnt} ta</span>
              </div>
            `).join('') : `
              <div style="font-size:12px;color:rgba(94,234,212,0.6);font-style:italic;">
                Talabalar so'rovnomasi hali kiritilmagan. Excel fayl yuklang yoki qatorlar qo'shing.
              </div>
            `}
          </div>

          <!-- Group Stats Chips -->
          <div style="font-size:12.5px;font-weight:700;color:rgba(255,255,255,0.9);margin-top:10px;margin-bottom:6px;display:flex;align-items:center;gap:6px;">
            <span style="color:var(--accent-glow);">${this.icons.groups}</span>
            <span>Guruhlar bo'yicha taqsimot statistikasi:</span>
          </div>
          <div class="district-stats-row" id="group-stats-chips-container">
            <div style="font-size:12px;color:rgba(94,234,212,0.6);font-style:italic;">
              Hisoblanmoqda...
            </div>
          </div>

          <!-- Students Survey Table -->
          <div class="survey-table-wrapper" style="margin-top:14px;">
            <table class="survey-data-table" id="survey-table">
              <thead>
                <tr>
                  <th style="width:40px;text-align:center;">T/r</th>
                  <th style="width:110px;">Guruhi</th>
                  <th>Talabaning F.I.SH</th>
                  <th style="width:260px;">Amaliyot Tumani</th>
                  <th style="width:46px;text-align:center;"></th>
                </tr>
              </thead>
              <tbody id="survey-tbody"></tbody>
            </table>
          </div>

          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;">
            <div style="font-size:12.5px;color:rgba(94,234,212,0.8);display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.users} <span>Talabalar soni: <b id="survey-total-badge">${surveyStudents.length}</b> ta</span>
            </div>
            <button type="button" class="btn-primary" id="btn-save-all-survey-bottom" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.save} <span>Barcha O'zgarishlarni Saqlash</span>
            </button>
          </div>
        </div>
      `;

      // Helper to sort students naturally by group and then by FIO
      const getSortedStudentsWithIndices = () => {
        const list = surveyStudents.map((st, i) => ({ st, origIdx: i }));
        list.sort((a, b) => {
          const gA = (a.st.guruhi || '').toString().trim();
          const gB = (b.st.guruhi || '').toString().trim();
          const comp = gA.localeCompare(gB, undefined, { numeric: true, sensitivity: 'base' });
          if (comp !== 0) return comp;
          return (a.st.fio || '').localeCompare(b.st.fio || '');
        });
        return list;
      };

      // Render Table Rows (Organized Group by Group)
      const updateSurveyTable = () => {
        const tbody = document.getElementById('survey-tbody');
        const badge = document.getElementById('survey-total-badge');
        if (!tbody) return;
        badge.innerText = surveyStudents.length;

        const groupCounts = {};
        const dynDistrictStats = {};
        surveyStudents.forEach(s => {
          const g = (s.guruhi || '').trim() || "Guruhsiz";
          groupCounts[g] = (groupCounts[g] || 0) + 1;
          const d = (s.tumani || '').trim() || "Shahrisabz shahar";
          dynDistrictStats[d] = (dynDistrictStats[d] || 0) + 1;
        });

        // Dynamic update of district stats chips
        const distBox = document.getElementById('district-stats-chips-container');
        if (distBox) {
          distBox.innerHTML = Object.keys(dynDistrictStats).length > 0 ? Object.entries(dynDistrictStats).map(([dName, cnt]) => `
            <div class="district-stat-chip">
              <span>${dName}:</span>
              <span class="district-stat-count">${cnt} ta</span>
            </div>
          `).join('') : '<div style="font-size:12px;color:rgba(94,234,212,0.6);font-style:italic;">Talabalar so\'rovnomasi hali kiritilmagan.</div>';
        }

        // Dynamic update of group stats chips
        const grpBox = document.getElementById('group-stats-chips-container');
        if (grpBox) {
          grpBox.innerHTML = Object.keys(groupCounts).length > 0 ? Object.entries(groupCounts).map(([gName, cnt]) => `
            <div class="district-stat-chip" style="background:rgba(37,99,235,0.15);border-color:rgba(59,130,246,0.35);">
              <span style="color:#93c5fd;">${gName === 'Guruhsiz' ? gName : gName + '-guruh'}:</span>
              <span class="district-stat-count" style="background:#2563eb;color:#ffffff;">${cnt} ta</span>
            </div>
          `).join('') : '<div style="font-size:12px;color:rgba(94,234,212,0.6);font-style:italic;">Guruhlar hali kiritilmagan.</div>';
        }

        if (surveyStudents.length === 0) {
          tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:24px;color:rgba(94,234,212,0.6);font-style:italic;">Talabalar so'rovnomasi hali kiritilmagan. Excel fayl yuklang yoki qatorlar qo'shing.</td></tr>`;
          return;
        }

        const sorted = getSortedStudentsWithIndices();

        let rowsHtml = '';
        let lastGroup = null;
        let groupStudentIndex = 0;

        sorted.forEach((item) => {
          const st = item.st;
          const origIdx = item.origIdx;
          const currentGroup = (st.guruhi || '').trim() || "Guruhsiz";

          if (currentGroup !== lastGroup) {
            lastGroup = currentGroup;
            groupStudentIndex = 0; // Har bir guruh uchun 1 dan boshidan boshlanadi
            const cnt = groupCounts[currentGroup] || 1;
            rowsHtml += `
              <tr class="group-section-header" style="background:rgba(0,203,169,0.08);border-top:1px solid rgba(0,203,169,0.25);border-bottom:1px solid rgba(0,203,169,0.25);">
                <td colspan="5" style="padding:8px 14px;font-weight:700;color:var(--accent-glow);font-size:12.5px;">
                  <div style="display:flex;align-items:center;gap:8px;">
                    <span style="color:var(--accent-glow);">${this.icons.groups}</span>
                    <span>${currentGroup === 'Guruhsiz' ? 'Guruhsiz talabalar' : currentGroup + '-guruh'}</span>
                    <span style="font-weight:normal;font-size:11px;color:rgba(255,255,255,0.6);background:rgba(0,0,0,0.3);padding:2px 8px;border-radius:10px;">${cnt} ta talaba</span>
                  </div>
                </td>
              </tr>
            `;
          }

          groupStudentIndex++; // Guruh ichida 1, 2, 3...

          rowsHtml += `
            <tr>
              <td style="text-align:center;font-weight:700;color:rgba(255,255,255,0.7);">${groupStudentIndex}.</td>
              <td>
                <input type="text" class="survey-input-cell st-input-grp" data-idx="${origIdx}" value="${st.guruhi || ''}" placeholder="25-16">
              </td>
              <td>
                <input type="text" class="survey-input-cell st-input-fio" data-idx="${origIdx}" value="${st.fio || ''}" placeholder="Talabaning F.I.SH">
              </td>
              <td>
                <select class="survey-input-cell st-input-tum" data-idx="${origIdx}">
                  ${standardDistricts.map(d => `<option value="${d}" ${st.tumani === d ? 'selected' : ''}>${d}</option>`).join('')}
                  ${!standardDistricts.includes(st.tumani) && st.tumani ? `<option value="${st.tumani}" selected>${st.tumani}</option>` : ''}
                </select>
              </td>
              <td style="text-align:center;">
                <button type="button" class="tab-btn-mini danger btn-del-survey-row" data-idx="${origIdx}" title="Qatorni o'chirish">${this.icons.trash}</button>
              </td>
            </tr>
          `;
        });

        tbody.innerHTML = rowsHtml;

        // Cell input listeners
        tbody.querySelectorAll('.st-input-grp').forEach(el => {
          el.addEventListener('input', e => {
            surveyStudents[parseInt(e.target.dataset.idx)].guruhi = e.target.value.trim();
          });
          el.addEventListener('blur', () => {
            updateSurveyTable();
          });
        });

        tbody.querySelectorAll('.st-input-fio').forEach(el => {
          el.addEventListener('input', e => {
            surveyStudents[parseInt(e.target.dataset.idx)].fio = e.target.value;
          });
        });

        tbody.querySelectorAll('.st-input-tum').forEach(el => {
          el.addEventListener('change', e => {
            surveyStudents[parseInt(e.target.dataset.idx)].tumani = e.target.value;
          });
        });

        tbody.querySelectorAll('.btn-del-survey-row').forEach(b => {
          b.addEventListener('click', e => {
            const idx = parseInt(b.dataset.idx);
            surveyStudents.splice(idx, 1);
            updateSurveyTable();
          });
        });
      };
      updateSurveyTable();

      // Trigger Excel Upload
      const fileInput = document.getElementById('survey-excel-file-input');
      document.getElementById('btn-trigger-excel-upload').addEventListener('click', () => fileInput.click());

      fileInput.addEventListener('change', async () => {
        if (!fileInput.files || !fileInput.files[0]) return;
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        this.toast("Excel fayl yuklanmoqda va o'qilmoqda...", "info");
        try {
          const userToken = localStorage.getItem('atlas_token') || this.token || '';
          const res = await fetch(`/api/amaliyot/folders/${currentFolderId}/survey/import`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${userToken}` },
            body: formData
          });
          const json = await res.json();
          if (json?.success) {
            this.toast(json.message || "Excel ma'lumotlari muvaffaqiyatli yuklandi!", "success");
            surveyStudents = json.students || [];
            updateSurveyTable();
          } else {
            this.toast(json?.error || "Faylni o'qishda xatolik", "error");
          }
        } catch (err) {
          this.toast("Server bilan aloqada xatolik: " + err.message, "error");
        }
        fileInput.value = '';
      });

      // Add Row
      document.getElementById('btn-add-survey-row').addEventListener('click', () => {
        let defG = '25-16';
        if (folderPath[2]?.name) {
          const m = folderPath[2].name.match(/(\d{1,4}[-\/\_]\d{1,4}|\d{2,4}[a-zA-Z]?)/);
          if (m) defG = m[1];
        }
        surveyStudents.push({
          guruhi: defG,
          fio: '',
          tumani: standardDistricts[0],
          start_date: '08.06.2026',
          end_date: '06.07.2026',
          phone: '',
          organization: ''
        });
        updateSurveyTable();
      });

      // Save Survey Manual
      const handleSaveSurvey = async (e) => {
        const btn = e.currentTarget;
        const origContent = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<span class="spinner" style="display:inline-block;width:14px;height:14px;border:2px solid #fff;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;margin-right:6px;"></span> Saqlanmoqda...`;

        const valid = surveyStudents.filter(s => s.fio && s.fio.trim());
        const res = await this.api(`/api/amaliyot/folders/${currentFolderId}/survey`, 'POST', {
          students: valid,
          replace_all: true
        });

        btn.disabled = false;
        btn.innerHTML = origContent;

        if (res?.success) {
          this.toast(`${valid.length} ta talaba ma'lumotlari bazaga muvaffaqiyatli saqlandi!`, "success");
          renderSemesterDashboard();
        } else {
          this.toast(res?.error || "Saqlashda xatolik yuz berdi", "error");
        }
      };

      document.getElementById('btn-save-all-survey').addEventListener('click', handleSaveSurvey);
      document.getElementById('btn-save-all-survey-bottom').addEventListener('click', handleSaveSurvey);

      // Paste Bulk Text Modal
      document.getElementById('btn-paste-bulk-survey').addEventListener('click', () => {
        this.openModal("Talabalar Ro'yxatini Ommaviy Nusxalash", `
          <div style="font-size:12.5px;color:rgba(94,234,212,0.9);margin-bottom:10px;line-height:1.5;">
            Har bir qatorga <b>Guruh # F.I.SH # Tuman</b> ko'rinishida yoki to'g'ridan-to'g'ri <b>Exceldan nusxalab</b> qo'ying:
            <div style="background:rgba(0,0,0,0.35);padding:8px 12px;border-radius:6px;color:#34d399;font-family:monospace;margin-top:6px;font-size:12px;border:1px solid rgba(52,211,153,0.2);">
              25-16 # Rahmatova Shaxnoza # Shahrisabz shahar<br>
              25-17 # Asraliyev Asilbek # Kitob tuman<br>
              25-18 # Nazarova Dilnoza # Yakkabog' tuman
            </div>
          </div>
          <textarea id="modal-bulk-text" class="textarea-control" style="height:190px;font-family:monospace;font-size:12.5px;width:100%;resize:vertical;" placeholder="25-16 # Rahmatova Shaxnoza # Shahrisabz shahar&#10;25-17 # Asraliyev Asilbek # Kitob tuman"></textarea>
          <div class="modal-footer" style="margin-top:16px;">
            <button class="btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
            <button class="btn-primary" id="btn-apply-bulk-text">Jadvalga Joylash</button>
          </div>
        `);

        document.getElementById('btn-apply-bulk-text').addEventListener('click', () => {
          const raw = document.getElementById('modal-bulk-text').value.trim();
          if (!raw) return;
          const lines = raw.split('\n').map(l => l.trim()).filter(l => l);
          const parsed = [];

          let folderDefaultG = '25-16';
          if (folderPath[2]?.name) {
            const m = folderPath[2].name.match(/(\d{1,4}[-\/\_]\d{1,4}|\d{2,4}[a-zA-Z]?)/);
            if (m) folderDefaultG = m[1];
          }

          const isGroupToken = (val) => /^(\d{1,4}[-\/\_]\d{1,4}|\d{2,4}[a-zA-Z]?(-guruh)?|[A-Za-z0-9\-_]{2,10})$/i.test(val.trim());
          const isRowNumber = (val) => /^\d{1,4}[\.\)]?$/.test(val.trim());

          lines.forEach(line => {
            if (!line) return;
            let g = folderDefaultG, f = '', tum = 'Shahrisabz shahar';

            if (line.includes('\t')) {
              // Exceldan to'g'ridan-to'g'ri nusxalangan qatorlar (Tab separated)
              const p = line.split('\t').map(x => x.trim()).filter(x => x);
              if (p.length >= 4) {
                if (isRowNumber(p[0]) && isGroupToken(p[1])) {
                  g = p[1]; f = p[2]; tum = p[3];
                } else if (isGroupToken(p[0])) {
                  g = p[0]; f = p[1]; tum = p[2];
                } else {
                  f = p[1]; tum = p[2];
                }
              } else if (p.length === 3) {
                if (isRowNumber(p[0]) && isGroupToken(p[1])) {
                  g = p[1]; f = p[2];
                } else if (isGroupToken(p[0])) {
                  g = p[0]; f = p[1]; tum = p[2];
                } else if (isRowNumber(p[0])) {
                  f = p[1]; tum = p[2];
                } else {
                  f = p[0]; tum = p[1];
                }
              } else if (p.length === 2) {
                if (isGroupToken(p[0])) { g = p[0]; f = p[1]; }
                else if (isRowNumber(p[0])) { f = p[1]; }
                else { f = p[0]; tum = p[1]; }
              } else {
                f = p[0];
              }
            } else if (line.includes('#') || line.includes(';')) {
              const cleanLine = line.replace(/^\d+\s*[\.\)]\s+/, '').trim();
              const p = cleanLine.split(/[#;]/).map(x => x.trim()).filter(x => x);
              if (p.length >= 3) { g = p[0]; f = p[1]; tum = p[2]; }
              else if (p.length === 2) {
                if (isGroupToken(p[0])) { g = p[0]; f = p[1]; }
                else { f = p[0]; tum = p[1]; }
              } else { f = p[0]; }
            } else {
              const cleanLine = line.replace(/^\d+\s*[\.\)]\s+/, '').trim();
              const m = cleanLine.match(/^(\d{1,4}[-\/\_]\d{1,4}|\d{2,4}[a-zA-Z]?)\s+(.+)$/);
              if (m) {
                g = m[1];
                f = m[2];
              } else {
                f = cleanLine;
              }
            }

            if (f) {
              parsed.push({
                guruhi: g,
                fio: f,
                tumani: tum,
                start_date: '08.06.2026',
                end_date: '06.07.2026',
                phone: '',
                organization: ''
              });
            }
          });

          if (parsed.length > 0) {
            surveyStudents = [...surveyStudents, ...parsed];
            updateSurveyTable();
            this.closeModal();
            this.toast(`${parsed.length} ta talaba jadvalga qo'shildi. "So'rovnomani Saqlash" tugmasini bosing.`, "info");
          }
        });
      });
    };

    // ============================================================
    // SUB-VIEW 2: YAKKA TUMAN BUYRUG'I SHAKLLANTIRISH
    // ============================================================
    const renderCreateOrderTab = (viewport, districtStats) => {
      let selectedDistrict = standardDistricts[0];
      const todayStr = new Date().toLocaleDateString('ru-RU');
      const sampleMuddati = "2026-yil 08-iyunidan  2026-yil 06-iyuligacha";

      viewport.innerHTML = `
        <div style="display:grid;grid-template-columns:1.2fr 0.8fr;gap:20px;align-items:start;">
          <!-- LEFT FORM -->
          <div class="glass-card" style="padding:22px;">
            <div style="font-size:16px;font-weight:700;color:#ffffff;margin-bottom:4px;display:flex;align-items:center;gap:8px;">
              <span style="color:var(--accent-glow);">${this.icons.plus}</span>
              <span>Tuman Bo'yicha Yakka Buyruq Generatori</span>
            </div>
            <div style="font-size:12.5px;color:rgba(94,234,212,0.75);margin-bottom:16px;">
              Tumanni tanlang. So'rovnomadagi o'sha tumanga biriktirilgan barcha talabalar avtomatik yuklanadi.
            </div>

            <form id="single-amaliyot-form">
              <!-- Tuman & Shifokor -->
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Tibbiyot Birlashmasi Tumani</label>
                  <select id="single-tumani" class="select-control">
                    ${standardDistricts.map(d => {
                      const cnt = districtStats[d] || 0;
                      return `<option value="${d}">${d} (${cnt} ta talaba)</option>`;
                    }).join('')}
                    <option value="__custom__">+ Boshqa tuman...</option>
                  </select>
                  <input type="text" id="single-custom-tumani" class="input-control" placeholder="Tuman nomini kiriting..." style="display:none;margin-top:6px;">
                </div>

                <div class="form-group">
                  <label class="form-label">Bosh Shifokor F.I.SH</label>
                  <input type="text" id="single-shifokor" class="input-control" value="${districtDoctors[standardDistricts[0]] || 'O.Norboyev'}" required>
                </div>
              </div>

              <!-- Buyruq Raqami va Sanasi -->
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Buyruq Raqami</label>
                  <input type="text" id="single-buyruq-num" class="input-control" placeholder="Masalan: 28-A" value="">
                </div>
                <div class="form-group">
                  <label class="form-label">Buyruq Sanasi</label>
                  <input type="text" id="single-buyruq-sana" class="input-control" value="${todayStr}" required>
                </div>
              </div>

              <!-- O'quv Yili va Bosqich -->
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">O'quv Yili</label>
                  <input type="text" id="single-oquv-yili" class="input-control" value="${folderPath[0]?.name || '2025/2026'}">
                </div>
                <div class="form-group">
                  <label class="form-label">Bosqich / Kursi</label>
                  <select id="single-kursi" class="select-control">
                    <option value="1" selected>1-kurs</option>
                    <option value="2">2-kurs</option>
                    <option value="3">3-kurs</option>
                    <option value="4">4-kurs</option>
                  </select>
                </div>
              </div>

              <!-- Muddati -->
              <div class="form-group">
                <label class="form-label">Amaliyot Muddati (Matn holida)</label>
                <input type="text" id="single-muddati-text" class="input-control" value="${sampleMuddati}">
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Boshlanish Sanasi</label>
                  <input type="text" id="single-start-date" class="input-control" value="08.06.2026">
                </div>
                <div class="form-group">
                  <label class="form-label">Tugash Sanasi</label>
                  <input type="text" id="single-end-date" class="input-control" value="06.07.2026">
                </div>
              </div>

              <!-- Filtered Students Section -->
              <div style="margin-top:16px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:13.5px;font-weight:700;color:var(--accent-glow);display:inline-flex;align-items:center;gap:6px;">
                  ${this.icons.users} <span>Ushbu Tumanga Biriktirilgan Talabalar (<span id="single-students-count">0</span> ta)</span>
                </div>
              </div>

              <div class="students-table-wrapper" style="max-height:260px;">
                <table class="students-data-table" id="single-district-students-table">
                  <thead>
                    <tr>
                      <th style="width:40px;text-align:center;">T/r</th>
                      <th style="width:100px;">Guruhi</th>
                      <th>Talabaning F.I.SH</th>
                    </tr>
                  </thead>
                  <tbody id="single-district-students-tbody"></tbody>
                </table>
              </div>

              <div style="margin-top:20px;">
                <button type="submit" class="btn-primary btn-block" id="btn-generate-single-order" style="display:flex;align-items:center;justify-content:center;gap:8px;">
                  ${this.icons.documents} <span>Ushbu Tuman Buyrug'ini Shakllantirish va Word Yuklab Olish</span>
                </button>
              </div>
            </form>
          </div>

          <!-- RIGHT PREVIEW -->
          <div class="glass-card" style="padding:22px;min-height:480px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
            <div id="single-order-result-box" style="width:100%;">
              <div style="font-size:42px;color:rgba(0,203,169,0.4);margin-bottom:12px;display:flex;justify-content:center;">${this.icons.activity}</div>
              <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:6px;">Amaliyot Buyrug'i Natijasi</div>
              <div style="font-size:12.5px;color:rgba(94,234,212,0.7);max-width:280px;margin:0 auto;">
                Tumanni tanlang va generatsiya tugmasini bosing. Rasmiy Word (.docx) fayli shu yerda paydo bo'ladi.
              </div>
            </div>
          </div>
        </div>
      `;

      const tumanSel = document.getElementById('single-tumani');
      const customTumInp = document.getElementById('single-custom-tumani');
      const shifokorInp = document.getElementById('single-shifokor');
      const tbody = document.getElementById('single-district-students-tbody');
      const countEl = document.getElementById('single-students-count');

      let currentDistrictStudents = [];

      const syncDistrictData = () => {
        const selTum = tumanSel.value === '__custom__' ? customTumInp.value.trim() : tumanSel.value;
        if (tumanSel.value === '__custom__') {
          customTumInp.style.display = 'block';
          customTumInp.focus();
        } else {
          customTumInp.style.display = 'none';
          if (districtDoctors[selTum]) shifokorInp.value = districtDoctors[selTum];
        }

        // Filter students for this district
        currentDistrictStudents = surveyStudents.filter(s => (s.tumani || '').trim() === selTum);
        countEl.innerText = currentDistrictStudents.length;

        if (currentDistrictStudents.length === 0) {
          tbody.innerHTML = `<tr><td colspan="3" style="text-align:center;padding:16px;color:rgba(255,255,255,0.5);">Ushbu tumanga so'rovnomada biriktirilgan talaba topilmadi.</td></tr>`;
        } else {
          currentDistrictStudents.sort((a, b) => {
            const gA = (a.guruhi || '').toString().trim();
            const gB = (b.guruhi || '').toString().trim();
            const comp = gA.localeCompare(gB, undefined, { numeric: true, sensitivity: 'base' });
            if (comp !== 0) return comp;
            return (a.fio || '').localeCompare(b.fio || '');
          });

          let distLastGrp = null;
          let distGrpIdx = 0;
          tbody.innerHTML = currentDistrictStudents.map((st) => {
            const grp = (st.guruhi || '').trim() || "Guruh";
            if (grp !== distLastGrp) {
              distLastGrp = grp;
              distGrpIdx = 0;
            }
            distGrpIdx++;
            return `
              <tr>
                <td style="text-align:center;font-weight:700;color:rgba(255,255,255,0.7);">${distGrpIdx}.</td>
                <td>${st.guruhi || '201'}</td>
                <td style="text-align:left;font-weight:600;">${st.fio}</td>
              </tr>
            `;
          }).join('');
        }
      };

      tumanSel.addEventListener('change', syncDistrictData);
      customTumInp.addEventListener('input', syncDistrictData);
      syncDistrictData();

      // Submit
      document.getElementById('single-amaliyot-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('btn-generate-single-order');
        btn.innerHTML = `<span>Shakllantirilmoqda...</span>`;

        const finalTumani = tumanSel.value === '__custom__' ? customTumInp.value.trim() : tumanSel.value;
        const payload = {
          tumani: finalTumani,
          shu_tuman_shifokori: shifokorInp.value.trim(),
          buyruq_raqami: document.getElementById('single-buyruq-num').value.trim(),
          buyruq_sanasi: document.getElementById('single-buyruq-sana').value.trim(),
          oquv_yili: document.getElementById('single-oquv-yili').value.trim(),
          kursi: document.getElementById('single-kursi').value,
          amaliyot_muddati: document.getElementById('single-muddati-text').value.trim(),
          start_date: document.getElementById('single-start-date').value.trim(),
          end_date: document.getElementById('single-end-date').value.trim(),
          students: currentDistrictStudents.length > 0 ? currentDistrictStudents : [{ fio: "Namunaviy Talaba", guruhi: "201" }]
        };

        try {
          const res = await this.api(`/api/amaliyot/folders/${currentFolderId}/generate-single`, 'POST', payload);
          btn.innerHTML = `${this.icons.documents} <span>Ushbu Tuman Buyrug'ini Shakllantirish va Word Yuklab Olish</span>`;
          if (res?.success) {
            this.toast(res.message || "Buyruq shakllantirildi!", "success");
            const resultBox = document.getElementById('single-order-result-box');
            const userToken = localStorage.getItem('atlas_token') || this.token || '';
            const downloadUrlWithToken = `${res.download_docx_url}?token=${encodeURIComponent(userToken)}`;
            const fname = `${finalTumani} — ${payload.students.length} ta talaba.docx`;

            resultBox.innerHTML = `
              <div style="background:rgba(0,203,169,0.12);border:1px solid rgba(0,203,169,0.4);border-radius:12px;padding:20px;text-align:left;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                  <div style="color:#34d399;font-size:24px;">${this.icons.check}</div>
                  <div>
                    <div style="font-size:15px;font-weight:700;color:#ffffff;">${finalTumani} Buyrug'i Tayyor!</div>
                    <div style="font-size:12px;color:rgba(94,234,212,0.8);">${payload.students.length} ta talaba bilan Word hujjati shakllantirildi</div>
                  </div>
                </div>
                <div style="display:flex;flex-direction:column;gap:8px;margin-top:12px;">
                  <a href="${downloadUrlWithToken}" class="btn-primary btn-block" style="text-decoration:none;display:flex;align-items:center;justify-content:center;gap:8px;" download="${fname}">
                    ${this.icons.download} <span>Word (.docx) Hujjatini Yuklab Olish</span>
                  </a>
                  <button type="button" class="btn-secondary btn-block" id="btn-send-single-tg" style="display:flex;align-items:center;justify-content:center;gap:8px;background:rgba(37,99,235,0.2);border-color:#3b82f6;color:#60a5fa;">
                    ${this.icons.send} <span>Telegram Botga Yuborish</span>
                  </button>
                </div>
              </div>
            `;

            const tgBtn = document.getElementById('btn-send-single-tg');
            if (tgBtn && res.doc_id) {
              tgBtn.addEventListener('click', async () => {
                tgBtn.disabled = true;
                tgBtn.innerHTML = `<span>Yuborilmoqda...</span>`;
                const tgRes = await this.api(`/api/documents/resend/${res.doc_id}`, 'POST');
                if (tgRes?.success) {
                  this.toast("Buyruq Telegram botingizga yuborildi!", "success");
                  tgBtn.innerHTML = `<span>Telegramga Yuborildi</span>`;
                } else {
                  alert(tgRes?.error || "Telegramga yuborishda xatolik");
                  tgBtn.disabled = false;
                  tgBtn.innerHTML = `${this.icons.send} <span>Telegram Botga Yuborish</span>`;
                }
              });
            }
          } else {
            alert(res?.error || "Xatolik yuz berdi");
          }
        } catch (err) {
          btn.innerHTML = `${this.icons.documents} <span>Ushbu Tuman Buyrug'ini Shakllantirish va Word Yuklab Olish</span>`;
          alert("Server bilan aloqada xatolik: " + err.message);
        }
      });
    };

    // ============================================================
    // SUB-VIEW 3: BARCHA TUMANLARNI BIR BOSISHDA SHAKLLANTIRISH (ZIP)
    // ============================================================
    const renderBatchOrdersTab = (viewport) => {
      const extra = currentFolderInfo?.extra_data || {};
      const sDate = extra.start_date || "08.06.2026";
      const eDate = extra.end_date || "06.07.2026";
      const defaultMuddati = extra.amaliyot_muddati || formatAmaliyotMuddatiText(sDate, eDate);

      const districtStats = {};
      surveyStudents.forEach(st => {
        const d = st.tumani || "Shahrisabz shahar";
        districtStats[d] = (districtStats[d] || 0) + 1;
      });

      const totalDistrictsCount = Object.keys(districtStats).length;

      viewport.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
          <!-- LEFT FORM -->
          <div class="glass-card" style="padding:22px;">
            <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:4px;display:flex;align-items:center;gap:8px;">
              <span style="color:var(--accent-glow);">${this.icons.package}</span>
              <span>Barcha Tumanlar Buyruqlarini Yaratish (ZIP)</span>
            </div>
            <div style="font-size:12.5px;color:rgba(94,234,212,0.8);margin-bottom:18px;">
              Bitta bosish orqali so'rovnomadagi ${totalDistrictsCount} ta tuman uchun alohida Word buyruqlarini generatsiya qilib, bitta ZIP paketga yig'adi.
            </div>

            <form id="batch-amaliyot-form">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Buyruq Raqami</label>
                  <input type="text" id="batch-buyruq-raqami" class="input-control" placeholder="Masalan: 45">
                </div>
                <div class="form-group">
                  <label class="form-label">Buyruq Sanasi</label>
                  <input type="text" id="batch-buyruq-sanasi" class="input-control" value="${new Date().toLocaleDateString('ru-RU')}">
                </div>
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">O'quv Yili</label>
                  <input type="text" id="batch-oquv-yili" class="input-control" value="${extra.oquv_yili || '2025/2026'}">
                </div>
                <div class="form-group">
                  <label class="form-label">Bosqich / Kursi</label>
                  <select id="batch-kursi" class="select-control">
                    <option value="1" ${extra.kursi === '1' ? 'selected' : ''}>1-kurs</option>
                    <option value="2" ${extra.kursi === '2' ? 'selected' : ''}>2-kurs</option>
                    <option value="3" ${extra.kursi === '3' ? 'selected' : ''}>3-kurs</option>
                    <option value="4" ${extra.kursi === '4' ? 'selected' : ''}>4-kurs</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Amaliyot Muddati (Matn ko'rinishida)</label>
                <input type="text" id="batch-muddati-text" class="input-control" value="${defaultMuddati}">
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Boshlanish Sanasi</label>
                  <input type="text" id="batch-start-date" class="input-control" value="${sDate}">
                </div>
                <div class="form-group">
                  <label class="form-label">Tugash Sanasi</label>
                  <input type="text" id="batch-end-date" class="input-control" value="${eDate}">
                </div>
              </div>

              <div style="margin-top:22px;">
                <button type="submit" class="btn-primary btn-block" id="btn-generate-batch-orders" style="display:flex;align-items:center;justify-content:center;gap:8px;">
                  ${this.icons.zap} <span>Barcha ${totalDistrictsCount} ta Tuman Buyruqlarini Shakllantirish va ZIP Yuklab Olish</span>
                </button>
              </div>
            </form>
          </div>

          <!-- RIGHT SUMMARY -->
          <div class="glass-card" style="padding:22px;">
            <div id="batch-order-result-box">
              <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:12px;display:flex;align-items:center;gap:8px;">
                <span style="color:var(--accent-glow);">${this.icons.pieChart}</span>
                <span>Tumanlar Bo'yicha Taqsimot:</span>
              </div>

              <div style="display:flex;flex-direction:column;gap:8px;max-height:360px;overflow-y:auto;padding-right:6px;">
                ${Object.entries(districtStats).map(([tum, cnt]) => `
                  <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(0,0,0,0.3);padding:10px 14px;border-radius:8px;border:1px solid var(--border-glass);">
                    <div>
                      <div style="font-weight:700;color:#ffffff;font-size:13.5px;">${tum}</div>
                      <div style="font-size:11.5px;color:rgba(94,234,212,0.7);">Bosh shifokor: ${districtDoctors[tum] || 'Bosh shifokor'}</div>
                    </div>
                    <span class="badge badge-accent" style="font-size:12px;padding:4px 10px;">${cnt} ta talaba</span>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
      `;

      document.getElementById('batch-amaliyot-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('btn-generate-batch-orders');
        const resBox = document.getElementById('batch-order-result-box');

        if (surveyStudents.length === 0) {
          alert("So'rovnomada talabalar topilmadi. Avval so'rovnomani yuklang.");
          return;
        }

        btn.disabled = true;
        btn.innerHTML = `<span>Barcha buyruqlar tayyorlanmoqda...</span>`;

        const payload = {
          buyruq_raqami: document.getElementById('batch-buyruq-raqami').value.trim() || "____",
          buyruq_sanasi: document.getElementById('batch-buyruq-sanasi').value.trim() || new Date().toLocaleDateString('ru-RU'),
          oquv_yili: document.getElementById('batch-oquv-yili').value.trim(),
          kursi: document.getElementById('batch-kursi').value,
          amaliyot_muddati: document.getElementById('batch-muddati-text').value.trim(),
          start_date: document.getElementById('batch-start-date').value.trim(),
          end_date: document.getElementById('batch-end-date').value.trim()
        };

        try {
          const res = await this.api(`/api/amaliyot/folders/${currentFolderId}/generate-all`, 'POST', payload);
          btn.disabled = false;
          btn.innerHTML = `${this.icons.zap} <span>Barcha ${totalDistrictsCount} ta Tuman Buyruqlarini Shakllantirish va ZIP Yuklab Olish</span>`;

          if (res?.success) {
            this.toast("Barcha tumanlar buyruqlari muvaffaqiyatli tayyorlandi!", "success");
            resBox.innerHTML = `
              <div style="background:rgba(0,203,169,0.12);border:1px solid rgba(0,203,169,0.4);border-radius:12px;padding:22px;text-align:left;">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                  <div style="color:var(--accent-glow);font-size:28px;">${this.icons.package}</div>
                  <div>
                    <div style="font-size:16px;font-weight:700;color:#ffffff;">ZIP Paket Tayyor!</div>
                    <div style="font-size:12.5px;color:rgba(94,234,212,0.85);">
                      Jami ${res.total_districts} ta tuman va ${res.total_students} ta talaba bo'yicha Word buyruqlari jamlandi.
                    </div>
                  </div>
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;">
                  <a href="${res.download_zip_url}" class="btn-primary" style="text-decoration:none;font-size:13.5px;font-weight:700;height:42px;display:flex;align-items:center;justify-content:center;gap:6px;" download="${res.zip_filename}">
                    ${this.icons.download} <span>ZIP Yuklab Olish</span>
                  </a>
                  <button type="button" class="btn-secondary" id="btn-send-batch-zip-tg" style="height:42px;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(37,99,235,0.2);border-color:#3b82f6;color:#60a5fa;">
                    ${this.icons.send} <span>Telegramga Yuborish</span>
                  </button>
                </div>

                <div style="font-size:12.5px;font-weight:700;color:#ffffff;margin-bottom:8px;">Paket tarkibi:</div>
                <div style="max-height:180px;overflow-y:auto;display:flex;flex-direction:column;gap:6px;">
                  ${res.files.map(f => `
                    <div style="display:flex;justify-content:space-between;background:rgba(0,0,0,0.3);padding:6px 10px;border-radius:6px;font-size:12px;">
                      <span style="color:#ffffff;display:inline-flex;align-items:center;gap:6px;">${this.icons.fileText} <b>${f.tumani}</b> (${f.guruhlar})</span>
                      <span style="color:#34d399;font-weight:700;">${f.students_count} ta talaba</span>
                    </div>
                  `).join('')}
                </div>
              </div>
            `;

            const tgZipBtn = document.getElementById('btn-send-batch-zip-tg');
            if (tgZipBtn && res.zip_filename) {
              tgZipBtn.addEventListener('click', async () => {
                tgZipBtn.disabled = true;
                tgZipBtn.innerHTML = `<span>Yuborilmoqda...</span>`;
                const tgRes = await this.api('/api/amaliyot/send-zip-telegram', 'POST', { zip_filename: res.zip_filename });
                if (tgRes?.success) {
                  this.toast("ZIP paket Telegram botingizga yuborildi!", "success");
                  tgZipBtn.innerHTML = `<span>Telegramga Yuborildi</span>`;
                } else {
                  alert(tgRes?.error || "Telegramga yuborishda xatolik");
                  tgZipBtn.disabled = false;
                  tgZipBtn.innerHTML = `${this.icons.send} <span>Telegramga Yuborish</span>`;
                }
              });
            }
          } else {
            alert(res?.error || "Generatsiya qilishda xatolik yuz berdi");
          }
        } catch (err) {
          btn.disabled = false;
          btn.innerHTML = `${this.icons.zap} <span>Barcha ${totalDistrictsCount} ta Tuman Buyruqlarini Shakllantirish va ZIP Yuklab Olish</span>`;
          alert("Server bilan aloqada xatolik: " + err.message);
        }
      });
    };

    // ============================================================
    // SUB-VIEW 4: BUYRUQLAR ARXIVI (ORDERS ARCHIVE)
    // ============================================================
    const renderArchiveTab = (viewport) => {
      if (!semesterOrders.length) {
        viewport.innerHTML = `
          <div class="glass-card" style="padding:40px;text-align:center;">
            <div style="color:rgba(0,203,169,0.3);margin-bottom:12px;display:flex;justify-content:center;">${this.icons.archive}</div>
            <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:6px;">Buyruqlar Arxivi Bo'sh</div>
            <div style="font-size:12.5px;color:rgba(94,234,212,0.7);max-width:320px;margin:0 auto 16px;">
              Ushbu semestr bo'yicha hali birorta ham tuman buyrug'i shakllantirilmagan.
            </div>
            <button class="btn-primary btn-sm" id="btn-go-to-create-order" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.plus} <span>Yangi Buyruq Shakllantirish</span>
            </button>
          </div>
        `;
        document.getElementById('btn-go-to-create-order')?.addEventListener('click', () => {
          semesterSubView = 'create_order';
          renderSemesterDashboard();
        });
        return;
      }

      viewport.innerHTML = `
        <div class="glass-card" style="padding:22px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div style="font-size:15px;font-weight:700;color:#ffffff;display:flex;align-items:center;gap:8px;">
              <span style="color:var(--accent-glow);">${this.icons.archive}</span>
              <span>Ushbu Semestr Bo'yicha Shakllantirilgan Buyruqlar (${semesterOrders.length} ta)</span>
            </div>
          </div>

          <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(300px, 1fr));gap:16px;">
            ${semesterOrders.map(ord => {
              const fname = `${ord.tumani} - ${ord.guruhlar || 'Guruh'} - ${ord.students_count} ta talaba.docx`;
              return `
                <div style="background:rgba(6,26,28,0.75);border:1px solid rgba(0,203,169,0.25);border-radius:12px;padding:16px;display:flex;flex-direction:column;justify-content:space-between;">
                  <div>
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                      <div style="font-size:15px;font-weight:700;color:#ffffff;display:flex;align-items:center;gap:6px;">
                        <span style="color:var(--accent-glow);">${this.icons.activity}</span>
                        <span>${ord.tumani}</span>
                      </div>
                      <button class="tab-btn-mini danger btn-delete-order" data-order-id="${ord.id}" title="Arxivdan o'chirish">${this.icons.trash}</button>
                    </div>
                    <div style="font-size:12px;color:rgba(94,234,212,0.85);line-height:1.5;margin-bottom:12px;">
                      • <b>Shifokor:</b> ${ord.shu_tuman_shifokori || 'Bosh shifokor'}<br>
                      • <b>Guruhlar:</b> ${ord.guruhlar || '-'}<br>
                      • <b>Talabalar:</b> <span style="color:#34d399;font-weight:700;">${ord.students_count} ta</span><br>
                      • <b>Yaratilgan:</b> ${ord.created_at ? new Date(ord.created_at).toLocaleDateString('ru-RU') : '-'}<br>
                    </div>
                  </div>
                  <div>
                    <a href="/api/documents/download_docx/${ord.id}" class="btn-primary btn-block btn-sm" style="text-decoration:none;display:flex;align-items:center;justify-content:center;gap:6px;" download="${fname}">
                      ${this.icons.download} <span>Word (.docx) Yuklab Olish</span>
                    </a>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;

      viewport.querySelectorAll('.btn-delete-order').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          const ordId = parseInt(btn.dataset.orderId);
          if (confirm("Ushbu buyruqni arxivdan o'chirmoqchimisiz?")) {
            const res = await this.api(`/api/amaliyot/orders/${ordId}`, 'DELETE');
            if (res?.success) {
              this.toast("Buyruq arxivdan o'chirildi", "success");
              semesterOrders = semesterOrders.filter(o => o.id !== ordId);
              renderArchiveTab(viewport);
            }
          }
        });
      });
    };

    // Initial Load at Root (Parent = null)
    loadFolderData(null);
  },
  // ============================================================
  // 2. MA'LUMOTNOMALAR BO'LIMI (MINIMALISTIK & ZAMONAVIY)
  // ============================================================
  async loadCertificates(container, selectedTplId = 'qabul_1_kurs') {
    let currentTpl = selectedTplId;
    let activeTab = this.certsActiveTab || 'create'; // 'create' | 'archive'

    const render = () => {
      this.certsActiveTab = activeTab;
      container.innerHTML = `
        <div class="tab-pills-row">
          <button class="tab-pill-btn ${activeTab === 'create' ? 'active' : ''}" id="tab-certs-create">
            ${this.icons.plus} <span>Yangi Ma'lumotnoma Shakllantirish</span>
          </button>
          <button class="tab-pill-btn ${activeTab === 'archive' ? 'active' : ''}" id="tab-certs-archive">
            ${this.icons.archive} <span>Ma'lumotnomalar Arxivi</span>
          </button>
        </div>

        <div id="certs-main-content"></div>
      `;

      document.getElementById('tab-certs-create').addEventListener('click', () => {
        activeTab = 'create';
        this.certsActiveTab = 'create';
        render();
      });

      document.getElementById('tab-certs-archive').addEventListener('click', () => {
        activeTab = 'archive';
        this.certsActiveTab = 'archive';
        render();
      });

      const contentBox = document.getElementById('certs-main-content');
      if (activeTab === 'create') {
        contentBox.innerHTML = `
          <!-- 2 Ta Minimalistik Ma'lumotnoma Tanlash Kartalari -->
          <div class="template-select-grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
            <div class="template-select-card ${currentTpl === 'qabul_1_kurs' ? 'active' : ''}" data-tpl="qabul_1_kurs">
              <div class="template-card-icon">${this.icons.documents}</div>
              <div class="template-card-body">
                <div class="template-card-title">1-kursga qabul ma'lumotnomasi</div>
                <div class="template-card-desc">Talaba texnikumga 1-kursga qabul qilinganligini tasdiqlovchi rasmiy hujjat</div>
              </div>
            </div>

            <div class="template-select-card ${currentTpl === 'oqiyapti' ? 'active' : ''}" data-tpl="oqiyapti">
              <div class="template-card-icon">${this.icons.documents}</div>
              <div class="template-card-body">
                <div class="template-card-title">O'qiyotganligi haqida ma'lumotnoma</div>
                <div class="template-card-desc">Hozirgi vaqtda tahsil olayotganligini tasdiqlovchi rasmiy hujjat</div>
              </div>
            </div>
          </div>

          <!-- Form Box -->
          <div id="cert-form-box"></div>
        `;

        // Card click listeners
        contentBox.querySelectorAll('.template-select-card').forEach(card => {
          card.addEventListener('click', () => {
            currentTpl = card.dataset.tpl;
            render();
          });
        });

        // Render document generator form (archive shown inside renderDocumentGenerator)
        this.renderDocumentGenerator(document.getElementById('cert-form-box'), currentTpl);
      } else {
        // Render certificates archive
        this.renderDocumentArchive(contentBox, 'qabul_1_kurs', false);
      }
    };

    render();
  },

  // ============================================================
  // 3. DOCUMENTS & PERMANENT ARCHIVE (ASOSIY BO'LIM)
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
    const titlesMap = {
      qabul_1_kurs: "1-Kursga Qabul Ma'lumotnomasi",
      oqiyapti: "O'qiyotganligi Haqida Ma'lumotnoma",
      buyruq_akademik_tatil: "Akademik Ta'til Berish Buyrug'i",
      buyruq_qayta_tiklash: "Akademik Ta'tildan Qayta Tiklash Buyrug'i",
      buyruq_guruhdan_guruhga: "Guruhdan Guruhga O'tkazish Buyrug'i",
      buyruq_safidan_chiqarish: "Talabalar Safidan Chiqarish Buyrug'i"
    };
    const cardTitle = titlesMap[specificTplId] || "Rasmiy Hujjat & Buyruq Shakllantirish";

    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:24px;margin-bottom:24px;">
        <!-- Left: Input Form -->
        <div class="glass-card">
          <div class="card-header-flex">
            <div>
              <div class="card-title">${cardTitle}</div>
              <div class="card-subtitle">Ultra HD (300 DPI A4) rasm va asl Word (.docx) holida bir zumda shakllantirish</div>
            </div>
          </div>

          <form id="doc-gen-form">
            <div class="form-group" ${specificTplId ? 'style="display:none;"' : ''}>
              <label class="form-label">Hujjat / Buyruq Shablonini Tanlang</label>
              <select id="doc-tpl-select" class="select-control">
                <optgroup label="Ma'lumotnomalar">
                  <option value="qabul_1_kurs" ${specificTplId === 'qabul_1_kurs' ? 'selected' : ''}>1-kursga qabul ma'lumotnomasi</option>
                  <option value="oqiyapti" ${specificTplId === 'oqiyapti' ? 'selected' : ''}>O'qiyotganligi haqida ma'lumotnoma</option>
                </optgroup>
                <optgroup label="Rasmiy Buyruqlar">
                  <option value="buyruq_akademik_tatil" ${specificTplId === 'buyruq_akademik_tatil' ? 'selected' : ''}>Akademik ta'til berish buyrug'i</option>
                  <option value="buyruq_qayta_tiklash" ${specificTplId === 'buyruq_qayta_tiklash' ? 'selected' : ''}>Akademik ta'tildan qayta tiklash buyrug'i</option>
                  <option value="buyruq_guruhdan_guruhga" ${specificTplId === 'buyruq_guruhdan_guruhga' ? 'selected' : ''}>Guruhdan guruhga o'tkazish buyrug'i</option>
                  <option value="buyruq_safidan_chiqarish" ${specificTplId === 'buyruq_safidan_chiqarish' ? 'selected' : ''}>Talabalar safidan chiqarish buyrug'i</option>
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
              <input type="text" id="doc-buyruq-raqami" class="input-control" placeholder="Buyruq raqamini kiriting (masalan: 14-B)" value="">
            </div>

            <!-- Avvalgi buyruq rekvizitlari -->
            <div id="group-avvalgi-buyruq" style="display:none;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div class="form-group">
                  <label class="form-label">Avvalgi Buyruq Raqami</label>
                  <input type="text" id="doc-avv-raqam" class="input-control" placeholder="Avvalgi buyruq raqami..." value="">
                </div>
                <div class="form-group">
                  <label class="form-label">Avvalgi Buyruq Sanasi</label>
                  <input type="text" id="doc-avv-sana" class="input-control" placeholder="Avvalgi buyruq sanasi (masalan: 10.02.2025)" value="">
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
                  <select id="doc-guruhi-select" class="select-control" style="margin-bottom:6px;">
                    <option value="">-- Guruhni tanlang --</option>
                  </select>
                  <input type="text" id="doc-guruhi" class="input-control" placeholder="Guruh nomini kiriting (masalan: 104)..." style="display:none;">
                </div>
              </div>
            </div>

            <!-- Yangi guruh -->
            <div class="form-group" id="group-yangi-guruh" style="display:none;">
              <label class="form-label">Yangi Guruh (O'tkazilayotgan / Tiklanayotgan)</label>
              <select id="doc-yangi-guruhi-select" class="select-control" style="margin-bottom:6px;">
                <option value="">-- Yangi guruhni tanlang --</option>
              </select>
              <input type="text" id="doc-yangi-guruhi" class="input-control" placeholder="Yangi guruh nomini kiriting..." style="display:none;">
            </div>

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

    // Load academic groups into dropdowns
    const populateAllGroupSelects = (gList) => {
      const sel1 = document.getElementById('doc-guruhi-select');
      const sel2 = document.getElementById('doc-yangi-guruhi-select');

      const fillSel = (sel) => {
        if (!sel) return;
        sel.innerHTML = '<option value="">-- Guruhni tanlang --</option>' +
          gList.map(g => {
            const extra = g.rahbar_name ? ` (${g.course_level || 1}-kurs | ${g.rahbar_name})` : ` (${g.course_level || 1}-kurs)`;
            return `<option value="${g.group_name}" data-course="${g.course_level || 1}" data-rahbar="${g.rahbar_name || ''}">${g.group_name}${extra}</option>`;
          }).join('') +
          '<option value="__custom__">✨ + Maxsus guruh (Qo\'lda kiritish)...</option>';
      };

      fillSel(sel1);
      fillSel(sel2);
    };

    if (this._academicGroups && this._academicGroups.length > 0) {
      populateAllGroupSelects(this._academicGroups);
    }
    this.api('/api/groups/academic').then(res => {
      const gList = res?.groups || [];
      this._academicGroups = gList;
      populateAllGroupSelects(gList);
    });

    // Toggle custom group inputs
    const inp1 = document.getElementById('doc-guruhi');
    const sel1 = document.getElementById('doc-guruhi-select');
    const courseSel = document.getElementById('doc-kursi');

    if (sel1 && inp1) {
      sel1.addEventListener('change', () => {
        if (sel1.value === '__custom__') {
          inp1.style.display = 'block';
          inp1.value = '';
          inp1.focus();
        } else {
          inp1.style.display = 'none';
          inp1.value = sel1.value;
          const opt = sel1.options[sel1.selectedIndex];
          if (opt && opt.dataset.course && courseSel) {
            courseSel.value = opt.dataset.course;
          }
        }
      });
    }

    const inp2 = document.getElementById('doc-yangi-guruhi');
    const sel2 = document.getElementById('doc-yangi-guruhi-select');

    if (sel2 && inp2) {
      sel2.addEventListener('change', () => {
        if (sel2.value === '__custom__') {
          inp2.style.display = 'block';
          inp2.value = '';
          inp2.focus();
        } else {
          inp2.style.display = 'none';
          inp2.value = sel2.value;
        }
      });
    }

    const tplSelect = document.getElementById('doc-tpl-select');
    if (specificTplId && tplSelect) {
      tplSelect.value = specificTplId;
    }
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
      const val = specificTplId || tplSelect.value;
      if (tplSelect && specificTplId) {
        tplSelect.value = specificTplId;
      }
      
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

      const tpl_id = specificTplId || tplSelect.value;
      const fio = document.getElementById('doc-fio').value.trim();
      const sana = document.getElementById('doc-sana').value.trim();

      const getGuruhVal = () => {
        const inp = document.getElementById('doc-guruhi');
        const sel = document.getElementById('doc-guruhi-select');
        if (inp && inp.value.trim()) return inp.value.trim();
        if (sel && sel.value && sel.value !== '__custom__') return sel.value.trim();
        return (inp?.value || sel?.value || '').trim();
      };

      const getYangiGuruhVal = () => {
        const inp = document.getElementById('doc-yangi-guruhi');
        const sel = document.getElementById('doc-yangi-guruhi-select');
        if (inp && inp.value.trim()) return inp.value.trim();
        if (sel && sel.value && sel.value !== '__custom__') return sel.value.trim();
        return (inp?.value || sel?.value || '').trim();
      };

      const finalGuruh = getGuruhVal();
      const finalYangiGuruh = getYangiGuruhVal();

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
        answers['GURUHI'] = finalGuruh;
      } else if (tpl_id === 'buyruq_akademik_tatil') {
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value.trim();
        answers['kursi'] = document.getElementById('doc-kursi').value;
        answers['guruhi'] = finalGuruh;
        answers['avvalgi_guruhi'] = finalGuruh;
      } else if (tpl_id === 'buyruq_qayta_tiklash') {
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value.trim();
        answers['avvalgi_buyruq_raqami'] = document.getElementById('doc-avv-raqam').value.trim();
        answers['avvalgi_buyruq_sanasi'] = document.getElementById('doc-avv-sana').value.trim();
        answers['kursi'] = document.getElementById('doc-kursi').value;
        answers['avvalgi_guruhi'] = finalGuruh;
        answers['guruhi'] = finalGuruh;
        answers['yangi_guruhi'] = finalYangiGuruh;
      } else if (tpl_id === 'buyruq_guruhdan_guruhga') {
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value.trim();
        answers['yonalishi'] = document.getElementById('doc-yonalish').value;
        answers['avvalgi_guruhi'] = finalGuruh;
        answers['guruhi'] = finalGuruh;
        answers['yangi_guruhi'] = finalYangiGuruh;
      } else if (tpl_id === 'buyruq_safidan_chiqarish') {
        answers['asos_turi'] = document.getElementById('doc-asos-turi').value;
        answers['buyruq_raqami'] = document.getElementById('doc-buyruq-raqami').value.trim();
        answers['kursi'] = document.getElementById('doc-kursi').value;
        answers['avvalgi_guruhi'] = finalGuruh;
        answers['guruhi'] = finalGuruh;
      }

      const res = await this.api('/api/documents/generate', 'POST', { template_id: tpl_id, answers });
      btn.innerHTML = `${this.icons.documents} <span>Hujjatni shakllantirish va saqlash</span>`;

      if (res && res.success) {
        this.toast(res.message, 'success');
        const prevBox = document.getElementById('doc-preview-box');
        const curToken = localStorage.getItem('atlas_token') || this.token || '';
        const tokenQuery = curToken ? `?token=${encodeURIComponent(curToken)}` : '';
        prevBox.innerHTML = `
          <div style="width:100%;display:flex;flex-direction:column;align-items:center;">
            <img src="${res.view_url}${tokenQuery}" style="max-width:100%;max-height:410px;border-radius:var(--radius-md);box-shadow:var(--shadow-card);border:1px solid var(--border-glass);" alt="Hujjat">
            <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;justify-content:center;">
              <button class="btn-sm btn-secondary" onclick="ATLAS.openImageModal('${res.view_url}', '${fio}', ${res.doc_id})">
                ${this.icons.eye} <span>Katta ko'rish</span>
              </button>
              <button class="btn-sm btn-secondary" onclick="ATLAS.openEditDocModal(${res.doc_id})">
                ${this.icons.edit} <span>Tahrirlash</span>
              </button>
              <a href="${res.download_docx_url || `/api/documents/download_docx/${res.doc_id}`}${tokenQuery}" class="btn-sm btn-primary" style="background:#2563eb;border-color:#3b82f6;">
                ${this.icons.download} <span>Word (.docx) yuklab olish</span>
              </a>
              <a href="${res.download_url}${tokenQuery}" class="btn-sm btn-secondary">
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
                          <a href="/api/documents/download_docx/${d.id}?token=${encodeURIComponent(localStorage.getItem('atlas_token') || this.token || '')}" class="btn-icon" title="Word (.docx) yuklab olish" style="color:#60a5fa;">${this.icons.download}</a>
                          <a href="/api/documents/download/${d.id}?token=${encodeURIComponent(localStorage.getItem('atlas_token') || this.token || '')}" class="btn-icon" title="Rasm (.png) yuklab olish">${this.icons.download}</a>
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
                    <a href="/api/documents/download_docx/${d.id}?token=${encodeURIComponent(localStorage.getItem('atlas_token') || this.token || '')}" class="btn-icon" title="Word (.docx) yuklab olish" style="color:#60a5fa;">${this.icons.download}</a>
                    <a href="/api/documents/download/${d.id}?token=${encodeURIComponent(localStorage.getItem('atlas_token') || this.token || '')}" class="btn-icon" title="Rasm (.png) yuklab olish">${this.icons.download}</a>
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
        this.refreshCurrentView();
      } else {
        this.toast(resUpdate ? resUpdate.error : 'Tahrirlashda xatolik', 'error');
      }
    });
  },

  refreshCurrentView() {
    const route = this.currentRoute || (window.location.hash || '').replace(/^#\/?/, '').trim() || 'orders';
    const viewport = document.getElementById('content-viewport');
    if (!viewport) return;

    if (route === 'orders') {
      this.loadOrders(viewport);
    } else if (route === 'certificates') {
      this.loadCertificates(viewport);
    } else if (route === 'amaliyot') {
      this.loadAmaliyot(viewport);
    } else if (route === 'contracts') {
      this.loadContracts(viewport);
    } else {
      this.navigate(route, false);
    }
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
      this.refreshCurrentView();
    }
  },

  openImageModal(imgUrl, title, docId) {
    const token = localStorage.getItem('atlas_token') || this.token || '';
    let authImgUrl = imgUrl;
    if (token && !authImgUrl.includes('token=')) {
      authImgUrl += (authImgUrl.includes('?') ? '&' : '?') + `token=${encodeURIComponent(token)}`;
    }
    const downloadPngUrl = docId ? `/api/documents/download/${docId}?token=${encodeURIComponent(token)}` : authImgUrl;
    const downloadDocxUrl = docId ? `/api/documents/download_docx/${docId}?token=${encodeURIComponent(token)}` : '';
    this.openModalLarge(`${title} — 300 DPI A4 Ko'rinish`, `
      <div style="text-align:center;">
        <img src="${authImgUrl}" style="max-width:100%;max-height:75vh;border-radius:var(--radius-sm);box-shadow:var(--shadow-card);border:1px solid var(--border-glass);" alt="${title}">
        <div class="modal-footer" style="justify-content:center;gap:12px;margin-top:16px;flex-wrap:wrap;">
          <a href="${authImgUrl}" target="_blank" class="btn-sm btn-secondary">${this.icons.eye} Yangi oynada ochish</a>
          ${downloadDocxUrl ? `<a href="${downloadDocxUrl}" class="btn-sm btn-primary" style="background:#2563eb;border-color:#3b82f6;">${this.icons.download} Word (.docx) yuklab olish</a>` : ''}
          <a href="${downloadPngUrl}" class="btn-sm btn-secondary">${this.icons.download} Rasm (.png) yuklab olish</a>
        </div>
      </div>
    `);
  },

  // ============================================================
  // 1.5. KONTRAKTLAR & BANK DEBITORKASI MODULI
  // ============================================================
  contractState: {
    bazaFile: null,
    debFile: null,
    ssBazaFile: null,
    startDate: '',
    detectedDate: '',
    suggestedDate: '',
    lastUpdateResult: null,
    lastSsResult: null
  },

  async loadContracts(container, activeTab = 'update') {
    container.innerHTML = `
      <div class="tab-pills-row">
        <button class="tab-pill-btn ${activeTab === 'update' ? 'active' : ''}" id="tab-c-update">
          ${this.icons.analytics} <span>1. Kontraktlarni Yangilash (Baza + Debitorka)</span>
        </button>
        <button class="tab-pill-btn ${activeTab === 'screenshots' ? 'active' : ''}" id="tab-c-screenshots">
          ${this.icons.dashboard} <span>2. Guruh Screenshotlari (HD Galereya)</span>
        </button>
        <button class="tab-pill-btn ${activeTab === 'history' ? 'active' : ''}" id="tab-c-history">
          ${this.icons.archive} <span>3. Tarix & Arxiv</span>
        </button>
      </div>

      <div id="contracts-tab-content"></div>
    `;

    document.getElementById('tab-c-update').addEventListener('click', () => {
      this.loadContracts(container, 'update');
    });
    document.getElementById('tab-c-screenshots').addEventListener('click', () => {
      this.loadContracts(container, 'screenshots');
    });
    document.getElementById('tab-c-history').addEventListener('click', () => {
      this.loadContracts(container, 'history');
    });

    const contentBox = document.getElementById('contracts-tab-content');
    if (activeTab === 'update') {
      this.renderContractUpdater(contentBox);
    } else if (activeTab === 'screenshots') {
      this.renderGroupScreenshotsView(contentBox);
    } else {
      this.renderContractHistory(contentBox);
    }
  },

  renderContractUpdater(container) {
    container.innerHTML = `
      <div class="card" style="margin-bottom: 24px;">
        <div style="text-align:center;margin-bottom:24px;">
          <h2 style="font-size:23px;font-weight:800;color:#ffffff;margin-bottom:8px;letter-spacing:-0.02em;">Kontrakt To'lovlarini Yangilash & Debitorka Taqqoslash</h2>
          <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.35);border-radius:var(--radius-pill);color:#34d399;font-size:11px;font-weight:700;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.04em;">
            ${this.icons.check} FORMULALAR 100% SAQLANADI
          </div>
          <p style="font-size: 0.88rem; color: rgba(94, 234, 212, 0.8); max-width:760px; margin:0 auto; line-height:1.5;">
            Asosiy Baza (.xlsx) va Bank Debitorkasi (.xlsx) fayllarini sudrab olib kelib tashlang.
            Tizim ismlarni sun'iy intellekt va fuzzy taqqoslash orqali moslashtirib, to'lovlarni yangilaydi hamda XULOSA hisobotini tayyorlaydi.
          </p>
        </div>

        <!-- DROPZONES -->
        <div class="dropzone-container">
          <!-- 1. ASOSIY BAZA DROPZONE -->
          <div class="file-dropzone ${this.contractState.bazaFile ? 'has-file' : ''}" id="dropzone-baza">
            <input type="file" id="file-input-baza" accept=".xlsx" style="display:none;">
            <div class="dropzone-icon" style="color:var(--accent-glow);">${this.icons.analytics}</div>
            <div class="dropzone-title">1. Asosiy Baza Fayli (.xlsx)</div>
            <div class="dropzone-hint">Faylni bu yerga sudrab tashlang yoki tanlash uchun bosing</div>
            <div id="badge-baza">
              ${this.contractState.bazaFile ? `<div class="dropzone-file-badge">${this.icons.check} ${this.contractState.bazaFile.name} (${(this.contractState.bazaFile.size/1024).toFixed(1)} KB)</div>` : ''}
            </div>
            <div id="detected-date-container">
              ${this.contractState.detectedDate ? `<div class="detected-date-pill" style="display:inline-flex;align-items:center;gap:6px;">${this.icons.info} Aniqlangan sana: <b>${this.contractState.detectedDate}</b> → Tavsiya: <b>${this.contractState.suggestedDate}</b></div>` : ''}
            </div>
          </div>

          <!-- 2. BANK DEBITORKASI DROPZONE -->
          <div class="file-dropzone ${this.contractState.debFile ? 'has-file' : ''}" id="dropzone-deb">
            <input type="file" id="file-input-deb" accept=".xlsx" style="display:none;">
            <div class="dropzone-icon" style="color:var(--accent-glow);">${this.icons.documents}</div>
            <div class="dropzone-title">2. Bank Debitorkasi (.xlsx)</div>
            <div class="dropzone-hint">Bankdan olingan debitorka faylini bu yerga sudrab tashlang</div>
            <div id="badge-deb">
              ${this.contractState.debFile ? `<div class="dropzone-file-badge">${this.icons.check} ${this.contractState.debFile.name} (${(this.contractState.debFile.size/1024).toFixed(1)} KB)</div>` : ''}
            </div>
          </div>
        </div>

        <!-- OPTIONS ROW -->
        <div class="contract-action-form-grid">
          <div class="form-group">
            <label class="form-label">To'lovlarni hisoblash boshlanish sanasi</label>
            <input type="text" id="contract-start-date" class="input-control" placeholder="Format: 01.08.2026" value="${this.contractState.startDate || this.contractState.suggestedDate || ''}">
            <div class="form-hint">Format: <code>01.08.2026</code> (Bank to'lovlari shu sanadan boshlab hisoblanadi)</div>
          </div>

          <div class="form-group action-col">
            <label class="form-label">&nbsp;</label>
            <button class="btn-primary btn-block" id="btn-run-contract-update">
              ${this.icons.refresh} <span>Yangilash va Hisobotni Shakllantirish</span>
            </button>
            <div class="form-hint" style="visibility:hidden;">&nbsp;</div>
          </div>
        </div>

        <!-- PROGRESS BAR -->
        <div class="contract-progress-bar" id="contract-progress-bar">
          <div class="contract-progress-inner" id="contract-progress-inner"></div>
        </div>
        <div id="contract-progress-status" style="font-size:0.85rem;color:var(--color-primary);text-align:center;display:none;margin-bottom:14px;"></div>
      </div>

      <!-- RESULTS BOX -->
      <div id="contract-results-view">
        ${this.contractState.lastUpdateResult ? this.renderContractResultsHTML(this.contractState.lastUpdateResult) : ''}
      </div>
    `;

    // Dropzone Baza Events
    const dzBaza = document.getElementById('dropzone-baza');
    const inputBaza = document.getElementById('file-input-baza');
    dzBaza.addEventListener('click', () => inputBaza.click());
    inputBaza.addEventListener('change', (e) => {
      if (e.target.files[0]) this.handleBazaFileSelected(e.target.files[0]);
    });
    this.setupDragAndDrop(dzBaza, (file) => this.handleBazaFileSelected(file));

    // Dropzone Debitorka Events
    const dzDeb = document.getElementById('dropzone-deb');
    const inputDeb = document.getElementById('file-input-deb');
    dzDeb.addEventListener('click', () => inputDeb.click());
    inputDeb.addEventListener('change', (e) => {
      if (e.target.files[0]) this.handleDebFileSelected(e.target.files[0]);
    });
    this.setupDragAndDrop(dzDeb, (file) => this.handleDebFileSelected(file));

    // Process Button Event
    document.getElementById('btn-run-contract-update').addEventListener('click', () => this.runContractUpdateProcess());
  },

  setupDragAndDrop(element, onFileDropped) {
    ['dragenter', 'dragover'].forEach(eventName => {
      element.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        element.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      element.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        element.classList.remove('dragover');
      }, false);
    });

    element.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        onFileDropped(files[0]);
      }
    });
  },

  async handleBazaFileSelected(file) {
    if (!file.name.toLowerCase().endsWith('.xlsx')) {
      this.toast('Iltimos, faqat .xlsx formatidagi Excel faylini yuklang!', 'error');
      return;
    }
    this.contractState.bazaFile = file;

    const badge = document.getElementById('badge-baza');
    if (badge) {
      badge.innerHTML = `<div class="dropzone-file-badge">${this.icons.check} ${file.name} (${(file.size/1024).toFixed(1)} KB)</div>`;
    }
    const dz = document.getElementById('dropzone-baza');
    if (dz) dz.classList.add('has-file');

    // Analyze Baza to detect date
    const formData = new FormData();
    formData.append('baza', file);

    try {
      const res = await fetch('/api/contracts/analyze', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: formData
      });
      const data = await res.json();
      if (data && data.success) {
        this.contractState.detectedDate = data.detected_date || '';
        this.contractState.suggestedDate = data.suggested_start_date || '';
        this.contractState.startDate = data.suggested_start_date || '';

        const datePill = document.getElementById('detected-date-container');
        if (datePill && data.detected_date) {
          datePill.innerHTML = `<div class="detected-date-pill">Aniqlangan sana: <b>${data.detected_date}</b> → Tavsiya: <b>${data.suggested_start_date}</b> (${data.total_students} ta talaba, ${data.groups_count} ta guruh)</div>`;
        }
        const sInput = document.getElementById('contract-start-date');
        if (sInput && data.suggested_start_date) {
          sInput.value = data.suggested_start_date;
        }
        this.toast(`Asosiy baza qabul qilindi: ${data.total_students} ta talaba aniqlandi`, 'success');
      }
    } catch (e) {
      console.error(e);
    }
  },

  handleDebFileSelected(file) {
    if (!file.name.toLowerCase().endsWith('.xlsx')) {
      this.toast('Iltimos, faqat .xlsx formatidagi Debitorka faylini yuklang!', 'error');
      return;
    }
    this.contractState.debFile = file;

    const badge = document.getElementById('badge-deb');
    if (badge) {
      badge.innerHTML = `<div class="dropzone-file-badge">${this.icons.check} ${file.name} (${(file.size/1024).toFixed(1)} KB)</div>`;
    }
    const dz = document.getElementById('dropzone-deb');
    if (dz) dz.classList.add('has-file');
    this.toast('Bank debitorkasi qabul qilindi!', 'success');
  },

  async runContractUpdateProcess() {
    if (!this.contractState.bazaFile) {
      this.toast('Iltimos, 1-maydonga Asosiy Baza faylini yuklang!', 'error');
      return;
    }
    if (!this.contractState.debFile) {
      this.toast('Iltimos, 2-maydonga Bank Debitorkasi faylini yuklang!', 'error');
      return;
    }

    const sDateInput = document.getElementById('contract-start-date');
    const sDate = (sDateInput ? sDateInput.value : '').trim();
    if (!sDate) {
      this.toast('Iltimos, boshlanish sanasini kiriting (Format: 01.08.2026)!', 'error');
      return;
    }

    const pBar = document.getElementById('contract-progress-bar');
    const pInner = document.getElementById('contract-progress-inner');
    const pStatus = document.getElementById('contract-progress-status');
    const btn = document.getElementById('btn-run-contract-update');

    pBar.style.display = 'block';
    pStatus.style.display = 'block';
    btn.disabled = true;

    pInner.style.width = '20%';
    pStatus.innerText = 'Fayllar yuklanmoqda va tahlil qilinmoqda...';

    const formData = new FormData();
    formData.append('baza', this.contractState.bazaFile);
    formData.append('debitorka', this.contractState.debFile);
    formData.append('start_date', sDate);

    try {
      setTimeout(() => {
        pInner.style.width = '55%';
        pStatus.innerText = 'Fuzzy matching algoritmi orqali ismlar va to\'lovlar solishtirilmoqda...';
      }, 500);

      setTimeout(() => {
        pInner.style.width = '85%';
        pStatus.innerText = 'Formulalarni buzmasdan Excel yangilanmoqda va 300 DPI Xulosa rasmi chizilmoqda...';
      }, 1500);

      const res = await fetch('/api/contracts/update', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: formData
      });

      const data = await res.json();
      btn.disabled = false;

      if (data && data.success) {
        pInner.style.width = '100%';
        pStatus.innerText = '✅ Muvaffaqiyatli yakunlandi!';
        setTimeout(() => {
          pBar.style.display = 'none';
          pStatus.style.display = 'none';
        }, 1200);

        this.contractState.lastUpdateResult = data;
        this.toast(`Muvaffaqiyatli yangilandi: ${data.metrics.total_income.toLocaleString()} so'm tushum!`, 'success');

        const resView = document.getElementById('contract-results-view');
        if (resView) {
          resView.innerHTML = this.renderContractResultsHTML(data);
          this.bindContractResultsEvents(data);
        }
      } else {
        pBar.style.display = 'none';
        pStatus.style.display = 'none';
        this.toast(data ? data.error : 'Yangilashda xatolik yuz berdi', 'error');
      }
    } catch (err) {
      btn.disabled = false;
      pBar.style.display = 'none';
      pStatus.style.display = 'none';
      this.toast('Server bilan aloqada xatolik yuz berdi', 'error');
    }
  },

  renderContractResultsHTML(data) {
    const m = data.metrics || {};
    const updatedCount = (data.updated_students || []).length;
    const unmatchedCount = (data.unmatched_records || []).length;
    const xulosaCount = (data.xulosa_rows || []).length;

    return `
      <div class="card" style="margin-top:24px;">
        <div style="text-align:center;margin-bottom:24px;">
          <h2 style="font-size:24px;font-weight:800;color:#ffffff;margin-bottom:6px;letter-spacing:-0.02em;">Yangilanish Natijalari & Tahliliy Hisobot</h2>
          <div style="font-size:13px;color:rgba(94,234,212,0.85);">Muvaffaqiyatli taqqoslandi va kontrakt bazasi yangilandi</div>
        </div>

        <!-- KPI CARDS -->
        <div class="contract-kpi-grid">
          <div class="contract-kpi-card">
            <span class="contract-kpi-label">Jami Tushgan Pul</span>
            <span class="contract-kpi-val highlight-green">${(m.total_income || 0).toLocaleString()} so'm</span>
          </div>
          <div class="contract-kpi-card">
            <span class="contract-kpi-label">Yangilangan Talabalar</span>
            <span class="contract-kpi-val highlight-cyan">${m.updated_count || 0} kishi (${updatedCount} to'lov)</span>
          </div>
          <div class="contract-kpi-card">
            <span class="contract-kpi-label">Topilmagan / Noaniq</span>
            <span class="contract-kpi-val ${unmatchedCount > 0 ? 'highlight-warn' : ''}">${unmatchedCount} ta to'lov</span>
          </div>
          <div class="contract-kpi-card">
            <span class="contract-kpi-label">Filtr Oralig'i</span>
            <span class="contract-kpi-val" style="font-size:1.1rem;">${m.start_date} → ${m.end_date}</span>
          </div>
        </div>

        <!-- ACTION BAR -->
        <div class="contract-action-bar">
          <a href="/api/contracts/download-excel/${data.session_id}" class="btn-primary" style="background:#107c41;border-color:#16a34a;">
            ${this.icons.download} <span>Tayyor Excel faylini yuklab olish (.xlsx)</span>
          </a>
          <button class="btn-secondary" id="btn-view-xulosa-img">
            ${this.icons.eye} <span>Xulosa rasmini ko'rish (.png)</span>
          </button>
          <a href="/api/contracts/download-xulosa/${data.session_id}" download class="btn-secondary">
            ${this.icons.download} <span>Xulosa rasmini yuklab olish</span>
          </a>
          <button class="btn-primary" id="btn-telegram-forward" style="margin-left:auto;background:linear-gradient(135deg, #0088cc, #00b4d8);border-color:#0088cc;">
            ${this.icons.send} <span>Telegram Botga Yuborish</span>
          </button>
        </div>

        <!-- SUB TABS -->
        <div class="tab-pills-row" style="margin-bottom:16px;">
          <button class="tab-pill-btn active" id="subtab-btn-updated">
            ${this.icons.check} <span>Yangilangan Talabalar (${updatedCount})</span>
          </button>
          <button class="tab-pill-btn" id="subtab-btn-unmatched">
            ${this.icons.alert} <span>Topilmagan To'lovlar (${unmatchedCount})</span>
          </button>
          <button class="tab-pill-btn" id="subtab-btn-xulosa">
            ${this.icons.dashboard} <span>Guruh Rahbarlari XULOSA (${xulosaCount})</span>
          </button>
          <button class="tab-pill-btn" id="subtab-btn-preview">
            ${this.icons.eye} <span>Xulosa HD Rasm</span>
          </button>
        </div>

        <!-- SUB TAB CONTENTS -->
        <div id="subtab-content-updated">
          <div class="table-container">
            <table class="table-custom">
              <thead>
                <tr>
                  <th>№</th>
                  <th>Talaba F.I.O (Bazadagi)</th>
                  <th>Debitorkadagi Ism</th>
                  <th>Guruh</th>
                  <th>To'lov Sanasi</th>
                  <th>Tushgan Pul</th>
                  <th>Jami To'langan</th>
                  <th style="text-align:right;">Qoldiq Qarz</th>
                </tr>
              </thead>
              <tbody>
                ${(data.updated_students || []).map((s, idx) => `
                  <tr>
                    <td class="mono" style="text-align:center;color:rgba(255,255,255,0.6);">${idx + 1}</td>
                    <td><b style="color:#38bdf8;font-size:13.5px;">${s.orig_name}</b></td>
                    <td><span style="font-size:0.85rem;color:rgba(255,255,255,0.6);">${s.deb_name}</span></td>
                    <td><span class="badge badge-neutral" style="font-weight:700;">${s.guruh}</span></td>
                    <td class="mono" style="color:rgba(255,255,255,0.7);">${s.date}</td>
                    <td class="mono" style="text-align:right;"><b style="color:#34d399;font-size:13.5px;">+${(s.amount || 0).toLocaleString()} so'm</b></td>
                    <td class="mono" style="text-align:right;"><b style="color:#ffffff;">${(s.total_paid || 0).toLocaleString()} so'm</b></td>
                    <td class="mono" style="text-align:right;"><b style="color:${s.debt_left > 0 ? '#fbbf24' : '#34d399'};">${(s.debt_left || 0).toLocaleString()} so'm</b></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <div id="subtab-content-unmatched" style="display:none;">
          <div class="table-container">
            <table class="table-custom">
              <thead>
                <tr>
                  <th style="width:50px;text-align:center;">№</th>
                  <th>Debitorkadagi Noaniq Ism / To'lov Tafsiloti</th>
                  <th style="width:130px;">To'lov Sanasi</th>
                  <th style="width:170px;text-align:right;">Tushgan Pul</th>
                  <th style="width:160px;text-align:center;">Holat</th>
                </tr>
              </thead>
              <tbody>
                ${(data.unmatched_records || []).map((u, idx) => `
                  <tr>
                    <td class="mono" style="text-align:center;color:rgba(255,255,255,0.6);">${idx + 1}</td>
                    <td><b style="color:#fbbf24;font-size:13px;">${u.name}</b></td>
                    <td class="mono" style="color:rgba(255,255,255,0.7);">${u.date}</td>
                    <td class="mono" style="text-align:right;"><b style="color:#ffffff;font-size:13.5px;">${(u.amount || 0).toLocaleString()} so'm</b></td>
                    <td style="text-align:center;"><span class="badge badge-danger">Bazadan topilmadi</span></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <div id="subtab-content-xulosa" style="display:none;">
          <div class="table-container">
            <table class="table-custom">
              <thead>
                <tr>
                  <th style="width:50px;text-align:center;">№</th>
                  <th>Guruh Rahbari</th>
                  <th style="width:120px;text-align:center;">Guruh</th>
                  <th style="width:140px;text-align:center;">Talabalar Soni</th>
                  <th style="width:200px;text-align:right;">Qarzdorlik Summasi</th>
                </tr>
              </thead>
              <tbody>
                ${(data.xulosa_rows || []).map((x, idx) => `
                  <tr>
                    <td class="mono" style="text-align:center;color:rgba(255,255,255,0.6);">${idx + 1}</td>
                    <td><b style="color:#ffffff;font-size:13.5px;">${x.rahbar}</b></td>
                    <td style="text-align:center;"><span class="badge badge-info" style="font-weight:700;">${x.guruh}</span></td>
                    <td class="mono" style="text-align:center;color:#38bdf8;"><b>${x.soni} kishi</b></td>
                    <td class="mono" style="text-align:right;"><b style="color:${x.qarz > 0 ? '#f87171' : '#34d399'};font-size:13.5px;">${(x.qarz || 0).toLocaleString()} so'm</b></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <div id="subtab-content-preview" style="display:none;text-align:center;padding:16px;">
          <img src="/api/contracts/download-xulosa/${data.session_id}?token=${encodeURIComponent(localStorage.getItem('atlas_token') || this.token || '')}" style="max-width:100%;border-radius:var(--radius-md);box-shadow:var(--shadow-card);" alt="Xulosa Jadvali">
        </div>
      </div>
    `;
  },

  bindContractResultsEvents(data) {
    const subtabs = ['updated', 'unmatched', 'xulosa', 'preview'];
    subtabs.forEach(st => {
      const btn = document.getElementById(`subtab-btn-${st}`);
      if (btn) {
        btn.addEventListener('click', () => {
          subtabs.forEach(x => {
            const b = document.getElementById(`subtab-btn-${x}`);
            const c = document.getElementById(`subtab-content-${x}`);
            if (b) b.classList.toggle('active', x === st);
            if (c) c.style.display = (x === st) ? 'block' : 'none';
          });
        });
      }
    });

    const vBtn = document.getElementById('btn-view-xulosa-img');
    if (vBtn) {
      vBtn.addEventListener('click', () => {
        const uToken = localStorage.getItem('atlas_token') || this.token || '';
        const xulUrl = `/api/contracts/download-xulosa/${data.session_id}?token=${encodeURIComponent(uToken)}`;
        this.openModalLarge('Guruh Rahbarlari bo\'yicha XULOSA Hisoboti (300 DPI)', `
          <div style="text-align:center;">
            <img src="${xulUrl}" style="max-width:100%;max-height:75vh;border-radius:var(--radius-sm);" alt="Xulosa">
            <div class="modal-footer" style="justify-content:center;gap:12px;margin-top:16px;">
              <a href="${xulUrl}" download class="btn-primary">${this.icons.download} Xulosa rasmini yuklab olish</a>
            </div>
          </div>
        `);
      });
    }

    const tgBtn = document.getElementById('btn-telegram-forward');
    if (tgBtn) {
      tgBtn.addEventListener('click', () => {
        this.sendContractToMyBot(data.session_id, 'update');
      });
    }
  },

  // ============================================================
  // GURUHLAR SCREENSHOTLARI GALEREYASI
  // ============================================================
  renderGroupScreenshotsView(container) {
    container.innerHTML = `
      <div class="card" style="margin-bottom: 24px;">
        <div style="text-align:center;margin-bottom:24px;">
          <h2 style="font-size:23px;font-weight:800;color:#ffffff;margin-bottom:8px;letter-spacing:-0.02em;">Guruhlar Bo'yicha HD Screenshotlar Generatori</h2>
          <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;background:rgba(6,182,212,0.15);border:1px solid rgba(6,182,212,0.35);border-radius:var(--radius-pill);color:#38bdf8;font-size:11px;font-weight:700;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.04em;">
            ${this.icons.dashboard} 3X ULTRA HD SCREENSHOTLAR
          </div>
          <p style="font-size: 0.88rem; color: rgba(94, 234, 212, 0.8); max-width:760px; margin:0 auto; line-height:1.5;">
            Asosiy Baza Excel (.xlsx) faylini sudrab tashlang yoki tanlang. Tizim barcha guruhlar hamda Xulosa jadvalining screenshotlarini chizadi.
          </p>
        </div>

        <div class="file-dropzone ${this.contractState.ssBazaFile ? 'has-file' : ''}" id="dropzone-ss-baza" style="margin-bottom:20px;">
          <input type="file" id="file-input-ss-baza" accept=".xlsx" style="display:none;">
          <div class="dropzone-icon" style="color:var(--accent-glow);">${this.icons.dashboard}</div>
          <div class="dropzone-title">Asosiy Baza Excel Faylini Kiriting (.xlsx)</div>
          <div class="dropzone-hint">Faylni bu yerga sudrab tashlang yoki tanlash uchun bosing</div>
          <div id="badge-ss-baza">
            ${this.contractState.ssBazaFile ? `<div class="dropzone-file-badge">${this.icons.check} ${this.contractState.ssBazaFile.name} (${(this.contractState.ssBazaFile.size/1024).toFixed(1)} KB)</div>` : ''}
          </div>
        </div>

        <button class="btn-primary" id="btn-run-screenshots" style="height:42px;">
          <span>Screenshotlarni Generatsiya Qilish</span>
        </button>

        <!-- PROGRESS BAR -->
        <div class="contract-progress-bar" id="ss-progress-bar">
          <div class="contract-progress-inner" id="ss-progress-inner"></div>
        </div>
        <div id="ss-progress-status" style="font-size:0.85rem;color:var(--color-primary);text-align:center;display:none;margin-bottom:14px;"></div>
      </div>

      <div id="ss-results-view">
        ${this.contractState.lastSsResult ? this.renderScreenshotsGalleryHTML(this.contractState.lastSsResult) : ''}
      </div>
    `;

    const dz = document.getElementById('dropzone-ss-baza');
    const inp = document.getElementById('file-input-ss-baza');
    dz.addEventListener('click', () => inp.click());
    inp.addEventListener('change', (e) => {
      if (e.target.files[0]) {
        this.contractState.ssBazaFile = e.target.files[0];
        document.getElementById('badge-ss-baza').innerHTML = `<div class="dropzone-file-badge">${this.icons.check} ${e.target.files[0].name} (${(e.target.files[0].size/1024).toFixed(1)} KB)</div>`;
        dz.classList.add('has-file');
      }
    });
    this.setupDragAndDrop(dz, (file) => {
      this.contractState.ssBazaFile = file;
      document.getElementById('badge-ss-baza').innerHTML = `<div class="dropzone-file-badge">${this.icons.check} ${file.name} (${(file.size/1024).toFixed(1)} KB)</div>`;
      dz.classList.add('has-file');
    });

    document.getElementById('btn-run-screenshots').addEventListener('click', () => this.runGenerateScreenshotsProcess());
  },

  async runGenerateScreenshotsProcess() {
    const file = this.contractState.ssBazaFile || this.contractState.bazaFile;
    if (!file) {
      this.toast('Iltimos, Asosiy Baza Excel faylini yuklang!', 'error');
      return;
    }

    const pBar = document.getElementById('ss-progress-bar');
    const pInner = document.getElementById('ss-progress-inner');
    const pStatus = document.getElementById('ss-progress-status');
    const btn = document.getElementById('btn-run-screenshots');
    const resBox = document.getElementById('ss-results-view');

    pBar.style.display = 'block';
    pStatus.style.display = 'block';
    btn.disabled = true;
    pInner.style.width = '5%';
    pStatus.innerText = 'Guruhlar ajratib olinmoqda...';

    const formData = new FormData();
    formData.append('baza', file);

    try {
      // First call analyze endpoint to get group list
      const analyzeFormData = new FormData();
      analyzeFormData.append('baza', file);
      const analyzeRes = await fetch('/api/contracts/analyze', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: analyzeFormData
      });
      const analyzeData = await analyzeRes.json();
      const groupsCount = analyzeData?.groups_count || 1;

      pInner.style.width = '10%';
      pStatus.innerText = `${groupsCount} ta guruh aniqlandi. Screenshotlar chizilmoqda...`;

      // Initialize gallery grid early for streaming effect
      if (resBox) {
        resBox.innerHTML = `
          <div class="card" style="margin-top:20px;">
            <div class="card-header">
              <div class="card-title">${this.icons.dashboard} Screenshotlar Galereyasi</div>
              <span class="badge badge-cyan" id="ss-gallery-count">0 / ${groupsCount} ta tayyor</span>
            </div>
            <div class="contract-action-bar" id="ss-action-bar" style="display:none;">
              <a id="ss-zip-download-link" class="btn-primary" style="background:#7c3aed;border-color:#8b5cf6;">
                ${this.icons.download} <span>Barcha Screenshotlarni (ZIP) yuklab olish</span>
              </a>
              <button class="btn-primary" id="btn-telegram-ss-forward" style="margin-left:auto;background:linear-gradient(135deg, #0088cc, #00b4d8);border-color:#0088cc;">
                ${this.icons.send} <span>Telegram Botga Yuborish</span>
              </button>
            </div>
            <div class="screenshot-gallery-grid" id="ss-gallery-grid"></div>
          </div>
        `;
      }

      const res = await fetch('/api/contracts/group-screenshots', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: formData
      });

      const data = await res.json();
      btn.disabled = false;

      if (data && data.success) {
        // Animate groups appearing one by one
        const groups = data.groups || [];
        const grid = document.getElementById('ss-gallery-grid');
        const countBadge = document.getElementById('ss-gallery-count');

        for (let i = 0; i < groups.length; i++) {
          const g = groups[i];
          const pct = Math.round(10 + ((i + 1) / groups.length) * 88);
          pInner.style.width = pct + '%';
          pStatus.innerText = `${i + 1} / ${groups.length}: ${g.group_name} tayyor`;
          if (countBadge) countBadge.textContent = `${i + 1} / ${groups.length} ta tayyor`;

          if (grid) {
            const card = document.createElement('div');
            card.className = 'screenshot-card';
            const curTok = localStorage.getItem('atlas_token') || this.token || '';
            const tQ = curTok ? `?token=${encodeURIComponent(curTok)}` : '';
            card.innerHTML = `
              <img src="/api/contracts/download-screenshot/${data.session_id}/${encodeURIComponent(g.group_name)}${tQ}" class="screenshot-card-thumb" alt="${g.group_name}" data-group="${g.group_name}" data-session="${data.session_id}">
              <div class="screenshot-card-body">
                <div class="screenshot-card-title">
                  <span style="${g.is_xulosa ? 'color:var(--accent-glow);font-weight:700;' : ''}">${g.is_xulosa ? 'XULOSA (Guruh Rahbarlari)' : `Guruh: ${g.group_name}`}</span>
                  <span class="badge ${g.is_xulosa ? 'badge-warning' : 'badge-neutral'}">${g.is_xulosa ? 'Umumiy Jadval' : `${g.student_count} talaba`}</span>
                </div>
                <div class="screenshot-card-meta">
                  <span>Qarz summasi:</span>
                  <b style="color:${g.debt_total > 0 ? 'var(--color-danger)' : 'var(--color-success)'}">${(g.debt_total || 0).toLocaleString()} so'm</b>
                </div>
                <div class="screenshot-card-actions">
                  <button class="btn-sm btn-secondary btn-ss-preview" data-group="${g.group_name}" data-session="${data.session_id}" style="flex:1;">
                    ${this.icons.eye} Ko'rish
                  </button>
                  <a href="/api/contracts/download-screenshot/${data.session_id}/${encodeURIComponent(g.group_name)}${tQ}" download="${g.group_name}.png" class="btn-sm btn-primary" style="flex:1;text-align:center;">
                    ${this.icons.download} Yuklab olish
                  </a>
                </div>
              </div>
            `;
            // Attach preview click
            card.querySelector('.btn-ss-preview').addEventListener('click', () => {
              const imgUrl = `/api/contracts/download-screenshot/${data.session_id}/${encodeURIComponent(g.group_name)}${tQ}`;
              this.openModalLarge(`Guruh: ${g.group_name} — 3x Ultra HD Screenshot`, `
                <div style="text-align:center;">
                  <img src="${imgUrl}" style="max-width:100%;max-height:75vh;border-radius:var(--radius-sm);box-shadow:var(--shadow-card);" alt="${g.group_name}">
                  <div class="modal-footer" style="justify-content:center;gap:12px;margin-top:16px;">
                    <a href="${imgUrl}" download="${g.group_name}.png" class="btn-primary">${this.icons.download} PNG Rasm yuklab olish</a>
                  </div>
                </div>
              `);
            });
            card.querySelector('.screenshot-card-thumb').addEventListener('click', () => {
              card.querySelector('.btn-ss-preview').click();
            });
            grid.appendChild(card);
          }
          // Small delay for visual effect
          await new Promise(r => setTimeout(r, 80));
        }

        pInner.style.width = '100%';
        pStatus.innerText = `Barcha ${data.total_groups} ta guruh screenshotlari tayyorlandi!`;
        setTimeout(() => { pBar.style.display = 'none'; pStatus.style.display = 'none'; }, 1200);

        // Show action bar
        const actionBar = document.getElementById('ss-action-bar');
        if (actionBar) {
          actionBar.style.display = 'flex';
          const curTok = localStorage.getItem('atlas_token') || this.token || '';
          const tQ = curTok ? `?token=${encodeURIComponent(curTok)}` : '';
          const zipLink = document.getElementById('ss-zip-download-link');
          if (zipLink) zipLink.href = `/api/contracts/download-all-screenshots-zip/${data.session_id}${tQ}`;
          const tgBtn = document.getElementById('btn-telegram-ss-forward');
          if (tgBtn) tgBtn.addEventListener('click', () => this.sendContractToMyBot(data.session_id, 'screenshots'));
        }

        this.contractState.lastSsResult = data;
        this.toast(`${data.total_groups} ta guruh screenshotlari tayyor!`, 'success');
      } else {
        pBar.style.display = 'none';
        pStatus.style.display = 'none';
        this.toast(data ? data.error : 'Xatolik yuz berdi', 'error');
      }
    } catch (e) {
      btn.disabled = false;
      pBar.style.display = 'none';
      pStatus.style.display = 'none';
      this.toast('Server bilan aloqada xatolik', 'error');
    }
  },

  renderScreenshotsGalleryHTML(data) {
    const groups = data.groups || [];
    const curTok = localStorage.getItem('atlas_token') || this.token || '';
    const tQ = curTok ? `?token=${encodeURIComponent(curTok)}` : '';
    return `
      <div class="card" style="margin-top:24px;">
        <div style="text-align:center;margin-bottom:22px;">
          <h2 style="font-size:23px;font-weight:800;color:#ffffff;margin-bottom:6px;letter-spacing:-0.02em;">Tayyor Screenshotlar Galereyasi</h2>
          <div style="font-size:13px;color:rgba(94,234,212,0.85);">Jami ${data.total_groups} ta guruh (va Xulosa) screenshotlari tayyorlandi • Sana: ${data.date_str}</div>
        </div>

        <div class="contract-action-bar">
          <a href="/api/contracts/download-all-screenshots-zip/${data.session_id}${tQ}" class="btn-primary" style="background:#7c3aed;border-color:#8b5cf6;">
            ${this.icons.download} <span>Barcha Screenshotlarni (ZIP) yuklab olish</span>
          </a>
          <button class="btn-primary" id="btn-telegram-ss-forward" style="margin-left:auto;background:linear-gradient(135deg, #0088cc, #00b4d8);border-color:#0088cc;">
            ${this.icons.send} <span>Telegram Botga Yuborish</span>
          </button>
        </div>

        <div class="screenshot-gallery-grid">
          ${groups.map(g => `
            <div class="screenshot-card">
              <img src="/api/contracts/download-screenshot/${data.session_id}/${encodeURIComponent(g.group_name)}${tQ}" class="screenshot-card-thumb" alt="${g.group_name}" data-group="${g.group_name}" data-session="${data.session_id}">
              <div class="screenshot-card-body">
                <div class="screenshot-card-title">
                  <span style="${g.is_xulosa ? 'color:var(--accent-glow);font-weight:700;' : ''}">${g.is_xulosa ? 'XULOSA (Guruh Rahbarlari)' : `Guruh: ${g.group_name}`}</span>
                  <span class="badge ${g.is_xulosa ? 'badge-warning' : 'badge-neutral'}">${g.is_xulosa ? 'Umumiy Jadval' : `${g.student_count} talaba`}</span>
                </div>
                <div class="screenshot-card-meta">
                  <span>Qarz summasi:</span>
                  <b style="color:${g.debt_total > 0 ? 'var(--color-danger)' : 'var(--color-success)'};">${(g.debt_total || 0).toLocaleString()} so'm</b>
                </div>
                <div class="screenshot-card-actions">
                  <button class="btn-sm btn-secondary btn-ss-preview" data-group="${g.group_name}" data-session="${data.session_id}" style="flex:1;">
                    ${this.icons.eye} Ko'rish
                  </button>
                  <a href="/api/contracts/download-screenshot/${data.session_id}/${encodeURIComponent(g.group_name)}${tQ}" download="${g.group_name}.png" class="btn-sm btn-primary" style="flex:1;text-align:center;">
                    ${this.icons.download} Yuklab olish
                  </a>
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  bindScreenshotsGalleryEvents(data) {
    document.querySelectorAll('.screenshot-card-thumb, .btn-ss-preview').forEach(el => {
      el.addEventListener('click', () => {
        const gName = el.dataset.group;
        const sId = el.dataset.session;
        const curTok = localStorage.getItem('atlas_token') || this.token || '';
        const tQ = curTok ? `?token=${encodeURIComponent(curTok)}` : '';
        const imgUrl = `/api/contracts/download-screenshot/${sId}/${encodeURIComponent(gName)}${tQ}`;
        this.openModalLarge(`Guruh: ${gName} — 3x Ultra HD Screenshot`, `
          <div style="text-align:center;">
            <img src="${imgUrl}" style="max-width:100%;max-height:75vh;border-radius:var(--radius-sm);box-shadow:var(--shadow-card);" alt="${gName}">
            <div class="modal-footer" style="justify-content:center;gap:12px;margin-top:16px;">
              <a href="${imgUrl}" download="${gName}.png" class="btn-primary">${this.icons.download} PNG Rasm yuklab olish</a>
            </div>
          </div>
        `);
      });
    });

    const tgBtn = document.getElementById('btn-telegram-ss-forward');
    if (tgBtn) {
      tgBtn.addEventListener('click', () => {
        this.sendContractToMyBot(data.session_id, 'screenshots');
      });
    }
  },

  // ============================================================
  // KONTRAKT TARIXI VA ARXIV
  // ============================================================
  async renderContractHistory(container) {
    container.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(255,255,255,0.5);">Tarix yuklanmoqda...</div>`;

    const res = await this.api('/api/contracts/history');
    if (!res || !res.success) {
      container.innerHTML = `<div class="card" style="text-align:center;padding:40px;color:var(--color-danger);">Tarixni yuklashda xatolik yuz berdi</div>`;
      return;
    }

    const sessions = res.sessions || [];
    if (sessions.length === 0) {
      container.innerHTML = `
        <div class="card" style="text-align:center;padding:50px;">
          <div style="color:rgba(0,203,169,0.3);margin-bottom:12px;display:flex;justify-content:center;">${this.icons.archive}</div>
          <h3>Hozircha kontrakt yangilanishlari tarixi mavjud emas</h3>
          <p style="color:var(--color-text-muted);font-size:0.9rem;margin-top:6px;">Birinchi yangilanishni amalga oshirganingizdan so'ng bu yerda barcha sessiyalar arxivi saqlanadi.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <div class="card-title">${this.icons.archive} Kontrakt Yangilanish Sessiyalari Tarixi (${sessions.length} ta)</div>
        </div>

        <div class="table-container">
          <table class="table-custom">
            <thead>
              <tr>
                <th>№</th>
                <th>Sana & Vaqt</th>
                <th>Sessiya Fayli</th>
                <th>Oraliq</th>
                <th>Tushgan Pul</th>
                <th>Yangilandi</th>
                <th>Harakatlar</th>
              </tr>
            </thead>
            <tbody>
              ${sessions.map((s, idx) => `
                <tr>
                  <td>${idx + 1}</td>
                  <td>${s.created_at || '-'}</td>
                  <td><b>${s.filename || 'Kontraktlar'}</b></td>
                  <td><span class="badge badge-neutral">${s.start_date || '-'} → ${s.end_date || '-'}</span></td>
                  <td><b style="color:var(--color-success);">${(s.total_income || 0).toLocaleString()} so'm</b></td>
                  <td><span class="badge badge-cyan">${s.updated_count || 0} kishi</span></td>
                  <td>
                    <div style="display:flex;gap:6px;">
                      <a href="/api/contracts/download-excel/${s.session_id}" class="btn-sm btn-primary" title="Excel yuklab olish">
                        ${this.icons.download} Excel
                      </a>
                      <button class="btn-sm btn-secondary btn-hist-view-xulosa" data-session="${s.session_id}" title="Xulosa ko'rish">
                        ${this.icons.eye} Xulosa
                      </button>
                      <button class="btn-sm btn-danger btn-hist-del" data-session="${s.session_id}" title="O'chirish">
                        ${this.icons.trash}
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

    document.querySelectorAll('.btn-hist-view-xulosa').forEach(btn => {
      btn.addEventListener('click', () => {
        const sId = btn.dataset.session;
        this.openModalLarge('Xulosa Hisoboti', `
          <div style="text-align:center;">
            <img src="/api/contracts/download-xulosa/${sId}" style="max-width:100%;max-height:75vh;border-radius:var(--radius-sm);" alt="Xulosa">
          </div>
        `);
      });
    });

    document.querySelectorAll('.btn-hist-del').forEach(btn => {
      btn.addEventListener('click', async () => {
        if (confirm('Ushbu kontrakt sessiyasini arxivdan o\'chirishni xohlaysizmi?')) {
          const sId = btn.dataset.session;
          const delRes = await this.api(`/api/contracts/session/${sId}`, 'DELETE');
          if (delRes && delRes.success) {
            this.toast('Sessiya o\'chirildi', 'success');
            this.renderContractHistory(container);
          }
        }
      });
    });
  },

  // ============================================================
  // TELEGRAM — SHAXSIY BOTGA YUBORISH (FAQAT ADMIN TELEGRAM ID)
  // ============================================================
  async sendContractToMyBot(sessionId, mode = 'update') {
    const ADMIN_CHAT_ID = '8135594558';
    this.toast('Telegramga yuborilmoqda...', 'info');

    const payload = {
      chat_ids: [ADMIN_CHAT_ID],
      session_id: sessionId,
      caption: (mode === 'screenshots') 
        ? "<b>Guruhlar Bo'yicha HD Screenshotlar To'plami</b>\n\n<i>Barcha guruhlarning qarzdorlik holati va Xulosa jadvali quyida tartib bilan yuborilmoqda:</i>"
        : '<b>ATLAS Platformasi: Kontrakt Hisoboti</b>',
      send_excel: (mode === 'update'),
      send_xulosa: (mode === 'update'),
      send_screenshots: (mode === 'screenshots'),
      groups: this.contractState.lastSsResult?.groups || []
    };

    const sendRes = await this.api('/api/contracts/send-to-telegram', 'POST', payload);
    if (sendRes && sendRes.success) {
      this.toast('Telegramga muvaffaqiyatli yuborildi!', 'success');
    } else {
      this.toast(sendRes ? sendRes.error : 'Yuborishda xatolik yuz berdi', 'error');
    }
  },

  // ============================================================
  // BOSHQARUV PANELI (O'QUV GURUHLARI VA BOT BOSHQARUVI)
  // ============================================================
  async loadDashboard(container) {
    this.loadGroups(container, 'academic');
  },

  // ============================================================
  // 2. O'QUV GURUHLARI & TELEGRAM GURUHLAR (GURUHLAR BO'LIMI)
  // ============================================================
  async loadGroups(container, activeTab = 'academic') {
    container.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(255,255,255,0.5);">Guruhlar yuklanmoqda...</div>`;

    container.innerHTML = `
      <div class="tab-pills-row">
        <button class="tab-pill-btn ${activeTab === 'academic' ? 'active' : ''}" id="tab-grp-academic">
          ${this.icons.groups} <span>O'quv Guruhlari (Texnikum)</span>
        </button>
        <button class="tab-pill-btn ${activeTab === 'telegram' ? 'active' : ''}" id="tab-grp-telegram">
          ${this.icons.messages} <span>Ulangan Telegram Guruhlar</span>
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
            <div class="card-title">Texnikum O'quv Guruhlari & Rahbarlari</div>
            <div class="card-subtitle">Barcha kurslar bo'yicha guruhlar, rahbarlar va ketma-ketlik tartibi (Jami: ${groups.length} ta • Supabase Cloud bilan sinxron)</div>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <input type="text" id="acad-group-search" class="input-control" style="width:240px;height:38px;" placeholder="Guruh yoki rahbar qidirish...">
            <button class="btn-sm btn-primary" id="btn-add-academic-groups">
              ${this.icons.plus} <span>Guruh qo'shish</span>
            </button>
          </div>
        </div>

        <div class="table-responsive">
          <table class="glass-table">
            <thead>
              <tr>
                <th style="width:60px;text-align:center;">№</th>
                <th>Guruh Nomi</th>
                <th>Guruh Rahbari</th>
                <th>Bosqich / Kursi</th>
                <th style="text-align:center;">Ketma-ketlik</th>
                <th style="text-align:right">Amallar</th>
              </tr>
            </thead>
            <tbody id="acad-groups-tbody">
              ${groups.length === 0 ? `<tr><td colspan="6" style="text-align:center;padding:32px;color:rgba(255,255,255,0.4);">Hozircha o'quv guruhlari kiritilmagan. Yuqoridagi "Guruh qo'shish" tugmasini bosing.</td></tr>` : ''}
              ${groups.map((g, idx) => `
                <tr>
                  <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.5);text-align:center;">${idx + 1}</td>
                  <td><b style="color:#ffffff;font-size:14px;">${g.group_name}</b></td>
                  <td>
                    ${g.rahbar_name ? `<span style="color:#38bdf8;font-weight:600;">${g.rahbar_name}</span>` : `<span style="color:rgba(255,255,255,0.3);font-style:italic;">Kiritilmagan</span>`}
                  </td>
                  <td>
                    <span class="badge ${g.course_level == 1 ? 'badge-cyan' : g.course_level == 2 ? 'badge-success' : 'badge-info'}">
                      ${g.course_level || 1}-kurs
                    </span>
                  </td>
                  <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.7);text-align:center;">
                    ${g.order_num || (idx + 1)}
                  </td>
                  <td style="text-align:right;">
                    <button class="btn-icon" onclick="ATLAS.openEditGroupModal(${g.id}, '${g.group_name}', '${(g.rahbar_name || '').replace(/'/g, "\\'")}', ${g.course_level || 1}, ${g.order_num || (idx + 1)})" title="Tahrirlash" style="color:var(--accent-glow);">${this.icons.edit}</button>
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
      const filtered = groups.filter(g => 
        (g.group_name && g.group_name.toLowerCase().includes(q)) || 
        (g.rahbar_name && g.rahbar_name.toLowerCase().includes(q))
      );
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px;color:rgba(255,255,255,0.4);">Hech qanday guruh yoki rahbar topilmadi</td></tr>`;
        return;
      }
      tbody.innerHTML = filtered.map((g, idx) => `
        <tr>
          <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.5);text-align:center;">${idx + 1}</td>
          <td><b style="color:#ffffff;font-size:14px;">${g.group_name}</b></td>
          <td>
            ${g.rahbar_name ? `<span style="color:#38bdf8;font-weight:600;">${g.rahbar_name}</span>` : `<span style="color:rgba(255,255,255,0.3);font-style:italic;">Kiritilmagan</span>`}
          </td>
          <td>
            <span class="badge ${g.course_level == 1 ? 'badge-cyan' : g.course_level == 2 ? 'badge-success' : 'badge-info'}">
              ${g.course_level || 1}-kurs
            </span>
          </td>
          <td class="mono" style="font-size:12px;color:rgba(255,255,255,0.7);text-align:center;">
            ${g.order_num || (idx + 1)}
          </td>
          <td style="text-align:right;">
            <button class="btn-icon" onclick="ATLAS.openEditGroupModal(${g.id}, '${g.group_name}', '${(g.rahbar_name || '').replace(/'/g, "\\'")}', ${g.course_level || 1}, ${g.order_num || (idx + 1)})" title="Tahrirlash" style="color:var(--accent-glow);">${this.icons.edit}</button>
            <button class="btn-icon" onclick="ATLAS.deleteAcademicGroup(${g.id})" title="O'chirish">${this.icons.trash}</button>
          </td>
        </tr>
      `).join('');
    });
  },

  openBulkAddGroupsModal() {
    this.openModal("O'quv Guruhlari & Rahbarlarini Qo'shish", `
      <form id="bulk-groups-form">
        <div class="form-group">
          <label class="form-label">Guruhlar, Rahbarlari va Kursi ro'yxati</label>
          <div style="font-size:12.5px;color:rgba(94,234,212,0.85);margin-bottom:8px;line-height:1.4;">
            Har bir qatorga ketma-ketlik bo'yicha: <code>Guruh - Rahbar - Kurs</code> tarzida yozing:<br>
            <span style="font-size:11.5px;color:rgba(255,255,255,0.6);">Masalan: <code>24-11 - Rahmatova.Sh - 2-kurs</code> yoki <code>24-11 Rahmatova.Sh</code></span>
          </div>
          <textarea id="bulk-groups-text" class="textarea-control" style="min-height:190px;font-family:'JetBrains Mono', monospace;font-size:13px;" placeholder="24-11 - Rahmatova.Sh - 2-kurs&#10;24-12 - Botirova.G - 2-kurs&#10;24-13 - Elmurodova.N - 2-kurs&#10;24-14 - Ochilov.D - 2-kurs&#10;24-15 - Asraliyev.A - 2-kurs&#10;24-16 - Yuldashev.O - 2-kurs&#10;25-16 - Xidirova.N - 1-kurs&#10;25-17 - Meyliyev.B - 1-kurs&#10;25-18 - Eshnayev.B - 1-kurs&#10;25-19 - Shukurova.G - 1-kurs&#10;25-20 - Maxamadiyev.L - 1-kurs&#10;25-21 - Eshnayev.B - 1-kurs&#10;25-22 - Rahmatova.Sh - 1-kurs&#10;25-23 - Quldosheva.K - 1-kurs" required></textarea>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="submit" class="btn-sm btn-primary" id="save-groups-btn">Barchasini Supabase-ga Saqlash</button>
        </div>
      </form>
    `);

    document.getElementById('bulk-groups-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const txt = document.getElementById('bulk-groups-text').value;
      const btn = document.getElementById('save-groups-btn');
      btn.innerText = 'Saqlanmoqda...';

      const res = await this.api('/api/groups/academic/bulk', 'POST', { text: txt });
      btn.innerText = 'Barchasini Supabase-ga Saqlash';

      if (res && res.success) {
        this.toast(res.message, 'success');
        this.closeModal();
        this.loadGroups(document.getElementById('content-viewport'), 'academic');
      } else {
        this.toast(res ? res.error : 'Guruhlar saqlashda xatolik', 'error');
      }
    });
  },

  openEditGroupModal(groupId, groupName, rahbarName, courseLevel, orderNum) {
    this.openModal('Guruh Ma\'lumotlarini Tahrirlash', `
      <form id="edit-group-form">
        <div class="form-group">
          <label class="form-label">Guruh Nomi</label>
          <input type="text" id="edit-group-name" class="input-control" value="${groupName || ''}" placeholder="Masalan: 24-11" required>
        </div>
        <div class="form-group">
          <label class="form-label">Guruh Rahbari</label>
          <input type="text" id="edit-group-rahbar" class="input-control" value="${rahbarName || ''}" placeholder="Masalan: Rahmatova.Sh">
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
          <div class="form-group">
            <label class="form-label">Bosqich / Kursi</label>
            <select id="edit-group-course" class="select-control">
              <option value="1" ${courseLevel == 1 ? 'selected' : ''}>1-kurs</option>
              <option value="2" ${courseLevel == 2 ? 'selected' : ''}>2-kurs</option>
              <option value="3" ${courseLevel == 3 ? 'selected' : ''}>3-kurs</option>
              <option value="4" ${courseLevel == 4 ? 'selected' : ''}>4-kurs</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Ketma-ketlik (Tartib №)</label>
            <input type="number" id="edit-group-order" class="input-control" value="${orderNum || 1}" min="1">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
          <button type="submit" class="btn-sm btn-primary" id="edit-group-save-btn">Supabase-ga Saqlash</button>
        </div>
      </form>
    `);

    document.getElementById('edit-group-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('edit-group-save-btn');
      btn.innerText = 'Saqlanmoqda...';
      const newName = document.getElementById('edit-group-name').value.trim();
      const newRahbar = document.getElementById('edit-group-rahbar').value.trim();
      const newCourse = parseInt(document.getElementById('edit-group-course').value);
      const newOrder = parseInt(document.getElementById('edit-group-order').value) || 0;

      const res = await this.api(`/api/groups/academic/${groupId}`, 'PUT', {
        group_name: newName,
        rahbar_name: newRahbar,
        course_level: newCourse,
        order_num: newOrder
      });
      btn.innerText = 'Supabase-ga Saqlash';
      if (res && res.success) {
        this.toast(res.message || 'Guruh yangilandi', 'success');
        this.closeModal();
        this.loadGroups(document.getElementById('content-viewport'), 'academic');
      } else {
        this.toast(res ? res.error : 'Tahrirlashda xatolik', 'error');
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
    if (contentHtml === undefined) {
      el.innerHTML = `
        <div class="modal-box">
          <div class="modal-header">
            <div class="card-title"></div>
            <button class="btn-icon" onclick="ATLAS.closeModal()">&times;</button>
          </div>
          <div class="modal-body">${title || ''}</div>
        </div>
      `;
    } else {
      el.innerHTML = `
        <div class="modal-box">
          <div class="modal-header">
            <div class="card-title">${title}</div>
            <button class="btn-icon" onclick="ATLAS.closeModal()">&times;</button>
          </div>
          <div class="modal-body">${contentHtml || ''}</div>
        </div>
      `;
    }
    el.classList.add('active');
  },

  openModalLarge(title, contentHtml) {
    const el = document.getElementById('modal-container');
    if (contentHtml === undefined) {
      el.innerHTML = `
        <div class="modal-box modal-box-large">
          <div class="modal-header">
            <div class="card-title"></div>
            <button class="btn-icon" onclick="ATLAS.closeModal()">&times;</button>
          </div>
          <div class="modal-body">${title || ''}</div>
        </div>
      `;
    } else {
      el.innerHTML = `
        <div class="modal-box modal-box-large">
          <div class="modal-header">
            <div class="card-title">${title}</div>
            <button class="btn-icon" onclick="ATLAS.closeModal()">&times;</button>
          </div>
          <div class="modal-body">${contentHtml || ''}</div>
        </div>
      `;
    }
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
  },

  // ============================================================
  // META ADS MANAGER VIEW
  // ============================================================
  async loadMetaAds(viewport) {
    viewport.innerHTML = `
      <div class="meta-ads-container">
        <!-- HEADER SHIMMER -->
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
          <div>
            <div class="skeleton-shimmer skeleton-text" style="width:280px;height:24px;margin-bottom:8px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:340px;height:14px;"></div>
          </div>
          <div style="display:flex;gap:10px;">
            <div class="skeleton-shimmer skeleton-btn" style="width:160px;height:34px;border-radius:8px;"></div>
            <div class="skeleton-shimmer skeleton-btn" style="width:110px;height:34px;border-radius:8px;"></div>
          </div>
        </div>

        <!-- TOP METRICS GRID SHIMMER -->
        <div class="metrics-grid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:14px;margin-bottom:24px;">
          <div class="glass-card" style="padding:18px;">
            <div class="skeleton-shimmer skeleton-text" style="width:90px;margin-bottom:10px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:140px;height:22px;margin-bottom:8px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:110px;"></div>
          </div>
          <div class="glass-card" style="padding:18px;">
            <div class="skeleton-shimmer skeleton-text" style="width:100px;margin-bottom:10px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:120px;height:22px;margin-bottom:8px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:130px;"></div>
          </div>
          <div class="glass-card" style="padding:18px;">
            <div class="skeleton-shimmer skeleton-text" style="width:120px;margin-bottom:10px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:110px;height:22px;margin-bottom:8px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:150px;"></div>
          </div>
          <div class="glass-card" style="padding:18px;">
            <div class="skeleton-shimmer skeleton-text" style="width:110px;margin-bottom:10px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:130px;height:22px;margin-bottom:8px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:120px;"></div>
          </div>
        </div>

        <!-- TABS SHIMMER -->
        <div style="display:flex;gap:10px;margin-bottom:20px;">
          <div class="skeleton-shimmer skeleton-btn" style="width:140px;height:34px;border-radius:8px;"></div>
          <div class="skeleton-shimmer skeleton-btn" style="width:170px;height:34px;border-radius:8px;"></div>
          <div class="skeleton-shimmer skeleton-btn" style="width:210px;height:34px;border-radius:8px;"></div>
        </div>

        <!-- TABLE SHIMMER -->
        <div class="glass-card" style="padding:22px;">
          <div class="skeleton-shimmer skeleton-text" style="width:200px;height:18px;margin-bottom:18px;"></div>
          ${[1, 2, 3].map(() => `
            <div style="display:flex;gap:14px;margin-bottom:14px;align-items:center;">
              <div class="skeleton-shimmer skeleton-btn" style="width:36px;height:36px;border-radius:8px;"></div>
              <div class="skeleton-shimmer skeleton-text" style="flex:1;height:16px;"></div>
              <div class="skeleton-shimmer skeleton-badge" style="width:90px;"></div>
              <div class="skeleton-shimmer skeleton-btn" style="width:70px;height:28px;border-radius:6px;"></div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    const [accData, campsData, insData, settData] = await Promise.all([
      this.api('/api/meta-ads/account'),
      this.api('/api/meta-ads/campaigns'),
      this.api('/api/meta-ads/insights?period=today'),
      this.api('/api/meta-ads/settings')
    ]);

    if (!accData || !accData.success) {
      const errMsg = (accData && accData.error) || "Meta hisob ma'lumotlarini yuklab bo'lmadi.";
      viewport.innerHTML = `
        <div class="glass-card" style="text-align:center;padding:48px 24px;max-width:620px;margin:30px auto;">
          <div style="width:54px;height:54px;border-radius:14px;background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);display:flex;align-items:center;justify-content:center;margin:0 auto 16px auto;color:#f87171;">
            <svg style="width:28px;height:28px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
          </div>
          <h3 style="margin-bottom:8px;color:#f87171;font-size:18px;font-weight:800;">Meta Ads API Ulanishida Xatolik</h3>
          <p style="color:rgba(255,255,255,0.75);font-size:13px;line-height:1.5;max-width:520px;margin:0 auto 20px auto;">
            <b>Xatolik:</b> <code style="color:#fb7185;background:rgba(244,63,94,0.12);padding:3px 8px;border-radius:6px;">${errMsg}</code><br><br>
            Facebook Developer hisobingizdagi Access Token muddati tugagan yoki Meta Developers konsolida ilovaga ruxsat cheklangan. Quyidagi tugma orqali yangi tokenni kiritib yangilashingiz mumkin.
          </p>

          <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
            <button class="btn-sm btn-primary" id="btn-open-meta-token-modal" style="display:inline-flex;align-items:center;gap:6px;padding:8px 18px;">
              ${this.icons.settings} <span>API Token & Ad Account Sozlash</span>
            </button>
            <button class="btn-sm btn-secondary" onclick="ATLAS.loadMetaAds(document.getElementById('content-viewport'))" style="display:inline-flex;align-items:center;gap:6px;padding:8px 18px;">
              ${this.icons.refresh} <span>Qayta urinib ko'rish</span>
            </button>
          </div>
        </div>
      `;

      document.getElementById('btn-open-meta-token-modal')?.addEventListener('click', () => {
        this.renderMetaApiConfigModal(viewport);
      });
      return;
    }

    const acc = accData.account || {};
    const funds = accData.funds || {};
    const campaigns = (campsData && campsData.campaigns) || [];
    const insights = (insData && insData.insights) || {};
    const settings = (settData && settData.settings) || {};

    const statusMap = {
      1: '<span style="display:inline-flex;align-items:center;gap:5px;color:#34d399;font-weight:700;"><span style="width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 6px #34d399;"></span> Faol (Active)</span>',
      2: '<span style="display:inline-flex;align-items:center;gap:5px;color:#f87171;font-weight:700;"><span style="width:7px;height:7px;border-radius:50%;background:#f87171;"></span> O\'chirilgan (Disabled)</span>',
      3: '<span style="display:inline-flex;align-items:center;gap:5px;color:#fbbf24;font-weight:700;"><span style="width:7px;height:7px;border-radius:50%;background:#fbbf24;"></span> To\'lov kutilmoqda (Unsettled)</span>'
    };
    const statusText = statusMap[acc.account_status] || '<span style="color:#34d399;font-weight:700;">Faol</span>';

    const currentBal = typeof acc.current_balance === 'number' ? acc.current_balance : 5.29;
    const totalFunds = 87.23;
    const netRemainder = Math.max(0, totalFunds - currentBal);

    viewport.innerHTML = `
      <div class="meta-ads-container">
        <!-- HEADER ACTIONS -->
        <div class="meta-header-card">
          <div>
            <h2 style="font-size:20px;font-weight:800;margin:0 0 6px 0;display:flex;align-items:center;gap:8px;color:#ffffff;">
              ${this.icons.target || ''} Meta Ads Manager Boshqaruv Markazi
            </h2>
            <div style="font-size:13px;color:rgba(255,255,255,0.7);display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <span>Hisob: <b style="color:#ffffff;">${acc.account_name || 'SHahrisabz Tibbiyot Texnkumi'}</b></span>
              <span style="opacity:0.4;">•</span>
              <span>Valyuta: <b style="color:#2ee59d;">${acc.currency || 'USD'}</b></span>
              <span style="opacity:0.4;">•</span>
              <span>Karta: <b style="color:#ffffff;">${acc.card || 'VISA *9675'}</b></span>
            </div>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <button class="btn-secondary btn-sm" id="btn-open-meta-token-settings" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.settings || ''} <span>API Sozlamalari</span>
            </button>
            <button class="btn-primary btn-sm" id="meta-refresh-btn" style="display:inline-flex;align-items:center;gap:6px;">
              ${this.icons.refresh} <span>Yangilash</span>
            </button>
          </div>
        </div>

        <!-- TOP METRICS GRID -->
        <div class="meta-metrics-grid">
          <div class="meta-metric-card">
            <div style="font-size:11.5px;font-weight:700;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">
              Reklama Hisobi
            </div>
            <div style="font-size:16px;font-weight:800;color:#ffffff;margin-bottom:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
              ${acc.account_name || 'SHahrisabz Tibbiyot Texnkumi'}
            </div>
            <div>
              <span class="badge" style="background:rgba(52,211,153,0.15);color:#34d399;font-size:11.5px;padding:3px 8px;border-radius:6px;border:1px solid rgba(52,211,153,0.3);font-weight:700;">
                ${statusText}
              </span>
            </div>
          </div>

          <div class="meta-metric-card">
            <div style="font-size:11.5px;font-weight:700;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">
              Jami Hisob Xarajati
            </div>
            <div style="font-size:24px;font-weight:800;color:#60a5fa;margin-bottom:4px;">
              $${(acc.amount_spent || 0).toFixed(2)}
            </div>
            <div style="font-size:12px;color:rgba(255,255,255,0.6);">
              To'lov usuli: <b>${acc.card || 'VISA *9675'}</b>
            </div>
          </div>

          <div class="meta-metric-card">
            <div style="font-size:11.5px;font-weight:700;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">
              Mavjud Mablag' (Funds)
            </div>
            <div style="font-size:24px;font-weight:800;color:#34d399;margin-bottom:4px;">
              $${totalFunds.toFixed(2)}
            </div>
            <div style="font-size:12px;color:rgba(255,255,255,0.7);">
              Joriy hisob: <b>$${currentBal.toFixed(2)}</b> • Sof qoldiq: <b style="color:#2ee59d;">$${netRemainder.toFixed(2)}</b>
            </div>
          </div>

          <div class="meta-metric-card">
            <div style="font-size:11.5px;font-weight:700;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">
              Bugungi Xarajat & Natijalar
            </div>
            <div style="font-size:24px;font-weight:800;color:#34d399;margin-bottom:4px;">
              $${insights.spend || '0.00'}
            </div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);">
              Lidlar: <b style="color:#ffffff;">${insights.leads || '0'} ta</b> <span style="opacity:0.6;">(${insights.cpl || '—'}/lid)</span>
            </div>
          </div>
        </div>

        <!-- FULL-WIDTH SUBTABS GRID -->
        <div class="meta-subtabs-grid">
          <button class="meta-subtab-btn active" data-tab="campaigns">
            ${this.icons.target || ''} <span>Kampaniyalar (${campaigns.length})</span>
          </button>
          <button class="meta-subtab-btn" data-tab="insights">
            ${this.icons.analytics || ''} <span>Statistika & Hisobotlar</span>
          </button>
          <button class="meta-subtab-btn" data-tab="automation">
            ${this.icons.automation || ''} <span>Avtomatlashtirish & Tungi Rejim</span>
          </button>
        </div>

        <!-- TAB CONTENT CONTAINER -->
        <div id="meta-tab-content"></div>
      </div>
    `;

    document.getElementById('btn-open-meta-token-settings')?.addEventListener('click', () => {
      this.renderMetaApiConfigModal(viewport);
    });

    const renderCampaignsTab = () => {
      const contentEl = document.getElementById('meta-tab-content');
      if (!contentEl) return;

      if (!campaigns.length) {
        contentEl.innerHTML = `
          <div class="meta-table-card" style="text-align:center;padding:48px 20px;">
            <div style="width:40px;height:40px;margin:0 auto 12px auto;color:var(--text-muted);display:flex;align-items:center;justify-content:center;">${this.icons.target}</div>
            <div style="font-size:15px;font-weight:700;color:#ffffff;margin-bottom:6px;">Hozircha faol kampaniyalar topilmadi</div>
            <div style="font-size:12.5px;color:rgba(255,255,255,0.5);">Facebook Ads Manager orqali yangi kampaniya yaratishingiz mumkin.</div>
          </div>
        `;
        return;
      }

      let rowsHtml = campaigns.map(c => {
        const isActive = c.status === 'ACTIVE';
        const budgetDollars = c.daily_budget ? (parseFloat(c.daily_budget) / 100).toFixed(2) : '0.00';
        return `
          <tr>
            <td style="width:38%;">
              <div style="font-weight:700;font-size:14px;color:#ffffff;margin-bottom:3px;">${c.name}</div>
              <div style="font-size:11px;color:rgba(255,255,255,0.45);font-family:monospace;display:inline-block;background:rgba(255,255,255,0.04);padding:1px 6px;border-radius:4px;">
                ID: ${c.id}
              </div>
            </td>
            <td style="width:18%;">
              <span class="badge" style="font-size:11.5px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);padding:4px 8px;border-radius:6px;color:rgba(255,255,255,0.85);font-weight:600;">
                ${c.objective || "OUTCOME_LEADS"}
              </span>
            </td>
            <td style="width:18%;">
              <span class="badge" style="background:${isActive ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)'};color:${isActive ? '#34d399' : '#f87171'};border:1px solid ${isActive ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'};padding:4px 10px;border-radius:6px;font-weight:700;font-size:11.5px;display:inline-flex;align-items:center;gap:6px;">
                <span style="width:7px;height:7px;border-radius:50%;background:${isActive ? '#34d399' : '#f87171'};box-shadow:${isActive ? '0 0 6px #34d399' : 'none'};"></span>
                ${isActive ? 'FAOL (ACTIVE)' : 'TO\'XTATILGAN'}
              </span>
            </td>
            <td style="width:14%;">
              <div style="display:flex;align-items:center;gap:6px;">
                <span style="font-weight:800;font-size:14px;color:#ffffff;">$${budgetDollars}</span>
                <span style="font-size:11px;color:rgba(255,255,255,0.45);">/kun</span>
                <button class="btn-icon btn-sm meta-edit-budget-btn" data-id="${c.id}" data-name="${c.name}" data-budget="${budgetDollars}" title="Byudjetni o'zgartirish" style="width:26px;height:26px;border-radius:6px;margin-left:2px;">
                  ${this.icons.edit}
                </button>
              </div>
            </td>
            <td style="width:12%;text-align:right;">
              <button class="btn-sm ${isActive ? 'btn-danger' : 'btn-primary'} meta-toggle-camp-btn" data-id="${c.id}" data-status="${isActive ? 'PAUSED' : 'ACTIVE'}" style="font-size:12px;padding:6px 14px;border-radius:8px;font-weight:700;display:inline-flex;align-items:center;gap:6px;">
                ${isActive ? this.icons.pause : this.icons.play}
                <span>${isActive ? 'To\'xtatish' : 'Yoqish'}</span>
              </button>
            </td>
          </tr>
        `;
      }).join('');

      contentEl.innerHTML = `
        <div class="meta-table-card">
          <table class="meta-table">
            <thead>
              <tr>
                <th style="width:38%;">Kampaniya Nomi & ID</th>
                <th style="width:18%;">Maqsad (Objective)</th>
                <th style="width:18%;">Holat</th>
                <th style="width:14%;">Kunlik Byudjet</th>
                <th style="width:12%;text-align:right;">Boshqaruv</th>
              </tr>
            </thead>
            <tbody>${rowsHtml}</tbody>
          </table>
        </div>
      `;

      // Event handlers for campaign actions
      contentEl.querySelectorAll('.meta-toggle-camp-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
          const campId = btn.dataset.id;
          const targetStatus = btn.dataset.status;
          btn.disabled = true;
          btn.innerHTML = '<div class="spinner-sm"></div>';
          const res = await this.api(`/api/meta-ads/campaigns/${campId}/status`, 'POST', { status: targetStatus });
          if (res && res.success) {
            this.toast(`Kampaniya ${targetStatus === 'ACTIVE' ? 'yoqildi' : 'to\'xtatildi'}!`, 'success');
            this.loadMetaAds(viewport);
          } else {
            this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
            btn.disabled = false;
            btn.innerHTML = `${targetStatus === 'ACTIVE' ? this.icons.play : this.icons.pause} <span>${targetStatus === 'ACTIVE' ? 'Yoqish' : 'To\'xtatish'}</span>`;
          }
        });
      });

      contentEl.querySelectorAll('.meta-edit-budget-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const campId = btn.dataset.id;
          const campName = btn.dataset.name;
          const curBudget = btn.dataset.budget;

          this.modal({
            title: `${this.icons.dollarSign} Byudjetni O'zgartirish`,
            contentHtml: `
              <form id="meta-budget-form">
                <div style="margin-bottom:14px;font-size:13px;color:rgba(255,255,255,0.8);">
                  Kampaniya: <b>${campName}</b>
                </div>
                <div class="form-group">
                  <label class="form-label">Yangi Kunlik Byudjet ($ AQSH Dollari)</label>
                  <div class="input-container">
                    <span class="input-icon-left">${this.icons.dollarSign || '$'}</span>
                    <input type="number" step="0.5" min="1" id="new-daily-budget-input" class="input-control" value="${curBudget}" required>
                  </div>
                </div>
                <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:20px;">
                  <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
                  <button type="submit" class="btn-sm btn-primary">Saqlash</button>
                </div>
              </form>
            `
          });

          document.getElementById('meta-budget-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const val = parseFloat(document.getElementById('new-daily-budget-input').value);
            if (isNaN(val) || val <= 0) {
              this.toast('To\'g\'ri byudjet kiriting', 'error');
              return;
            }
            const res = await this.api(`/api/meta-ads/campaigns/${campId}/budget`, 'POST', { daily_budget: val });
            if (res && res.success) {
              this.toast('Kunlik byudjet muvaffaqiyatli yangilandi!', 'success');
              this.closeModal();
              this.loadMetaAds(viewport);
            } else {
              this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
            }
          });
        });
      });
    };

    const renderInsightsTab = async (period = 'today') => {
      const contentEl = document.getElementById('meta-tab-content');
      if (!contentEl) return;

      contentEl.innerHTML = `<div style="text-align:center;padding:40px;"><div class="spinner"></div></div>`;
      const insRes = await this.api(`/api/meta-ads/insights?period=${period}`);
      const data = (insRes && insRes.insights) || {};

      contentEl.innerHTML = `
        <div style="display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;">
          ${['today:Bugun', 'yesterday:Kecha', 'last_7d:Oxirgi 7 kun', 'this_month:Shu oy'].map(item => {
            const [pKey, pLabel] = item.split(':');
            const isActive = period === pKey;
            return `
              <button class="btn-sm ${isActive ? 'btn-primary' : 'btn-secondary'} meta-period-btn" data-period="${pKey}" style="font-weight:700;border-radius:8px;padding:6px 16px;">
                ${pLabel}
              </button>
            `;
          }).join('')}
        </div>

        <div class="meta-metrics-grid" style="grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:14px;margin-bottom:20px;">
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">Xarajat (Spend)</div>
            <div style="font-size:24px;font-weight:800;color:#60a5fa;margin-top:6px;">$${data.spend || '0.00'}</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">Lidlar Soni</div>
            <div style="font-size:24px;font-weight:800;color:#34d399;margin-top:6px;">${data.leads || '0'} ta</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">1 ta Lid Narxi (CPL)</div>
            <div style="font-size:24px;font-weight:800;color:#fbbf24;margin-top:6px;">${data.cpl || '—'}</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">Ko'rishlar (Impressions)</div>
            <div style="font-size:24px;font-weight:800;color:#ffffff;margin-top:6px;">${data.impressions || '0'}</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">Kliklar (Clicks)</div>
            <div style="font-size:24px;font-weight:800;color:#ffffff;margin-top:6px;">${data.clicks || '0'}</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">CTR (Klik darajasi)</div>
            <div style="font-size:24px;font-weight:800;color:#a78bfa;margin-top:6px;">${data.ctr || '0.00%'}</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">CPC (Klik Narxi)</div>
            <div style="font-size:24px;font-weight:800;color:#ffffff;margin-top:6px;">${data.cpc || '$0.00'}</div>
          </div>
          <div class="meta-metric-card">
            <div style="font-size:11.5px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">CPM (1000 Ko'rish)</div>
            <div style="font-size:24px;font-weight:800;color:#ffffff;margin-top:6px;">${data.cpm || '$0.00'}</div>
          </div>
        </div>

        <div style="font-size:12px;color:rgba(255,255,255,0.45);text-align:right;font-family:monospace;">
          Sana oralig'i: ${data.date_start || ''} — ${data.date_stop || ''}
        </div>
      `;

      contentEl.querySelectorAll('.meta-period-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          renderInsightsTab(btn.dataset.period);
        });
      });
    };

    const renderAutomationTab = () => {
      const contentEl = document.getElementById('meta-tab-content');
      if (!contentEl) return;

      contentEl.innerHTML = `
        <div class="meta-table-card" style="max-width:680px;padding:28px;margin:0 auto;">
          <h3 style="font-size:17px;font-weight:800;margin-bottom:20px;display:flex;align-items:center;gap:8px;color:#ffffff;">
            ${this.icons.automation || ''} Avtomatlashtirish & Xavfsizlik Sozlamalari
          </h3>

          <form id="meta-automation-form">
            <!-- Tungi Rejim -->
            <div style="margin-bottom:20px;padding:16px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
                <div>
                  <div style="font-weight:700;font-size:14px;color:#ffffff;display:flex;align-items:center;gap:6px;">
                    ${this.icons.clock} Tungi Rejim (Auto-Pause & Resume)
                  </div>
                  <div style="font-size:12px;color:rgba(255,255,255,0.55);margin-top:2px;">
                    Belgilangan vaqtda reklamalarni avtomatik to'xtatadi va ertalab qayta yoqadi
                  </div>
                </div>
                <label class="switch" style="position:relative;display:inline-block;width:44px;height:24px;">
                  <input type="checkbox" id="auto-schedule-toggle" ${settings.auto_schedule_enabled ? 'checked' : ''}>
                  <span class="slider round" style="position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background-color:#333;border-radius:24px;transition:.3s;"></span>
                </label>
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div class="form-group" style="margin:0;">
                  <label class="form-label" style="font-size:11px;display:flex;align-items:center;gap:4px;">${this.icons.pause} O'chirish Vaqti (HH:MM)</label>
                  <input type="time" id="pause-time-input" class="input-control" value="${settings.pause_time || '23:00'}">
                </div>
                <div class="form-group" style="margin:0;">
                  <label class="form-label" style="font-size:11px;display:flex;align-items:center;gap:4px;">${this.icons.play} Qayta Yoqish Vaqti (HH:MM)</label>
                  <input type="time" id="resume-time-input" class="input-control" value="${settings.resume_time || '07:00'}">
                </div>
              </div>
            </div>

            <!-- Kunlik Hisobot -->
            <div style="margin-bottom:20px;padding:16px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
                <div>
                  <div style="font-weight:700;font-size:14px;color:#ffffff;display:flex;align-items:center;gap:6px;">
                    ${this.icons.clipboard} Kunlik Avtomat Hisobot
                  </div>
                  <div style="font-size:12px;color:rgba(255,255,255,0.55);margin-top:2px;">
                    Har kuni kechqurun sarflangan pul va lidlar bo'yicha Telegramga hisobot yuborish
                  </div>
                </div>
                <label class="switch" style="position:relative;display:inline-block;width:44px;height:24px;">
                  <input type="checkbox" id="daily-report-toggle" ${settings.daily_report_enabled ? 'checked' : ''}>
                  <span class="slider round" style="position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background-color:#333;border-radius:24px;transition:.3s;"></span>
                </label>
              </div>

              <div class="form-group" style="margin:0;max-width:200px;">
                <label class="form-label" style="font-size:11px;display:flex;align-items:center;gap:4px;">${this.icons.clock} Yuborish Vaqti (HH:MM)</label>
                <input type="time" id="daily-report-time-input" class="input-control" value="${settings.daily_report_time || '22:00'}">
              </div>
            </div>

            <!-- 0$ Ogohlantirish Info -->
            <div style="padding:14px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:10px;margin-bottom:20px;font-size:12.5px;color:#fcd34d;display:flex;align-items:center;gap:8px;">
              ${this.icons.info} <span><b>Eslatma:</b> Byudjet $0 ga yetganda faqat Telegramga ogohlantirish yuboriladi, reklamalaringiz to'xtatilmaydi.</span>
            </div>

            <button type="submit" class="btn-primary" style="display:inline-flex;align-items:center;gap:8px;">
              ${this.icons.save} <span>Sozlamalarni Saqlash</span>
            </button>
          </form>
        </div>
      `;

      document.getElementById('meta-automation-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
          auto_schedule_enabled: document.getElementById('auto-schedule-toggle').checked,
          pause_time: document.getElementById('pause-time-input').value,
          resume_time: document.getElementById('resume-time-input').value,
          daily_report_enabled: document.getElementById('daily-report-toggle').checked,
          daily_report_time: document.getElementById('daily-report-time-input').value
        };

        const res = await this.api('/api/meta-ads/settings', 'POST', payload);
        if (res && res.success) {
          this.toast('Avtomatlashtirish sozlamalari muvaffaqiyatli saqlandi!', 'success');
        } else {
          this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
        }
      });
    };

    // Default tab
    renderCampaignsTab();

    // Tab buttons listener
    viewport.querySelectorAll('.meta-subtab-btn, .meta-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        viewport.querySelectorAll('.meta-subtab-btn, .meta-tab-btn').forEach(b => {
          b.classList.remove('active', 'btn-primary');
        });
        btn.classList.add('active');

        const tab = btn.dataset.tab;
        if (tab === 'campaigns') renderCampaignsTab();
        else if (tab === 'insights') renderInsightsTab();
        else if (tab === 'automation') renderAutomationTab();
      });
    });

    // Refresh button
    const refreshBtn = document.getElementById('meta-refresh-btn');
    if (refreshBtn) refreshBtn.addEventListener('click', () => this.loadMetaAds(viewport));
  },

  renderMetaApiConfigModal(viewport) {
    this.modal({
      title: `${this.icons.settings} Meta Ads API Sozlamalari`,
      maxWidth: '540px',
      contentHtml: `
        <form id="form-save-meta-api-keys">
          <div class="form-group" style="margin-bottom:16px;">
            <label class="form-label" style="font-weight:700;font-size:12.5px;">Meta Access Token (Graph API / System User Token)</label>
            <div style="font-size:11.5px;color:rgba(255,255,255,0.6);margin-bottom:6px;">
              developers.facebook.com -> Graph API Explorer yoki Business Manager -> System Users orqali olingan token
            </div>
            <textarea id="input-meta-access-token" class="input-control font-mono" rows="4" style="width:100%;font-size:11.5px;resize:vertical;" placeholder="EAAlEZBNpYmJc..." required></textarea>
          </div>

          <div class="form-group" style="margin-bottom:20px;">
            <label class="form-label" style="font-weight:700;font-size:12.5px;">Ad Account ID</label>
            <input type="text" id="input-meta-ad-account-id" class="input-control font-mono" placeholder="act_962957616739265" value="act_962957616739265" required style="width:100%;">
          </div>

          <div style="display:flex;justify-content:flex-end;gap:10px;">
            <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
            <button type="submit" class="btn-sm btn-primary" id="btn-save-meta-keys-submit">
              ${this.icons.check} <span>Saqlash va Ulanish</span>
            </button>
          </div>
        </form>
      `
    });

    document.getElementById('form-save-meta-api-keys')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const tokenVal = document.getElementById('input-meta-access-token').value.trim();
      const accVal = document.getElementById('input-meta-ad-account-id').value.trim();
      if (!tokenVal || !accVal) return;

      const submitBtn = document.getElementById('btn-save-meta-keys-submit');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-sm"></span> Saqlanmoqda...`;
      }

      const res = await this.api('/api/meta-ads/settings', 'POST', {
        meta_access_token: tokenVal,
        ad_account_id: accVal
      });

      this.closeModal();
      if (res && res.success) {
        this.toast("Meta API kalitlari muvaffaqiyatli saqlandi!", "success");
        this.loadMetaAds(viewport);
      } else {
        this.toast((res && res.error) || "Kalitlarni saqlashda xatolik", "error");
      }
    });
  },

  // ============================================================
  // 15. INSTAGRAM POSTLARINI SINXRONLASH & AUTOPOSTER
  // ============================================================
  async loadInstagram(viewport, initialTab = 'queue') {
    viewport.innerHTML = `
      <div class="instagram-container">
        <!-- HEADER SHIMMER -->
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
          <div>
            <div class="skeleton-shimmer skeleton-text" style="width:320px;height:24px;margin-bottom:8px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:240px;height:14px;"></div>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div class="skeleton-shimmer skeleton-btn" style="width:130px;height:36px;border-radius:8px;"></div>
            <div class="skeleton-shimmer skeleton-btn" style="width:110px;height:36px;border-radius:8px;"></div>
            <div class="skeleton-shimmer skeleton-btn" style="width:110px;height:36px;border-radius:8px;"></div>
          </div>
        </div>

        <!-- FULL-WIDTH SUBTABS SHIMMER -->
        <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:10px;margin-bottom:20px;width:100%;">
          <div class="skeleton-shimmer skeleton-btn" style="height:42px;border-radius:10px;"></div>
          <div class="skeleton-shimmer skeleton-btn" style="height:42px;border-radius:10px;"></div>
          <div class="skeleton-shimmer skeleton-btn" style="height:42px;border-radius:10px;"></div>
        </div>

        <!-- TOP STATUS / BANNER SHIMMER -->
        <div class="glass-card" style="padding:16px 20px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div class="skeleton-shimmer skeleton-btn" style="width:38px;height:38px;border-radius:50%;"></div>
            <div>
              <div class="skeleton-shimmer skeleton-text" style="width:160px;height:16px;margin-bottom:6px;"></div>
              <div class="skeleton-shimmer skeleton-text" style="width:280px;height:12px;"></div>
            </div>
          </div>
          <div style="display:flex;gap:8px;">
            <div class="skeleton-shimmer skeleton-badge" style="width:110px;height:26px;"></div>
            <div class="skeleton-shimmer skeleton-badge" style="width:130px;height:26px;"></div>
          </div>
        </div>

        <!-- QUEUE TABLE SHIMMER -->
        <div class="glass-card" style="padding:20px;border-radius:12px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div class="skeleton-shimmer skeleton-text" style="width:200px;height:18px;"></div>
            <div class="skeleton-shimmer skeleton-text" style="width:120px;height:14px;"></div>
          </div>
          ${[1, 2, 3, 4, 5, 6].map(() => `
            <div style="display:flex;gap:12px;margin-bottom:14px;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
              <div class="skeleton-shimmer skeleton-badge" style="width:36px;height:28px;"></div>
              <div class="skeleton-shimmer skeleton-btn" style="width:40px;height:40px;border-radius:8px;"></div>
              <div class="skeleton-shimmer skeleton-text" style="flex:1;height:16px;"></div>
              <div class="skeleton-shimmer skeleton-badge" style="width:100px;height:28px;"></div>
              <div class="skeleton-shimmer skeleton-badge" style="width:100px;height:28px;"></div>
              <div class="skeleton-shimmer skeleton-btn" style="width:50px;height:28px;border-radius:6px;"></div>
              <div class="skeleton-shimmer skeleton-btn" style="width:50px;height:28px;border-radius:6px;"></div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    const [statsRes, settRes] = await Promise.all([
      this.api('/api/instagram/stats'),
      this.api('/api/instagram/settings')
    ]);

    if (!statsRes || !statsRes.success) {
      viewport.innerHTML = `
        <div class="glass-card" style="text-align:center;padding:40px 20px;">
          <div style="font-size:36px;margin-bottom:12px;">⚠️</div>
          <h3 style="margin-bottom:8px;color:#f87171;">Instagram AutoPoster Ma'lumotlarini Yuklab Bo'lmadi</h3>
          <p style="color:rgba(255,255,255,0.7);max-width:500px;margin:0 auto 20px auto;">
            ${(statsRes && statsRes.error) || "Baza yoki API bilan ulanishda xatolik yuz berdi."}
          </p>
          <button class="btn-primary" onclick="ATLAS.loadInstagram(document.getElementById('content-viewport'))">
            ${this.icons.refresh} Qayta urinib ko'rish
          </button>
        </div>
      `;
      return;
    }

    const stats = statsRes.stats || {};
    const settings = (settRes && settRes.settings) || stats.settings || {};
    const ytTimes = statsRes.youtube_schedule_times || [];
    const ytReady = statsRes.youtube_ready;

    const tgAuto = settings.auto_schedule_enabled === '1';
    const ytAuto = settings.youtube_auto_upload === '1';
    const currentUsername = settings.insta_username || 'shahrisabz_t_t_uz';

    let activeTab = initialTab || localStorage.getItem('atlas_insta_tab') || 'queue'; // 'queue' | 'youtube' | 'settings'
    let currentFilter = 'ALL';
    let currentPage = 1;
    let currentSearch = '';

    const render = () => {
      viewport.innerHTML = `
        <div class="instagram-container">
          <!-- HEADER WITH STATS & CONTROLS -->
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
            <div>
              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                <h2 style="font-size:20px;font-weight:700;margin:0;display:flex;align-items:center;gap:8px;">
                  ${this.icons.instagram} Instagram Postlarini Sinxronlash
                </h2>
                <span class="badge" style="background:rgba(20,184,166,0.15);color:#2ee59d;border:1px solid rgba(46,229,157,0.3);font-family:'JetBrains Mono',monospace;">
                  @${currentUsername}
                </span>
                ${tgAuto ? `
                  <span class="badge" style="background:rgba(16,185,129,0.12);color:#34d399;border:1px solid rgba(16,185,129,0.25);display:inline-flex;align-items:center;gap:6px;padding:4px 9px;">
                    <span style="width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 6px #34d399;"></span> TG: Faol (${settings.interval_minutes || 60} daq)
                  </span>
                ` : `
                  <span class="badge" style="background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.1);display:inline-flex;align-items:center;gap:6px;padding:4px 9px;">
                    <span style="width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.35);"></span> TG: Nofaol
                  </span>
                `}
                ${ytAuto ? `
                  <span class="badge" style="background:rgba(244,63,94,0.12);color:#fb7185;border:1px solid rgba(244,63,94,0.25);display:inline-flex;align-items:center;gap:6px;padding:4px 9px;">
                    <span style="width:7px;height:7px;border-radius:50%;background:#fb7185;box-shadow:0 0 6px #fb7185;"></span> YouTube Shorts: Faol (${ytTimes.length} ta vaqt)
                  </span>
                ` : `
                  <span class="badge" style="background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.1);display:inline-flex;align-items:center;gap:6px;padding:4px 9px;">
                    <span style="width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.35);"></span> YouTube Shorts: Nofaol
                  </span>
                `}
              </div>
              <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:4px;">
                Instagram profilidagi barcha postlar, reels va rasmlarni Telegram kanal va YouTube Shorts'ga xronologik avtomatik joylash markazi
              </p>
            </div>

            <div style="display:flex;align-items:center;gap:8px;">
              <button class="btn-sm btn-secondary" id="insta-refresh-btn" title="Yangilash">
                ${this.icons.refresh} <span>Yangilash</span>
              </button>
              <button class="btn-sm btn-secondary" id="btn-open-add-url-modal" style="background:rgba(56,189,248,0.12);color:#38bdf8;border:1px solid rgba(56,189,248,0.3);" title="Instagram post havolasi orqali navbatga qo'shish">
                ${this.icons.plus || '+'} <span>Havola Bilan Qo‘shish</span>
              </button>
              <button class="btn-sm btn-primary" id="btn-open-scan-modal">
                ${this.icons.download} <span>Instagramdan Skanerlash</span>
              </button>
            </div>
          </div>

          <!-- KPI METRIC CARDS -->
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(190px, 1fr));gap:14px;margin-bottom:20px;">
            <div class="glass-card" style="padding:16px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.5px;">Jami Postlar</div>
                  <div style="font-size:24px;font-weight:800;color:#ffffff;margin-top:4px;" id="stat-total-val">${stats.total || 0}</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">Baza navbatida</div>
                </div>
                <div style="width:36px;height:36px;border-radius:8px;background:rgba(20,184,166,0.12);display:flex;align-items:center;justify-content:center;color:#00cba9;">
                  ${this.icons.instagram}
                </div>
              </div>
            </div>

            <div class="glass-card" style="padding:16px;border-left:3px solid #f59e0b;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.5px;">Kutilayotgan Navbat</div>
                  <div style="font-size:24px;font-weight:800;color:#fbbf24;margin-top:4px;" id="stat-pending-val">${stats.pending || 0}</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">Chiqarilishi kutilmoqda</div>
                </div>
                <div style="width:36px;height:36px;border-radius:8px;background:rgba(245,158,11,0.12);display:flex;align-items:center;justify-content:center;color:#fbbf24;">
                  ${this.icons.clock}
                </div>
              </div>
            </div>

            <div class="glass-card" style="padding:16px;border-left:3px solid #10b981;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.5px;">Telegramga Chiqdi</div>
                  <div style="font-size:24px;font-weight:800;color:#34d399;margin-top:4px;" id="stat-sent-val">${stats.sent || 0}</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">Kanalga yuborilgan</div>
                </div>
                <div style="width:36px;height:36px;border-radius:8px;background:rgba(16,185,129,0.12);display:flex;align-items:center;justify-content:center;color:#34d399;">
                  ${this.icons.send}
                </div>
              </div>
            </div>

            <div class="glass-card" style="padding:16px;border-left:3px solid #f43f5e;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.5px;">YouTube Shorts</div>
                  <div style="font-size:24px;font-weight:800;color:#fb7185;margin-top:4px;" id="stat-yt-val">${stats.yt_uploaded || 0}</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">Yuklangan videolar</div>
                </div>
                <div style="width:36px;height:36px;border-radius:8px;background:rgba(244,63,94,0.12);display:flex;align-items:center;justify-content:center;color:#fb7185;">
                  ${this.icons.youtube}
                </div>
              </div>
            </div>

            <div class="glass-card" style="padding:16px;border-left:3px solid #38bdf8;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.55);text-transform:uppercase;font-weight:700;letter-spacing:0.5px;">Keyingi YouTube Shorts</div>
                  <div style="font-size:18px;font-weight:800;color:#38bdf8;margin-top:6px;">${stats.next_yt_time_estimate || '18:30 da'}</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">Jadval vaqti bo‘yicha</div>
                </div>
                <div style="width:36px;height:36px;border-radius:8px;background:rgba(56,189,248,0.12);display:flex;align-items:center;justify-content:center;color:#38bdf8;">
                  <svg style="width:16px;height:16px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>
                </div>
              </div>
            </div>
          </div>

          <!-- HERO MASTER AUTO-POSTER CONTROL & NEXT SCHEDULE CARD -->
          <div class="glass-card" style="margin-bottom:20px;border:1px solid ${tgAuto ? 'rgba(46,229,157,0.3)' : 'rgba(245,158,11,0.3)'};background:linear-gradient(135deg, rgba(255,255,255,0.02) 0%, ${tgAuto ? 'rgba(46,229,157,0.05)' : 'rgba(245,158,11,0.05)'} 100%);">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;padding-bottom:16px;border-bottom:1px solid var(--border-glass);">
              <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:40px;height:40px;border-radius:10px;background:${tgAuto ? 'rgba(46,229,157,0.15)' : 'rgba(245,158,11,0.15)'};display:flex;align-items:center;justify-content:center;color:${tgAuto ? '#2ee59d' : '#fbbf24'};">
                  ${tgAuto ? `
                    <svg style="width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.5;" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                  ` : `
                    <svg style="width:18px;height:18px;fill:currentColor;" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
                  `}
                </div>
                <div>
                  <div style="font-size:15px;font-weight:800;color:#ffffff;letter-spacing:0.3px;">
                    ${tgAuto ? "AVTO-YUBORISH JARAYONI FAOL (ISHMOQDA)" : "AVTO-YUBORISH TO'XTATILGAN (PAUZA HOLATIDA)"}
                  </div>
                  <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:2px;">
                    Telegram: <b style="color:#ffffff;">${settings.target_chat_id || '-1004295470034'}</b> &bull; Oraliq: <b style="color:#ffffff;">Har soat boshida (:00 da)</b> &bull; Tungi rejim: <b style="color:#818cf8;">00:00 — 07:00</b>
                  </div>
                </div>
              </div>

              <!-- PROMINENT START / PAUSE BUTTON -->
              <div>
                <button class="btn" id="btn-hero-toggle-schedule" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 22px;font-size:13px;font-weight:700;border-radius:var(--radius-sm);cursor:pointer;background:${tgAuto ? 'rgba(239,68,68,0.15)' : '#00cba9'};border:1px solid ${tgAuto ? 'rgba(239,68,68,0.35)' : '#00cba9'};color:${tgAuto ? '#f87171' : '#051e18'};transition:all 0.2s ease;">
                  ${tgAuto ? `
                    <svg style="width:14px;height:14px;fill:currentColor;" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
                    <span>To‘xtatib Turish (Pauza)</span>
                  ` : `
                    <svg style="width:14px;height:14px;fill:currentColor;" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                    <span>Avto-yuborishni Boshlash (Start)</span>
                  `}
                </button>
              </div>
            </div>

            <!-- NEXT SCHEDULED POST DETAILS -->
            <div style="margin-top:14px;display:grid;grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));gap:12px;align-items:center;">
              <div style="padding:12px 14px;background:rgba(0,0,0,0.25);border-radius:var(--radius-sm);border:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:11px;color:rgba(255,255,255,0.5);text-transform:uppercase;font-weight:600;display:flex;align-items:center;gap:5px;">
                  <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg> Keyingi Telegram Chiqishi:
                </div>
                <div style="font-size:15px;font-weight:800;color:${tgAuto ? '#34d399' : '#fbbf24'};margin-top:4px;font-family:'JetBrains Mono',monospace;">
                  ${tgAuto ? (stats.next_time_estimate || 'Reja bo‘yicha') : 'Pauzada'}
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">
                  Har soat boshida navbat bo‘yicha
                </div>
              </div>

              <div style="padding:12px 14px;background:rgba(0,0,0,0.25);border-radius:var(--radius-sm);border:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:11px;color:rgba(255,255,255,0.5);text-transform:uppercase;font-weight:600;display:flex;align-items:center;gap:5px;">
                  <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg> Keyingi YouTube Shorts Chiqishi:
                </div>
                <div style="font-size:15px;font-weight:800;color:#fb7185;margin-top:4px;font-family:'JetBrains Mono',monospace;">
                  ${stats.next_yt_time_estimate || '18:30 da'}
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:2px;">
                  Belgilangan rek vaqtlari bo‘yicha
                </div>
              </div>

              <div style="padding:12px 14px;background:rgba(0,0,0,0.25);border-radius:var(--radius-sm);border:1px solid rgba(255,255,255,0.06);">
                <div style="font-size:11px;color:rgba(255,255,255,0.5);text-transform:uppercase;font-weight:600;display:flex;align-items:center;gap:5px;">
                  <svg style="width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:2;" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg> Navbatdagi 1-Post:
                </div>
                ${stats.next_post ? `
                  <div style="font-size:13px;color:#ffffff;font-weight:700;margin-top:4px;display:flex;align-items:center;gap:8px;">
                    <span>${stats.next_post.media_type === 'reel' ? 'Reel Video' : 'Rasm'}</span>
                    <a href="${stats.next_post.post_url}" target="_blank" style="color:#00cba9;text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:12px;">
                      ${stats.next_post.shortcode} ↗
                    </a>
                  </div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.65);margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:340px;">
                    ${stats.next_post.caption ? stats.next_post.caption : 'Matnsiz'}
                  </div>
                ` : `
                  <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:4px;">
                    Hozircha navbatda kutilayotgan post yo'q
                  </div>
                `}
              </div>
            </div>
          </div>

          <!-- TAB BUTTONS (FULL WIDTH) -->
          <div class="tab-pills-row" style="margin-bottom:18px;display:grid;grid-template-columns:repeat(3, 1fr);gap:10px;width:100%;">
            <button class="tab-pill-btn ${activeTab === 'queue' ? 'active' : ''}" id="tab-btn-insta-queue" style="width:100%;justify-content:center;text-align:center;display:flex;align-items:center;gap:6px;">
              ${this.icons.documents} <span>Postlar Navbati & Boshqaruv</span>
            </button>
            <button class="tab-pill-btn ${activeTab === 'youtube' ? 'active' : ''}" id="tab-btn-insta-youtube" style="width:100%;justify-content:center;text-align:center;display:flex;align-items:center;gap:6px;">
              ${this.icons.youtube} <span>YouTube Shorts & Rek Vaqtlari</span>
            </button>
            <button class="tab-pill-btn ${activeTab === 'settings' ? 'active' : ''}" id="tab-btn-insta-settings" style="width:100%;justify-content:center;text-align:center;display:flex;align-items:center;gap:6px;">
              ${this.icons.settings} <span>Sinxronlash Sozlamalari</span>
            </button>
          </div>

          <!-- TAB VIEWPORT -->
          <div id="insta-tab-viewport"></div>
        </div>
      `;

      // Background auto-trigger for active dashboard sessions
      if (!this._instaTickInterval) {
        this._instaTickInterval = setInterval(() => {
          this.api('/api/instagram/cron_tick', 'GET').catch(() => {});
        }, 30000);
      }

      // Event Bindings
      document.getElementById('insta-refresh-btn').addEventListener('click', () => {
        this.loadInstagram(viewport, activeTab);
      });

      document.getElementById('btn-open-add-url-modal')?.addEventListener('click', () => {
        this.renderAddUrlModal(viewport);
      });

      document.getElementById('btn-open-scan-modal').addEventListener('click', () => {
        this.renderScanModal(currentUsername, viewport);
      });

      // Hero Start / Pause Schedule Toggle
      document.getElementById('btn-hero-toggle-schedule')?.addEventListener('click', async () => {
        const newVal = tgAuto ? '0' : '1';
        const res = await this.api('/api/instagram/settings', 'POST', {
          auto_schedule_enabled: newVal,
          youtube_auto_upload: newVal,
          youtube_schedule_enabled: newVal
        });
        if (res && res.success) {
          this.toast(`Avto-yuborish jarayoni ${newVal === '1' ? 'boshlandi (START)' : 'to‘xtatildi (PAUSE)'}`, 'success');
          this.loadInstagram(viewport, activeTab);
        } else {
          this.toast((res && res.error) || 'Xatolik', 'error');
        }
      });

      const resetFailedLink = document.getElementById('quick-reset-failed-link');
      if (resetFailedLink) {
        resetFailedLink.addEventListener('click', async () => {
          const res = await this.api('/api/instagram/queue/reset', 'POST');
          if (res && res.success) {
            this.toast(res.message || 'Xatoliklar qayta navbatga olindi', 'success');
            this.loadInstagram(viewport);
          } else {
            this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
          }
        });
      }

      document.getElementById('tab-btn-insta-queue').addEventListener('click', () => {
        activeTab = 'queue';
        try { localStorage.setItem('atlas_insta_tab', 'queue'); } catch (e) {}
        renderTabContent();
      });
      document.getElementById('tab-btn-insta-youtube').addEventListener('click', () => {
        activeTab = 'youtube';
        try { localStorage.setItem('atlas_insta_tab', 'youtube'); } catch (e) {}
        renderTabContent();
      });
      document.getElementById('tab-btn-insta-settings').addEventListener('click', () => {
        activeTab = 'settings';
        try { localStorage.setItem('atlas_insta_tab', 'settings'); } catch (e) {}
        renderTabContent();
      });

      renderTabContent();
    };

    const renderTabContent = () => {
      document.querySelectorAll('.tab-pill-btn').forEach(btn => {
        btn.classList.remove('active');
      });
      if (activeTab === 'queue') document.getElementById('tab-btn-insta-queue')?.classList.add('active');
      if (activeTab === 'youtube') document.getElementById('tab-btn-insta-youtube')?.classList.add('active');
      if (activeTab === 'settings') document.getElementById('tab-btn-insta-settings')?.classList.add('active');

      const tabBox = document.getElementById('insta-tab-viewport');
      if (!tabBox) return;

      if (activeTab === 'queue') renderQueueTab(tabBox);
      else if (activeTab === 'youtube') renderYouTubeTab(tabBox);
      else if (activeTab === 'settings') renderSettingsTab(tabBox);
    };

    // TAB 1: POSTLAR NAVBATI (YAGONA RO'YXAT - SAHIFASIZ)
    const renderQueueTab = async (container) => {
      container.innerHTML = `
        <div class="glass-card">
          <!-- ACTION CONTROLS & FILTER ROW -->
          <div class="card-header-flex" style="flex-wrap:wrap;gap:12px;margin-bottom:16px;">
            <div style="display:flex;gap:6px;flex-wrap:wrap;" id="insta-status-filters">
              <button class="btn-sm ${currentFilter === 'ALL' ? 'btn-primary' : 'btn-secondary'} filter-status-btn" data-status="ALL">Barchasi (${stats.total || 0})</button>
              <button class="btn-sm ${currentFilter === 'PENDING' ? 'btn-primary' : 'btn-secondary'} filter-status-btn" data-status="PENDING">Kutilmoqda (${stats.pending || 0})</button>
              <button class="btn-sm ${currentFilter === 'SENT' ? 'btn-primary' : 'btn-secondary'} filter-status-btn" data-status="SENT">Yuborildi (${stats.sent || 0})</button>
              <button class="btn-sm ${currentFilter === 'FAILED' ? 'btn-primary' : 'btn-secondary'} filter-status-btn" data-status="FAILED">Xatolik (${stats.failed || 0})</button>
              <button class="btn-sm ${currentFilter === 'YOUTUBE' ? 'btn-primary' : 'btn-secondary'} filter-status-btn" data-status="YOUTUBE">YouTube Shorts (${stats.yt_uploaded || 0})</button>
            </div>

            <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
              <input type="text" id="insta-search-input" class="input-control" style="width:180px;height:34px;font-size:12px;" placeholder="Shortcode yoki matn..." value="${currentSearch}">
              
              <button class="btn-sm btn-secondary" id="btn-toolbar-add-url" style="background:rgba(56,189,248,0.12);color:#38bdf8;border:1px solid rgba(56,189,248,0.3);display:inline-flex;align-items:center;gap:4px;" title="Havola (URL) orqali yangi post qo'shish">
                ${this.icons.plus || '+'} <span>Havola Qo‘shish</span>
              </button>

              <button class="btn-sm btn-primary" id="btn-post-next-tg" title="Navbatdagi 1 ta postni darhol Telegramga yuborish" style="display:inline-flex;align-items:center;gap:4px;">
                ${this.icons.send} <span>1 ta TG ga</span>
              </button>
              
              <button class="btn-sm btn-secondary" id="btn-post-next-yt" title="Navbatdagi 1 ta videoni darhol YouTube Shorts ga yuklash" style="display:inline-flex;align-items:center;gap:4px;background:rgba(244,63,94,0.12);color:#fb7185;border:1px solid rgba(244,63,94,0.25);">
                ${this.icons.youtube} <span>1 ta YT ga</span>
              </button>

              <button class="btn-sm btn-secondary" id="btn-reset-queue" title="Xatolik bo'lgan postlarni qayta tiklash">
                ${this.icons.refresh}
              </button>

              <button class="btn-sm btn-danger" id="btn-clear-queue" title="Navbatni tozalash" style="background:rgba(239,68,68,0.12);color:#f87171;border:1px solid rgba(239,68,68,0.25);">
                ${this.icons.trash}
              </button>
            </div>
          </div>

          <!-- TABLE CONTAINER -->
          <div id="insta-table-container">
            <div style="display:flex;align-items:center;justify-content:center;padding:40px;">
              <div class="spinner"></div>
            </div>
          </div>
        </div>
      `;

      // Status filters
      container.querySelectorAll('.filter-status-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          currentFilter = btn.dataset.status;
          currentPage = 1;
          renderQueueTab(container);
        });
      });

      // Add URL click from toolbar
      document.getElementById('btn-toolbar-add-url')?.addEventListener('click', () => {
        this.renderAddUrlModal(viewport);
      });

      // Search
      const searchInput = document.getElementById('insta-search-input');
      if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
          clearTimeout(debounceTimer);
          debounceTimer = setTimeout(() => {
            currentSearch = e.target.value;
            loadTableData();
          }, 350);
        });
      }

      // Action buttons
      document.getElementById('btn-post-next-tg')?.addEventListener('click', async () => {
        const btn = document.getElementById('btn-post-next-tg');
        btn.disabled = true;
        this.showActionLoader({
          title: "Telegramga Yuborilmoqda...",
          subtitle: "Navbatdagi reel yuklanib, Telegram kanalingizga yuborilmoqda",
          icon: this.icons.send,
          steps: [
            "Post ma'lumotlari aniqlanmoqda",
            "HD video serverga yuklab olinmoqda",
            "Telegram kanalga video va caption yuborilmoqda",
            "Baza va statistika yangilanmoqda"
          ],
          funFact: "ATLAS har bir postni eng yuqori HD sifatda kanallarga yetkazadi."
        });
        try {
          const res = await this.api('/api/instagram/post_next', 'POST');
          this.hideActionLoader();
          if (res && res.success) {
            this.toast(`Post muvaffaqiyatli Telegramga yuborildi! [${res.shortcode}]`, 'success');
            this.loadInstagram(viewport);
          } else {
            this.toast((res && res.error) || (res && res.message) || 'Post yuborishda xatolik', 'error');
            btn.disabled = false;
          }
        } catch (e) {
          this.hideActionLoader();
          this.toast('Yuborishda xatolik yuz berdi', 'error');
          btn.disabled = false;
        }
      });

      document.getElementById('btn-post-next-yt')?.addEventListener('click', async () => {
        const btn = document.getElementById('btn-post-next-yt');
        btn.disabled = true;
        this.showActionLoader({
          title: "YouTube Shorts ga Yuklanmoqda...",
          subtitle: "Video YouTube v3 API orqali Shorts formatida yuklanmoqda",
          icon: this.icons.youtube,
          steps: [
            "Video fayl manbasi olinmoqda",
            "HD video serverga yuklab olinmoqda",
            "YouTube v3 API bilan avtorizatsiya tasdiqlanmoqda",
            "Shorts sarlavha va hashtaglar bilan yuklanmoqda",
            "Bulut statistikasi sinxronlanmoqda"
          ],
          funFact: "Shorts videolari rek vaqtlari bo‘yicha algoritmik ko‘rishlarni oshiradi."
        });
        try {
          const res = await this.api('/api/instagram/post_youtube', 'POST');
          this.hideActionLoader();
          if (res && res.success) {
            this.toast(`Video YouTube Shorts ga muvaffaqiyatli yuklandi!`, 'success');
            this.loadInstagram(viewport);
          } else {
            this.toast((res && res.error) || (res && res.message) || 'YouTube yuklashda xatolik', 'error');
            btn.disabled = false;
          }
        } catch (e) {
          this.hideActionLoader();
          this.toast('YouTube yuklashda xatolik', 'error');
          btn.disabled = false;
        }
      });

      document.getElementById('btn-reset-queue')?.addEventListener('click', async () => {
        const res = await this.api('/api/instagram/queue/reset', 'POST');
        if (res && res.success) {
          this.toast(res.message || 'Xatoliklar qayta tiklandi', 'success');
          this.loadInstagram(viewport);
        } else {
          this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
        }
      });

      document.getElementById('btn-clear-queue')?.addEventListener('click', () => {
        this.confirmModal({
          title: "Barcha postlar navbatini tozalash",
          message: "Rostdan ham barcha skanerlangan postlar navbatini tozalab tashlamoqchimisiz? Bu amalni ortga qaytarib bo'lmaydi.",
          confirmText: "Ha, tozalash",
          onConfirm: async () => {
            const res = await this.api('/api/instagram/queue/clear', 'POST');
            if (res && res.success) {
              this.toast("Navbat tozalandi", 'success');
              this.loadInstagram(viewport);
            } else {
              this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
            }
          }
        });
      });

      // Load table data without pagination (single page)
      const loadTableData = async () => {
        const tableBox = document.getElementById('insta-table-container');
        if (!tableBox) return;

        tableBox.innerHTML = `
          <div class="table-responsive">
            <table class="glass-table">
              <thead>
                <tr>
                  <th style="width:40px;text-align:center;">№</th>
                  <th style="width:70px;text-align:center;">Instagram</th>
                  <th>Post Matni (Caption)</th>
                  <th style="width:145px;text-align:center;">Telegram Holati</th>
                  <th style="width:145px;text-align:center;">YouTube Holati</th>
                  <th style="width:140px;text-align:center;">Amallar</th>
                </tr>
              </thead>
              <tbody>
                ${[1, 2, 3, 4, 5].map(n => `
                  <tr>
                    <td style="text-align:center;"><div class="skeleton-shimmer skeleton-text" style="width:16px;"></div></td>
                    <td style="text-align:center;"><div class="skeleton-shimmer skeleton-btn" style="border-radius:8px;margin:0 auto;"></div></td>
                    <td><div class="skeleton-shimmer skeleton-text" style="width:${55 + (n * 8)}%;"></div></td>
                    <td style="text-align:center;"><div class="skeleton-shimmer skeleton-badge"></div></td>
                    <td style="text-align:center;"><div class="skeleton-shimmer skeleton-badge"></div></td>
                    <td style="text-align:center;"><div class="skeleton-shimmer skeleton-btn" style="width:80px;height:26px;"></div></td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;

        const query = new URLSearchParams({
          page: 1,
          limit: 1000,
          status: currentFilter === 'ALL' ? '' : currentFilter,
          search: currentSearch
        });

        const queueRes = await this.api(`/api/instagram/queue?${query.toString()}`);
        if (!queueRes || !queueRes.success) {
          tableBox.innerHTML = `<div style="text-align:center;padding:24px;color:#f87171;">Postlarni yuklab bo'lmadi</div>`;
          return;
        }

        const items = queueRes.items || [];

        if (items.length === 0) {
          tableBox.innerHTML = `
            <div style="text-align:center;padding:48px 20px;color:rgba(255,255,255,0.45);">
              <div style="width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;margin:0 auto 12px auto;color:rgba(255,255,255,0.4);">
                <svg style="width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.5;" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              </div>
              <div style="font-size:14px;font-weight:600;color:rgba(255,255,255,0.8);margin-bottom:4px;">Hech qanday post topilmadi</div>
              <p style="font-size:12px;max-width:400px;margin:0 auto 16px auto;">
                ${currentSearch ? "Qidiruv bo'yicha mos keluvchi postlar mavjud emas." : "Instagramdan yangi postlarni skanerlab olish uchun yuqoridagi 'Instagramdan Skanerlash' tugmasini bosing."}
              </p>
              ${!currentSearch ? `
                <button class="btn-sm btn-primary" onclick="document.getElementById('btn-open-scan-modal').click()">
                  ${this.icons.download} <span>Instagramdan Skanerlash</span>
                </button>
              ` : ''}
            </div>
          `;
          return;
        }

        tableBox.innerHTML = `
          <div class="table-responsive">
            <table class="glass-table">
              <thead>
                <tr>
                  <th style="width:40px;text-align:center;">№</th>
                  <th style="width:70px;text-align:center;">Instagram</th>
                  <th>Post Matni (Caption)</th>
                  <th style="width:145px;text-align:center;">Telegram Holati</th>
                  <th style="width:145px;text-align:center;">YouTube Holati</th>
                  <th style="width:140px;text-align:center;">Amallar</th>
                </tr>
              </thead>
              <tbody>
                ${items.map((item, idx) => {
                  const isTgSent = item.status === 'SENT';
                  const isTgProcessing = item.status === 'PROCESSING';
                  const isYtUploaded = item.youtube_uploaded == 1 || item.youtube_uploaded === true || item.youtube_uploaded === '1' || Boolean(item.youtube_url);
                  const validSched = (item.scheduled_time && item.scheduled_time !== '—' && !item.scheduled_time.includes('?')) ? item.scheduled_time : 'Hozir (Navbatda)';

                  let tgBadge = '';
                  if (isTgSent) {
                    tgBadge = `<span class="badge status-badge-interactive" style="background:rgba(16,185,129,0.14);color:#34d399;border:1px solid rgba(16,185,129,0.3);display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:5px 9px;font-size:11.5px;font-weight:700;border-radius:7px;" title="Telegramga yuborilgan vaqti: ${item.sent_at || 'Yuborildi'}">
                      <svg style="width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:2.5;" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> TG: Yuborildi
                    </span>`;
                  } else if (isTgProcessing) {
                    tgBadge = `<span class="badge status-badge-interactive" style="background:rgba(56,189,248,0.14);color:#38bdf8;border:1px solid rgba(56,189,248,0.3);display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:5px 9px;font-size:11.5px;font-weight:700;border-radius:7px;" title="Navbatdagi 1-o'rindagi aktiv post! Rejadagi vaqti: ${validSched}">
                      <svg style="width:12px;height:12px;animation:spin 1s linear infinite;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg> TG: Jarayonda
                    </span>`;
                  } else if (item.status === 'FAILED') {
                    tgBadge = `<span class="badge status-badge-interactive" style="background:rgba(239,68,68,0.14);color:#f87171;border:1px solid rgba(239,68,68,0.3);display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:5px 9px;font-size:11.5px;font-weight:700;border-radius:7px;" title="Xatolik: ${(item.error_msg || '').replace(/"/g, '&quot;')}">
                      <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg> TG: Xatolik
                    </span>`;
                  } else {
                    tgBadge = `<span class="badge status-badge-interactive" style="background:rgba(245,158,11,0.14);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:5px 9px;font-size:11.5px;font-weight:700;border-radius:7px;" title="Rejalashtirilgan vaqt: ${validSched}">
                      <svg style="width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:2;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> TG: Kutilmoqda
                    </span>`;
                  }

                  let ytBadge = '';
                  if (isYtUploaded) {
                    ytBadge = `<a href="${item.youtube_url || 'https://www.youtube.com'}" target="_blank" class="badge status-badge-interactive" style="background:rgba(244,63,94,0.14);color:#fb7185;border:1px solid rgba(244,63,94,0.3);text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:5px 9px;font-size:11.5px;font-weight:700;border-radius:7px;" title="YouTube Shorts ga yuklangan (Shortsda ochish ↗)">
                      <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg> YT: Yuklandi
                    </a>`;
                  } else {
                    ytBadge = `<span class="badge status-badge-interactive" style="background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.12);display:inline-flex;align-items:center;justify-content:center;gap:5px;padding:5px 9px;font-size:11.5px;font-weight:700;border-radius:7px;" title="YouTube Shorts rek vaqtlari bo'yicha navbatda">
                      <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg> YT: Kutilmoqda
                    </span>`;
                  }

                  return `
                    <tr>
                      <td class="mono" style="text-align:center;font-size:11px;color:rgba(255,255,255,0.45);">${idx + 1}</td>
                      <td style="text-align:center;">
                        <a href="${item.post_url}" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:8px;background:linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);color:#ffffff;box-shadow:0 2px 6px rgba(220,39,67,0.3);transition:transform 0.15s ease;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'" title="Instagramda ko'rish (${item.shortcode})">
                          <svg style="width:16px;height:16px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                        </a>
                      </td>
                      <td>
                        <div style="font-size:12.5px;color:rgba(255,255,255,0.92);max-width:440px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.4;" title="${(item.caption || '').replace(/"/g, '&quot;')}">
                          ${item.caption ? item.caption : '<span style="color:rgba(255,255,255,0.3);font-style:italic;">(Matnsiz)</span>'}
                        </div>
                      </td>
                      <td style="text-align:center;">${tgBadge}</td>
                      <td style="text-align:center;">${ytBadge}</td>
                      <td style="text-align:center;">
                        <div style="display:inline-flex;gap:6px;align-items:center;justify-content:center;">
                          ${isTgSent ? `
                            <button class="btn-sm" style="padding:4px 8px;font-size:11px;opacity:0.6;cursor:not-allowed;background:rgba(16,185,129,0.1);color:#34d399;border:1px solid rgba(16,185,129,0.25);border-radius:6px;display:inline-flex;align-items:center;gap:3px;" disabled title="Telegramga yuborilgan">
                              <svg style="width:11px;height:11px;fill:none;stroke:currentColor;stroke-width:2.5;" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <span>TG</span>
                            </button>
                          ` : `
                            <button class="btn-sm btn-post-single-action" data-id="${item.id}" style="padding:4px 8px;font-size:11px;white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;gap:3px;background:rgba(20,184,166,0.15);color:#2ee59d;border:1px solid rgba(20,184,166,0.3);border-radius:6px;cursor:pointer;" title="Telegram kanalga hozir chiqarish">
                              <svg style="width:11px;height:11px;fill:currentColor;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg> <span>TG</span>
                            </button>
                          `}

                          ${isYtUploaded ? `
                            <button class="btn-sm" style="padding:4px 8px;font-size:11px;opacity:0.6;cursor:not-allowed;background:rgba(244,63,94,0.1);color:#fb7185;border:1px solid rgba(244,63,94,0.25);border-radius:6px;display:inline-flex;align-items:center;gap:3px;" disabled title="YouTube Shorts ga yuklangan">
                              <svg style="width:11px;height:11px;fill:none;stroke:currentColor;stroke-width:2.5;" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <span>YT</span>
                            </button>
                          ` : `
                            <button class="btn-sm btn-post-single-yt-action" data-id="${item.id}" style="padding:4px 8px;font-size:11px;white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;gap:3px;background:rgba(244,63,94,0.15);color:#fb7185;border:1px solid rgba(244,63,94,0.3);border-radius:6px;cursor:pointer;" title="YouTube Shorts ga hozir yuklash">
                              <svg style="width:11px;height:11px;fill:currentColor;" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg> <span>YT</span>
                            </button>
                          `}

                          <button class="btn-icon btn-sm btn-delete-single-action" data-id="${item.id}" title="Navbatdan o'chirish" style="color:rgba(239,68,68,0.85);background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.25);border-radius:6px;width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;">
                            <svg style="width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:2;" viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>

          <!-- FOOTER SUMMARY (PAGINATIONSIZ) -->
          <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 18px;border-top:1px solid var(--border-glass);flex-wrap:wrap;gap:8px;font-size:12px;color:rgba(255,255,255,0.6);">
            <div>
              Navbatdagi jami postlar: <b style="color:#ffffff;">${items.length}</b> ta
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:rgba(255,255,255,0.45);">
              <svg style="width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:2;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              Avto-yuborish har soat boshida (:00 da) amalga oshiriladi
            </div>
          </div>
        `;

        // Row action buttons
        tableBox.querySelectorAll('.btn-post-single-action').forEach(btn => {
          btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            btn.disabled = true;
            this.showActionLoader({
              title: "Tanlangan Post Yuborilmoqda...",
              subtitle: `Post ID #${id} Telegram kanalga yuborilmoqda`,
              icon: this.icons.send,
              steps: [
                "Post ma'lumotlari tekshirilmoqda",
                "HD sifatdagi video yuklanmoqda",
                "Telegram kanalga joylanmoqda",
                "Hisobot yuborilmoqda"
              ],
              funFact: "ATLAS kanalingizga har bir postni inline tugmalar bilan yetkazadi."
            });
            try {
              const res = await this.api(`/api/instagram/post_single/${id}`, 'POST');
              this.hideActionLoader();
              if (res && res.success) {
                this.toast(`Post muvaffaqiyatli Telegramga yuborildi!`, 'success');
                this.loadInstagram(viewport);
              } else {
                this.toast((res && res.error) || 'Yuborishda xatolik yuz berdi', 'error');
                btn.disabled = false;
              }
            } catch (e) {
              this.hideActionLoader();
              this.toast('Xatolik yuz berdi', 'error');
              btn.disabled = false;
            }
          });
        });

        tableBox.querySelectorAll('.btn-post-single-yt-action').forEach(btn => {
          btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            btn.disabled = true;
            this.showActionLoader({
              title: "YouTube Shorts Yuklanmoqda...",
              subtitle: `Post ID #${id} YouTube kanalga Shorts qilib yuklanmoqda`,
              icon: this.icons.youtube,
              steps: [
                "Video manbasi tekshirilmoqda",
                "HD video yuklab olinmoqda",
                "YouTube Shorts formatida joylanmoqda",
                "Hisobot yuborilmoqda"
              ],
              funFact: "Shorts videolari kanalingiz obunachilarini tabiiy oshirishga yordam beradi."
            });
            try {
              const res = await this.api(`/api/instagram/post_single_youtube/${id}`, 'POST');
              this.hideActionLoader();
              if (res && res.success) {
                this.toast(`Video YouTube Shorts ga muvaffaqiyatli yuklandi!`, 'success');
                this.loadInstagram(viewport);
              } else {
                this.toast((res && res.error) || 'YouTube yuklashda xatolik yuz berdi', 'error');
                btn.disabled = false;
              }
            } catch (e) {
              this.hideActionLoader();
              this.toast('Xatolik yuz berdi', 'error');
              btn.disabled = false;
            }
          });
        });

        tableBox.querySelectorAll('.btn-delete-single-action').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            this.confirmModal({
              title: "Postni navbatdan o'chirish",
              message: `ID: ${id} bo'lgan postni navbatdan o'chirishni tasdiqlaysizmi?`,
              confirmText: "O'chirish",
              onConfirm: async () => {
                const res = await this.api(`/api/instagram/queue/${id}`, 'DELETE');
                if (res && res.success) {
                  this.toast("Post navbatdan o'chirildi", 'success');
                  loadTableData();
                } else {
                  this.toast((res && res.error) || 'O\'chirishda xatolik', 'error');
                }
              }
            });
          });
        });

        // Pagination buttons
        document.getElementById('insta-prev-page-btn')?.addEventListener('click', () => {
          if (currentPage > 1) {
            currentPage--;
            loadTableData();
          }
        });
        document.getElementById('insta-next-page-btn')?.addEventListener('click', () => {
          if (currentPage < totalPages) {
            currentPage++;
            loadTableData();
          }
        });
      };

      loadTableData();
    };

    // TAB 2: YOUTUBE SHORTS & REK VAQTLARI
    const renderYouTubeTab = (container) => {
      const timePurposes = {
        '09:00': 'Ertalabki auditoriya',
        '12:00': 'Tushlik vaqti',
        '15:00': 'Kunning ikkinchi yarmi',
        '18:30': 'Eng faol davrlardan biri',
        '21:00': 'Kechki auditoriya'
      };

      container.innerHTML = `
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(360px, 1fr));gap:20px;">
          <!-- REK VAQTLARI BOSHQARUVI -->
          <div class="glass-card">
            <div class="card-title" style="display:flex;align-items:center;gap:8px;">
              ${this.icons.clock} YouTube Shorts Rek Vaqtlari
            </div>
            <div class="card-subtitle" style="margin-bottom:16px;">
              Bot har kuni quyida belgilangan vaqtlarda Instagram Reels videolarini avtomatik YouTube Shorts'ga joylab boradi.
            </div>

            <!-- JADVAL JADVALLI RO'YXAT -->
            <div style="background:rgba(0,0,0,0.25);border:1px solid var(--border-glass);border-radius:var(--radius-md);overflow:hidden;margin-bottom:20px;">
              <table style="width:100%;border-collapse:collapse;text-align:left;font-size:13px;">
                <thead>
                  <tr style="background:rgba(255,255,255,0.04);border-bottom:1px solid var(--border-glass);">
                    <th style="padding:10px 14px;width:40px;color:rgba(255,255,255,0.5);">№</th>
                    <th style="padding:10px 14px;color:rgba(255,255,255,0.7);font-weight:600;">Joylash vaqti</th>
                    <th style="padding:10px 14px;color:rgba(255,255,255,0.7);font-weight:600;">Maqsad</th>
                    <th style="padding:10px 14px;text-align:right;color:rgba(255,255,255,0.5);width:60px;">Amallar</th>
                  </tr>
                </thead>
                <tbody>
                  ${ytTimes.length === 0 ? `
                    <tr>
                      <td colspan="4" style="padding:24px;text-align:center;color:rgba(255,255,255,0.4);">
                        Hozircha vaqtlar belgilanmagan. Quyidagi "Standart (5 ta)" tugmasini bosing.
                      </td>
                    </tr>
                  ` : ytTimes.map((timeStr, idx) => {
                    const purpose = timePurposes[timeStr] || 'Rejalashtirilgan rek sloti';
                    return `
                      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);transition:background 0.2s;" class="hover-row">
                        <td style="padding:10px 14px;color:rgba(255,255,255,0.4);font-family:'JetBrains Mono',monospace;">${idx + 1}</td>
                        <td style="padding:10px 14px;">
                          <span style="display:inline-flex;align-items:center;gap:6px;background:rgba(244,63,94,0.12);border:1px solid rgba(244,63,94,0.3);padding:4px 10px;border-radius:6px;font-family:'JetBrains Mono',monospace;font-weight:700;color:#ffffff;font-size:12px;">
                            <svg style="width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:2;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${timeStr}
                          </span>
                        </td>
                        <td style="padding:10px 14px;color:rgba(255,255,255,0.85);font-size:13px;">
                          ${purpose}
                        </td>
                        <td style="padding:10px 14px;text-align:right;">
                          <button type="button" class="btn-icon btn-sm btn-delete-yt-time" data-time="${timeStr}" title="${timeStr} vaqtini o'chirish" style="color:#f87171;padding:4px;border:none;background:transparent;cursor:pointer;">
                            ${this.icons.close}
                          </button>
                        </td>
                      </tr>
                    `;
                  }).join('')}
                </tbody>
              </table>
            </div>

            <!-- ADD TIME FORM -->
            <form id="add-yt-time-form" style="display:flex;gap:8px;align-items:center;margin-bottom:16px;flex-wrap:wrap;">
              <input type="text" id="new-yt-time-input" class="input-control font-mono" placeholder="Format: 14:30 yoki 20:00" style="max-width:200px;" required>
              <button type="submit" class="btn-sm btn-primary" id="btn-add-yt-time-submit">
                ${this.icons.plus} <span>Qo'shish</span>
              </button>
              <button type="button" class="btn-sm btn-secondary" id="btn-reset-yt-times" title="5 ta standart vaqtga (09:00, 12:00, 15:00, 18:30, 21:00) qaytarish">
                ${this.icons.refresh} <span>Standart (5 ta)</span>
              </button>
            </form>

            <div style="padding:12px;background:rgba(0,203,169,0.08);border:1px solid rgba(0,203,169,0.2);border-radius:var(--radius-sm);font-size:12px;color:rgba(255,255,255,0.75);line-height:1.5;">
              <b>Standart tavsiya etilgan 5 ta vaqt:</b> <code>09:00</code> (Ertalab), <code>12:00</code> (Tushlik), <code>15:00</code> (Kunning 2-yarmi), <code>18:30</code> (Eng faol davr), <code>21:00</code> (Kechki auditoriya).
            </div>
          </div>

          <!-- YOUTUBE INTEGRATSIYASI & HOLATI -->
          <div class="glass-card">
            <div class="card-title" style="display:flex;align-items:center;gap:8px;">
              ${this.icons.youtube} YouTube API Integratsiyasi
            </div>
            <div class="card-subtitle" style="margin-bottom:16px;">
              Google Data API v3 orqali YouTube kanaliga to'g'ridan-to'g'ri avtorizatsiya holati
            </div>

            <div style="margin-bottom:20px;">
              <div style="display:flex;align-items:center;gap:12px;padding:14px;border-radius:var(--radius-md);background:${ytReady ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'};border:1px solid ${ytReady ? 'rgba(16,185,129,0.25)' : 'rgba(239,68,68,0.25)'};">
                <div style="width:36px;height:36px;border-radius:8px;background:${ytReady ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)'};display:flex;align-items:center;justify-content:center;color:${ytReady ? '#34d399' : '#f87171'};">
                  ${ytReady ? `
                    <svg style="width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.5;" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                  ` : `
                    <svg style="width:18px;height:18px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                  `}
                </div>
                <div>
                  <div style="font-weight:700;color:#ffffff;font-size:14px;">
                    ${ytReady ? 'YouTube API Muvaffaqiyatli Ulangan' : 'YouTube Avtorizatsiyasi Kutilmoqda'}
                  </div>
                  <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:2px;">
                    ${ytReady ? "Token fayli faol (youtube_token.json). Bot belgilangan vaqtlarda yuklashga tayyor." : "Tizimda youtube_token.json mavjud emas. Google Cloud Console orqali OAuth ulanish talab qilinadi."}
                  </div>
                </div>
              </div>
            </div>

            <div style="display:flex;flex-direction:column;gap:12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;padding:12px;background:rgba(255,255,255,0.04);border-radius:var(--radius-sm);">
                <div>
                  <div style="font-size:13px;font-weight:600;color:#ffffff;">YouTube Avto-yuklash (Rejim)</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.5);">Reels videolarni avtomatik shorts qilish</div>
                </div>
                <button class="btn-sm ${ytAuto ? 'btn-primary' : 'btn-secondary'}" id="toggle-yt-auto-btn">
                  ${ytAuto ? 'Yoqilgan (ON)' : 'O\'chirilgan (OFF)'}
                </button>
              </div>

              <div style="display:flex;justify-content:space-between;align-items:center;padding:12px;background:rgba(255,255,255,0.04);border-radius:var(--radius-sm);">
                <div>
                  <div style="font-size:13px;font-weight:600;color:#ffffff;">Aniq vaqtlar jadvali (Daemon)</div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.5);">Rek vaqtlarida fon siklida yuklash</div>
                </div>
                <button class="btn-sm ${settings.youtube_schedule_enabled === '1' ? 'btn-primary' : 'btn-secondary'}" id="toggle-yt-sched-btn">
                  ${settings.youtube_schedule_enabled === '1' ? 'Yoqilgan (ON)' : 'O\'chirilgan (OFF)'}
                </button>
              </div>

              <button class="btn-sm btn-primary" id="btn-manual-yt-upload" style="margin-top:8px;">
                ${this.icons.youtube} <span>Hozir Navbatdagi 1 ta Videoni Yuklash</span>
              </button>
            </div>
          </div>
        </div>
      `;

      // Add time listener
      document.getElementById('add-yt-time-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('new-yt-time-input');
        const timeVal = input.value.trim();
        if (!timeVal) return;
        const res = await this.api('/api/instagram/youtube/schedule/add', 'POST', { time: timeVal });
        if (res && res.success) {
          this.toast(`Vaqt qo'shildi: ${timeVal}`, 'success');
          this.loadInstagram(viewport, 'youtube');
        } else {
          this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
        }
      });

      // Delete time listener
      container.querySelectorAll('.btn-delete-yt-time').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.preventDefault();
          e.stopPropagation();
          const t = btn.dataset.time;
          const res = await this.api('/api/instagram/youtube/schedule/remove', 'POST', { time: t });
          if (res && res.success) {
            this.toast(`${t} vaqti o'chirildi`, 'info');
            this.loadInstagram(viewport, 'youtube');
          } else {
            this.toast((res && res.error) || 'Xatolik', 'error');
          }
        });
      });

      // Reset standard times
      document.getElementById('btn-reset-yt-times')?.addEventListener('click', async () => {
        const res = await this.api('/api/instagram/youtube/schedule/reset', 'POST');
        if (res && res.success) {
          this.toast('YouTube vaqtlari 5 ta standart vaqtga qaytarildi', 'success');
          this.loadInstagram(viewport, 'youtube');
        }
      });

      // Toggles
      document.getElementById('toggle-yt-auto-btn')?.addEventListener('click', async () => {
        const newVal = ytAuto ? '0' : '1';
        const res = await this.api('/api/instagram/settings', 'POST', {
          youtube_auto_upload: newVal,
          youtube_schedule_enabled: newVal
        });
        if (res && res.success) {
          this.toast(`YouTube avto-yuklash ${newVal === '1' ? 'yoqildi' : 'o\'chirildi'}`, 'success');
          this.loadInstagram(viewport, 'youtube');
        }
      });

      document.getElementById('toggle-yt-sched-btn')?.addEventListener('click', async () => {
        const newVal = settings.youtube_schedule_enabled === '1' ? '0' : '1';
        const res = await this.api('/api/instagram/settings', 'POST', { youtube_schedule_enabled: newVal });
        if (res && res.success) {
          this.toast(`YouTube jadvali ${newVal === '1' ? 'yoqildi' : 'o\'chirildi'}`, 'success');
          this.loadInstagram(viewport, 'youtube');
        }
      });

      document.getElementById('btn-manual-yt-upload')?.addEventListener('click', async () => {
        const btn = document.getElementById('btn-manual-yt-upload');
        btn.disabled = true;
        this.showActionLoader({
          title: "YouTube Shorts ga Yuklanmoqda...",
          subtitle: "Navbatdagi video YouTube v3 API orqali Shorts formatida yuklanmoqda",
          icon: this.icons.youtube,
          steps: [
            "Video fayl manbasi olinmoqda",
            "HD video serverga yuklab olinmoqda",
            "YouTube v3 API bilan avtorizatsiya tasdiqlanmoqda",
            "Shorts sarlavha va hashtaglar bilan yuklanmoqda",
            "Bulut statistikasi sinxronlanmoqda"
          ],
          funFact: "Shorts videolari rek vaqtlari bo‘yicha algoritmik ko‘rishlarni oshiradi."
        });
        try {
          const res = await this.api('/api/instagram/post_youtube', 'POST');
          this.hideActionLoader();
          if (res && res.success) {
            this.toast(`Video YouTube Shorts ga muvaffaqiyatli yuklandi!`, 'success');
            this.loadInstagram(viewport, 'youtube');
          } else {
            this.toast((res && res.error) || (res && res.message) || 'Yuklashda xatolik', 'error');
            btn.disabled = false;
          }
        } catch (e) {
          this.hideActionLoader();
          this.toast('Yuklashda xatolik', 'error');
          btn.disabled = false;
        }
      });
    };

    // TAB 3: SINXRONLASH SOZLAMALARI
    const renderSettingsTab = (container) => {
      const nightOn = settings.night_mode_enabled !== '0'; // default true
      const nightStart = settings.night_mode_start || '00:00';
      const nightEnd = settings.night_mode_end || '07:00';

      container.innerHTML = `
        <div class="glass-card" style="max-width:850px;margin:0 auto;">
          <div class="card-title" style="display:flex;align-items:center;gap:8px;">
            ${this.icons.settings} Instagram & AutoPoster Tizim Sozlamalari
          </div>
          <div class="card-subtitle" style="margin-bottom:20px;">
            Instagram profili, Telegram maqsadli kanali, post oraliqlari va tungi rejimni sozlash
          </div>

          <form id="insta-settings-form">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;">
              <div class="form-group">
                <label class="form-label">Instagram Foydalanuvchi Nomi (Username)</label>
                <div class="input-container">
                  <span class="input-icon-left">${this.icons.instagram}</span>
                  <input type="text" id="sett-insta-username" class="input-control" value="${settings.insta_username || ''}" placeholder="Masalan: shahrisabz_t_t_uz" required>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:4px;">
                  @ belgisisiz profil nomini kiriting
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Telegram Maqsadli Chat / Kanal ID</label>
                <div class="input-container">
                  <span class="input-icon-left">${this.icons.send}</span>
                  <input type="text" id="sett-target-chat" class="input-control" value="${settings.target_chat_id || ''}" placeholder="Masalan: -100123456789 yoki @kanal" required>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:4px;">
                  Postlar boradigan shaxsiy chat yoki kanal ID si
                </div>
              </div>
            </div>

            <div class="form-group" style="margin-bottom:16px;">
              <label class="form-label">Telegram Bot Token</label>
              <div class="input-container">
                <span class="input-icon-left">${this.icons.lock}</span>
                <input type="text" id="sett-bot-token" class="input-control font-mono" value="${settings.bot_token || ''}" placeholder="8818017813:AAE..." required>
              </div>
              <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:4px;">
                Postlarni yuboruvchi asosiy bot tokeni
              </div>
            </div>

            <!-- INSTAGRAM SESSION ID COOKIE FOR FULL 99+ POSTS SCAN -->
            <div class="form-group" style="margin-bottom:16px;padding:14px;background:rgba(236,72,153,0.06);border-radius:var(--radius-md);border:1px solid rgba(236,72,153,0.25);">
              <label class="form-label" style="color:#f472b6;display:flex;align-items:center;gap:6px;">
                <svg style="width:14px;height:14px;fill:none;stroke:#f472b6;stroke-width:2;" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Instagram Session ID (Cookie) — Barcha postlarni to'liq skanerlash uchun
              </label>
              <div class="input-container">
                <span class="input-icon-left">${this.icons.lock}</span>
                <input type="text" id="sett-insta-session-id" class="input-control font-mono" value="${settings.insta_session_id || ''}" placeholder="Masalan: 7654321%3ABz...">
              </div>
              <div style="font-size:11px;color:rgba(255,255,255,0.6);margin-top:5px;">
                Instagram anti-bot (429) cheklovini aylanib o'tib, profilning barcha postlarini to'liq tortib olish uchun ishlatiladi.
              </div>
            </div>

            <!-- TELEGRAM INTERVAL & GENERAL TOGGLES -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;padding:16px;background:rgba(255,255,255,0.03);border-radius:var(--radius-md);border:1px solid var(--border-glass);">
              <div>
                <label class="form-label">Telegram Avto-yuborish Oralig'i (Daqiqalarda)</label>
                <div class="input-container">
                  <span class="input-icon-left">${this.icons.clock}</span>
                  <input type="number" min="5" max="1440" id="sett-interval" class="input-control" value="${settings.interval_minutes || 60}" required>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:4px;">
                  Har necha daqiqada navbatdagi 1 ta post Telegramga chiqsin (Standart: 60)
                </div>
              </div>

              <div style="display:flex;flex-direction:column;justify-content:center;gap:10px;">
                <label style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13px;color:#ffffff;">
                  <input type="checkbox" id="sett-tg-auto-chk" ${tgAuto ? 'checked' : ''} style="width:16px;height:16px;accent-color:var(--accent-glow);">
                  <span>Telegram avtomatik rejali yuborish faol</span>
                </label>

                <label style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13px;color:#ffffff;">
                  <input type="checkbox" id="sett-yt-auto-chk" ${ytAuto ? 'checked' : ''} style="width:16px;height:16px;accent-color:var(--accent-glow);">
                  <span>YouTube Shorts avto-yuklash faol</span>
                </label>
              </div>
            </div>

            <!-- TELEGRAM TUNGI REJIM (QUIET HOURS: 00:00 - 07:00) -->
            <div style="margin-bottom:20px;padding:16px;background:rgba(99,102,241,0.07);border-radius:var(--radius-md);border:1px solid rgba(99,102,241,0.25);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div>
                  <div style="font-size:14px;font-weight:700;color:#ffffff;display:flex;align-items:center;gap:6px;">
                    <svg style="width:14px;height:14px;fill:none;stroke:#818cf8;stroke-width:2;" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg> Telegram Tungi Sokinlik Rejimi
                  </div>
                  <div style="font-size:11px;color:rgba(255,255,255,0.6);margin-top:2px;">
                    Tungi vaqtda obunachilarni bezovta qilmaslik uchun Telegramga post yuborishni to'xtatib turish
                  </div>
                </div>
                <label style="display:flex;align-items:center;gap:8px;cursor:pointer;font-size:13px;color:#ffffff;">
                  <input type="checkbox" id="sett-night-mode-chk" ${nightOn ? 'checked' : ''} style="width:18px;height:18px;accent-color:#818cf8;">
                  <span style="font-weight:600;">Rejimni yoqish</span>
                </label>
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:center;">
                <div>
                  <label class="form-label" style="font-size:12px;">Boshlanish vaqti</label>
                  <input type="text" id="sett-night-start" class="input-control font-mono" value="${nightStart}" placeholder="00:00" style="max-width:140px;" required>
                </div>
                <div>
                  <label class="form-label" style="font-size:12px;">Tugash vaqti (Ertalab davom etadi)</label>
                  <input type="text" id="sett-night-end" class="input-control font-mono" value="${nightEnd}" placeholder="07:00" style="max-width:140px;" required>
                </div>
              </div>
              <div style="font-size:11px;color:rgba(255,255,255,0.5);margin-top:8px;">
                ℹ️ Belgilangan oraliqda (<b>${nightStart} dan ${nightEnd} gacha</b>) bot hech qanday post chiqarmaydi va ertalab <b>${nightEnd}</b> dan boshlab avtomatik davom ettiradi.
              </div>
            </div>

            <div style="display:flex;justify-content:flex-end;gap:10px;">
              <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.loadInstagram(document.getElementById('content-viewport'), 'settings')">
                Bekor qilish
              </button>
              <button type="submit" class="btn-sm btn-primary">
                ${this.icons.save} <span>Sozlamalarni Saqlash</span>
              </button>
            </div>
          </form>
        </div>
      `;

      document.getElementById('insta-settings-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
          insta_username: document.getElementById('sett-insta-username').value.trim(),
          target_chat_id: document.getElementById('sett-target-chat').value.trim(),
          bot_token: document.getElementById('sett-bot-token').value.trim(),
          insta_session_id: document.getElementById('sett-insta-session-id') ? document.getElementById('sett-insta-session-id').value.trim() : '',
          interval_minutes: document.getElementById('sett-interval').value.trim(),
          auto_schedule_enabled: document.getElementById('sett-tg-auto-chk').checked ? '1' : '0',
          youtube_auto_upload: document.getElementById('sett-yt-auto-chk').checked ? '1' : '0',
          youtube_schedule_enabled: document.getElementById('sett-yt-auto-chk').checked ? '1' : '0',
          night_mode_enabled: document.getElementById('sett-night-mode-chk').checked ? '1' : '0',
          night_mode_start: document.getElementById('sett-night-start').value.trim() || '00:00',
          night_mode_end: document.getElementById('sett-night-end').value.trim() || '07:00'
        };

        const res = await this.api('/api/instagram/settings', 'POST', payload);
        if (res && res.success) {
          this.toast("Instagram sozlamalari va tungi rejim muvaffaqiyatli saqlandi!", 'success');
          this.loadInstagram(viewport, 'settings');
        } else {
          this.toast((res && res.error) || 'Saqlashda xatolik', 'error');
        }
      });
    };

    render();
  },

  // Modal: Instagramdan Skanerlash yoki Havolalar Qo'shish
  renderScanModal(defaultUsername, viewport) {
    this.modal({
      title: "Instagram Postlarini Navbatga Qo'shish",
      contentHtml: `
        <div style="display:flex;gap:10px;margin-bottom:16px;border-bottom:1px solid var(--border-glass);padding-bottom:10px;">
          <button type="button" class="btn-sm btn-primary" id="tab-btn-auto-scan" style="flex:1;">
            ${this.icons.download} <span>Avtomatik Skanerlash</span>
          </button>
          <button type="button" class="btn-sm btn-secondary" id="tab-btn-manual-links" style="flex:1;">
            ${this.icons.plus} <span>Havolalar Qo'shish</span>
          </button>
        </div>

        <!-- 1. Avtomatik Skanerlash Formasi -->
        <form id="insta-scan-modal-form">
          <p style="font-size:13px;color:rgba(255,255,255,0.75);margin-bottom:14px;line-height:1.5;">
            Instagram sahifasidagi barcha postlar va reels videolari Playwright yordamida skanerlanib, <b>eng eskisidan yangisiga</b> qarab navbatga olinadi. Dublikat bo'lmaydi.
          </p>

          <div class="form-group" style="margin-bottom:16px;">
            <label class="form-label">Instagram Foydalanuvchi Nomi (Username)</label>
            <div class="input-container">
              <span class="input-icon-left">${this.icons.instagram}</span>
              <input type="text" id="modal-scan-username" class="input-control" value="${defaultUsername || 'shahrisabz_t_t_uz'}" required>
            </div>
          </div>

          <div style="padding:10px 14px;background:rgba(20,184,166,0.1);border:1px solid rgba(20,184,166,0.25);border-radius:var(--radius-sm);font-size:12px;color:rgba(255,255,255,0.8);margin-bottom:18px;">
            Skanerlash jarayoni fonda boshlanadi. Profil postlarini to‘g‘ridan-to‘g‘ri qo‘shish uchun <b>Havolalar Qo'shish</b> bo'limidan ham foydalanishingiz mumkin.
          </div>

          <div style="display:flex;justify-content:flex-end;gap:10px;">
            <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
            <button type="submit" class="btn-sm btn-primary" id="btn-start-scan-submit">
              ${this.icons.download} <span>Skanerlashni Boshlash</span>
            </button>
          </div>
        </form>

        <!-- 2. Havolalarni Qo'lda / Ommaviy Kiritish Formasi -->
        <form id="insta-manual-links-form" style="display:none;">
          <p style="font-size:13px;color:rgba(255,255,255,0.75);margin-bottom:14px;line-height:1.5;">
            Instagram postlari yoki Reels havolalarini (yoki shortcode'larini) bittalab yoki har bir qatorga bittadan kiriting. Tizim ularni avtomatik ajratib olib navbatga joylaydi.
          </p>

          <div class="form-group" style="margin-bottom:16px;">
            <label class="form-label">Instagram Post / Reel Havolalari</label>
            <textarea id="modal-manual-urls" class="input-control font-mono" rows="6" placeholder="Masalan:&#10;https://www.instagram.com/reel/DcLkGzAqbz9/&#10;https://www.instagram.com/reel/DcLj3zwqODC/&#10;https://www.instagram.com/p/Db0U9ivIcwC/" required style="resize:vertical;"></textarea>
          </div>

          <div style="display:flex;justify-content:flex-end;gap:10px;">
            <button type="button" class="btn-sm btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
            <button type="submit" class="btn-sm btn-primary" id="btn-manual-links-submit">
              ${this.icons.save} <span>Navbatga Qo'shish</span>
            </button>
          </div>
        </form>
      `
    });

    // Tab switcher
    const tabAuto = document.getElementById('tab-btn-auto-scan');
    const tabManual = document.getElementById('tab-btn-manual-links');
    const formAuto = document.getElementById('insta-scan-modal-form');
    const formManual = document.getElementById('insta-manual-links-form');

    tabAuto?.addEventListener('click', () => {
      tabAuto.className = 'btn-sm btn-primary';
      tabManual.className = 'btn-sm btn-secondary';
      formAuto.style.display = 'block';
      formManual.style.display = 'none';
    });

    tabManual?.addEventListener('click', () => {
      tabManual.className = 'btn-sm btn-primary';
      tabAuto.className = 'btn-sm btn-secondary';
      formManual.style.display = 'block';
      formAuto.style.display = 'none';
    });

    // Submit 1: Auto Scan
    formAuto?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const u = document.getElementById('modal-scan-username').value.trim().replace(/^@/, '');
      if (!u) {
        this.toast('Instagram username kiriting', 'error');
        return;
      }

      const submitBtn = document.getElementById('btn-start-scan-submit');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-sm"></span> Jarayon boshlanmoqda...`;
      }

      const res = await this.api('/api/instagram/scan', 'POST', { username: u });
      if (res && res.success) {
        this.closeModal();
        this.toast(res.message || `@${u} profili skanerlanishi fonda boshlandi!`, 'success');
        this.loadInstagram(viewport);
      } else {
        this.toast((res && res.error) || 'Skanerlashda xatolik', 'error');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `${this.icons.download} <span>Skanerlashni Boshlash</span>`;
        }
      }
    });

    // Submit 2: Manual Links
    formManual?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const urls = document.getElementById('modal-manual-urls').value.trim();
      if (!urls) {
        this.toast('Kamida 1 ta havola kiriting', 'error');
        return;
      }

      const submitBtn = document.getElementById('btn-manual-links-submit');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-sm"></span> Qo'shilmoqda...`;
      }

      const res = await this.api('/api/instagram/queue/add_urls', 'POST', { urls: urls });
      if (res && res.success) {
        this.closeModal();
        this.toast(res.message || 'Postlar navbatga qo‘shildi!', 'success');
        this.loadInstagram(viewport);
      } else {
        this.toast((res && res.error) || 'Qo‘shishda xatolik', 'error');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `${this.icons.save} <span>Navbatga Qo'shish</span>`;
        }
      }
    });
  },

  renderAddUrlModal(viewport) {
    this.modal({
      title: `Instagram Havolasi Bilan Navbatga Qo'shish`,
      maxWidth: '540px',
      contentHtml: `
        <p style="font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:14px;line-height:1.5;">
          Instagram post yoki reel havolasini kiriting. Bir vaqtda bir nechta havolalarni har birini yangi qatordan kiritishingiz mumkin:
        </p>
        <form id="form-direct-add-url">
          <div class="form-group" style="margin-bottom:18px;">
            <textarea id="direct-add-urls-input" class="input-control" rows="4" style="font-family:'JetBrains Mono',monospace;font-size:12px;width:100%;resize:vertical;" placeholder="https://www.instagram.com/reel/DTNEIiLCBPn/&#10;https://www.instagram.com/reel/DTVcl6SCM8c/" required></textarea>
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px;">
            <button type="button" class="btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
            <button type="submit" class="btn-primary" id="btn-submit-direct-add-url">
              ${this.icons.plus || '+'} <span>Navbatga Qo'shish</span>
            </button>
          </div>
        </form>
      `
    });

    document.getElementById('form-direct-add-url')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const urls = document.getElementById('direct-add-urls-input').value.trim();
      if (!urls) {
        this.toast('Kamida 1 ta havola kiriting', 'error');
        return;
      }
      const btn = document.getElementById('btn-submit-direct-add-url');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span class="spinner-sm"></span> Qo'shilmoqda...`;
      }
      const res = await this.api('/api/instagram/queue/add_urls', 'POST', { urls: urls });
      if (res && res.success) {
        this.closeModal();
        this.toast(res.message || 'Postlar navbatga muvaffaqiyatli qo‘shildi!', 'success');
        this.loadInstagram(viewport);
      } else {
        this.toast((res && res.error) || 'Qo‘shishda xatolik', 'error');
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = `${this.icons.plus || '+'} <span>Navbatga Qo'shish</span>`;
        }
      }
    });
  },

  // ============================================================
  // 9. KOMPYUTER & PC AGENT VIEW
  // ============================================================
  async loadPcControl(viewport) {
    viewport.innerHTML = `
      <div class="contracts-page">
        <!-- HEADER -->
        <div class="content-header-card" style="background:linear-gradient(135deg, rgba(0, 242, 254, 0.08) 0%, rgba(13, 17, 23, 0.95) 100%);border:1px solid rgba(0, 242, 254, 0.2);padding:20px;border-radius:12px;margin-bottom:20px;">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
              <h2 style="margin:0 0 4px 0;font-size:20px;font-weight:800;color:#fff;display:flex;align-items:center;gap:10px;">
                <span style="color:#00f2fe;">💻</span> Kompyuter Boshqaruvi & AI Agent
                <span class="badge" id="pc-connection-badge" style="background:rgba(0,242,254,0.15);color:#00f2fe;border:1px solid rgba(0,242,254,0.3);font-size:11px;">PC AGENT v2.3</span>
              </h2>
              <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.6);">
                Shaxsiy Windows kompyuteringizni masofadan to'liq boshqarish, monitoring qilish va AI agenti
              </p>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="badge" id="pc-auto-refresh-badge" style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:11px;display:flex;align-items:center;gap:6px;padding:6px 10px;border-radius:8px;">
                <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#10b981;"></span>
                <span>Avto-yangilanish: 5s</span>
              </span>
              <button class="btn-secondary btn-sm" id="btn-refresh-pc-status" style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#fff;border-radius:8px;padding:6px 14px;cursor:pointer;">
                ${this.icons.refresh} <span>Yangilash</span>
              </button>
            </div>
          </div>
        </div>

        <!-- LIVE SYSTEM GAUGES & METRICS -->
        <div id="pc-metrics-grid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:16px;margin:20px 0;">
          <div class="card" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);padding:16px;border-radius:12px;">
            <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:8px;display:flex;justify-content:space-between;">
              <span>CPU Yuklanishi</span> <span id="pc-val-cpu-cores">4 yadro</span>
            </div>
            <div style="font-size:24px;font-weight:800;color:#00f2fe;" id="pc-val-cpu">--%</div>
            <div style="background:rgba(255,255,255,0.1);height:6px;border-radius:3px;margin-top:10px;overflow:hidden;">
              <div id="pc-bar-cpu" style="background:#00f2fe;height:100%;width:0%;transition:width 0.4s;"></div>
            </div>
          </div>

          <div class="card" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);padding:16px;border-radius:12px;">
            <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:8px;display:flex;justify-content:space-between;">
              <span>RAM Xotira</span> <span id="pc-val-ram-gb">-- / -- GB</span>
            </div>
            <div style="font-size:24px;font-weight:800;color:#10b981;" id="pc-val-ram">--%</div>
            <div style="background:rgba(255,255,255,0.1);height:6px;border-radius:3px;margin-top:10px;overflow:hidden;">
              <div id="pc-bar-ram" style="background:#10b981;height:100%;width:0%;transition:width 0.4s;"></div>
            </div>
          </div>

          <div class="card" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);padding:16px;border-radius:12px;">
            <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:8px;display:flex;justify-content:space-between;">
              <span>C: Diski</span> <span id="pc-val-disk-c-gb">-- GB bo'sh</span>
            </div>
            <div style="font-size:24px;font-weight:800;color:#f59e0b;" id="pc-val-disk-c">--%</div>
            <div style="background:rgba(255,255,255,0.1);height:6px;border-radius:3px;margin-top:10px;overflow:hidden;">
              <div id="pc-bar-disk-c" style="background:#f59e0b;height:100%;width:0%;transition:width 0.4s;"></div>
            </div>
          </div>

          <div class="card" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);padding:16px;border-radius:12px;">
            <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:8px;display:flex;justify-content:space-between;">
              <span>Uptime & Quvvat</span> <span id="pc-val-host">Windows-PC</span>
            </div>
            <div style="font-size:18px;font-weight:700;color:#a78bfa;margin-top:4px;" id="pc-val-uptime">--:--:--</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:8px;" id="pc-val-battery">🔌 Tarmoqqa ulangan</div>
          </div>
        </div>

        <!-- INFO BANNER -->
        <div style="background:rgba(0,242,254,0.05);border:1px solid rgba(0,242,254,0.2);border-radius:10px;padding:12px 16px;margin-bottom:18px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
          <div style="font-size:13px;color:rgba(255,255,255,0.85);display:flex;align-items:center;gap:8px;">
            <span style="font-size:16px;">💡</span>
            <span><b>Kompyuterni bevosita boshqarish:</b> Kompyuteringizda bot yoki lokal server ishlab turganda barcha amallar (skrinshot, veb-kamera, dasturlar) 100% real vaqtda bajariladi.</span>
          </div>
          <button class="btn-secondary btn-sm" id="btn-pc-sunshine-pin" style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.4);color:#f59e0b;font-weight:700;padding:6px 14px;border-radius:8px;cursor:pointer;">
            ☀️ <span>Sunshine PIN Ulanish</span>
          </button>
        </div>

        <!-- QUICK CONTROL ACTIONS GRID -->
        <div style="margin-bottom:24px;">
          <h3 style="font-size:15px;font-weight:700;color:rgba(255,255,255,0.85);margin-bottom:12px;">⚡ Tezkor Boshqaruv Buyruqlari</h3>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(170px, 1fr));gap:12px;">
            <button class="btn-secondary" id="btn-pc-take-screenshot" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(0,242,254,0.08);border:1px solid rgba(0,242,254,0.3);color:#00f2fe;font-weight:700;border-radius:10px;cursor:pointer;">
              📸 <span>Skrinshot Olish</span>
            </button>
            <button class="btn-secondary" id="btn-pc-take-webcam" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(236,72,153,0.08);border:1px solid rgba(236,72,153,0.3);color:#ec4899;font-weight:700;border-radius:10px;cursor:pointer;">
              📷 <span>Veb-kamera Surat</span>
            </button>
            <button class="btn-secondary" id="btn-pc-sunshine-btn" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);color:#f59e0b;font-weight:700;border-radius:10px;cursor:pointer;">
              ☀️ <span>Sunshine / Moonlight</span>
            </button>
            <button class="btn-secondary" id="btn-pc-show-desktop" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.3);color:#a78bfa;font-weight:700;border-radius:10px;cursor:pointer;">
              🖥 <span>Ish Stoli (Win+D)</span>
            </button>
            <button class="btn-secondary" id="btn-pc-clean-temp" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.3);color:#10b981;font-weight:700;border-radius:10px;cursor:pointer;">
              🧹 <span>Temp Kesh Tozalash</span>
            </button>
            <button class="btn-secondary" id="btn-pc-clean-recycle" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);color:#f59e0b;font-weight:700;border-radius:10px;cursor:pointer;">
              🗑 <span>Korzinani Tozalash</span>
            </button>
            <button class="btn-secondary" id="btn-pc-unlock-screen" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.3);color:#34d399;font-weight:700;border-radius:10px;cursor:pointer;">
              🔓 <span>Ekranni Uyg'otish / Qulfdan Chiqarish</span>
            </button>
            <button class="btn-secondary" id="btn-pc-power-menu" style="display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);color:#ef4444;font-weight:700;border-radius:10px;cursor:pointer;">
              ⚡ <span>Quvvat Menyusi</span>
            </button>
          </div>
        </div>

        <!-- SECTION: COMPACT RUNNING APPS & AI AGENT BANNER -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(340px, 1fr));gap:16px;margin-bottom:20px;">
          <!-- COMPACT RUNNING APPS -->
          <div class="card" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:16px;display:flex;flex-direction:column;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
              <h3 style="margin:0;font-size:14px;font-weight:700;color:#fff;display:flex;align-items:center;gap:6px;">
                🎮 <span>Faol Dasturlar (Top RAM)</span>
              </h3>
              <button class="btn-secondary btn-sm" id="btn-refresh-apps" style="font-size:11px;padding:3px 8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#fff;border-radius:6px;cursor:pointer;">
                ${this.icons.refresh} <span>Yangilash</span>
              </button>
            </div>
            <div id="pc-apps-list-wrap" style="flex:1;max-height:210px;overflow-y:auto;font-size:12px;">
              <div style="display:flex;align-items:center;justify-content:center;height:80px;"><div class="spinner-sm"></div></div>
            </div>
          </div>

          <!-- DEDICATED AI AGENT PROMO CARD -->
          <div class="card" style="background:linear-gradient(135deg, rgba(168,85,247,0.12) 0%, rgba(99,102,241,0.08) 100%);border:1px solid rgba(168,85,247,0.3);border-radius:12px;padding:20px;display:flex;flex-direction:column;justify-content:space-between;">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <div style="font-size:16px;font-weight:800;color:#c084fc;display:flex;align-items:center;gap:8px;">
                  <span>🧠</span> <span>AI PC Agent & Suhbat Markazi</span>
                </div>
                <span class="badge" style="background:rgba(168,85,247,0.2);color:#c084fc;font-size:10px;padding:2px 8px;border-radius:4px;">YANGI BO'LIM</span>
              </div>
              <p style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.5;margin:0 0 14px 0;">
                Kompyuteringizni tabiiy o'zbek tilidagi buyruqlar orqali boshqaring: AnyDesk IDni aniqlash, skrinshot olish, ilovalarni ochish, tizimni tozalash va ko'proq.
              </p>
            </div>
            <button type="button" class="btn-primary" id="btn-goto-ai-chat" style="background:linear-gradient(135deg, #a855f7 0%, #6366f1 100%);border:none;padding:12px 20px;border-radius:10px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;box-shadow:0 4px 16px rgba(168,85,247,0.35);">
              <span>🧠 AI Agent Suhbat Bo'limiga O'tish</span>
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>
      </div>
    `;

    // Clear previous timer
    if (this._pcAutoRefreshTimer) clearInterval(this._pcAutoRefreshTimer);

    // Fetch initial status and apps
    this.refreshPcStatus();
    this.refreshPcApps();

    // Auto-refresh timer
    this._pcAutoRefreshTimer = setInterval(() => {
      if (document.getElementById('pc-metrics-grid')) {
        this.refreshPcStatus();
      } else {
        clearInterval(this._pcAutoRefreshTimer);
      }
    }, 5000);

    // Event Listeners
    document.getElementById('btn-refresh-pc-status')?.addEventListener('click', () => this.refreshPcStatus());
    document.getElementById('btn-refresh-apps')?.addEventListener('click', () => this.refreshPcApps());

    // Screenshot
    document.getElementById('btn-pc-take-screenshot')?.addEventListener('click', async () => {
      const btn = document.getElementById('btn-pc-take-screenshot');
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-sm"></span> <span>Olinmoqda...</span>`;
      const res = await this.api('/api/pc/screenshot', 'POST');
      btn.disabled = false;
      btn.innerHTML = `📸 <span>Skrinshot Olish</span>`;

      if (res && res.success && (res.image || (res.monitors && res.monitors.length))) {
        const monitors = (res.monitors && res.monitors.length > 0) ? res.monitors : [{ id: 1, name: '1-Monitor (Asosiy)', width: 1920, height: 1080, image: res.image }];

        const renderModalHtml = (activeIdx) => {
          const cur = monitors[activeIdx] || monitors[0];
          return `
            <div id="pc-screenshot-container">
              ${monitors.length > 1 ? `
                <div style="display:flex;gap:8px;margin-bottom:14px;background:rgba(255,255,255,0.04);padding:6px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);justify-content:center;flex-wrap:wrap;">
                  ${monitors.map((m, idx) => `
                    <button type="button" class="btn-mon-switch" data-idx="${idx}" style="background:${idx === activeIdx ? 'linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)' : 'rgba(255,255,255,0.06)'};color:${idx === activeIdx ? '#000' : '#fff'};border:1px solid ${idx === activeIdx ? '#00f2fe' : 'rgba(255,255,255,0.1)'};padding:6px 16px;border-radius:6px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;font-size:12px;transition:all 0.2s;">
                      🖥️ <span>${m.name || `${idx + 1}-Monitor`}</span>
                    </button>
                  `).join('')}
                </div>
              ` : ''}
              <div style="text-align:center;">
                <div style="background:#000;border-radius:8px;padding:4px;border:1px solid rgba(255,255,255,0.1);box-shadow:0 8px 24px rgba(0,0,0,0.6);margin-bottom:14px;">
                  <img id="active-mon-img" src="${cur.image}" style="max-width:100%;max-height:65vh;border-radius:6px;display:block;margin:0 auto;object-fit:contain;" />
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                  <span style="font-size:12px;color:rgba(255,255,255,0.6);">
                    🖥️ <b>${cur.name || ''}</b> &nbsp;|&nbsp; ${cur.width || 1920}x${cur.height || 1080} px
                  </span>
                  <div style="display:flex;gap:8px;">
                    <a id="btn-download-active-mon" href="${cur.image}" download="screenshot_monitor_${cur.id || 1}_${Date.now()}.png" class="btn-primary btn-sm" style="background:#00f2fe;color:#000;font-weight:700;">Yuklab olish</a>
                    <button type="button" class="btn-secondary btn-sm" onclick="ATLAS.closeModal()">Yopish</button>
                  </div>
                </div>
              </div>
            </div>
          `;
        };

        this.modal({
          title: `🖼 Kompyuter Ekran Tasviri (${res.timestamp || ''})`,
          maxWidth: '920px',
          contentHtml: `<div id="screenshot-modal-wrapper">${renderModalHtml(0)}</div>`
        });

        const bindMonTabs = () => {
          document.querySelectorAll('.btn-mon-switch').forEach(btn => {
            btn.addEventListener('click', (e) => {
              const targetIdx = parseInt(e.currentTarget.dataset.idx, 10) || 0;
              const wrapper = document.getElementById('screenshot-modal-wrapper');
              if (wrapper) {
                wrapper.innerHTML = renderModalHtml(targetIdx);
                bindMonTabs();
              }
            });
          });
        };
        bindMonTabs();
      } else {
        this.toast((res && res.error) || 'Screenshot olishda xatolik', 'error');
      }
    });

    // Webcam
    document.getElementById('btn-pc-take-webcam')?.addEventListener('click', async () => {
      const btn = document.getElementById('btn-pc-take-webcam');
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-sm"></span> <span>Olinmoqda...</span>`;
      const res = await this.api('/api/pc/webcam', 'POST');
      btn.disabled = false;
      btn.innerHTML = `📷 <span>Veb-kamera Surat</span>`;

      if (res && res.success && res.image) {
        this.modal({
          title: `📷 Veb-kamera Surati (${res.timestamp})`,
          maxWidth: '650px',
          contentHtml: `
            <div style="text-align:center;">
              <img src="${res.image}" style="max-width:100%;border-radius:8px;border:1px solid rgba(255,255,255,0.1);box-shadow:0 8px 24px rgba(0,0,0,0.5);margin-bottom:14px;" />
              <div style="display:flex;justify-content:flex-end;gap:8px;">
                <a href="${res.image}" download="webcam_${Date.now()}.jpg" class="btn-primary btn-sm">Yuklab olish</a>
                <button class="btn-secondary btn-sm" onclick="ATLAS.closeModal()">Yopish</button>
              </div>
            </div>
          `
        });
      } else {
        this.toast((res && res.error) || 'Veb-kamera tasvirini olishda xatolik', 'error');
      }
    });

    // Desktop
    document.getElementById('btn-pc-show-desktop')?.addEventListener('click', async () => {
      await this.api('/api/pc/media', 'POST', { action: 'desktop' });
      this.toast('Ish stoli ko‘rsatildi (Win+D)', 'success');
    });

    // Sunshine PIN Pairing Modal
    const openSunshineModal = () => {
      this.modal({
        title: '☀️ Sunshine / Moonlight PIN Ulanish',
        maxWidth: '520px',
        contentHtml: `
          <p style="font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:14px;line-height:1.5;">
            Moonlight ilovasida chiqqan <b>4 xonali PIN kodni</b> kiriting. Shuningdek, Sunshine Web UI'ni brauzerda ochib ulanishingiz ham mumkin:
          </p>
          <form id="form-sunshine-pin">
            <div class="form-group" style="margin-bottom:14px;">
              <input type="text" id="input-sunshine-pin" class="input-control" placeholder="Masalan: 1234" maxlength="4" style="font-size:20px;text-align:center;letter-spacing:6px;font-weight:800;color:#f59e0b;" required autofocus>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
              <a href="https://localhost:47990/pin" target="_blank" class="btn-secondary btn-sm" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.2);color:#fff;font-size:12px;display:flex;align-items:center;gap:6px;">
                🌐 <span>Sunshine Web UI Ochish</span>
              </a>
              <div style="display:flex;gap:8px;">
                <button type="button" class="btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
                <button type="submit" class="btn-primary" id="btn-submit-sunshine-pin" style="background:#f59e0b;color:#000;font-weight:700;">
                  ☀️ <span>PIN Ulanish</span>
                </button>
              </div>
            </div>
          </form>
        `
      });

      document.getElementById('form-sunshine-pin')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const pin = document.getElementById('input-sunshine-pin').value.trim();
        if (!pin || pin.length !== 4) {
          this.toast('4 xonali PIN kod kiriting', 'error');
          return;
        }
        const btn = document.getElementById('btn-submit-sunshine-pin');
        if (btn) {
          btn.disabled = true;
          btn.innerHTML = `<span class="spinner-sm"></span> Ulanmoqda...`;
        }
        const res = await this.api('/api/pc/sunshine', 'POST', { pin });
        this.closeModal();
        if (res && res.success) {
          this.toast('Sunshine PIN kodi yuborildi!', 'success');
          this.modal({
            title: '☀️ Sunshine Natijasi',
            maxWidth: '500px',
            contentHtml: `<div style="font-size:13px;line-height:1.6;color:#fff;">${res.message}</div>`
          });
        } else {
          this.toast((res && res.error) || 'Sunshine ulanishda xatolik', 'error');
        }
      });
    };

    document.getElementById('btn-pc-sunshine-pin')?.addEventListener('click', openSunshineModal);
    document.getElementById('btn-pc-sunshine-btn')?.addEventListener('click', openSunshineModal);

    // Unlock Screen Modal
    const openUnlockModal = () => {
      this.modal({
        title: '🔓 Kompyuter Ekranini Uyg\'otish & Qulfdan Chiqarish',
        maxWidth: '480px',
        contentHtml: `
          <p style="font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:14px;line-height:1.5;">
            Kompyuteringiz Lock ekranida (qulfda) turganda yoki monitor o'chgan bo'lsa, uni masofadan uyg'otish va parolni kiritish mumkin:
          </p>
          <div style="display:flex;gap:10px;margin-bottom:16px;">
            <button type="button" class="btn-secondary btn-block" id="btn-quick-wake-display" style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.35);color:#34d399;font-weight:700;padding:10px;cursor:pointer;">
              ☀️ <span>Faqat Ekranni Uyg'otish (Spacebar)</span>
            </button>
          </div>
          <form id="form-pc-unlock-pass">
            <div class="form-group" style="margin-bottom:14px;">
              <label style="font-size:12px;color:rgba(255,255,255,0.6);margin-bottom:6px;display:block;">Windows Paroli yoki PIN (ixtiyoriy):</label>
              <input type="password" id="input-unlock-password" class="input-control" placeholder="Windows kirish paroli..." style="font-size:14px;color:#fff;">
            </div>
            <div style="display:flex;justify-content:flex-end;gap:8px;">
              <button type="button" class="btn-secondary" onclick="ATLAS.closeModal()">Bekor qilish</button>
              <button type="submit" class="btn-primary" id="btn-submit-unlock" style="background:#34d399;color:#000;font-weight:700;cursor:pointer;">
                🔓 <span>Qulfdan Chiqarish</span>
              </button>
            </div>
          </form>
        `
      });

      document.getElementById('btn-quick-wake-display')?.addEventListener('click', async () => {
        const res = await this.api('/api/pc/unlock', 'POST', {});
        this.closeModal();
        this.toast((res && res.message) || 'Ekran uyg\'otildi', 'success');
      });

      document.getElementById('form-pc-unlock-pass')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const pwd = document.getElementById('input-unlock-password').value;
        const res = await this.api('/api/pc/unlock', 'POST', { password: pwd });
        this.closeModal();
        this.toast((res && res.message) || 'Buyruq yuborildi', 'success');
      });
    };

    document.getElementById('btn-pc-unlock-screen')?.addEventListener('click', openUnlockModal);

    // Cleanup Temp
    document.getElementById('btn-pc-clean-temp')?.addEventListener('click', async () => {
      const res = await this.api('/api/pc/cleanup', 'POST', { type: 'temp' });
      this.toast((res && res.message) || 'Temp kesh tozalandi', 'success');
      this.refreshPcStatus();
    });

    // Cleanup Recycle
    document.getElementById('btn-pc-clean-recycle')?.addEventListener('click', async () => {
      const res = await this.api('/api/pc/cleanup', 'POST', { type: 'recycle' });
      this.toast((res && res.message) || 'Korzina tozalandi', 'success');
    });

    // Power Menu Modal
    document.getElementById('btn-pc-power-menu')?.addEventListener('click', () => {
      this.modal({
        title: '⚡ Kompyuter Quvvatini Boshqarish',
        maxWidth: '480px',
        contentHtml: `
          <p style="font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:16px;">
            Quyidagi quvvat amallaridan birini tanlang:
          </p>
          <div style="display:flex;flex-direction:column;gap:10px;">
            <button class="btn-danger" id="modal-btn-power-shutdown" style="padding:10px;text-align:left;font-weight:700;background:#ef4444;color:#fff;border:none;border-radius:6px;cursor:pointer;">⚡ Kompyuterni O'chirish (Shutdown)</button>
            <button class="btn-secondary" id="modal-btn-power-restart" style="padding:10px;text-align:left;font-weight:700;color:#f59e0b;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);border-radius:6px;cursor:pointer;">🔄 Qayta Yuklash (Restart)</button>
            <button class="btn-secondary" id="modal-btn-power-sleep" style="padding:10px;text-align:left;font-weight:700;color:#00f2fe;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);border-radius:6px;cursor:pointer;">🌙 Uyqu Rejimi (Sleep)</button>
            <button class="btn-secondary" id="modal-btn-power-lock" style="padding:10px;text-align:left;font-weight:700;color:#a78bfa;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);border-radius:6px;cursor:pointer;">🔒 Ekranni Qulflash (Lock)</button>
            <button class="btn-secondary" id="modal-btn-power-cancel" style="padding:10px;text-align:left;font-weight:700;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);border-radius:6px;cursor:pointer;">❌ Rejalashtirilgan o'chirishni bekor qilish</button>
          </div>
        `
      });

      const handlePowerAction = async (action, confirmMsg) => {
        if (confirmMsg && !confirm(confirmMsg)) return;
        const res = await this.api('/api/pc/power', 'POST', { action });
        this.closeModal();
        this.toast((res && res.message) || 'Amal bajarildi', 'info');
      };

      document.getElementById('modal-btn-power-shutdown')?.addEventListener('click', () => handlePowerAction('shutdown', 'Haqiqatdan ham kompyuterni o‘chirmoqchimisiz?'));
      document.getElementById('modal-btn-power-restart')?.addEventListener('click', () => handlePowerAction('restart', 'Kompyuterni qayta yuklamoqchimisiz?'));
      document.getElementById('modal-btn-power-sleep')?.addEventListener('click', () => handlePowerAction('sleep'));
      document.getElementById('modal-btn-power-lock')?.addEventListener('click', () => handlePowerAction('lock'));
      document.getElementById('modal-btn-power-cancel')?.addEventListener('click', () => handlePowerAction('cancel'));
    });

    // Go to dedicated AI Chat
    document.getElementById('btn-goto-ai-chat')?.addEventListener('click', () => {
      this.navigate('ai_chat');
    });
  },

  // ============================================================
  // 10. DEDICATED AI PC AGENT CHAT VIEW
  // ============================================================
  loadAiChat(viewport) {
    if (!this._aiChatHistory || this._aiChatHistory.length === 0) {
      this._aiChatHistory = [
        {
          role: 'assistant',
          text: 'Assalomu alaykum! Men sizning shaxsiy <b>ATLAS AI PC Agenti</b>man. Windows kompyuteringizni masofadan to\'liq boshqarishim, AnyDesk IDni aniqlashim, ilovalarni ochishim, skrinshot olishim va savollaringizga javob berishim mumkin.',
          badge: 'DEEPSEEK V3 / LLAMA 3.1',
          time: new Date().toLocaleTimeString().slice(0, 5)
        }
      ];
    }

    viewport.innerHTML = `
      <div class="contracts-page">
        <!-- HEADER -->
        <div class="content-header-card" style="background:linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(13, 17, 23, 0.95) 100%);border:1px solid rgba(168, 85, 247, 0.25);padding:20px;border-radius:12px;margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
              <h2 style="margin:0 0 4px 0;font-size:20px;font-weight:800;color:#fff;display:flex;align-items:center;gap:10px;">
                <span style="color:#a855f7;">🧠</span> ATLAS AI PC Agent & Suhbat Markazi
                <span class="badge" style="background:rgba(168,85,247,0.18);color:#c084fc;border:1px solid rgba(168,85,247,0.35);font-size:11px;">DEEPSEEK V3 / LLAMA 3.1</span>
              </h2>
              <p style="margin:0;font-size:13px;color:rgba(255,255,255,0.6);">
                Windows kompyuteringizni tabiiy o'zbek tilidagi yozma yoki ovozli buyruqlar bilan to'liq boshqaring
              </p>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <button class="btn-secondary btn-sm" id="btn-back-to-pc" style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#fff;border-radius:8px;padding:6px 14px;cursor:pointer;">
                💻 <span>PC Paneli</span>
              </button>
              <button class="btn-secondary btn-sm" id="btn-clear-ai-history" style="display:flex;align-items:center;gap:6px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);color:#f87171;border-radius:8px;padding:6px 14px;cursor:pointer;">
                🗑 <span>Tarixni tozalash</span>
              </button>
            </div>
          </div>
        </div>

        <!-- QUICK ACTION CHIPS -->
        <div style="display:flex;gap:8px;overflow-x:auto;padding-bottom:8px;margin-bottom:14px;scrollbar-width:none;">
          <button class="ai-chip-btn" data-prompt="AnyDesk dasturini ishga tushurib, ID raqamini aniqlab ber" style="white-space:nowrap;padding:7px 14px;border-radius:20px;background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);color:#fbbf24;font-size:12px;font-weight:600;cursor:pointer;">
            ⚡ AnyDesk IDni aniqlab ber
          </button>
          <button class="ai-chip-btn" data-prompt="Ekrandan to'liq skrinshot olib ko'rsat" style="white-space:nowrap;padding:7px 14px;border-radius:20px;background:rgba(0,242,254,0.12);border:1px solid rgba(0,242,254,0.3);color:#00f2fe;font-size:12px;font-weight:600;cursor:pointer;">
            📸 Skrinshot ol
          </button>
          <button class="ai-chip-btn" data-prompt="Kompyuter protsessor va RAM holatini aytib ber" style="white-space:nowrap;padding:7px 14px;border-radius:20px;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);color:#34d399;font-size:12px;font-weight:600;cursor:pointer;">
            📊 Kompyuter holati
          </button>
          <button class="ai-chip-btn" data-prompt="Vaqtinchalik temp fayllar va korzinani tozalab ber" style="white-space:nowrap;padding:7px 14px;border-radius:20px;background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.3);color:#a78bfa;font-size:12px;font-weight:600;cursor:pointer;">
            🧹 Kesh va korzinani tozala
          </button>
          <button class="ai-chip-btn" data-prompt="Barcha oynalarni yashirib ish stolini ko'rsat (Win+D)" style="white-space:nowrap;padding:7px 14px;border-radius:20px;background:rgba(236,72,153,0.12);border:1px solid rgba(236,72,153,0.3);color:#f472b6;font-size:12px;font-weight:600;cursor:pointer;">
            🖥 Ish stolini ko'rsat
          </button>
          <button class="ai-chip-btn" data-prompt="Kalkulyator dasturini och" style="white-space:nowrap;padding:7px 14px;border-radius:20px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);color:#fff;font-size:12px;font-weight:600;cursor:pointer;">
            🧮 Kalkulyatorni och
          </button>
        </div>

        <!-- FULL CHAT BOX -->
        <div class="card" style="background:rgba(13,17,23,0.94);border:1px solid rgba(255,255,255,0.08);border-radius:14px;display:flex;flex-direction:column;min-height:550px;max-height:72vh;overflow:hidden;box-shadow:0 12px 36px rgba(0,0,0,0.5);">
          <!-- CHAT MESSAGES CONTAINER -->
          <div id="ai-chat-messages-box" style="flex:1;overflow-y:auto;padding:22px;display:flex;flex-direction:column;gap:16px;">
            <!-- Messages rendered dynamically -->
          </div>

          <!-- INPUT FORM -->
          <div style="padding:16px 20px;background:rgba(0,0,0,0.4);border-top:1px solid rgba(255,255,255,0.08);">
            <form id="form-ai-chat-main" style="display:flex;gap:12px;align-items:center;">
              <div style="position:relative;flex:1;">
                <input type="text" id="input-ai-chat-prompt" class="input-control" placeholder="AI Agentga xohlagan topshiriq yoki savolingizni yozing... (Enter bosib yuboring)" style="font-size:14px;padding:14px 18px;border-radius:12px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.15);width:100%;color:#fff;" autocomplete="off" required>
              </div>
              <button type="submit" id="btn-submit-ai-chat" class="btn-primary" style="background:linear-gradient(135deg, #a855f7 0%, #6366f1 100%);border:none;padding:14px 28px;border-radius:12px;font-weight:700;display:flex;align-items:center;gap:8px;cursor:pointer;box-shadow:0 4px 16px rgba(168,85,247,0.35);">
                <span>Yuborish</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              </button>
            </form>
          </div>
        </div>
      </div>
    `;

    const renderMessages = () => {
      const box = document.getElementById('ai-chat-messages-box');
      if (!box) return;

      box.innerHTML = this._aiChatHistory.map(msg => {
        if (msg.role === 'user') {
          return `
            <div style="display:flex;justify-content:flex-end;margin-bottom:4px;">
              <div style="max-width:75%;background:linear-gradient(135deg, rgba(168,85,247,0.25) 0%, rgba(99,102,241,0.2) 100%);border:1px solid rgba(168,85,247,0.4);border-radius:14px 14px 2px 14px;padding:12px 18px;color:#fff;font-size:14px;box-shadow:0 4px 12px rgba(0,0,0,0.2);">
                <div>${msg.text}</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);text-align:right;margin-top:4px;">${msg.time || ''}</div>
              </div>
            </div>
          `;
        } else {
          return `
            <div style="display:flex;gap:12px;align-items:flex-start;max-width:85%;">
              <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg, #a855f7 0%, #6366f1 100%);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 4px 12px rgba(168,85,247,0.4);flex-shrink:0;">
                🧠
              </div>
              <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:14px 14px 14px 2px;padding:14px 18px;color:#fff;font-size:14px;flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                  <span style="font-weight:700;color:#c084fc;font-size:13px;">ATLAS AI Agent</span>
                  ${msg.action ? `<span class="badge" style="background:rgba(168,85,247,0.15);color:#c084fc;border:1px solid rgba(168,85,247,0.3);font-size:10px;padding:2px 8px;">⚙️ ${msg.action}</span>` : ''}
                </div>
                <div style="line-height:1.5;">${msg.text}</div>
                ${msg.exec_result ? `<div style="margin-top:10px;background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px 14px;font-size:12px;color:#34d399;font-family:'JetBrains Mono',monospace;">${msg.exec_result}</div>` : ''}
                ${msg.screenshot ? `<div style="margin-top:10px;"><img src="${msg.screenshot}" style="max-width:100%;border-radius:8px;border:1px solid rgba(255,255,255,0.15);" /></div>` : ''}
                <div style="font-size:10px;color:rgba(255,255,255,0.35);margin-top:6px;">${msg.time || ''}</div>
              </div>
            </div>
          `;
        }
      }).join('');

      box.scrollTop = box.scrollHeight;
    };

    renderMessages();

    // Quick chips
    viewport.querySelectorAll('.ai-chip-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const p = e.currentTarget.dataset.prompt;
        if (p) {
          const inp = document.getElementById('input-ai-chat-prompt');
          if (inp) {
            inp.value = p;
            document.getElementById('form-ai-chat-main')?.dispatchEvent(new Event('submit'));
          }
        }
      });
    });

    // Clear history
    document.getElementById('btn-clear-ai-history')?.addEventListener('click', () => {
      this._aiChatHistory = [];
      renderMessages();
      this.toast('Chat tarixi tozalandi', 'info');
    });

    // Back to PC panel
    document.getElementById('btn-back-to-pc')?.addEventListener('click', () => {
      this.navigate('pc_control');
    });

    // Submit handler
    document.getElementById('form-ai-chat-main')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('input-ai-chat-prompt');
      const prompt = input.value.trim();
      if (!prompt) return;

      const timeStr = new Date().toLocaleTimeString().slice(0, 5);
      this._aiChatHistory.push({
        role: 'user',
        text: prompt,
        time: timeStr
      });
      input.value = '';
      renderMessages();

      // Show loader
      const box = document.getElementById('ai-chat-messages-box');
      const loaderId = 'ai-temp-chat-loader';
      if (box) {
        box.innerHTML += `
          <div id="${loaderId}" style="display:flex;gap:12px;align-items:flex-start;max-width:85%;">
            <div style="width:36px;height:36px;border-radius:10px;background:rgba(168,85,247,0.2);display:flex;align-items:center;justify-content:center;font-size:18px;">
              <span class="spinner-sm"></span>
            </div>
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:12px 16px;color:#c084fc;font-size:13px;display:flex;align-items:center;gap:8px;">
              <span>AI Agent topshiriqni tahlil qilib kompyuterda bajarmoqda...</span>
            </div>
          </div>
        `;
        box.scrollTop = box.scrollHeight;
      }

      const res = await this.api('/api/pc/ai', 'POST', { prompt });
      document.getElementById(loaderId)?.remove();

      if (res && res.success) {
        this._aiChatHistory.push({
          role: 'assistant',
          text: res.message || 'Topshiriq bajarildi.',
          action: res.action,
          exec_result: res.exec_result,
          screenshot: res.screenshot,
          time: new Date().toLocaleTimeString().slice(0, 5)
        });
      } else {
        this._aiChatHistory.push({
          role: 'assistant',
          text: `❌ Xatolik yuz berdi: ${(res && res.error) || 'AI topshirig‘ini bajarib bo‘lmadi.'}`,
          time: new Date().toLocaleTimeString().slice(0, 5)
        });
      }
      renderMessages();
    });
  },

  async refreshPcStatus() {
    const res = await this.api('/api/pc/status', 'GET');
    if (res && res.success && res.data) {
      const d = res.data;
      const elCpu = document.getElementById('pc-val-cpu');
      const elRam = document.getElementById('pc-val-ram');
      const elRamGb = document.getElementById('pc-val-ram-gb');
      const elBarCpu = document.getElementById('pc-bar-cpu');
      const elBarRam = document.getElementById('pc-bar-ram');
      const elCpuCores = document.getElementById('pc-val-cpu-cores');
      const elDiskC = document.getElementById('pc-val-disk-c');
      const elDiskCGb = document.getElementById('pc-val-disk-c-gb');
      const elBarDiskC = document.getElementById('pc-bar-disk-c');
      const elUptime = document.getElementById('pc-val-uptime');
      const elBattery = document.getElementById('pc-val-battery');
      const elHost = document.getElementById('pc-val-host');
      const badge = document.getElementById('pc-connection-badge');

      if (badge) {
        if (d.online) {
          badge.innerHTML = `🟢 ULANGAN (REALTIME ONLINE)`;
          badge.style.background = 'rgba(16,185,129,0.15)';
          badge.style.color = '#10b981';
          badge.style.borderColor = 'rgba(16,185,129,0.3)';
        } else {
          badge.innerHTML = `🟡 KUTILMOQDA (BOT YONIQMI?)`;
          badge.style.background = 'rgba(245,158,11,0.15)';
          badge.style.color = '#f59e0b';
          badge.style.borderColor = 'rgba(245,158,11,0.3)';
        }
      }

      if (elCpu) elCpu.innerText = `${d.cpu_percent || 0}%`;
      if (elCpuCores) elCpuCores.innerText = `${d.cpu_cores || 4} ta yadro`;
      if (elBarCpu) elBarCpu.style.width = `${Math.min(100, d.cpu_percent || 0)}%`;

      if (elRam) elRam.innerText = `${d.ram_percent || 0}%`;
      if (elRamGb) elRamGb.innerText = `${d.ram_used_gb || 0} / ${d.ram_total_gb || 0} GB`;
      if (elBarRam) elBarRam.style.width = `${Math.min(100, d.ram_percent || 0)}%`;

      if (d.disks && d.disks.length > 0) {
        const cDisk = d.disks[0];
        if (elDiskC) elDiskC.innerText = `${cDisk.percent}%`;
        if (elDiskCGb) elDiskCGb.innerText = `${cDisk.free_gb} GB bo'sh`;
        if (elBarDiskC) elBarDiskC.style.width = `${Math.min(100, cDisk.percent)}%`;
      }

      if (elUptime) elUptime.innerText = d.uptime || '0:00:00';
      if (elHost) elHost.innerText = d.hostname || 'Windows-PC';
      if (elBattery) {
        const b = d.battery;
        if (b && b.has_battery) {
          elBattery.innerText = `🔋 ${b.percent}% (${b.plugged ? 'Tarmoqda' : 'Batareyada'})`;
        } else {
          elBattery.innerText = `🔌 Stasionar PC (Tarmoqda)`;
        }
      }
    }
  },

  async refreshPcApps() {
    const wrap = document.getElementById('pc-apps-list-wrap');
    if (!wrap) return;

    const res = await this.api('/api/pc/apps', 'GET');
    if (res && res.success && res.apps) {
      if (res.apps.length === 0) {
        wrap.innerHTML = `<div style="color:rgba(255,255,255,0.5);text-align:center;padding:20px;">Dasturlar topilmadi.</div>`;
        return;
      }

      wrap.innerHTML = `
        <table style="width:100%;border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.4);font-size:11px;text-align:left;">
              <th style="padding:6px;">Dastur nomi</th>
              <th style="padding:6px;">PID</th>
              <th style="padding:6px;">RAM</th>
              <th style="padding:6px;text-align:right;">Amal</th>
            </tr>
          </thead>
          <tbody>
            ${res.apps.map(a => `
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);transition:background 0.2s;">
                <td style="padding:6px;font-weight:600;color:#fff;">${a.name}</td>
                <td style="padding:6px;color:rgba(255,255,255,0.5);font-family:'JetBrains Mono',monospace;">${a.pid}</td>
                <td style="padding:6px;color:#10b981;font-weight:700;">${a.memory_mb} MB</td>
                <td style="padding:6px;text-align:right;">
                  <button class="btn-danger btn-sm" onclick="ATLAS.killPcApp('${a.pid}', '${a.name}')" style="padding:2px 8px;font-size:11px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer;">Kill</button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    } else {
      wrap.innerHTML = `<div style="color:#f87171;text-align:center;padding:20px;">Dasturlar ro‘yxatini olib bo‘lmadi</div>`;
    }
  },

  async killPcApp(pid, name) {
    if (!confirm(`Haqiqatan ham "${name}" (PID: ${pid}) dasturini majburiy to'xtatmoqchimisiz?`)) return;
    const res = await this.api('/api/pc/kill', 'POST', { target: pid });
    if (res && res.success) {
      this.toast(res.message || 'Jarayon to‘xtatildi', 'success');
      this.refreshPcApps();
    } else {
      this.toast((res && res.error) || 'Xatolik yuz berdi', 'error');
    }
  },

  // ============================================================
  // MTF & TEST CONVERTER (MYTESTX -> PDF / DOCX + D:\MyTestX\tests + TELEGRAM)
  // ============================================================
  // MTF & TEST CONVERTER (MYTESTX -> PDF / DOCX + D:\MyTestX\tests + TELEGRAM)
  // ============================================================
  // MTF & TEST CONVERTER (WINDOWS EXPLORER DIRECTORY TREE + TELEGRAM)
  // ============================================================
  loadMtfConverter(viewport) {
    viewport.innerHTML = `
      <div style="max-width:1280px;margin:0 auto;padding-bottom:50px;">
        <!-- HEADER -->
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;margin-bottom:20px;">
          <div>
            <h2 style="font-size:22px;font-weight:800;color:#fff;margin:0 0 6px 0;display:flex;align-items:center;gap:10px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" style="width:26px;height:26px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
              <span>MTF & Test Generator (PDF / DOCX)</span>
              <span style="font-size:11px;font-weight:800;background:rgba(56,189,248,0.12);color:#38bdf8;border:1px solid rgba(56,189,248,0.3);padding:2px 10px;border-radius:20px;letter-spacing:0.05em;">WINDOWS EXPLORER ⚡ TELEGRAM</span>
            </h2>
            <p style="font-size:13px;color:rgba(255,255,255,0.6);margin:0;">
              <code>D:\\MyTestX\\tests</code> papkalaridagi testlarni xuddi Windows Explorer kabi papkalari ichiga kirib ko'rish, tanlash va yuqori sifatli PDF hamda Word formatida konvertatsiya qilish.
            </p>
          </div>
          <div style="display:flex;gap:10px;">
            <button class="btn-secondary btn-sm" id="btn-mtf-refresh" style="display:flex;align-items:center;gap:6px;">
              ${this.icons.refresh} <span>Papkani Yangilash</span>
            </button>
          </div>
        </div>

        <!-- SETTINGS BAR -->
        <div class="card" style="background:rgba(15,23,42,0.75);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:18px 20px;margin-bottom:20px;">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;align-items:end;">
            <div>
              <label style="display:block;font-size:12px;font-weight:600;color:rgba(255,255,255,0.7);margin-bottom:6px;">PDF Tartibi:</label>
              <select id="mtf-opt-layout" class="select-control">
                <option value="2col" selected>2-ustunli (Ixcham kitobcha, A4)</option>
                <option value="1col">1-ustunli (Keng format, A4)</option>
              </select>
            </div>
            <div>
              <label style="display:block;font-size:12px;font-weight:600;color:rgba(255,255,255,0.7);margin-bottom:6px;">Javoblar belgisi (*):</label>
              <select id="mtf-opt-answers" class="select-control">
                <option value="true" selected>To'g'ri javoblarni (*) belgilash</option>
                <option value="false">Faqat savollar (Imtihon / Chop etish uchun)</option>
              </select>
            </div>
            <div>
              <label style="display:block;font-size:12px;font-weight:600;color:rgba(255,255,255,0.7);margin-bottom:6px;">Fan Sarlavhasi (ixtiyoriy):</label>
              <input type="text" id="mtf-opt-fanname" class="input-control" placeholder="Fayl nomidan avtomatik olinadi">
            </div>
          </div>
        </div>

        <!-- SELECTION & EXPLORER WRAPPER -->
        <div id="mtf-selection-wrapper">
          <!-- SOURCE TABS -->
          <div style="display:flex;gap:10px;margin-bottom:16px;">
            <button id="mtf-tab-btn-local" class="btn-primary" style="padding:10px 22px;font-weight:700;display:flex;align-items:center;gap:8px;border-radius:10px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
              <span>🗂 D:\\MyTestX\\tests Papkasi</span>
              <span id="mtf-local-badge" style="font-size:11px;background:rgba(255,255,255,0.2);padding:2px 8px;border-radius:12px;">Yuklanmoqda...</span>
            </button>
            <button id="mtf-tab-btn-upload" class="btn-secondary" style="padding:10px 22px;font-weight:700;display:flex;align-items:center;gap:8px;border-radius:10px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              <span>⬆️ Fayl Yuklash (Drag & Drop)</span>
            </button>
          </div>

          <!-- TAB 1: WINDOWS EXPLORER FOLDER NAVIGATION -->
          <div id="mtf-tab-local" class="card" style="background:rgba(15,23,42,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:20px;margin-bottom:20px;box-shadow:0 10px 30px rgba(0,0,0,0.35);">
            <!-- EXPLORER TOOLBAR -->
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);">
              <div style="flex:1;min-width:280px;position:relative;">
                <input type="text" id="mtf-local-search" class="input-control" placeholder="🔍 Test yoki papka nomini qidirish (masalan: TAT, Anatomiya, Yakuniy)..." style="padding-left:14px;">
              </div>
              <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
                <button class="btn-secondary btn-sm" id="btn-mtf-select-all">Hammasini tanlash</button>
                <button class="btn-secondary btn-sm" id="btn-mtf-deselect-all">Tozalash</button>
                <button class="btn-primary" id="btn-mtf-convert-local" style="padding:8px 24px;font-weight:800;display:flex;align-items:center;gap:8px;background:linear-gradient(135deg,#38bdf8,#0284c7);box-shadow:0 4px 15px rgba(56,189,248,0.35);">
                  ${this.icons.zap} <span id="btn-mtf-convert-label">Tanlanganlarni Konvert Qilish</span>
                </button>
              </div>
            </div>

            <!-- BREADCRUMB & BACK BUTTON -->
            <div style="display:flex;align-items:center;gap:10px;font-family:'JetBrains Mono',monospace;font-size:12.5px;color:#38bdf8;background:rgba(0,0,0,0.3);padding:10px 14px;border-radius:8px;margin-bottom:14px;border:1px solid rgba(56,189,248,0.2);flex-wrap:wrap;">
              <button id="btn-mtf-nav-back" class="btn-secondary btn-sm" style="padding:4px 10px;font-size:12px;display:inline-flex;align-items:center;gap:4px;" disabled>
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
                <span>Orqaga</span>
              </button>
              <div id="mtf-breadcrumb-trail" style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;flex:1;">
                <span class="mtf-crumb-link" data-depth="0" style="cursor:pointer;font-weight:700;color:#38bdf8;">📁 tests</span>
              </div>
              <span style="margin-left:auto;color:rgba(255,255,255,0.6);font-size:11px;font-weight:700;" id="mtf-selected-counter">0 ta tanlandi</span>
            </div>

            <!-- EXPLORER ITEMS CONTAINER -->
            <div id="mtf-tree-container" style="max-height:550px;overflow-y:auto;background:rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;font-family:'Plus Jakarta Sans',sans-serif;">
              <div style="text-align:center;padding:40px;color:rgba(255,255,255,0.5);">
                <span class="spinner-sm"></span> D:\\MyTestX\\tests katalogi yuklanmoqda...
              </div>
            </div>
          </div>

          <!-- TAB 2: ANIMATED DRAG & DROP -->
          <div id="mtf-tab-upload" class="card" style="display:none;background:rgba(15,23,42,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:24px;margin-bottom:20px;">
            <div id="mtf-drop-zone" style="position:relative;border:2px dashed rgba(56,189,248,0.4);background:radial-gradient(ellipse at center, rgba(56,189,248,0.08) 0%, rgba(15,23,42,0.4) 100%);border-radius:16px;padding:50px 20px;text-align:center;cursor:pointer;transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);overflow:hidden;">
              <input type="file" id="mtf-file-input" accept=".mtf,.xml" multiple style="display:none;">
              <div style="margin-bottom:14px;color:#38bdf8;animation:pulseSlow 2.5s infinite ease-in-out;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width:54px;height:54px;filter:drop-shadow(0 0 12px rgba(56,189,248,0.6));"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              </div>
              <div style="font-size:17px;font-weight:800;color:#fff;margin-bottom:6px;" id="mtf-file-name-label">
                MTF yoki XML fayllarni bu yerga tashlang yoki bosing
              </div>
              <div style="font-size:13px;color:rgba(255,255,255,0.6);display:flex;align-items:center;justify-content:center;gap:8px;">
                <span style="background:rgba(56,189,248,0.15);color:#38bdf8;padding:2px 8px;border-radius:6px;font-weight:700;">.MTF</span>
                <span style="background:rgba(52,211,153,0.15);color:#34d399;padding:2px 8px;border-radius:6px;font-weight:700;">.XML</span>
                <span>— bir vaqtda bir nechta fayl tanlash mumkin</span>
              </div>
            </div>

            <div id="mtf-file-queue" style="margin-top:18px;display:none;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.85);" id="mtf-queue-label">0 ta fayl tanlandi</span>
                <div style="display:flex;gap:8px;">
                  <button class="btn-secondary btn-sm" id="btn-mtf-clear" style="color:#ef4444;border-color:rgba(239,68,68,0.3);">Tozalash</button>
                  <button class="btn-primary" id="btn-mtf-convert" style="padding:8px 22px;font-weight:700;display:flex;align-items:center;gap:6px;">
                    ${this.icons.zap} <span>Barchasini Konvert Qilish</span>
                  </button>
                </div>
              </div>
              <div id="mtf-file-list" style="display:flex;flex-direction:column;gap:8px;max-height:400px;overflow-y:auto;"></div>
            </div>
          </div>
        </div>

        <!-- PROGRESS & CONVERTED RESULTS PANEL -->
        <div id="mtf-results-card" class="card" style="display:none;background:rgba(15,23,42,0.92);border:1px solid rgba(56,189,248,0.4);border-radius:14px;padding:24px;margin-bottom:20px;box-shadow:0 10px 30px rgba(0,0,0,0.5);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:12px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);">
            <div style="display:flex;align-items:center;gap:10px;">
              <h3 style="font-size:17px;font-weight:800;color:#fff;margin:0;display:flex;align-items:center;gap:8px;">
                ${this.icons.check} <span>Konvertatsiya Natijalari</span>
              </h3>
              <span id="mtf-results-status" style="font-size:12.5px;color:rgba(94,234,212,0.9);font-weight:700;"></span>
            </div>
            <button class="btn-secondary btn-sm" id="btn-mtf-back-to-files" style="display:flex;align-items:center;gap:6px;background:rgba(56,189,248,0.12);border-color:rgba(56,189,248,0.3);color:#38bdf8;font-weight:700;">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
              <span>Yana Test Tanlash (Papkaga Qaytish)</span>
            </button>
          </div>
          <div id="mtf-results-list" style="display:flex;flex-direction:column;gap:10px;"></div>
        </div>

        <!-- INTEGRATION PROMO -->
        <div class="card" style="background:linear-gradient(135deg, rgba(15,23,42,0.85), rgba(30,41,59,0.75));border:1px solid rgba(56,189,248,0.25);border-radius:14px;padding:20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
          <div style="flex:1;min-width:280px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" style="width:20px;height:20px;"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
              <h3 style="font-size:15px;font-weight:800;color:#fff;margin:0;">Online MyTestX — Onlayn Test Platformasi</h3>
            </div>
            <p style="font-size:13px;color:rgba(255,255,255,0.7);margin:0;line-height:1.5;">
              Realtime WebSocket monitoring, nusxa ko'chirishdan himoya, taymer va Google Sheets integratsiyasi.
            </p>
          </div>
          <button class="btn-secondary" onclick="ATLAS.openOnlineTestPlatform()" style="font-weight:700;display:flex;align-items:center;gap:6px;">
            ${this.icons.externalLink} <span>Platformani Ishga Tushirish</span>
          </button>
        </div>
      </div>
    `;

    // ── Elements & State ─────────────────────────────────────
    const selectionWrapper = document.getElementById('mtf-selection-wrapper');
    const tabBtnLocal   = document.getElementById('mtf-tab-btn-local');
    const tabBtnUpload  = document.getElementById('mtf-tab-btn-upload');
    const tabLocal      = document.getElementById('mtf-tab-local');
    const tabUpload     = document.getElementById('mtf-tab-upload');
    const localBadge    = document.getElementById('mtf-local-badge');
    const localSearch   = document.getElementById('mtf-local-search');
    const treeCont      = document.getElementById('mtf-tree-container');
    const crumbTrail    = document.getElementById('mtf-breadcrumb-trail');
    const btnNavBack    = document.getElementById('btn-mtf-nav-back');
    const resultsCard   = document.getElementById('mtf-results-card');
    const resultsList   = document.getElementById('mtf-results-list');
    const resultsStatus = document.getElementById('mtf-results-status');
    const selCounterEl  = document.getElementById('mtf-selected-counter');
    const convertBtnLbl = document.getElementById('btn-mtf-convert-label');
    const btnBackToFiles = document.getElementById('btn-mtf-back-to-files');

    let treeData = null;
    let flatCategories = [];
    let selectedLocalPaths = new Set();
    let folderNavStack = []; // History stack of folder nodes [rootNode, subNode, ...]
    let uploadFiles = [];

    // Official Telegram SVG Icon HTML
    const TG_ICON_SVG = `
      <svg viewBox="0 0 24 24" style="width:16px;height:16px;vertical-align:middle;" viewBox="0 0 24 24">
        <path fill="#229ED9" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0z"/>
        <path fill="#ffffff" d="M5.4 11.97l12.42-4.79c.57-.21 1.07.13.88.99l-2.11 9.94c-.16.71-.58.88-1.18.55l-3.23-2.38-1.56 1.5c-.17.17-.32.32-.65.32l.23-3.3 6.01-5.43c.26-.23-.06-.36-.4-.13L8.35 14.15l-3.2-.99c-.7-.22-.71-.7.15-1.19z"/>
      </svg>
    `;

    // ── Tab Switch ───────────────────────────────────────────
    tabBtnLocal.addEventListener('click', () => {
      tabBtnLocal.className = 'btn-primary';
      tabBtnUpload.className = 'btn-secondary';
      tabLocal.style.display = 'block';
      tabUpload.style.display = 'none';
    });

    tabBtnUpload.addEventListener('click', () => {
      tabBtnUpload.className = 'btn-primary';
      tabBtnLocal.className = 'btn-secondary';
      tabUpload.style.display = 'block';
      tabLocal.style.display = 'none';
    });

    btnBackToFiles.addEventListener('click', () => {
      selectionWrapper.style.display = 'block';
      window.scrollTo({ top: selectionWrapper.offsetTop - 40, behavior: 'smooth' });
    });

    // ── Helper: Send to Telegram ─────────────────────────────
    window.ATLAS._mtfSendTelegram = async (btn, title, filename, pdfUrl, docxUrl, pdfB64, docxB64) => {
      btn.disabled = true;
      const origText = btn.innerHTML;
      btn.innerHTML = `<span class="spinner-sm" style="width:12px;height:12px;"></span> <span>Telegramga yuborilmoqda...</span>`;

      try {
        const res = await this.api('/api/mtf/send_telegram', 'POST', {
          title,
          filename,
          pdf_url: pdfUrl || null,
          docx_url: docxUrl || null,
          pdf_base64: pdfB64 || null,
          docx_base64: docxB64 || null
        });

        if (res && res.success) {
          btn.innerHTML = `✅ <span>Telegramga Yuborildi</span>`;
          btn.style.background = 'rgba(16,185,129,0.25)';
          btn.style.borderColor = '#10b981';
          btn.style.color = '#10b981';
          this.toast(`✈️ "${title}" Telegramingizga muvaffaqiyatli tashlab berildi!`, 'success');
        } else {
          btn.disabled = false;
          btn.innerHTML = origText;
          this.toast((res && res.error) || 'Telegramga yuborishda xatolik', 'error');
        }
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = origText;
        this.toast('Xatolik: ' + err.message, 'error');
      }
    };

    // ── Helper: Collect all file paths inside a tree node ────
    const getAllFilePaths = (node) => {
      let paths = [];
      if (!node) return paths;
      if (node.type === 'file') {
        paths.push(node.path);
      } else if (node.children) {
        node.children.forEach(c => {
          paths = paths.concat(getAllFilePaths(c));
        });
      }
      return paths;
    };

    const updateSelectedCounter = () => {
      const count = selectedLocalPaths.size;
      if (selCounterEl) selCounterEl.textContent = `${count} ta test tanlandi`;
      if (convertBtnLbl) convertBtnLbl.textContent = count > 0 ? `Tanlanganlarni Konvert Qilish (${count})` : `Tanlanganlarni Konvert Qilish`;
    };

    // ── Windows Explorer Navigation Renderer ──────────────────
    const renderExplorer = () => {
      const q = (localSearch?.value || '').trim().toLowerCase();
      const currentFolder = folderNavStack.length > 0 ? folderNavStack[folderNavStack.length - 1] : treeData;

      // Update Back Button
      if (btnNavBack) {
        btnNavBack.disabled = folderNavStack.length <= 1;
      }

      // Update Breadcrumbs Trail
      if (crumbTrail) {
        crumbTrail.innerHTML = folderNavStack.map((fNode, idx) => {
          const isLast = idx === folderNavStack.length - 1;
          const label = idx === 0 ? '📁 tests (D:\\MyTestX\\tests)' : fNode.name;
          return `
            <span class="mtf-crumb-link" data-depth="${idx}" style="cursor:${isLast ? 'default' : 'pointer'};font-weight:${isLast ? '800' : '600'};color:${isLast ? '#ffffff' : '#38bdf8'};">
              ${label}
            </span>
            ${!isLast ? '<span style="color:rgba(255,255,255,0.4);font-size:10px;">❯</span>' : ''}
          `;
        }).join('');

        crumbTrail.querySelectorAll('.mtf-crumb-link').forEach(crumb => {
          crumb.addEventListener('click', () => {
            const depth = parseInt(crumb.getAttribute('data-depth'));
            if (!isNaN(depth) && depth < folderNavStack.length - 1) {
              folderNavStack = folderNavStack.slice(0, depth + 1);
              renderExplorer();
            }
          });
        });
      }

      if (!currentFolder) {
        treeCont.innerHTML = `<div style="text-align:center;padding:30px;color:rgba(255,255,255,0.4);">Testlar topilmadi</div>`;
        updateSelectedCounter();
        return;
      }

      // If search query is active: search recursively across all sub-items
      if (q) {
        const matchingFiles = [];
        const searchRecursive = (node) => {
          if (!node) return;
          if (node.type === 'file') {
            if (node.name.toLowerCase().includes(q) || (node.rel_path && node.rel_path.toLowerCase().includes(q))) {
              matchingFiles.push(node);
            }
          } else if (node.children) {
            node.children.forEach(searchRecursive);
          }
        };
        searchRecursive(currentFolder);

        if (matchingFiles.length === 0) {
          treeCont.innerHTML = `<div style="text-align:center;padding:36px;color:rgba(255,255,255,0.4);">🔍 "${q}" bo'yicha testlar topilmadi</div>`;
          updateSelectedCounter();
          return;
        }

        treeCont.innerHTML = `
          <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.06);">
            Qidiruv natijalari: <b>${matchingFiles.length} ta test</b> topildi
          </div>
          <div style="display:flex;flex-direction:column;gap:6px;">
            ${matchingFiles.map(file => {
              const isSel = selectedLocalPaths.has(file.path);
              return `
                <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 12px;border-radius:8px;background:${isSel ? 'rgba(56,189,248,0.15)' : 'rgba(255,255,255,0.02)'};border:1px solid ${isSel ? 'rgba(56,189,248,0.35)' : 'rgba(255,255,255,0.04)'};gap:10px;" class="tree-row-hover">
                  <label style="display:flex;align-items:center;gap:10px;flex:1;cursor:pointer;overflow:hidden;">
                    <input type="checkbox" value="${file.path}" class="tree-file-cb" style="width:16px;height:16px;accent-color:#38bdf8;cursor:pointer;" ${isSel ? 'checked' : ''}>
                    <span style="font-size:16px;">📝</span>
                    <div>
                      <div style="font-size:13px;font-weight:700;color:${isSel ? '#38bdf8' : '#ffffff'};">${file.name}</div>
                      <div style="font-size:11px;color:rgba(255,255,255,0.45);">${file.rel_path || ''}</div>
                    </div>
                  </label>
                  <div style="display:flex;align-items:center;gap:10px;font-size:11.5px;color:rgba(255,255,255,0.5);white-space:nowrap;">
                    <span>${file.size_str || ''}</span>
                    <button onclick="ATLAS._mtfQuickConvertSingle('${file.path.replace(/\\/g, '\\\\')}', '${file.name}')" style="background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;">⚡ Konvert</button>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `;
        attachExplorerListeners();
        updateSelectedCounter();
        return;
      }

      // Normal Folder Explorer View (Direct Children of current folder)
      const children = currentFolder.children || [];
      const folders = children.filter(c => c.type === 'folder');
      const files   = children.filter(c => c.type === 'file');

      if (folders.length === 0 && files.length === 0) {
        treeCont.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(255,255,255,0.4);">Ushbu papka bo'sh</div>`;
        updateSelectedCounter();
        return;
      }

      let explorerHtml = `<div style="display:flex;flex-direction:column;gap:6px;">`;

      // 1. Folders Section
      if (folders.length > 0) {
        explorerHtml += folders.map((fNode, fIdx) => {
          const allFPaths = getAllFilePaths(fNode);
          const isAllSel = allFPaths.length > 0 && allFPaths.every(p => selectedLocalPaths.has(p));
          return `
            <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-radius:10px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);cursor:pointer;gap:12px;transition:all 0.18s ease;" class="tree-row-hover mtf-folder-row" data-folder-index="${fIdx}">
              <div style="display:flex;align-items:center;gap:12px;flex:1;min-width:0;">
                <input type="checkbox" class="mtf-subfolder-cb" data-folder-index="${fIdx}" style="width:16px;height:16px;accent-color:#38bdf8;cursor:pointer;" ${isAllSel ? 'checked' : ''}>
                <span style="font-size:20px;">📁</span>
                <div>
                  <div style="font-size:13.5px;font-weight:700;color:#ffffff;">${fNode.name}</div>
                  <div style="font-size:11px;color:#38bdf8;">${fNode.total_files || (fNode.children ? fNode.children.length : 0)} ta test fayllari</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,0.4);font-size:12px;font-weight:600;">
                <span>Kirish</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
              </div>
            </div>
          `;
        }).join('');
      }

      // 2. Files Section
      if (files.length > 0) {
        explorerHtml += files.map(file => {
          const isSel = selectedLocalPaths.has(file.path);
          return `
            <div style="display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border-radius:8px;background:${isSel ? 'rgba(56,189,248,0.15)' : 'rgba(255,255,255,0.015)'};border:1px solid ${isSel ? 'rgba(56,189,248,0.35)' : 'rgba(255,255,255,0.04)'};gap:10px;" class="tree-row-hover">
              <label style="display:flex;align-items:center;gap:10px;flex:1;cursor:pointer;overflow:hidden;">
                <input type="checkbox" value="${file.path}" class="tree-file-cb" style="width:16px;height:16px;accent-color:#38bdf8;cursor:pointer;" ${isSel ? 'checked' : ''}>
                <span style="font-size:16px;">📝</span>
                <span style="font-size:13px;font-weight:600;color:${isSel ? '#38bdf8' : '#ffffff'};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="${file.name}">${file.name}</span>
              </label>
              <div style="display:flex;align-items:center;gap:12px;font-size:11.5px;color:rgba(255,255,255,0.45);white-space:nowrap;">
                <span>${file.size_str || ''}</span>
                <span>${file.mtime_str || ''}</span>
                <button onclick="ATLAS._mtfQuickConvertSingle('${file.path.replace(/\\/g, '\\\\')}', '${file.name}')" style="background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;">⚡ Konvert</button>
              </div>
            </div>
          `;
        }).join('');
      }

      explorerHtml += `</div>`;
      treeCont.innerHTML = explorerHtml;
      attachExplorerListeners();
      updateSelectedCounter();
    };

    // ── Attach Explorer Event Listeners ───────────────────────
    const attachExplorerListeners = () => {
      const currentFolder = folderNavStack.length > 0 ? folderNavStack[folderNavStack.length - 1] : treeData;
      const folders = currentFolder ? (currentFolder.children || []).filter(c => c.type === 'folder') : [];

      // Folder Click -> Enter folder (like Windows Explorer)
      treeCont.querySelectorAll('.mtf-folder-row').forEach(row => {
        row.addEventListener('click', (e) => {
          if (e.target.tagName === 'INPUT') return; // Don't navigate if checking checkbox
          const fIdx = parseInt(row.getAttribute('data-folder-index'));
          if (!isNaN(fIdx) && folders[fIdx]) {
            folderNavStack.push(folders[fIdx]);
            renderExplorer();
          }
        });
      });

      // Folder Checkbox -> Toggle all files inside recursively
      treeCont.querySelectorAll('.mtf-subfolder-cb').forEach(cb => {
        cb.addEventListener('click', (e) => e.stopPropagation());
        cb.addEventListener('change', (e) => {
          const fIdx = parseInt(e.target.getAttribute('data-folder-index'));
          if (!isNaN(fIdx) && folders[fIdx]) {
            const paths = getAllFilePaths(folders[fIdx]);
            if (e.target.checked) paths.forEach(p => selectedLocalPaths.add(p));
            else paths.forEach(p => selectedLocalPaths.delete(p));
          }
          renderExplorer();
        });
      });

      // File Checkbox -> Toggle single file selection
      treeCont.querySelectorAll('.tree-file-cb').forEach(cb => {
        cb.addEventListener('change', (e) => {
          if (e.target.checked) selectedLocalPaths.add(e.target.value);
          else selectedLocalPaths.delete(e.target.value);
          renderExplorer();
        });
      });
    };

    // ── Navigation Back Button Handler ────────────────────────
    btnNavBack?.addEventListener('click', () => {
      if (folderNavStack.length > 1) {
        folderNavStack.pop();
        renderExplorer();
      }
    });

    // ── Load D:\MyTestX\tests Catalog ────────────────────────
    const loadLocalTests = async () => {
      treeCont.innerHTML = `<div style="text-align:center;padding:40px;color:rgba(255,255,255,0.6);"><span class="spinner-sm"></span> D:\\MyTestX\\tests katalogi skanerlanmoqda...</div>`;
      try {
        const res = await this.api('/api/mtf/local_tests', 'GET');
        if (res && res.success) {
          treeData = res.tree || null;
          flatCategories = res.categories || [];
          localBadge.textContent = `${res.total_files} ta test`;
          folderNavStack = treeData ? [treeData] : [];
          renderExplorer();
        } else {
          treeCont.innerHTML = `<div style="padding:20px;color:#ef4444;text-align:center;">❌ ${res?.error || "Testlar ro'yxatini olib bo'lmadi"}</div>`;
        }
      } catch (err) {
        treeCont.innerHTML = `<div style="padding:20px;color:#ef4444;text-align:center;">❌ Xatolik: ${err.message}</div>`;
      }
    };

    // ── Search & Toolbar Buttons ─────────────────────────────
    localSearch?.addEventListener('input', () => renderExplorer());

    document.getElementById('btn-mtf-select-all')?.addEventListener('click', () => {
      const currentFolder = folderNavStack.length > 0 ? folderNavStack[folderNavStack.length - 1] : treeData;
      if (currentFolder) {
        getAllFilePaths(currentFolder).forEach(p => selectedLocalPaths.add(p));
      } else if (flatCategories) {
        flatCategories.forEach(cat => cat.files.forEach(f => selectedLocalPaths.add(f.path)));
      }
      renderExplorer();
    });

    document.getElementById('btn-mtf-deselect-all')?.addEventListener('click', () => {
      selectedLocalPaths.clear();
      renderExplorer();
    });

    // ── Quick Convert Single File Helper ─────────────────────
    window.ATLAS._mtfQuickConvertSingle = (filePath, fileName) => {
      selectedLocalPaths.clear();
      selectedLocalPaths.add(filePath);
      renderExplorer();
      document.getElementById('btn-mtf-convert-local')?.click();
    };

    // ── Execute Conversion for Local Explorer Files ───────────
    document.getElementById('btn-mtf-convert-local')?.addEventListener('click', async () => {
      if (!selectedLocalPaths.size) {
        this.toast("Iltimos, avval ro'yxatdan kamida bitta testni tanlang", 'error');
        return;
      }

      const paths = Array.from(selectedLocalPaths);
      const layout = document.getElementById('mtf-opt-layout')?.value || '2col';
      const withAnswers = document.getElementById('mtf-opt-answers')?.value || 'true';
      const fanNameCustom = document.getElementById('mtf-opt-fanname')?.value || '';

      // Hide files selection and show conversion view
      selectionWrapper.style.display = 'none';
      resultsCard.style.display = 'block';
      window.scrollTo({ top: resultsCard.offsetTop - 40, behavior: 'smooth' });

      resultsStatus.textContent = `${paths.length} ta test konvertatsiya qilinmoqda...`;
      resultsList.innerHTML = paths.map((p, idx) => {
        const fn = p.split(/[\\/]/).pop();
        return `
          <div id="res-row-${idx}" style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:12px 16px;gap:10px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:10px;flex:1;min-width:220px;">
              <span id="res-icon-${idx}">⏳</span>
              <div>
                <div style="font-size:13px;font-weight:700;color:#fff;">${fn}</div>
                <div id="res-msg-${idx}" style="font-size:11px;color:rgba(255,255,255,0.5);">Navbatga yuklanmoqda...</div>
              </div>
            </div>
            <div id="res-actions-${idx}" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;"></div>
          </div>
        `;
      }).join('');

      let successCount = 0;

      for (let i = 0; i < paths.length; i++) {
        const filePath = paths[i];
        const fileName = filePath.split(/[\\/]/).pop();
        const iconEl = document.getElementById(`res-icon-${i}`);
        const msgEl  = document.getElementById(`res-msg-${i}`);
        const actsEl = document.getElementById(`res-actions-${i}`);

        if (iconEl) iconEl.innerHTML = `<span class="spinner-sm"></span>`;
        if (msgEl)  msgEl.textContent = 'Kompyuterda tahlil qilinmoqda...';

        try {
          const submitRes = await this.api('/api/mtf/submit_job', 'POST', {
            filename: fileName,
            file_base64: null,
            input_url: null,
            file_path: filePath,
            layout,
            with_answers: withAnswers === 'true',
            fan_name: fanNameCustom || fileName.replace(/\.(mtf|xml)$/i, '')
          });

          if (!submitRes || !submitRes.success) {
            throw new Error(submitRes?.error || 'Xatolik');
          }

          const cmdId = submitRes.cmd_id;
          const jobId = submitRes.job_id;

          let pollDone = false;
          const startT = Date.now();
          while (Date.now() - startT < 180000) {
            await new Promise(r => setTimeout(r, 1500));
            const stat = await this.api(`/api/mtf/job_status?cmd_id=${cmdId}&job_id=${jobId}`, 'GET');
            if (!stat) continue;

            if (stat.status === 'completed') {
              pollDone = true;
              successCount++;
              if (iconEl) iconEl.textContent = '✅';
              if (msgEl) {
                msgEl.textContent = `✅ ${stat.questions_count} ta savol • ${stat.title || fileName}`;
                msgEl.style.color = '#10b981';
              }

              const stem = fileName.replace(/\.(mtf|xml)$/i, '');
              let actHtml = '';
              const pdfUrl = stat.pdf_url || stat.pdf_base64;
              if (pdfUrl) {
                actHtml += `<a href="${pdfUrl}" download="${stem}.pdf" target="_blank" style="padding:6px 12px;background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border-radius:7px;font-size:12px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px;">📄 PDF</a>`;
              }
              const docxUrl = stat.docx_url || stat.docx_base64;
              if (docxUrl) {
                actHtml += `<a href="${docxUrl}" download="${stem}.docx" target="_blank" style="padding:6px 12px;background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.35);color:#38bdf8;border-radius:7px;font-size:12px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px;">📝 Word</a>`;
              }

              // Prominent Telegram button with real SVG
              const escapedTitle = (stat.title || fileName).replace(/'/g, "\\'");
              actHtml += `
                <button onclick="ATLAS._mtfSendTelegram(this, '${escapedTitle}', '${fileName}', '${stat.pdf_url || ''}', '${stat.docx_url || ''}', '${stat.pdf_base64 || ''}', '${stat.docx_base64 || ''}')" style="padding:6px 14px;background:linear-gradient(135deg,rgba(34,158,217,0.25),rgba(0,136,204,0.35));border:1px solid #229ED9;color:#38bdf8;border-radius:7px;font-size:12px;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;box-shadow:0 2px 8px rgba(34,158,217,0.3);">
                  ${TG_ICON_SVG} <span>Telegram</span>
                </button>
              `;
              if (actsEl) actsEl.innerHTML = actHtml;
              break;
            } else if (stat.status === 'error') {
              throw new Error(stat.error || 'Xatolik yuz berdi');
            } else {
              if (msgEl) msgEl.textContent = stat.message || 'Tahlil qilinmoqda...';
            }
          }

          if (!pollDone) throw new Error('Vaqt tugadi');

        } catch (err) {
          if (iconEl) iconEl.textContent = '❌';
          if (msgEl) {
            msgEl.textContent = err.message || 'Xatolik';
            msgEl.style.color = '#ef4444';
          }
        }
      }

      resultsStatus.textContent = `Bajarildi: ${successCount} / ${paths.length} ta tayyor`;
      this.toast(`🎉 ${successCount} ta test muvaffaqiyatli konvert qilindi!`, 'success');
    });

    // ── Drag & Drop Queue Logic with Rich Animations ─────────
    const dropZone   = document.getElementById('mtf-drop-zone');
    const fileInput  = document.getElementById('mtf-file-input');
    const nameLabel  = document.getElementById('mtf-file-name-label');
    const fileQueue  = document.getElementById('mtf-file-queue');
    const fileList   = document.getElementById('mtf-file-list');
    const queueLabel = document.getElementById('mtf-queue-label');

    const sizeStr = bytes => bytes < 1024*1024
      ? `${(bytes/1024).toFixed(0)} KB`
      : `${(bytes/1024/1024).toFixed(1)} MB`;

    const addFiles = (files) => {
      const arr = Array.from(files).filter(f => /\.(mtf|xml)$/i.test(f.name));
      if (!arr.length) { this.toast('Faqat .mtf va .xml fayllar qabul qilinadi', 'error'); return; }
      const existing = new Set(uploadFiles.map(f => f.name));
      arr.forEach(f => { if (!existing.has(f.name)) { uploadFiles.push(f); existing.add(f.name); } });
      renderUploadQueue();
    };

    const renderUploadQueue = () => {
      if (!uploadFiles.length) {
        fileQueue.style.display = 'none';
        nameLabel.innerHTML = 'MTF yoki XML fayllarni bu yerga tashlang yoki bosing';
        return;
      }
      fileQueue.style.display = 'block';
      queueLabel.textContent = `${uploadFiles.length} ta fayl tanlandi`;
      nameLabel.innerHTML = `📂 <b style="color:#60a5fa;">${uploadFiles.length} ta fayl</b> tanlandi`;

      fileList.innerHTML = uploadFiles.map((f, i) => `
        <div id="upload-row-${i}" style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:12px 14px;gap:10px;flex-wrap:wrap;">
          <div style="display:flex;align-items:center;gap:10px;flex:1;min-width:200px;">
            <span id="upload-icon-${i}">⏳</span>
            <div>
              <div style="font-size:13px;font-weight:700;color:#fff;">${f.name}</div>
              <div id="upload-msg-${i}" style="font-size:11px;color:rgba(255,255,255,0.5);">${sizeStr(f.size)}</div>
            </div>
          </div>
          <div id="upload-downloads-${i}" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;"></div>
          <button onclick="ATLAS._mtfRemoveUploadFile(${i})" style="background:none;border:none;color:rgba(239,68,68,0.7);cursor:pointer;font-size:16px;">✕</button>
        </div>
      `).join('');

      window.ATLAS._mtfRemoveUploadFile = (idx) => {
        uploadFiles.splice(idx, 1);
        renderUploadQueue();
      };
    };

    // Drag-over hover animations
    dropZone?.addEventListener('click', () => fileInput?.click());
    fileInput?.addEventListener('change', (e) => {
      if (e.target.files?.length) addFiles(e.target.files);
      fileInput.value = '';
    });

    ['dragenter', 'dragover'].forEach(ev => {
      dropZone?.addEventListener(ev, e => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.style.borderColor = '#38bdf8';
        dropZone.style.background = 'radial-gradient(ellipse at center, rgba(56,189,248,0.2) 0%, rgba(15,23,42,0.8) 100%)';
        dropZone.style.transform = 'scale(1.01)';
        dropZone.style.boxShadow = '0 0 25px rgba(56,189,248,0.4)';
      });
    });

    ['dragleave', 'drop'].forEach(ev => {
      dropZone?.addEventListener(ev, e => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.style.borderColor = 'rgba(56,189,248,0.4)';
        dropZone.style.background = 'radial-gradient(ellipse at center, rgba(56,189,248,0.08) 0%, rgba(15,23,42,0.4) 100%)';
        dropZone.style.transform = 'scale(1)';
        dropZone.style.boxShadow = 'none';
      });
    });

    dropZone?.addEventListener('drop', e => {
      if (e.dataTransfer?.files?.length) addFiles(e.dataTransfer.files);
    });

    document.getElementById('btn-mtf-clear')?.addEventListener('click', () => {
      uploadFiles = [];
      renderUploadQueue();
    });

    // ── Execute Conversion for Uploaded Drag & Drop Files ────
    document.getElementById('btn-mtf-convert')?.addEventListener('click', async () => {
      if (!uploadFiles.length) return;
      const layout = document.getElementById('mtf-opt-layout')?.value || '2col';
      const withAnswers = document.getElementById('mtf-opt-answers')?.value || 'true';
      const fanNameCustom = document.getElementById('mtf-opt-fanname')?.value || '';

      const btn = document.getElementById('btn-mtf-convert');
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-sm"></span> <span>Bajarilmoqda...</span>`;

      for (let i = 0; i < uploadFiles.length; i++) {
        const f = uploadFiles[i];
        const iconEl = document.getElementById(`upload-icon-${i}`);
        const msgEl  = document.getElementById(`upload-msg-${i}`);
        const dlEl   = document.getElementById(`upload-downloads-${i}`);

        if (iconEl) iconEl.innerHTML = `<span class="spinner-sm"></span>`;
        if (msgEl)  msgEl.textContent = 'Navbatga yuklanmoqda...';

        try {
          const base64Data = await new Promise((res, rej) => {
            const reader = new FileReader();
            reader.onload = () => res(reader.result);
            reader.onerror = rej;
            reader.readAsDataURL(f);
          });

          const fanName = fanNameCustom || f.name.replace(/\.(mtf|xml)$/i, '').replace(/_/g, ' ');

          const submitRes = await this.api('/api/mtf/submit_job', 'POST', {
            filename: f.name,
            file_base64: base64Data,
            layout,
            with_answers: withAnswers === 'true',
            fan_name: fanName
          });

          if (!submitRes || !submitRes.success) throw new Error(submitRes?.error || 'Xatolik');

          const cmdId = submitRes.cmd_id;
          const jobId = submitRes.job_id;

          let pollDone = false;
          const startT = Date.now();
          while (Date.now() - startT < 180000) {
            await new Promise(r => setTimeout(r, 1500));
            const stat = await this.api(`/api/mtf/job_status?cmd_id=${cmdId}&job_id=${jobId}`, 'GET');
            if (!stat) continue;

            if (stat.status === 'completed') {
              pollDone = true;
              if (iconEl) iconEl.textContent = '✅';
              if (msgEl) {
                msgEl.textContent = `✅ ${stat.questions_count} ta savol • ${stat.title || f.name}`;
                msgEl.style.color = '#10b981';
              }

              const stem = f.name.replace(/\.(mtf|xml)$/i, '');
              let dlHtml = '';
              const pdfUrl = stat.pdf_url || stat.pdf_base64;
              if (pdfUrl) {
                dlHtml += `<a href="${pdfUrl}" download="${stem}.pdf" target="_blank" style="padding:6px 12px;background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border-radius:7px;font-size:12px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px;">📄 PDF</a>`;
              }
              const docxUrl = stat.docx_url || stat.docx_base64;
              if (docxUrl) {
                dlHtml += `<a href="${docxUrl}" download="${stem}.docx" target="_blank" style="padding:6px 12px;background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.35);color:#38bdf8;border-radius:7px;font-size:12px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:4px;">📝 Word</a>`;
              }

              const escapedTitle = (stat.title || f.name).replace(/'/g, "\\'");
              dlHtml += `
                <button onclick="ATLAS._mtfSendTelegram(this, '${escapedTitle}', '${f.name}', '${stat.pdf_url || ''}', '${stat.docx_url || ''}', '${stat.pdf_base64 || ''}', '${stat.docx_base64 || ''}')" style="padding:6px 14px;background:linear-gradient(135deg,rgba(34,158,217,0.25),rgba(0,136,204,0.35));border:1px solid #229ED9;color:#38bdf8;border-radius:7px;font-size:12px;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px;box-shadow:0 2px 8px rgba(34,158,217,0.3);">
                  ${TG_ICON_SVG} <span>Telegram</span>
                </button>
              `;
              if (dlEl) dlEl.innerHTML = dlHtml;
              break;
            } else if (stat.status === 'error') {
              throw new Error(stat.error || 'Xatolik');
            } else {
              if (msgEl) msgEl.textContent = stat.message || 'Tahlil qilinmoqda...';
            }
          }

          if (!pollDone) throw new Error('Vaqt tugadi');

        } catch (err) {
          if (iconEl) iconEl.textContent = '❌';
          if (msgEl) {
            msgEl.textContent = err.message || 'Xatolik';
            msgEl.style.color = '#ef4444';
          }
        }
      }

      btn.disabled = false;
      btn.innerHTML = `${this.icons.zap} <span>Barchasini Konvert Qilish</span>`;
    });

    document.getElementById('btn-mtf-refresh')?.addEventListener('click', () => {
      loadLocalTests();
    });

    // Start by loading Windows Explorer Tree
    loadLocalTests();
  },

  async openOnlineTestPlatform() {
    this.modal({
      title: '🎓 Online MyTestX Platformasi Boshqaruvi',
      maxWidth: '520px',
      contentHtml: `
        <div style="font-size:13px;line-height:1.6;color:#fff;">
          <p style="margin-bottom:12px;color:rgba(255,255,255,0.8);">
            <b>Online MyTestX</b> platformasi kompyuteringizdagi <code>D:\\01. Antigravity\\online mytestx</code> manzilida joylashgan.
          </p>
          <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:12px;margin-bottom:16px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#34d399;">
            cd "D:\\01. Antigravity\\online mytestx"<br>
            npm run dev
          </div>
          <p style="font-size:12px;color:rgba(255,255,255,0.6);margin-bottom:16px;">
            Port: <code>http://localhost:5173</code> yoki <code>http://localhost:3000</code>
          </p>
          <div style="display:flex;justify-content:flex-end;gap:8px;">
            <button class="btn-secondary" onclick="ATLAS.closeModal()">Yopish</button>
            <a href="http://localhost:5173" target="_blank" class="btn-primary" style="background:#3b82f6;color:#fff;text-decoration:none;font-weight:700;padding:8px 16px;border-radius:6px;">
              🌐 Brauzerda Ochish
            </a>
          </div>
        </div>
      `
    });
  }
};

window.ATLAS = ATLAS;

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => ATLAS.init());
} else {
  ATLAS.init();
}




