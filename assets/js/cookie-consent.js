/* ═══════════════════════════════════════
   COOKIE CONSENT
   Minimal, dependency-free. Remembers choice
   in localStorage. Listen for window events
   'cookies:accepted' / 'cookies:declined' to
   gate analytics or third-party scripts.
   ═══════════════════════════════════════ */

(function () {
    const KEY = 'cc:choice:v1';
    const stored = localStorage.getItem(KEY);

    const banner = document.getElementById('cookie-consent');
    if (!banner) return;

    if (!stored) banner.classList.add('visible');

    const accept = () => {
        localStorage.setItem(KEY, 'accept');
        banner.classList.remove('visible');
        window.dispatchEvent(new CustomEvent('cookies:accepted'));
    };
    const decline = () => {
        localStorage.setItem(KEY, 'decline');
        banner.classList.remove('visible');
        window.dispatchEvent(new CustomEvent('cookies:declined'));
    };

    banner.querySelector('[data-cc-accept]')?.addEventListener('click', accept);
    banner.querySelector('[data-cc-decline]')?.addEventListener('click', decline);

    window.cookieConsent = {
        status: () => localStorage.getItem(KEY),
        accept, decline
    };

    if (stored === 'accept') window.dispatchEvent(new CustomEvent('cookies:accepted'));
})();
