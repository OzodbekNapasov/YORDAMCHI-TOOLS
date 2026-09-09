/* ============================================================
 *  ATLAS Service Worker
 *  Root scope'dan beriladi (/sw.js), shuning uchun butun saytni qamraydi.
 *
 *  Strategiya:
 *    /api/...        -> faqat tarmoq. Hech qachon keshlanmaydi: javoblar
 *                       autentifikatsiyaga bog'liq va tez o'zgaradi.
 *    HTML (navigate)  -> avval tarmoq, uzilsa keshdagi qobiq.
 *    JS / CSS         -> keshdan darrov beriladi, fonda yangilanadi
 *                       (stale-while-revalidate) — eski kod qotib qolmaydi.
 *    Rasm / shrift    -> avval kesh.
 * ============================================================ */

const VERSION = 'atlas-v2.7.9';
const SHELL_CACHE = `${VERSION}-shell`;
const ASSET_CACHE = `${VERSION}-assets`;

const SHELL_URLS = [
  '/',
  '/static/css/atlas.css',
  '/static/js/atlas.js',
  '/static/img/pwa-icon-192.png',
  '/static/img/pwa-icon-512.png',
  '/static/manifest.webmanifest',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      // Bittasi tushmasa ham o'rnatish buzilmasin
      .then((cache) => Promise.allSettled(SHELL_URLS.map((u) => cache.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Sahifa "yangilanishni hoziroq qo'lla" desa
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

function isApi(url) {
  return url.pathname.startsWith('/api/')
    || url.pathname.startsWith('/set_webhook')
    || url.pathname.startsWith('/delete_webhook')
    || url.pathname.startsWith('/webhook_info');
}

function isAsset(url) {
  return /\.(css|js|png|jpg|jpeg|svg|webp|ico|woff2?|ttf)$/i.test(url.pathname);
}

self.addEventListener('fetch', (event) => {
  const req = event.request;

  // GET bo'lmagan (POST/DELETE) so'rovlarga umuman aralashmaymiz
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // Boshqa domenlar (Google Fonts va h.k.) — brauzerning o'ziga qoldiramiz
  if (url.origin !== self.location.origin) return;

  // API — hech qachon keshlanmaydi
  if (isApi(url)) return;

  // Sahifa ochilishi: avval tarmoq, oflaynda keshdagi qobiq
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(SHELL_CACHE).then((c) => c.put('/', copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match('/', { ignoreSearch: true })
          .then((cached) => cached || new Response(
            '<!doctype html><meta charset="utf-8">'
            + '<title>ATLAS — oflayn</title>'
            + '<body style="font-family:system-ui;background:#051a1d;color:#e6fffb;'
            + 'display:flex;align-items:center;justify-content:center;height:100vh;'
            + 'margin:0;text-align:center;padding:24px">'
            + '<div><h2>Internet aloqasi yo’q</h2>'
            + '<p style="opacity:.7">Aloqa tiklangach sahifani yangilang.</p></div>',
            { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
          ))
        )
    );
    return;
  }

  if (!isAsset(url)) return;

  const isCode = /\.(css|js)$/i.test(url.pathname);

  if (isCode) {
    // stale-while-revalidate: darrov keshdan, fonda yangisini olib qo'yadi
    event.respondWith(
      caches.open(ASSET_CACHE).then((cache) =>
        cache.match(req).then((cached) => {
          const network = fetch(req)
            .then((res) => {
              if (res && res.status === 200) cache.put(req, res.clone());
              return res;
            })
            .catch(() => cached);
          return cached || network;
        })
      )
    );
    return;
  }

  // Rasm/shrift — avval kesh
  event.respondWith(
    caches.match(req).then((cached) =>
      cached || fetch(req).then((res) => {
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(ASSET_CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      })
    )
  );
});
