// Service Worker for Offline Functionality and Caching
// This will make your site work offline and load faster

const CACHE_NAME = 'newport-centurions-v1.0.0';
const urlsToCache = [
  '/',
  '/assets/css/styles.css',
  '/assets/css/critical.css',
  '/images/newport-centurions-korfball-club-400.webp',
  '/images/newport-centurions-korfball-club-800.webp',
  '/images/newport-centurions-korfball-club.webp',
  '/about/',
  '/join-us/',
  '/support/',
  '/what-is-korfball/',
  '/contact/',
  '/assets/favicon/android-chrome-192x192.png',
  '/assets/favicon/android-chrome-512x512.png',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Install Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

// Update Service Worker
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for form submissions when offline
self.addEventListener('sync', function(event) {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Handle background sync operations
  return Promise.resolve();
}

// Push notifications support
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'New update from Newport Centurions!',
    icon: '/assets/favicon/android-chrome-192x192.png',
    badge: '/assets/favicon/android-chrome-192x192.png',
    data: {
      url: '/'
    }
  };

  event.waitUntil(
    self.registration.showNotification('Newport Centurions', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
