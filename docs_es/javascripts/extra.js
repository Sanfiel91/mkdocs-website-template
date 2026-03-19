(function () {
  var measurementId = window.siteAnalyticsMeasurementId || "";
  var initialized = false;

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

  function ensureGtag() {
    if (!window.dataLayer) {
      window.dataLayer = [];
    }

    if (!window.gtag) {
      window.gtag = function () {
        window.dataLayer.push(arguments);
      };
    }

    if (!document.querySelector('script[data-analytics-loader="ga4"]')) {
      var script = document.createElement("script");
      script.async = true;
      script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurementId;
      script.dataset.analyticsLoader = "ga4";
      document.head.appendChild(script);
    }
  }

  function initAnalytics() {
    if (initialized || !measurementId || !hasAnalyticsConsent()) {
      return;
    }

    ensureGtag();
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      anonymize_ip: true,
      page_path: window.location.pathname,
      page_title: document.title,
      page_location: window.location.href
    });
    initialized = true;
  }

  function trackPage(pathname) {
    if (!initialized || !window.gtag) {
      return;
    }

    window.gtag("config", measurementId, {
      page_path: pathname,
      page_title: document.title,
      page_location: window.location.href
    });
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
        if (!initialized || !window.gtag) {
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
    initAnalytics();
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
      initAnalytics();
      trackPage(url.pathname + url.hash);
    });
  }
})();
