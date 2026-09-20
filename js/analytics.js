/* =========================================================
 * 极简工具箱 · 数据分析埋点脚本
 * 兼容 Google Analytics 4 (GA4) 和 百度统计
 * ========================================================= */
(function () {
  'use strict';

  // ================= 配置 =================
  window.ANALYTICS_CONFIG = {
    // Google Analytics 4 (推荐)
    ga4: {
      enabled: false,
      trackingId: 'G-XXXXXXXXXX'  // 替换为你的 GA4 Measurement ID
    },
    // 百度统计
    baidu: {
      enabled: false,
      token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  // 替换为你的百度统计token
    }
  };

  // ================= Google Analytics 4 =================
  function initGA4(config) {
    if (!config.enabled || !config.trackingId) return;

    // GA4 脚本
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + config.trackingId;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', config.trackingId);

    console.log('[Analytics] GA4 initialized:', config.trackingId);
  }

  // ================= 百度统计 =================
  function initBaidu(config) {
    if (!config.enabled || !config.token) return;

    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://hm.baidu.com/hm.js?' + config.token;
    document.head.appendChild(script);

    console.log('[Analytics] Baidu Tongji initialized');
  }

  // ================= 事件追踪 =================
  var analyticsInitialized = false;

  function trackEvent(category, action, label, value) {
    var eventData = {
      event_category: category,
      event_action: action,
      event_label: label,
      event_value: value
    };

    // GA4 事件
    if (window.gtag) {
      gtag('event', action, eventData);
    }

    // 百度统计事件
    if (window._hmt) {
      _hmt.push(['_trackEvent', category, action, label, value]);
    }
  }

  // ================= 页面浏览追踪 =================
  function trackPageView() {
    var path = location.pathname;
    var title = document.title;

    trackEvent('Page', 'view', path, null);

    // 识别工具页面
    if (path.indexOf('/tools/') !== -1) {
      var toolName = path.split('/').pop().replace('.html', '');
      trackEvent('Tool', 'open', toolName, null);
    }
  }

  // ================= 初始化 =================
  function init() {
    if (analyticsInitialized) return;
    analyticsInitialized = true;

    var config = window.ANALYTICS_CONFIG || {};
    initGA4(config.ga4 || {});
    initBaidu(config.baidu || {});

    // 页面加载时自动追踪
    trackPageView();

    // 监听页面切换（单页应用）
    if (typeof history !== 'undefined') {
      var origPushState = history.pushState;
      history.pushState = function () {
        origPushState.apply(this, arguments);
        setTimeout(trackPageView, 100);
      };

      window.addEventListener('popstate', function () {
        setTimeout(trackPageView, 100);
      });
    }

    console.log('[Analytics] Initialized');
  }

  // 页面加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 暴露全局函数
  window.trackEvent = trackEvent;
  window.trackPageView = trackPageView;
})();
