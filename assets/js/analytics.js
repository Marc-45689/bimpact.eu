(function () {
    var GA_ID = 'G-PZEBPWJJFG';
    var CONSENT_KEY = 'bimpact_cookie_consent';

    function loadGA() {
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
        document.head.appendChild(s);

        window.dataLayer = window.dataLayer || [];
        window.gtag = function () { dataLayer.push(arguments); };
        gtag('js', new Date());
        gtag('config', GA_ID);
    }

    var consent;
    try { consent = localStorage.getItem(CONSENT_KEY); } catch (e) { consent = null; }

    if (consent === 'accepted') {
        loadGA();
    } else {
        window.addEventListener('cookies:accepted', loadGA, { once: true });
    }
})();
