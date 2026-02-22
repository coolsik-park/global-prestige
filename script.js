document.addEventListener('DOMContentLoaded', () => {

    /* --- Language Selection Logic --- */
    let currentLang = 'ko';

    function isHTMLString(str) {
        return /<[a-z][\s\S]*>/i.test(str);
    }

    function setLanguage(lang) {
        currentLang = lang;
        const els = document.querySelectorAll('[data-i18n]');

        els.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                const text = translations[lang][key];
                if (isHTMLString(text)) {
                    el.innerHTML = text; // Allow HTML inject for highlights etc
                } else {
                    el.textContent = text;
                }
            }
        });

        // Set placeholders
        const phs = document.querySelectorAll('[data-i18n-ph]');
        phs.forEach(el => {
            const key = el.getAttribute('data-i18n-ph');
            if (translations[lang] && translations[lang][key]) {
                el.placeholder = translations[lang][key];
            }
        });

        // Update active class on dropdown
        document.querySelectorAll('.lang-menu li a').forEach(a => {
            a.classList.remove('active');
            if (a.getAttribute('data-lang') === lang) {
                a.classList.add('active');
                // Update button text
                const langNameMap = {
                    ko: 'KOR', en: 'ENG', ja: 'JPN', zh: 'CHN', vi: 'VIE'
                };
                document.getElementById('current-lang').innerHTML = `<i class="fa-solid fa-globe"></i> ${langNameMap[lang]} <i class="fa-solid fa-chevron-down" style="font-size: 0.8em; margin-left: 5px;"></i>`;
            }
        });
    }

    // Bind dropdown click
    document.querySelectorAll('.lang-menu li a').forEach(a => {
        a.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedLang = a.getAttribute('data-lang');
            setLanguage(selectedLang);
        });
    });

    // Initialize Language
    setLanguage(currentLang);

    /* --- Reveal animations on scroll --- */
    const reveals = document.querySelectorAll('.reveal');

    function reveal() {
        const windowHeight = window.innerHeight;
        const elementVisible = 150;

        reveals.forEach((reveal) => {
            const elementTop = reveal.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    }

    // Initial check
    setTimeout(() => {
        reveal();
    }, 100);

    window.addEventListener('scroll', reveal);

    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            // On mobile, if this is a dropdown toggle, don't scroll
            if (window.innerWidth <= 768 && this.parentElement.classList.contains('dropdown')) {
                return;
            }

            e.preventDefault();
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                // Adjust scroll offset based on if it's a submenu item
                let offset = 70; // Default navbar height

                // Calculate absolute position relative to document
                const rect = targetElement.getBoundingClientRect();
                const absoluteY = window.pageYOffset + rect.top;

                // If targeting high-up sections specifically inside the service container, offset more to account for header
                if (targetId.startsWith('#service-')) {
                    offset = 120; // Allow enough space to see the title

                    if (targetId === '#service-1') {
                        offset = 180; // Add even more space for the first one so the section title "Exclusive Services" doesn't block it
                    }
                }

                window.scrollTo({
                    top: absoluteY - offset,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Simple mobile menu toggle
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navRight = document.querySelector('.nav-right');
    const dropdowns = document.querySelectorAll('.dropdown > a');

    if (mobileBtn) {
        mobileBtn.addEventListener('click', () => {
            const isActive = navLinks.classList.toggle('active');
            navRight.classList.toggle('active');

            // Toggle full screen menu class and body scroll lock
            if (isActive) {
                document.body.classList.add('no-scroll');
                navbar.classList.add('menu-open');
            } else {
                document.body.classList.remove('no-scroll');
                navbar.classList.remove('menu-open');
            }
        });
    }

    // Handle mobile dropdown clicks
    dropdowns.forEach(dropdownAttr => {
        dropdownAttr.addEventListener('click', (e) => {
            // Only prevent default and toggle if we're on mobile
            if (window.innerWidth <= 768) {
                e.preventDefault();
                dropdownAttr.parentElement.classList.toggle('active');
            }
        });
    });

    // Close mobile menu when a link is clicked
    document.querySelectorAll('.nav-links li a:not(.dropdown > a), .nav-btn, .lang-menu li a:not(.dropdown > a)').forEach(a => {
        a.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                navLinks.classList.remove('active');
                navRight.classList.remove('active');
                document.body.classList.remove('no-scroll');
                navbar.classList.remove('menu-open');
            }
        });
    });
});
