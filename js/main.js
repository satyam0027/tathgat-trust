/**
 * Tathagat Trust — Main JavaScript
 * Navigation, scroll animations, counters, lightbox, contact form
 */

(function () {
  'use strict';

  /* ── Mobile Navigation ── */
  const navToggle = document.querySelector('.nav-toggle');
  const mainNav = document.querySelector('.main-nav');
  const navDropdowns = document.querySelectorAll('.nav-dropdown');

  if (navToggle && mainNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = mainNav.classList.toggle('open');
      navToggle.classList.toggle('active', isOpen);
      navToggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    mainNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          mainNav.classList.remove('open');
          navToggle.classList.remove('active');
          navToggle.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        }
      });
    });
  }

  navDropdowns.forEach((dropdown) => {
    const toggle = dropdown.querySelector('.nav-dropdown__toggle');
    if (!toggle) return;

    toggle.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        dropdown.classList.toggle('open');
      }
    });
  });

  /* ── Header scroll shadow ── */
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* ── Active nav link ── */
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-list a').forEach((link) => {
    const href = link.getAttribute('href');
    if (!href || href === '#') return;
    const linkPage = href.split('/').pop();
    if (linkPage === currentPage || (currentPage === '' && linkPage === 'index.html')) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });

  /* ── Scroll Reveal (IntersectionObserver) ── */
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    revealElements.forEach((el) => revealObserver.observe(el));
  } else {
    revealElements.forEach((el) => el.classList.add('visible'));
  }

  /* ── Animated Stat Counters ── */
  const counters = document.querySelectorAll('[data-counter]');

  function animateCounter(el) {
    const target = parseFloat(el.dataset.counter);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const decimals = (el.dataset.decimals !== undefined) ? parseInt(el.dataset.decimals, 10) : 0;
    const duration = 2000;
    const start = performance.now();

    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = target * eased;

      el.textContent = prefix + (decimals > 0 ? current.toFixed(decimals) : Math.floor(current)) + suffix;

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = prefix + (decimals > 0 ? target.toFixed(decimals) : target) + suffix;
      }
    }

    requestAnimationFrame(update);
  }

  if (counters.length && 'IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach((counter) => counterObserver.observe(counter));
  }

  /* ── Gallery Lightbox ── */
  const lightbox = document.getElementById('lightbox');
  const galleryItems = document.querySelectorAll('.gallery-item[data-lightbox]');

  if (lightbox && galleryItems.length) {
    const lightboxImg = lightbox.querySelector('.lightbox__content img');
    const lightboxCaption = lightbox.querySelector('.lightbox__caption');
    const lightboxClose = lightbox.querySelector('.lightbox__close');

    function openLightbox(src, alt) {
      lightboxImg.src = src;
      lightboxImg.alt = alt || '';
      if (lightboxCaption) {
        lightboxCaption.textContent = alt || '';
      }
      lightbox.classList.add('active');
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      lightboxClose.focus();
    }

    function closeLightbox() {
      lightbox.classList.remove('active');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      lightboxImg.src = '';
    }

    galleryItems.forEach((item) => {
      item.addEventListener('click', () => {
        const img = item.querySelector('img');
        if (img) {
          openLightbox(img.src, img.alt);
        }
      });

      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const img = item.querySelector('img');
          if (img) openLightbox(img.src, img.alt);
        }
      });

      item.setAttribute('tabindex', '0');
      item.setAttribute('role', 'button');
    });

    lightboxClose.addEventListener('click', closeLightbox);

    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
      }
    });
  }

  /* ── Contact Form ── */
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const formData = {
        name: contactForm.querySelector('#name')?.value,
        email: contactForm.querySelector('#email')?.value,
        phone: contactForm.querySelector('#phone')?.value,
        message: contactForm.querySelector('#message')?.value,
      };

      // TODO: wire to backend/Google Sheets/CRM later
      console.log('Contact form submission:', formData);

      const successMsg = contactForm.querySelector('.form-success');
      if (successMsg) {
        successMsg.classList.add('visible');
        setTimeout(() => successMsg.classList.remove('visible'), 5000);
      }

      contactForm.reset();
    });
  }

  /* ── Hero video autoplay ── */
  const heroVideo = document.querySelector('.hero__video');
  if (heroVideo) {
    heroVideo.muted = true;
    heroVideo.defaultMuted = true;
    heroVideo.setAttribute('muted', '');

    const tryPlay = () => {
      const promise = heroVideo.play();
      if (promise) promise.catch(() => {});
    };

    tryPlay();
    heroVideo.addEventListener('loadeddata', tryPlay, { once: true });
  }

  /* ── Donate button placeholder ── */
  document.querySelectorAll('[data-donate]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      // TODO: Integrate donation payment gateway
      if (!btn.getAttribute('href') || btn.getAttribute('href') === '#') {
        e.preventDefault();
        alert('Donation portal coming soon. Please contact us for contribution details.');
      }
    });
  });

})();
