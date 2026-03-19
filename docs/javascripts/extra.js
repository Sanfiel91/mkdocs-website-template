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
})();
