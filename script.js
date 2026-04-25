(function () {
  'use strict';

  // ----- Scroll reveal -----
  const revealEls = document.querySelectorAll('.service-card, .project-card, .section__title, .section__subtitle, .contact__text, .contact__links');
  revealEls.forEach(function (el) {
    el.classList.add('reveal');
  });

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
        }
      });
    },
    { rootMargin: '0px 0px -60px 0px', threshold: 0.1 }
  );

  revealEls.forEach(function (el) {
    observer.observe(el);
  });

  // ----- Tilt effect on cards -----
  const tiltEls = document.querySelectorAll('[data-tilt]');
  tiltEls.forEach(function (card) {
    if (window.matchMedia('(hover: none)').matches) return;
    card.addEventListener('mousemove', function (e) {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = (y - centerY) / 25;
      const rotateY = (centerX - x) / 25;
      card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-6px) translateZ(8px)';
      card.style.transition = 'none';
    });
    card.addEventListener('mouseleave', function () {
      card.style.transform = '';
      card.style.transition = '';
    });
  });

  // ----- Burger menu -----
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  let drawerLock = false;
  // Lock the page at the user's current scroll-y when the drawer opens.
  // iOS Safari resets scroll to 0 when body has overflow:hidden — this preserves it.
  let savedScrollY = 0;

  function openDrawer() {
    if (!nav) return;
    savedScrollY = window.scrollY || window.pageYOffset || 0;
    burger && burger.classList.add('open');
    nav.classList.add('open');
    document.body.classList.add('menu-open');
    document.documentElement.classList.add('menu-open');
    // Pin the body in place at the saved offset so the page doesn't jump
    document.body.style.top = '-' + savedScrollY + 'px';
  }

  function closeDrawer(opts) {
    if (!nav) return;
    var preserveScroll = opts && opts.preserveScroll;
    burger && burger.classList.remove('open');
    nav.classList.remove('open');
    document.body.classList.remove('menu-open');
    document.documentElement.classList.remove('menu-open');
    document.body.style.top = '';
    if (!preserveScroll) {
      // Restore the scroll position the user was at when they opened the drawer
      window.scrollTo(0, savedScrollY);
    }
  }

  if (burger && nav) {
    var lastTap = 0;
    burger.addEventListener('click', function (e) {
      var now = Date.now();
      if (drawerLock || now - lastTap < 300) {
        e.preventDefault(); e.stopPropagation(); return;
      }
      lastTap = now;
      drawerLock = true;
      e.preventDefault();
      e.stopPropagation();

      if (nav.classList.contains('open')) closeDrawer();
      else                                openDrawer();

      setTimeout(function () { drawerLock = false; }, 320);
    });
  }

  // ----- Smooth scroll for anchor links (works through the drawer) -----
  function headerOffset() {
    var h = document.querySelector('.header');
    return h ? h.getBoundingClientRect().height : 72;
  }
  function scrollToEl(target) {
    var top = target.getBoundingClientRect().top + window.pageYOffset - headerOffset() - 8;
    if (top < 0) top = 0;
    try {
      window.scrollTo({ top: top, behavior: 'smooth' });
    } catch (_) {
      window.scrollTo(0, top);
    }
  }
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      e.preventDefault();
      var target = document.querySelector(id);
      if (!target) return;
      var wasOpen = nav && nav.classList.contains('open');
      if (wasOpen) {
        closeDrawer();
        // Wait for drawer transform transition (300ms) + body class flush
        setTimeout(function () {
          requestAnimationFrame(function () {
            requestAnimationFrame(function () { scrollToEl(target); });
          });
        }, 320);
      } else {
        scrollToEl(target);
      }
    });
  });
})();
