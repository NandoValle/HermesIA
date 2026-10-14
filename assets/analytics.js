/* ===================================================================
   HermesIA · Analytics (PostHog + Microsoft Clarity)
   -------------------------------------------------------------------
   >>> ÚNICO lugar a editar: cole as chaves abaixo. <<<
   Enquanto a chave não for colada, o serviço fica DESLIGADO
   (nada quebra no site — hmTrack() vira um no-op seguro).

   Como pegar a chave:  PostHog > Settings > Project > Project API Key
   Formato: phc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   Clarity Project ID:  clarity.microsoft.com > projeto > Settings > Overview
   (também aparece na URL: /projects/view/<PROJECT_ID>/)
   =================================================================== */
(function () {
  'use strict';

  var POSTHOG_KEY  = 'phc_pUP4S7Kry4KRGLUHkswYYTZao6YjuxQhaCrYGCVqVfR5';   // projeto "HermesIA" (org Hermesia.ia.br)
  var POSTHOG_HOST = 'https://us.i.posthog.com';        // US Cloud
  var CLARITY_ID   = 'y2x78qwj5j';                      // projeto "HermesIA" (hermesia.ia.br)

  /* ---- daqui pra baixo não precisa mexer ---- */

  var cfg = window.HM_ANALYTICS || {};

  // stub seguro: chamar window.hmTrack() nunca derruba a página,
  // mesmo antes do PostHog carregar ou se a chave ainda não existir.
  window.hmTrack = function () {};

  /* ---- Microsoft Clarity (mapas de calor + gravação de sessão) -------------
     Fica ANTES da trava do PostHog de propósito: os dois serviços são
     independentes, um não pode morrer por falta da chave do outro.
     Trava 1: sem ID real, não injeta nada (seguro publicar assim).
     Trava 2: mesma convenção do PostHog — página que declara
              window.HM_ANALYTICS={record:false} (ex.: /experimente/) fica fora.
     Trava 3: id "clarity-script" impede segunda injeção na mesma página.
     Loader idêntico ao do pacote oficial @microsoft/clarity v1.0.2.        */
  if (CLARITY_ID.indexOf('COLE_SEU') === -1 && cfg.record !== false) {
    (function (c, l, a, r, i, t, y) {
      if (l.getElementById('clarity-script')) return;
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1;
      t.src = 'https://www.clarity.ms/tag/' + i;
      t.id = 'clarity-script';
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }

  // TRAVA: sem chave real, não inicializa nada (seguro publicar assim).
  if (POSTHOG_KEY.indexOf('COLE_SUA_CHAVE') !== -1) return;

  // Loader oficial do PostHog (array.js)
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug getPageViewId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    person_profiles: 'identified_only',
    autocapture: true,
    capture_pageview: true,
    capture_pageleave: true,
    // Superfície de produto (ex.: /experimente/) manda { record:false } e o replay fica OFF.
    disable_session_recording: cfg.record === false,
    session_recording: {
      maskAllInputs: true,                                // nunca grava o que é digitado
      maskTextSelector: '.doc, .transcr, [data-ph-mask]'  // e mascara documento/transcrição gerados
    }
  });

  // Helper único usado pelas páginas: seguro e à prova de erro.
  // O mesmo evento vai para os dois: PostHog (com props) e Clarity (só o nome,
  // vira Smart event lá). Nenhum HTML precisou mudar por causa disso.
  window.hmTrack = function (ev, props) {
    try { if (window.posthog) posthog.capture(ev, props || {}); } catch (e) {}
    try { if (window.clarity)  clarity('event', ev); } catch (e) {}
  };
})();
