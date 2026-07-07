// Service worker mínimo — só pra o PWA ser instalável (ícone na tela inicial).
// Não faz cache offline: o painel precisa de dados ao vivo.
self.addEventListener('install', (e) => self.skipWaiting());
self.addEventListener('activate', (e) => self.clients.claim());
self.addEventListener('fetch', () => { /* pass-through; deixa a rede resolver */ });
