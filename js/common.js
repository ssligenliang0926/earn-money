/* =========================================================
 * 极简工具箱 · 公共脚本
 * 导航渲染 / 主题切换 / 广告位注入 / 通用工具函数
 * ========================================================= */
(function () {
  'use strict';

  /* ================= 广告配置（变现核心） =================
   * 操作步骤：
   * 1. 网站上线后注册 Google AdSense（或其他广告联盟），等待审核通过
   * 2. 将下方 enabled 改为 true，并把广告联盟给出的代码粘贴到 code 中
   * 3. 所有页面的 .ad-slot 广告位会自动展示广告，开始产生收益
   */
  window.AD_CONFIG = {
    enabled: false,
    code: ''
  };

  var isToolPage = location.pathname.indexOf('/tools/') !== -1;
  var BASE = isToolPage ? '../' : './';

  /* 全站工具清单（新增工具时在此登记，导航自动更新） */
  var TOOLS = [
    { file: 'json-formatter.html',     name: 'JSON 格式化',  icon: '{}',  desc: 'JSON 校验、格式化与压缩，错误精准定位' },
    { file: 'timestamp.html',          name: '时间戳转换',    icon: '⏱️', desc: 'Unix 时间戳与日期时间互转，实时更新' },
    { file: 'base64.html',             name: 'Base64 编解码', icon: '🔤', desc: '文本 Base64 编码与解码，完美支持中文' },
    { file: 'url-encode.html',         name: 'URL 编解码',    icon: '🔗', desc: 'URL 编码与解码，支持整段 URL 或单个参数' },
    { file: 'password-generator.html', name: '密码生成器',    icon: '🔑', desc: '生成高强度随机密码，长度与字符类型可定制' },
    { file: 'word-counter.html',       name: '字数统计',      icon: '📝', desc: '字符数、字数、行数实时统计，中英混排准确' },
    { file: 'color-converter.html',    name: '颜色转换',      icon: '🎨', desc: 'HEX、RGB、HSL 颜色互转，实时预览取色' },
    { file: 'uuid-generator.html',     name: 'UUID 生成器',   icon: '🆔', desc: '批量生成 UUID v4，支持大写与去连字符' },
    { file: 'markdown-to-html.html',   name: 'Markdown 转 HTML', icon: '📄', desc: 'Markdown 实时转换为 HTML，支持渲染预览' },
    { file: 'regex-tester.html',       name: '正则测试',      icon: '🔍', desc: '正则表达式实时匹配、高亮与替换' },
    { file: 'rmb-uppercase.html',      name: '金额转大写',    icon: '💰', desc: '人民币金额一键转财务规范中文大写' },
    { file: 'qrcode-generator.html',   name: '二维码生成器',  icon: '🔳', desc: '实时生成二维码，支持中文，下载 PNG' },
    { file: 'image-compressor.html',   name: '图片压缩',      icon: '🗜️', desc: '本地压缩图片体积，可调质量与尺寸' }
  ];

  function toolUrl(file) {
    return (isToolPage ? '../tools/' : 'tools/') + file;
  }

  /* ---------------- 顶部导航（自动注入） ---------------- */
  function renderHeader() {
    var current = location.pathname.split('/').pop() || 'index.html';
    var links = TOOLS.map(function (t) {
      var cls = current === t.file ? ' class="active"' : '';
      return '<a href="' + toolUrl(t.file) + '"' + cls + '>' + t.name + '</a>';
    }).join('');

    var html =
      '<header class="site-header"><div class="header-inner">' +
      '<a class="logo" href="' + BASE + 'index.html"><span class="logo-icon">🧰</span>极简工具箱</a>' +
      '<nav class="nav-links">' + links + '</nav>' +
      '<button class="theme-toggle" id="themeToggle" type="button" title="切换深浅主题">🌙</button>' +
      '</div></header>';

    document.body.insertAdjacentHTML('afterbegin', html);
  }

  /* ---------------- 主题切换 ---------------- */
  function initTheme() {
    var btn = document.getElementById('themeToggle');
    if (!btn) return;
    btn.textContent = document.documentElement.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';
    btn.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      btn.textContent = next === 'dark' ? '☀️' : '🌙';
    });
  }

  /* ---------------- 广告位注入 ---------------- */
  function renderAds() {
    var slots = document.querySelectorAll('.ad-slot');
    for (var i = 0; i < slots.length; i++) {
      if (window.AD_CONFIG && window.AD_CONFIG.enabled && window.AD_CONFIG.code) {
        slots[i].innerHTML = window.AD_CONFIG.code;
      } else {
        slots[i].innerHTML = '<span class="ad-placeholder">广告位</span>';
      }
    }
  }

  /* ---------------- 页脚（自动注入） ---------------- */
  function renderFooter() {
    var year = new Date().getFullYear();
    var html =
      '<footer class="site-footer">' +
      '<div class="footer-brand">🧰 极简工具箱 · 免费在线工具，打开即用</div>' +
      '<div>© ' + year + ' 极简工具箱 · 所有工具均在浏览器本地运行，数据不上传服务器</div>' +
      '</footer>';
    document.body.insertAdjacentHTML('beforeend', html);
  }

  /* ---------------- 通用：Toast 提示 ---------------- */
  function toast(msg) {
    var el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('show'); });
    setTimeout(function () { el.remove(); }, 1600);
  }

  /* ---------------- 通用：复制到剪贴板 ---------------- */
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      toast('已复制到剪贴板');
    } catch (e) {
      toast('复制失败，请手动复制');
    }
    ta.remove();
  }

  window.copyText = function (text) {
    if (text === undefined || text === null || text === '') {
      toast('没有可复制的内容');
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { toast('已复制到剪贴板'); },
        function () { fallbackCopy(text); }
      );
    } else {
      fallbackCopy(text);
    }
  };

  window.toast = toast;
  window.TOOL_LIST = TOOLS;

  /* ---------------- 启动 ---------------- */
  renderHeader();
  initTheme();
  renderAds();
  renderFooter();
})();
