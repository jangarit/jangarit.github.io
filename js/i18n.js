// i18n.js
// Handles automatic language detection and switching for ES/EN

(function() {
    function getSavedLang() {
        return localStorage.getItem('site_lang');
    }

    function getBrowserLang() {
        const lang = navigator.language || navigator.userLanguage;
        return lang.toLowerCase().startsWith('es') ? 'es' : 'en';
    }

    function getCurrentLang() {
        return getSavedLang() || getBrowserLang();
    }

    window.setLang = function(lang) {
        localStorage.setItem('site_lang', lang);
        applyLang(lang);
    };

    function applyLang(lang) {
        document.documentElement.lang = lang;

        // Simple text replacement based on data attributes
        document.querySelectorAll('[data-lang-es]').forEach(function(el) {
            const esText = el.getAttribute('data-lang-es');
            const enText = el.getAttribute('data-lang-en') || esText; // fallback to es if en is empty
            el.innerHTML = lang === 'es' ? esText : enText;
        });

        // Toggle visibility for paired elements (e.g. <span data-lang="es">)
        document.querySelectorAll('[data-lang]').forEach(function(el) {
            if (el.getAttribute('data-lang') === lang) {
                el.classList.remove('lang-hidden');
            } else {
                el.classList.add('lang-hidden');
            }
        });

        // Placeholders for inputs and textareas
        document.querySelectorAll('[data-lang-es-placeholder]').forEach(function(el) {
            const esPlaceholder = el.getAttribute('data-lang-es-placeholder');
            const enPlaceholder = el.getAttribute('data-lang-en-placeholder') || esPlaceholder;
            el.placeholder = lang === 'es' ? esPlaceholder : enPlaceholder;
        });
        
        // Form submit buttons
        document.querySelectorAll('input[type="submit"][data-lang-es-value]').forEach(function(el) {
            const esVal = el.getAttribute('data-lang-es-value');
            const enVal = el.getAttribute('data-lang-en-value') || esVal;
            el.value = lang === 'es' ? esVal : enVal;
        });

        // Update active class on language toggle links
        document.querySelectorAll('[data-lang-select]').forEach(function(el) {
            if (el.getAttribute('data-lang-select') === lang) {
                el.classList.add('lang-active');
            } else {
                el.classList.remove('lang-active');
            }
        });
    }

    // Run on DOM loaded
    document.addEventListener('DOMContentLoaded', function() {
        applyLang(getCurrentLang());
    });
})();

// ─── Preloader fallback for GitHub Pages ────────────────────────────────────
// Webflow's IX2 animation engine may not fire its "page loaded" trigger when
// hosted outside Webflow servers, leaving the preloader stuck on screen.
// This fallback forces it to hide after 3 s (or on window load, whichever
// comes first), so the user always sees the site content.
(function () {
    function hidePreloader() {
        var el = document.querySelector('.preloader');
        if (!el) return;
        el.style.transition = 'opacity 0.4s ease';
        el.style.opacity = '0';
        setTimeout(function () { el.style.display = 'none'; }, 420);
    }

    // Fire as soon as the window finishes loading
    window.addEventListener('load', function () {
        setTimeout(hidePreloader, 500); // small grace period for IX2
    });

    // Hard cap: never show the preloader for more than 3 seconds
    setTimeout(hidePreloader, 3000);
})();
