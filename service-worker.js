self.addEventListener('install', (e) => {
  console.log('NEXA Service Worker installé');
});

self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request));
});