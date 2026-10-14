/* ===================================================================
   HermesIA · Botão flutuante de WhatsApp (sempre visível)
   -------------------------------------------------------------------
   Único lugar a editar: WA_NUMBER e WA_TEXT abaixo.
   Formato do número: DDI + DDD + número, só dígitos (ex.: 5531999999999).
   =================================================================== */
(function () {
  'use strict';
  if (window.__hmWaFab) return;
  window.__hmWaFab = true;

  var WA_NUMBER = '553172285422';
  var WA_TEXT   = 'Olá! Vim pelo site da HermesIA e quero saber mais.';
  var HREF = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(WA_TEXT);

  var css =
    '.hm-wa-fab{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));' +
    'z-index:2147483000;display:flex;align-items:center;gap:10px;height:56px;padding:0 18px 0 14px;border-radius:999px;' +
    'background:#25D366;color:#073b1d;font:600 15px/1 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;' +
    'text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,.35),0 0 0 1px rgba(255,255,255,.12) inset;' +
    'transition:transform .18s ease,box-shadow .18s ease;-webkit-tap-highlight-color:transparent}' +
    '.hm-wa-fab:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(0,0,0,.42)}' +
    '.hm-wa-fab:focus-visible{outline:3px solid #fff;outline-offset:3px}' +
    '.hm-wa-fab svg{width:28px;height:28px;flex:none;fill:currentColor}' +
    '.hm-wa-fab span{white-space:nowrap}' +
    '@media (max-width:520px){.hm-wa-fab{width:58px;height:58px;padding:0;justify-content:center}' +
    '.hm-wa-fab span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}' +
    '@media (prefers-reduced-motion:reduce){.hm-wa-fab{transition:none}.hm-wa-fab:hover{transform:none}}' +
    '@media print{.hm-wa-fab{display:none}}';

  function mount() {
    if (document.querySelector('.hm-wa-fab')) return;

    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var a = document.createElement('a');
    a.className = 'hm-wa-fab';
    a.href = HREF;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.setAttribute('aria-label', 'Falar com a HermesIA no WhatsApp');
    a.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.18-1.14l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.39c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.55-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.25 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.23-.16-.48-.29Z"/>' +
      '</svg><span>Fale com a HermesIA</span>';

    a.addEventListener('click', function () {
      try { if (typeof window.hmTrack === 'function') window.hmTrack('whatsapp_fab_click', { page: location.pathname }); } catch (e) {}
    });

    document.body.appendChild(a);
  }

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);
})();
