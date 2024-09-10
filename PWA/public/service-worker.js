const CACHE_NAME = 'nota-cache-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/styles.css',
    '/icon-large.png',
    '/icon.png', 
    '/manifest.json',
];


self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Archivos cacheados');
                return cache.addAll(urlsToCache);
            })
    );
});

// Interceptar peticiones de red y servir archivos cacheados
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
    );
});

// Actualizar el Service Worker cuando se detectan cambios
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
