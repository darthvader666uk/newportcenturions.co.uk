/*
 * Newport Centurions Korfball Club — Service Worker
 *
 * Strategy matters here: the previous version was cache-first for *everything*,
 * which meant a returning visitor kept seeing the cached HTML forever and never
 * picked up updated training times, beginner dates or the announcement bar.
 *
 *   Navigations (HTML)  -> network-first, cache as fallback (offline support)
 *   Static assets       -> stale-while-revalidate (fast, self-healing)
 *
 * Bump CACHE_VERSION when the precache list changes.
 */

const CACHE_VERSION = 'v2.0.0';
const CACHE_NAME = `newport-centurions-${CACHE_VERSION}`;

// Offline fallback for navigations we've never cached.
const OFFLINE_URL = '/';

// Assets only — pages are cached on demand as visitors browse, so the list
// never goes stale when a page is added.
const PRECACHE_URLS = [
  '/',
  '/assets/css/styles.min.css',
  '/assets/css/critical.min.css',
  '/images/newport-centurions-korfball-club-400.webp',
  '/images/newport-centurions-korfball-club-800.webp',
  '/images/newport-centurions-korfball-club.webp',
  '/assets/favicon/android-chrome-192x192.png',
  '/assets/favicon/android-chrome-512x512.png',
  '/manifest.json'
];

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        // addAll rejects the whole batch if any single request fails, which
        // would leave the worker uninstalled. Add individually instead.
        return Promise.all(PRECACHE_URLS.map(function (url) {
          return cache.add(url).catch(function () { /* non-fatal */ });
        }));
      })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (names) {
        return Promise.all(names.map(function (name) {
          if (name !== CACHE_NAME) { return caches.delete(name); }
        }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

function isNavigation(request) {
  return request.mode === 'navigate' ||
    (request.method === 'GET' && (request.headers.get('accept') || '').indexOf('text/html') !== -1);
}

function isCacheableAsset(url) {
  return url.pathname.startsWith('/assets/') ||
    url.pathname.startsWith('/images/') ||
    url.hostname === 'cdnjs.cloudflare.com';
}

self.addEventListener('fetch', function (event) {
  const request = event.request;

  if (request.method !== 'GET') { return; }

  // Never intercept analytics — it must fail fast offline, not be cached.
  const url = new URL(request.url);
  if (url.hostname.indexOf('google-analytics.com') !== -1 ||
      url.hostname.indexOf('googletagmanager.com') !== -1) {
    return;
  }

  // --- HTML: network-first, so content updates are never held back by cache.
  if (isNavigation(request)) {
    event.respondWith(
      fetch(request)
        .then(function (response) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(function (cache) { cache.put(request, copy); });
          return response;
        })
        .catch(function () {
          return caches.match(request).then(function (cached) {
            return cached || caches.match(OFFLINE_URL);
          });
        })
    );
    return;
  }

  // --- Assets: serve cached immediately, refresh in the background.
  if (isCacheableAsset(url)) {
    event.respondWith(
      caches.match(request).then(function (cached) {
        const network = fetch(request).then(function (response) {
          if (response && (response.ok || response.type === 'opaque')) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(function (cache) { cache.put(request, copy); });
          }
          return response;
        }).catch(function () { return cached; });

        return cached || network;
      })
    );
    return;
  }

  // Everything else goes straight to the network.
});

// Allows the page to trigger an immediate update without a second reload.
self.addEventListener('message', function (event) {
  if (event.data === 'SKIP_WAITING') { self.skipWaiting(); }
});

self.addEventListener('push', function (event) {
  const options = {
    body: event.data ? event.data.text() : 'New update from Newport Centurions!',
    icon: '/assets/favicon/android-chrome-192x192.png',
    badge: '/assets/favicon/android-chrome-192x192.png',
    data: { url: '/' }
  };
  event.waitUntil(self.registration.showNotification('Newport Centurions', options));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url));
});
