(function () {
    var KEY = 'bimpact_cookie_consent';
    var banner = document.getElementById('cookieBanner');
    var accept = document.getElementById('cookieAccept');
    var refuse = document.getElementById('cookieRefuse');
    var manage = document.getElementById('cookieManage');

    function getConsent() {
        try { return localStorage.getItem(KEY); } catch (e) { return null; }
    }
    function setConsent(value) {
        try { localStorage.setItem(KEY, value); } catch (e) {}
    }
    function show() { if (banner) banner.hidden = false; }
    function hide() { if (banner) banner.hidden = true; }

    if (banner && !getConsent()) show();

    if (accept) {
        accept.addEventListener('click', function () {
            setConsent('accepted');
            hide();
            window.dispatchEvent(new Event('cookies:accepted'));
        });
    }
    if (refuse) {
        refuse.addEventListener('click', function () {
            setConsent('refused');
            hide();
        });
    }
    if (manage) {
        manage.addEventListener('click', show);
    }
})();
