const CACHE='miami-icon-v0.7.1';
const CORE=[
  './',
  './index.html',
  './manifest.webmanifest',
  './version.json',
  './icon-192.png',
  './icon-512.png',
  './offline.html'
];

self.addEventListener('install', event=>{
  event.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)));
});

self.addEventListener('activate', event=>{
  event.waitUntil(
    caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener('message', event=>{
  if(event.data && event.data.type==='SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', event=>{
  const req=event.request;
  if(req.method!=='GET') return;

  const url=new URL(req.url);
  if(url.origin!==self.location.origin) return; // LIVE/external links bypass cache.

  // Always ask network first for the version marker.
  if(url.pathname.endsWith('/version.json')){
    event.respondWith(
      fetch(req,{cache:'no-store'}).catch(()=>caches.match('./version.json'))
    );
    return;
  }

  // Navigation/index: network-first so deployments appear without reinstalling.
  if(req.mode==='navigate' || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/')){
    event.respondWith(
      fetch(req).then(resp=>{
        const copy=resp.clone();
        caches.open(CACHE).then(c=>c.put('./index.html',copy));
        return resp;
      }).catch(()=>caches.match('./index.html').then(x=>x||caches.match('./offline.html')))
    );
    return;
  }

  // Static app shell: cache-first with background refresh.
  event.respondWith(
    caches.match(req).then(hit=>{
      const refresh=fetch(req).then(resp=>{
        const copy=resp.clone();
        caches.open(CACHE).then(c=>c.put(req,copy));
        return resp;
      }).catch(()=>null);
      return hit || refresh || caches.match('./offline.html');
    })
  );
});
