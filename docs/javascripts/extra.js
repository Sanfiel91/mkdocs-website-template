(function () {
  var measurementId = window.siteAnalyticsMeasurementId || "";
  var lastConsentState = null;
  var lastTrackedPath = "";

  function getConsent() {
    try {
      if (typeof __md_get === "function") {
        return __md_get("__consent");
      }
    } catch (error) {
      return null;
    }

    return null;
  }

  function hasAnalyticsConsent() {
    var consent = getConsent();
    return !!(consent && consent.analytics);
  }

  function currentPath() {
    return window.location.pathname + window.location.hash;
  }

  function syncConsentState() {
    if (!measurementId || typeof window.gtag !== "function") {
      return hasAnalyticsConsent();
    }

    var granted = hasAnalyticsConsent();

    if (granted === lastConsentState) {
      return granted;
    }

    lastConsentState = granted;
    window.gtag("consent", "update", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: granted ? "granted" : "denied"
    });

    if (granted) {
      trackPage(currentPath(), true);
    }

    return granted;
  }

  function trackPage(pathname, force) {
    if (!measurementId || typeof window.gtag !== "function" || !hasAnalyticsConsent()) {
      return;
    }

    var resolvedPath = pathname || currentPath();

    if (!force && lastTrackedPath === resolvedPath) {
      return;
    }

    window.gtag("event", "page_view", {
      page_path: resolvedPath,
      page_title: document.title,
      page_location: window.location.href
    });
    lastTrackedPath = resolvedPath;
  }

  function bindConversions(root) {
    var scope = root || document;
    var links = scope.querySelectorAll("a.track-conversion");

    links.forEach(function (link) {
      if (link.dataset.analyticsBound === "true") {
        return;
      }

      link.dataset.analyticsBound = "true";
      link.addEventListener("click", function () {
        syncConsentState();

        if (!hasAnalyticsConsent() || typeof window.gtag !== "function") {
          return;
        }

        window.gtag("event", "generate_lead", {
          event_category: "engagement",
          event_label: link.dataset.conversionLabel || link.textContent.trim(),
          link_url: link.href,
          page_path: window.location.pathname
        });
      });
    });
  }

  function boot() {
    syncConsentState();
    bindConversions(document);
  }

  document.addEventListener("DOMContentLoaded", boot);

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      boot();
    });
  }

  if (typeof location$ !== "undefined") {
    location$.subscribe(function (url) {
      syncConsentState();
      trackPage(url.pathname + url.hash);
    });
  }

  window.setInterval(syncConsentState, 1000);

  /* ═══════════════════════════════════════════════════════
     Scroll-triggered reveal animations
     ═══════════════════════════════════════════════════════ */
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var revealTargets = [
    { selector: ".cta-panel", cls: "reveal" },
    { selector: ".webinar-highlight", cls: "reveal" },
    { selector: ".author-card", cls: "reveal" },
    { selector: ".about-preview", cls: "reveal" },
    { selector: ".embedded-video", cls: "reveal" },
    { selector: ".metric-highlight", cls: "reveal" },
    { selector: ".grid.cards > ul", cls: "reveal-stagger" }
  ];

  function initReveal() {
    if (prefersReducedMotion) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

    revealTargets.forEach(function (t) {
      document.querySelectorAll(t.selector).forEach(function (el) {
        if (!el.classList.contains(t.cls)) {
          el.classList.add(t.cls);
        }
        if (!el.classList.contains("is-visible")) {
          observer.observe(el);
        }
      });
    });
  }

  /* ═══════════════════════════════════════════════════════
     Animated metric counters
     ═══════════════════════════════════════════════════════ */
  function easeOutExpo(t) {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }

  function animateCounter(el) {
    if (el.dataset.counted) return;
    el.dataset.counted = "true";

    var text = el.textContent.trim();
    var match = text.match(/^(\d+)([%+]?)$/);

    if (!match) {
      el.style.opacity = "0";
      el.style.transition = "opacity 0.6s ease";
      requestAnimationFrame(function () { el.style.opacity = "1"; });
      return;
    }

    var target = parseInt(match[1], 10);
    var suffix = match[2];
    var duration = 1200;
    var start = performance.now();

    function step(now) {
      var progress = Math.min((now - start) / duration, 1);
      var value = Math.round(easeOutExpo(progress) * target);
      el.textContent = value + suffix;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + suffix;
        el.classList.add("counted");
      }
    }

    el.textContent = "0" + suffix;
    requestAnimationFrame(step);
  }

  function initMetricCounters() {
    if (prefersReducedMotion) return;

    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    document.querySelectorAll(".metric-number").forEach(function (el) {
      if (!el.dataset.counted) {
        counterObserver.observe(el);
      }
    });
  }

  /* ═══════════════════════════════════════════════════════
     Initialize design enhancements
     ═══════════════════════════════════════════════════════ */
  function initDesign() {
    initReveal();
    initMetricCounters();
  }

  document.addEventListener("DOMContentLoaded", initDesign);

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      initDesign();
    });
  }
})();
