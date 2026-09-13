/* ═══════════════════════════════════════
   SHARED JS
   Nav scroll state, mobile hamburger,
   reveal-on-scroll, scroll-to-top button.
   Vanilla, dependency-free.
   ═══════════════════════════════════════ */

(function () {
    // Nav scroll state
    const nav = document.querySelector('nav');
    if (nav) {
        const onScroll = () => {
            nav.classList.toggle('scrolled', window.scrollY > 40);
        };
        document.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // Mobile hamburger
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });
        navLinks.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => navLinks.classList.remove('open'));
        });
    }

    // Reveal on scroll
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        reveals.forEach(el => io.observe(el));
    }

    // Scroll progress bar + back-to-top
    const scrollBar = document.getElementById('scrollProgress');
    const scrollTop = document.getElementById('scrollTop');
    if (scrollBar || scrollTop) {
        const onScrollProgress = () => {
            const h = document.documentElement;
            const ratio = h.scrollTop / (h.scrollHeight - h.clientHeight);
            if (scrollBar) scrollBar.style.width = (ratio * 100) + '%';
            if (scrollTop) {
                const show = h.scrollTop > 600;
                scrollTop.style.opacity = show ? '1' : '0';
                scrollTop.style.pointerEvents = show ? 'auto' : 'none';
                scrollTop.style.transform = show ? 'translateY(0)' : 'translateY(10px)';
            }
        };
        document.addEventListener('scroll', onScrollProgress, { passive: true });
        onScrollProgress();
    }
    if (scrollTop) {
        scrollTop.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Current year in footer
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
