import json
import base64
import os
from datetime import datetime

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'test_screenshots')
RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'test_results.json')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'test_report.html')

# Load test results
with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
    results = json.load(f)

# Load and encode screenshots as base64
def get_base64_image(filename):
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return f'data:image/png;base64,{data}'
    return ''

# Build tool info with categories
tool_info = {
    "首页": {"category": "首页", "icon": "🏠", "desc": "极简工具箱首页，展示所有工具入口"},
    "JSON 格式化": {"category": "开发工具", "icon": "{}", "desc": "JSON校验、格式化与压缩，错误精准定位"},
    "时间戳转换": {"category": "开发工具", "icon": "⏱️", "desc": "Unix时间戳与日期时间互转，实时更新"},
    "Base64 编解码": {"category": "编解码", "icon": "🔤", "desc": "文本Base64编码与解码，完美支持中文"},
    "URL 编解码": {"category": "编解码", "icon": "🔗", "desc": "URL编码与解码，支持整段URL或单个参数"},
    "密码生成器": {"category": "安全工具", "icon": "🔑", "desc": "生成高强度随机密码，长度与字符类型可定制"},
    "字数统计": {"category": "文本工具", "icon": "📝", "desc": "字符数、字数、行数实时统计，中英混排准确"},
    "颜色转换": {"category": "设计工具", "icon": "🎨", "desc": "HEX、RGB、HSL颜色互转，实时预览取色"},
    "UUID 生成器": {"category": "开发工具", "icon": "🆔", "desc": "批量生成UUID v4，支持大写与去连字符"},
    "Markdown 转 HTML": {"category": "文本工具", "icon": "📄", "desc": "Markdown实时转换为HTML，支持渲染预览"},
    "正则测试": {"category": "开发工具", "icon": "🔍", "desc": "正则表达式实时匹配、高亮与替换"},
    "金额转大写": {"category": "财务工具", "icon": "💰", "desc": "人民币金额一键转财务规范中文大写"},
    "二维码生成器": {"category": "生成工具", "icon": "🔳", "desc": "实时生成二维码，支持中文，下载PNG"},
    "图片压缩": {"category": "图片工具", "icon": "🗜️", "desc": "本地压缩图片体积，可调质量与尺寸"},
    "图片转 Base64": {"category": "图片工具", "icon": "🖼️", "desc": "图片转Data URL / CSS / HTML多种格式"},
    "HTTP 状态码": {"category": "开发工具", "icon": "🚦", "desc": "60+状态码速查，中英文解释与分类筛选"},
    "Cron 生成器": {"category": "开发工具", "icon": "⏰", "desc": "可视化生成Cron表达式，附中文语义解读"},
    "BMI 计算器": {"category": "生活工具", "icon": "⚖️", "desc": "按中国成人标准判定体重等级与健康建议"},
    "单位换算": {"category": "生活工具", "icon": "📐", "desc": "长度/重量/温度等8大类单位一键换算"},
    "哈希计算": {"category": "安全工具", "icon": "#️⃣", "desc": "一键生成文本的MD5/SHA-1/SHA-256/SHA-512摘要"},
    "进制转换": {"category": "开发工具", "icon": "🔢", "desc": "二进制/八进制/十进制/十六进制实时互转"},
    "HTML 转义": {"category": "编解码", "icon": "🛡️", "desc": "文本与HTML实体互转，防XSS必备"},
    "日期天数计算": {"category": "生活工具", "icon": "📅", "desc": "计算两个日期相差天数，附周数月数估算"},
    "房贷计算器": {"category": "财务工具", "icon": "🏠", "desc": "等额本息/等额本金月供与总利息对比计算"},
}

# Test findings (from screenshot analysis)
test_findings = {
    "JSON 格式化": "功能完整，输入JSON后格式化输出正确，语法高亮，状态提示'JSON格式正确'。",
    "时间戳转换": "功能正常，时间戳1709251200正确转换为2024-03-01 08:00:00，支持秒/毫秒自动识别，UTC和ISO 8601格式输出正确。",
    "Base64 编解码": "功能正常，文本'Hello 世界'成功编码，支持中文。",
    "URL 编解码": "功能正常，URL含中文部分正确编码为%E6等格式。",
    "密码生成器": "功能正常，点击生成按钮后成功生成随机密码。",
    "字数统计": "功能正常，输入文本后实时显示字符数、字数、行数统计。",
    "颜色转换": "功能正常，输入#FF5733后正确显示RGB和HSL值。",
    "UUID 生成器": "功能正常，点击生成按钮后成功生成UUID v4。",
    "Markdown 转 HTML": "功能正常，Markdown输入后正确渲染为HTML（h1、strong、ul等标签）。",
    "正则测试": "功能正常，输入正则表达式[A-Z]\\w+和测试文本后，匹配结果正确显示。",
    "金额转大写": "功能正常，12345.67正确转换为'壹万贰仟叁佰肆拾伍元陆角柒分'格式。",
    "二维码生成器": "功能正常，输入https://quicktool.xin后成功生成二维码图片，支持容错级别和尺寸配置。",
    "图片压缩": "页面加载正常，有文件上传控件，但因测试环境无图片文件未进行完整压缩测试。",
    "图片转 Base64": "页面加载正常，有文件上传控件，但因测试环境无图片文件未进行完整转换测试。",
    "HTTP 状态码": "功能正常，状态码列表加载成功，支持搜索筛选（如搜索404）。",
    "Cron 生成器": "页面加载正常，Cron表达式生成器功能可用，支持下拉选择配置。",
    "BMI 计算器": "功能正常但发现输入验证问题：测试中身高和体重输入框顺序与预期不同（身高70cm/体重175kg导致BMI=357.1的异常值），建议增加输入合理性校验。",
    "单位换算": "页面加载正常，输入100后单位换算功能可用，支持下拉选择不同单位。",
    "哈希计算": "功能正常，输入'Hello World'后成功生成MD5/SHA-1/SHA-256/SHA-512哈希值。",
    "进制转换": "功能正常，输入255后正确显示十六进制FF、二进制11111111、八进制377。",
    "HTML 转义": "功能正常，输入<div>等HTML标签后正确转换为&lt;div&gt;等实体。",
    "日期天数计算": "功能正常，输入2024-01-01和2024-12-31后正确计算天数差。",
    "房贷计算器": "发现输入验证问题：输入框标签为'万元'但输入1000000时提示'请输入1~10000之间的贷款金额'，存在单位混淆。应输入100（代表100万）才能正确计算。建议优化输入提示。",
    "首页": "首页加载正常，标题'极简工具箱'，展示23个工具卡片，导航和响应式布局正常。",
}

# Generate HTML
pass_count = sum(1 for r in results if r['status'] == 'pass')
fail_count = sum(1 for r in results if r['status'] == 'fail')
total = len(results)
pass_rate = (pass_count / total * 100) if total > 0 else 0

# Category stats
categories = {}
for r in results:
    info = tool_info.get(r['tool_name'], {"category": "其他", "icon": "🔧"})
    cat = info['category']
    if cat not in categories:
        categories[cat] = {'pass': 0, 'fail': 0, 'tools': []}
    categories[cat]['tools'].append(r)
    if r['status'] == 'pass':
        categories[cat]['pass'] += 1
    else:
        categories[cat]['fail'] += 1

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Build tool cards HTML
tool_cards_html = ""
for i, r in enumerate(results):
    info = tool_info.get(r['tool_name'], {"category": "其他", "icon": "🔧", "desc": ""})
    img_data = get_base64_image(r['screenshot'])
    status_class = 'pass' if r['status'] == 'pass' else 'fail'
    status_text = '通过' if r['status'] == 'pass' else '失败'
    finding = test_findings.get(r['tool_name'], '')
    has_finding = bool(finding)
    
    tool_cards_html += f"""
    <div class="tool-card" id="tool-{i}">
      <div class="tool-header">
        <span class="tool-icon">{info['icon']}</span>
        <div class="tool-title-area">
          <h3 class="tool-title">{r['tool_name']}</h3>
          <span class="tool-category">{info['category']}</span>
        </div>
        <span class="status-badge {status_class}">{status_text}</span>
      </div>
      <div class="tool-desc">{info['desc']}</div>
      <div class="tool-meta">
        <div class="meta-item"><span class="meta-label">测试URL</span><code>{r['tool_url']}</code></div>
        <div class="meta-item"><span class="meta-label">测试详情</span><span>{r['details']}</span></div>
        <div class="meta-item"><span class="meta-label">控制台错误</span><span>{'无' if not r.get('console_errors') else ', '.join(r['console_errors'])}</span></div>
      </div>
      {f'<div class="tool-finding"><span class="finding-label">测试发现</span>{finding}</div>' if has_finding else ''}
      <div class="tool-screenshot">
        <img src="{img_data}" alt="{r['tool_name']}截图" loading="lazy" onclick="openModal(this.src, '{r['tool_name']}')" />
      </div>
    </div>
    """

# Category summary HTML
category_html = ""
for cat, data in categories.items():
    total_cat = data['pass'] + data['fail']
    rate = (data['pass'] / total_cat * 100) if total_cat > 0 else 0
    category_html += f"""
    <div class="cat-stat">
      <span class="cat-name">{cat}</span>
      <div class="cat-bar"><div class="cat-bar-fill" style="width: {rate}%"></div></div>
      <span class="cat-count">{data['pass']}/{total_cat}</span>
    </div>
    """

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>极简工具箱 - 全站工具测试报告</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f0f2f5; color: #333; line-height: 1.6; }}

.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; }}
.header h1 {{ font-size: 2.2rem; margin-bottom: 8px; }}
.header .subtitle {{ font-size: 1rem; opacity: 0.9; }}
.header .test-time {{ font-size: 0.85rem; opacity: 0.7; margin-top: 8px; }}

.summary {{ max-width: 1200px; margin: -30px auto 20px; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 30px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
.summary-item {{ text-align: center; }}
.summary-item .num {{ font-size: 2.5rem; font-weight: 700; }}
.summary-item .label {{ font-size: 0.9rem; color: #888; margin-top: 4px; }}
.summary-item.pass .num {{ color: #52c41a; }}
.summary-item.fail .num {{ color: #ff4d4f; }}
.summary-item.rate .num {{ color: #1890ff; }}
.summary-item.total .num {{ color: #722ed1; }}

.progress-bar {{ max-width: 1200px; margin: 0 auto 20px; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); padding: 20px 30px; }}
.progress-bar .bar-track {{ width: 100%; height: 24px; background: #f0f0f0; border-radius: 12px; overflow: hidden; margin-top: 8px; }}
.progress-bar .bar-fill {{ height: 100%; background: linear-gradient(90deg, #52c41a, #73d13d); border-radius: 12px; transition: width 0.5s; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px; color: white; font-weight: 600; font-size: 0.85rem; }}

.categories {{ max-width: 1200px; margin: 0 auto 30px; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); padding: 20px 30px; }}
.categories h2 {{ font-size: 1.1rem; margin-bottom: 16px; color: #555; }}
.cat-stat {{ display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }}
.cat-name {{ width: 100px; font-size: 0.9rem; color: #666; }}
.cat-bar {{ flex: 1; height: 16px; background: #f0f0f0; border-radius: 8px; overflow: hidden; }}
.cat-bar-fill {{ height: 100%; background: linear-gradient(90deg, #1890ff, #36cfc9); border-radius: 8px; }}
.cat-count {{ width: 50px; text-align: right; font-size: 0.85rem; color: #888; }}

.tools {{ max-width: 1200px; margin: 0 auto 40px; }}
.tools h2 {{ font-size: 1.3rem; margin-bottom: 20px; color: #333; padding-left: 10px; }}

.tool-card {{ background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 24px; overflow: hidden; transition: box-shadow 0.3s; }}
.tool-card:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.12); }}
.tool-header {{ display: flex; align-items: center; padding: 16px 24px; border-bottom: 1px solid #f0f0f0; }}
.tool-icon {{ font-size: 1.8rem; margin-right: 12px; }}
.tool-title-area {{ flex: 1; }}
.tool-title {{ font-size: 1.1rem; font-weight: 600; margin: 0; }}
.tool-category {{ font-size: 0.75rem; color: #999; background: #f5f5f5; padding: 2px 8px; border-radius: 4px; }}
.status-badge {{ padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
.status-badge.pass {{ background: #f6ffed; color: #52c41a; border: 1px solid #b7eb8f; }}
.status-badge.fail {{ background: #fff2f0; color: #ff4d4f; border: 1px solid #ffccc7; }}

.tool-desc {{ padding: 12px 24px; color: #666; font-size: 0.9rem; }}

.tool-meta {{ padding: 12px 24px; background: #fafafa; }}
.meta-item {{ display: flex; gap: 8px; margin-bottom: 6px; font-size: 0.85rem; }}
.meta-label {{ color: #999; min-width: 80px; }}
.meta-item code {{ background: #f0f0f0; padding: 1px 6px; border-radius: 3px; font-size: 0.8rem; }}

.tool-finding {{ padding: 12px 24px; background: #fffbe6; border-left: 4px solid #faad14; font-size: 0.85rem; color: #666; }}
.finding-label {{ display: inline-block; background: #faad14; color: white; padding: 1px 6px; border-radius: 3px; font-size: 0.75rem; margin-right: 8px; }}

.tool-screenshot {{ padding: 16px 24px; }}
.tool-screenshot img {{ width: 100%; border-radius: 8px; cursor: pointer; transition: opacity 0.2s; border: 1px solid #f0f0f0; }}
.tool-screenshot img:hover {{ opacity: 0.9; }}

.modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999; justify-content: center; align-items: center; }}
.modal.active {{ display: flex; }}
.modal img {{ max-width: 95%; max-height: 95%; border-radius: 8px; }}
.modal-close {{ position: fixed; top: 20px; right: 30px; color: white; font-size: 2rem; cursor: pointer; }}
.modal-title {{ position: fixed; top: 20px; left: 50%; transform: translateX(-50%); color: white; font-size: 1.2rem; }}

.footer {{ text-align: center; padding: 30px; color: #999; font-size: 0.85rem; }}

@media (max-width: 768px) {{
  .summary {{ grid-template-columns: repeat(2, 1fr); }}
  .tool-header {{ flex-wrap: wrap; }}
  .cat-name {{ width: 70px; }}
}}
</style>
</head>
<body>

<div class="header">
  <h1>极简工具箱 全站工具测试报告</h1>
  <div class="subtitle">https://quicktool.xin/ - Playwright 自动化测试</div>
  <div class="test-time">测试时间: {now}</div>
</div>

<div class="summary">
  <div class="summary-item total"><div class="num">{total}</div><div class="label">测试页面总数</div></div>
  <div class="summary-item pass"><div class="num">{pass_count}</div><div class="label">通过</div></div>
  <div class="summary-item fail"><div class="num">{fail_count}</div><div class="label">失败</div></div>
  <div class="summary-item rate"><div class="num">{pass_rate:.0f}%</div><div class="label">通过率</div></div>
</div>

<div class="progress-bar">
  <div style="font-size: 0.9rem; color: #666;">总体通过率</div>
  <div class="bar-track">
    <div class="bar-fill" style="width: {pass_rate}%">{pass_rate:.0f}%</div>
  </div>
</div>

<div class="categories">
  <h2>分类统计</h2>
  {category_html}
</div>

<div class="tools">
  <h2>工具测试详情（共 {total} 项）</h2>
  {tool_cards_html}
</div>

<div class="footer">
  <p>极简工具箱 Playwright 自动化测试报告 | 生成时间: {now}</p>
  <p>测试工具: Playwright + Chromium | 测试方式: Headless 浏览器自动化</p>
</div>

<div class="modal" id="modal" onclick="closeModal()">
  <span class="modal-close" onclick="closeModal()">&times;</span>
  <span class="modal-title" id="modal-title"></span>
  <img id="modal-img" src="" alt="截图" />
</div>

<script>
function openModal(src, title) {{
  document.getElementById('modal-img').src = src;
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal').classList.add('active');
}}
function closeModal() {{
  document.getElementById('modal').classList.remove('active');
}}
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') closeModal();
}});
</script>

</body>
</html>
"""

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

file_size = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"HTML报告已生成: {OUTPUT_FILE}")
print(f"文件大小: {file_size:.1f} MB")
print(f"包含 {total} 个测试结果和截图")
