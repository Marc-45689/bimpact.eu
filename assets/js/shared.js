/* ═══════════════════════════════════════
   SHARED JS
   Nav scroll state, mobile hamburger,
   reveal-on-scroll, scroll-to-top button,
   article FAQ accordion.
   Vanilla, dependency-free.
   ═══════════════════════════════════════ */

(function () {
    // Align the #contact illustration's top with the bottom of the intro
    // paragraph (.lead), plus a fixed nudge down (Marc's call): that
    // paragraph's height shifts with the heading above it (varies by page
    // and locale), so it's read from the DOM instead of hardcoded.
    const contactSection = document.getElementById('contact');
    const formWrap = contactSection ? contactSection.querySelector('.contact-form-wrap') : null;
    const lead = contactSection ? contactSection.querySelector('.lead') : null;
    const CONTACT_ILLU_NUDGE = 150;
    if (contactSection && formWrap) {
        const alignContactIllustration = () => {
            const target = (lead ? lead.offsetTop + lead.offsetHeight : formWrap.offsetTop) + CONTACT_ILLU_NUDGE;
            contactSection.style.setProperty('--contact-illu-top', target + 'px');
        };
        alignContactIllustration();
        window.addEventListener('resize', alignContactIllustration);
        window.addEventListener('load', alignContactIllustration);
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(alignContactIllustration);
        }
        // Belt and braces: whatever causes the heading/lead above the form
        // to reflow (font swap, translation-specific line wraps, anything
        // else), a ResizeObserver on #contact itself catches the resulting
        // height change directly instead of guessing which event fires it.
        if ('ResizeObserver' in window) {
            new ResizeObserver(alignContactIllustration).observe(contactSection);
        }
    }

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
            const open = navLinks.classList.toggle('open');
            hamburger.classList.toggle('open', open);
            hamburger.setAttribute('aria-expanded', open);
        });
        navLinks.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => {
                navLinks.classList.remove('open');
                hamburger.classList.remove('open');
                hamburger.setAttribute('aria-expanded', false);
            });
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
    const footer = document.querySelector('footer');
    if (scrollBar || scrollTop) {
        const onScrollProgress = () => {
            const h = document.documentElement;
            const ratio = h.scrollTop / (h.scrollHeight - h.clientHeight);
            if (scrollBar) scrollBar.style.width = (ratio * 100) + '%';
            if (scrollTop) {
                const show = h.scrollTop > 600;
                scrollTop.style.opacity = show ? '1' : '0';
                scrollTop.style.pointerEvents = show ? 'auto' : 'none';

                // Dock 10px above the footer instead of floating over it
                // once the footer's top edge reaches the button's resting
                // spot (24px/1.5rem from the viewport bottom).
                if (footer) {
                    const footerTop = footer.getBoundingClientRect().top;
                    const restBottom = 24;
                    if (footerTop < window.innerHeight - restBottom) {
                        scrollTop.classList.add('docked');
                        scrollTop.style.top = (footer.offsetTop - scrollTop.offsetHeight - 10) + 'px';
                    } else {
                        scrollTop.classList.remove('docked');
                        scrollTop.style.top = '';
                    }
                }

                scrollTop.style.transform = show ? 'translateY(0)' : 'translateY(10px)';
            }
        };
        document.addEventListener('scroll', onScrollProgress, { passive: true });
        window.addEventListener('resize', onScrollProgress);
        onScrollProgress();
    }
    if (scrollTop) {
        scrollTop.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // FAQ accordion
    document.querySelectorAll('.article-faq-item').forEach(item => {
        const btn = item.querySelector('.article-faq-question');
        if (btn) {
            btn.addEventListener('click', () => {
                const open = item.classList.toggle('open');
                btn.setAttribute('aria-expanded', open);
            });
        }
    });

    // Current year in footer
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
