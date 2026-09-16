(function () {
    var form = document.getElementById('contactForm');
    if (!form) return;

    var loadedAt = Date.now();
    var status = form.querySelector('.form-status');
    var submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (submitBtn.disabled) return;

        var payload = {
            name: form.querySelector('[name="name"]').value.trim(),
            email: form.querySelector('[name="email"]').value.trim(),
            message: form.querySelector('[name="message"]').value.trim(),
            company_website: form.querySelector('[name="company_website"]').value,
            elapsed: Date.now() - loadedAt,
            locale: document.documentElement.lang || 'fr'
        };

        submitBtn.disabled = true;
        status.textContent = '';
        status.className = 'form-status';

        fetch('/api/contact.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(function (r) {
                return r.json().then(function (data) { return { ok: r.ok, data: data }; });
            })
            .then(function (res) {
                if (res.ok && res.data && res.data.success) {
                    form.reset();
                    status.textContent = form.dataset.success;
                    status.classList.add('success');
                    if (typeof gtag === 'function') gtag('event', 'contact_form_submit');
                } else {
                    status.textContent = form.dataset.error;
                    status.classList.add('error');
                }
            })
            .catch(function () {
                status.textContent = form.dataset.error;
                status.classList.add('error');
            })
            .finally(function () {
                submitBtn.disabled = false;
            });
    });
})();
