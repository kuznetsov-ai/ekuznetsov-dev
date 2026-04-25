(function () {
  // Priority: ?lang= query → localStorage → browser language → English (default)
  var params = new URLSearchParams(window.location.search);
  var urlLang = params.get('lang');
  if (urlLang === 'en' || urlLang === 'ru') {
    try { localStorage.setItem('ek_lang', urlLang); } catch (_) {}
    params.delete('lang');
    var clean = window.location.pathname + (params.toString() ? '?' + params.toString() : '') + window.location.hash;
    history.replaceState(null, '', clean);
  }

  var stored;
  try { stored = localStorage.getItem('ek_lang'); } catch (_) {}

  var picked;
  if (stored === 'en' || stored === 'ru') {
    picked = stored;
  } else {
    // Auto-detect from browser. Russian only if browser explicitly says so;
    // every other language defaults to English.
    var langs = navigator.languages || [navigator.language || 'en'];
    picked = 'en';
    for (var i = 0; i < langs.length; i++) {
      if (langs[i] && langs[i].toLowerCase().indexOf('ru') === 0) {
        picked = 'ru';
        break;
      }
    }
  }

  window.__ekLang = picked;
  document.documentElement.lang = picked;
})();
