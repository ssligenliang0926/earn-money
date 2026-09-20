/* =========================================================
 * 极简工具箱 · Service Worker
 * 缓存策略：静态资源 Cache First，HTML Network First
 * ========================================================= */
var CACHE_NAME = 'quicktool-v1';
var STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/common.js',
  '/js/analytics.js',
  '/tools/json-formatter.html',
  '/tools/timestamp.html',
  '/tools/base64.html',
  '/tools/url-encode.html',
  '/tools/password-generator.html',
  '/tools/word-counter.html',
  '/tools/color-converter.html',
  '/tools/uuid-generator.html',
  '/tools/markdown-to-html.html',
  '/tools/markdown-preview.html',
  '/tools/regex-tester.html',
  '/tools/rmb-uppercase.html',
  '/tools/qrcode-generator.html',
  '/tools/image-compressor.html',
  '/tools/image-to-base64.html',
  '/tools/http-status-codes.html',
  '/tools/cron-generator.html',
  '/tools/bmi-calculator.html',
  '/tools/unit-converter.html',
  '/tools/hash-generator.html',
  '/tools/radix-converter.html',
  '/tools/html-escape.html',
  '/tools/date-difference.html',
  '/tools/mortgage-calculator.html'
];

// 安装事件：预缓存静态资源
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      console.log('[SW] Cached', STATIC_ASSETS.length, 'assets');
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// 激活事件：清理旧缓存
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames
          .filter(function (name) { return name !== CACHE_NAME; })
          .map(function (name) {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    })
  );
  self.clients.claim();
});

// 请求事件：静态资源 Cache First，HTML Network First
self.addEventListener('fetch', function (event) {
  var url = new URL(event.request.url);

  // API 请求：Network First
  if (url.pathname.indexOf('/api/') !== -1) {
    event.respondWith(
      fetch(event.request)
        .then(function (response) {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(event.request, clone);
          });
          return response;
        })
        .catch(function () {
          return caches.match(event.request);
        })
    );
    return;
  }

  // HTML 页面：Network First
  if (event.request.destination === 'document') {
    event.respondWith(
      fetch(event.request)
        .then(function (response) {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(event.request, clone);
          });
          return response;
        })
        .catch(function () {
          return caches.match(event.request);
        })
    );
    return;
  }

  // 静态资源：Cache First
  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        if (response) {
          return response;
        }
        return fetch(event.request).then(function (response) {
          if (response.status === 200) {
            var clone = response.clone();
            caches.open(CACHE_NAME).then(function (cache) {
              cache.put(event.request, clone);
            });
          }
          return response;
        });
      })
  );
});

// 后台同步（可选）
self.addEventListener('sync', function (event) {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // 后台同步逻辑
  return Promise.resolve();
}

console.log('[SW] Service Worker loaded');
