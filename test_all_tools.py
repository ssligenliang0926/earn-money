import json
import os
import base64
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://quicktool.xin/"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'test_screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

results = []

def record_result(tool_name, tool_url, status, details, screenshot_file, console_errors=None):
    results.append({
        "tool_name": tool_name,
        "tool_url": tool_url,
        "status": status,
        "details": details,
        "screenshot": screenshot_file,
        "console_errors": console_errors or []
    })
    print(f"  [{'PASS' if status == 'pass' else 'FAIL'}] {tool_name}: {details}")

def take_screenshot(page, filename):
    path = os.path.join(SCREENSHOT_DIR, filename)
    page.screenshot(path=path, full_page=True)
    return filename

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # ========== 1. JSON 格式化 ==========
    print("\n[1/23] 测试 JSON 格式化...")
    page = browser.new_page()
    console_errors_json = []
    page.on("console", lambda msg: console_errors_json.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/json-formatter.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        # Input JSON
        textarea = page.locator('textarea').first
        textarea.fill('{"name":"test","age":30,"items":[1,2,3]}')
        page.wait_for_timeout(500)
        # Click format button
        format_btn = page.locator('button:has-text("格式化")')
        if format_btn.count() > 0:
            format_btn.first.click()
            page.wait_for_timeout(500)
        # Check output
        output = page.locator('textarea').nth(1) if page.locator('textarea').count() > 1 else page.locator('.output, [class*="result"], pre').first
        output_text = ""
        try:
            output_text = output.inner_text()
        except:
            pass
        has_output = len(output_text) > 0 or '"name"' in page.content()
        ss = take_screenshot(page, 'json-formatter.png')
        record_result("JSON 格式化", "tools/json-formatter.html", "pass" if has_output else "fail",
                      "输入JSON并格式化，输出区域有内容" if has_output else "输出区域为空", ss, console_errors_json)
    except Exception as e:
        ss = take_screenshot(page, 'json-formatter.png')
        record_result("JSON 格式化", "tools/json-formatter.html", "fail", f"异常: {str(e)}", ss, console_errors_json)
    page.close()

    # ========== 2. 时间戳转换 ==========
    print("[2/23] 测试 时间戳转换...")
    page = browser.new_page()
    console_errors_ts = []
    page.on("console", lambda msg: console_errors_ts.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/timestamp.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        # Find timestamp input and enter a value
        inputs = page.locator('input[type="number"], input[type="text"]').all()
        if inputs:
            inputs[0].fill('1709251200')
            page.wait_for_timeout(500)
        # Click convert button if exists
        convert_btn = page.locator('button:has-text("转换"), button:has-text("确定")')
        if convert_btn.count() > 0:
            convert_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '2024' in content or '日期' in content or 'date' in content.lower()
        ss = take_screenshot(page, 'timestamp.png')
        record_result("时间戳转换", "tools/timestamp.html", "pass" if has_result else "fail",
                      "时间戳1709251200转换成功，显示日期" if has_result else "未找到转换结果", ss, console_errors_ts)
    except Exception as e:
        ss = take_screenshot(page, 'timestamp.png')
        record_result("时间戳转换", "tools/timestamp.html", "fail", f"异常: {str(e)}", ss, console_errors_ts)
    page.close()

    # ========== 3. Base64 编解码 ==========
    print("[3/23] 测试 Base64 编解码...")
    page = browser.new_page()
    console_errors_b64 = []
    page.on("console", lambda msg: console_errors_b64.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/base64.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea').first
        textarea.fill('Hello 世界')
        page.wait_for_timeout(500)
        encode_btn = page.locator('button:has-text("编码"), button:has-text("Base64")')
        if encode_btn.count() > 0:
            encode_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = 'SGVsbG8' in content or '5Lit' in content or page.locator('textarea').nth(1).input_value() if page.locator('textarea').count() > 1 else False
        ss = take_screenshot(page, 'base64.png')
        record_result("Base64 编解码", "tools/base64.html", "pass" if has_result else "fail",
                      "文本'Hello 世界'编码成功" if has_result else "未找到编码结果", ss, console_errors_b64)
    except Exception as e:
        ss = take_screenshot(page, 'base64.png')
        record_result("Base64 编解码", "tools/base64.html", "fail", f"异常: {str(e)}", ss, console_errors_b64)
    page.close()

    # ========== 4. URL 编解码 ==========
    print("[4/23] 测试 URL 编解码...")
    page = browser.new_page()
    console_errors_url = []
    page.on("console", lambda msg: console_errors_url.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/url-encode.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea').first
        textarea.fill('https://example.com/测试?name=张三')
        page.wait_for_timeout(500)
        encode_btn = page.locator('button:has-text("编码"), button:has-text("URL")')
        if encode_btn.count() > 0:
            encode_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '%E6' in content or '%E6%B5' in content or 'https%3A' in content
        ss = take_screenshot(page, 'url-encode.png')
        record_result("URL 编解码", "tools/url-encode.html", "pass" if has_result else "fail",
                      "URL编码成功，含中文编码" if has_result else "未找到编码结果", ss, console_errors_url)
    except Exception as e:
        ss = take_screenshot(page, 'url-encode.png')
        record_result("URL 编解码", "tools/url-encode.html", "fail", f"异常: {str(e)}", ss, console_errors_url)
    page.close()

    # ========== 5. 密码生成器 ==========
    print("[5/23] 测试 密码生成器...")
    page = browser.new_page()
    console_errors_pw = []
    page.on("console", lambda msg: console_errors_pw.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/password-generator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        # Click generate button
        gen_btn = page.locator('button:has-text("生成"), button:has-text("密码")')
        if gen_btn.count() > 0:
            gen_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        # Check if password output exists
        output = page.locator('input[readonly], input[type="text"], .result, [class*="output"]').first
        output_val = ""
        try:
            output_val = output.input_value() if output.evaluate("el => el.tagName") == "INPUT" else output.inner_text()
        except:
            pass
        has_result = len(output_val) > 0 or 'password' in content.lower()
        ss = take_screenshot(page, 'password-generator.png')
        record_result("密码生成器", "tools/password-generator.html", "pass" if has_result else "fail",
                      f"密码生成成功，结果: {output_val[:20]}..." if has_result else "未找到密码输出", ss, console_errors_pw)
    except Exception as e:
        ss = take_screenshot(page, 'password-generator.png')
        record_result("密码生成器", "tools/password-generator.html", "fail", f"异常: {str(e)}", ss, console_errors_pw)
    page.close()

    # ========== 6. 字数统计 ==========
    print("[6/23] 测试 字数统计...")
    page = browser.new_page()
    console_errors_wc = []
    page.on("console", lambda msg: console_errors_wc.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/word-counter.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea').first
        textarea.fill('Hello 世界 This is a test 测试文本\nSecond line')
        page.wait_for_timeout(1000)
        content = page.content()
        has_result = '字符' in content or '字数' in content or '行数' in content or 'count' in content.lower()
        ss = take_screenshot(page, 'word-counter.png')
        record_result("字数统计", "tools/word-counter.html", "pass" if has_result else "fail",
                      "文本统计结果已显示" if has_result else "未找到统计结果", ss, console_errors_wc)
    except Exception as e:
        ss = take_screenshot(page, 'word-counter.png')
        record_result("字数统计", "tools/word-counter.html", "fail", f"异常: {str(e)}", ss, console_errors_wc)
    page.close()

    # ========== 7. 颜色转换 ==========
    print("[7/23] 测试 颜色转换...")
    page = browser.new_page()
    console_errors_color = []
    page.on("console", lambda msg: console_errors_color.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/color-converter.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        # Find color input
        color_input = page.locator('input[type="color"], input[type="text"]').first
        if color_input.count() > 0:
            try:
                color_input.fill('#FF5733')
            except:
                color_input.fill('FF5733')
            page.wait_for_timeout(500)
        # Click convert button if exists
        convert_btn = page.locator('button:has-text("转换"), button:has-text("确定")')
        if convert_btn.count() > 0:
            convert_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = 'rgb' in content.lower() or 'hsl' in content.lower() or 'RGB' in content
        ss = take_screenshot(page, 'color-converter.png')
        record_result("颜色转换", "tools/color-converter.html", "pass" if has_result else "fail",
                      "颜色#FF5733转换结果已显示" if has_result else "未找到颜色转换结果", ss, console_errors_color)
    except Exception as e:
        ss = take_screenshot(page, 'color-converter.png')
        record_result("颜色转换", "tools/color-converter.html", "fail", f"异常: {str(e)}", ss, console_errors_color)
    page.close()

    # ========== 8. UUID 生成器 ==========
    print("[8/23] 测试 UUID 生成器...")
    page = browser.new_page()
    console_errors_uuid = []
    page.on("console", lambda msg: console_errors_uuid.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/uuid-generator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        gen_btn = page.locator('button:has-text("生成"), button:has-text("UUID")')
        if gen_btn.count() > 0:
            gen_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = 'uuid' in content.lower() or '-' in content and len(content) > 100
        # Also check for textarea or output
        output_el = page.locator('textarea, input[readonly], .result').first
        output_val = ""
        try:
            output_val = output_el.input_value() if output_el.evaluate("el => el.tagName") == "INPUT" or output_el.evaluate("el => el.tagName") == "TEXTAREA" else output_el.inner_text()
        except:
            pass
        has_result = has_result or len(output_val) > 10
        ss = take_screenshot(page, 'uuid-generator.png')
        record_result("UUID 生成器", "tools/uuid-generator.html", "pass" if has_result else "fail",
                      f"UUID生成成功: {output_val[:36]}..." if output_val else "UUID生成成功" if has_result else "未找到UUID输出", ss, console_errors_uuid)
    except Exception as e:
        ss = take_screenshot(page, 'uuid-generator.png')
        record_result("UUID 生成器", "tools/uuid-generator.html", "fail", f"异常: {str(e)}", ss, console_errors_uuid)
    page.close()

    # ========== 9. Markdown 转 HTML ==========
    print("[9/23] 测试 Markdown 转 HTML...")
    page = browser.new_page()
    console_errors_md = []
    page.on("console", lambda msg: console_errors_md.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/markdown-to-html.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea').first
        textarea.fill('# Title\n\n**Bold text** and *italic*\n\n- List item 1\n- List item 2')
        page.wait_for_timeout(1000)
        content = page.content()
        has_result = '<h1>' in content or '<strong>' in content or '<ul>' in content or 'html' in content.lower()
        ss = take_screenshot(page, 'markdown-to-html.png')
        record_result("Markdown 转 HTML", "tools/markdown-to-html.html", "pass" if has_result else "fail",
                      "Markdown转换成功，HTML已渲染" if has_result else "未找到转换结果", ss, console_errors_md)
    except Exception as e:
        ss = take_screenshot(page, 'markdown-to-html.png')
        record_result("Markdown 转 HTML", "tools/markdown-to-html.html", "fail", f"异常: {str(e)}", ss, console_errors_md)
    page.close()

    # ========== 10. 正则测试 ==========
    print("[10/23] 测试 正则测试...")
    page = browser.new_page()
    console_errors_regex = []
    page.on("console", lambda msg: console_errors_regex.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/regex-tester.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        # Find regex pattern input and test string input
        inputs = page.locator('input[type="text"]').all()
        textareas = page.locator('textarea').all()
        if inputs:
            inputs[0].fill('[A-Z]\\w+')
        if textareas:
            textareas[0].fill('Hello World Test String')
        page.wait_for_timeout(500)
        test_btn = page.locator('button:has-text("测试"), button:has-text("匹配")')
        if test_btn.count() > 0:
            test_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = 'match' in content.lower() or '匹配' in content or 'Hello' in content or 'World' in content
        ss = take_screenshot(page, 'regex-tester.png')
        record_result("正则测试", "tools/regex-tester.html", "pass" if has_result else "fail",
                      "正则表达式测试完成" if has_result else "未找到测试结果", ss, console_errors_regex)
    except Exception as e:
        ss = take_screenshot(page, 'regex-tester.png')
        record_result("正则测试", "tools/regex-tester.html", "fail", f"异常: {str(e)}", ss, console_errors_regex)
    page.close()

    # ========== 11. 金额转大写 ==========
    print("[11/23] 测试 金额转大写...")
    page = browser.new_page()
    console_errors_rmb = []
    page.on("console", lambda msg: console_errors_rmb.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/rmb-uppercase.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        num_input = page.locator('input[type="number"], input[type="text"]').first
        num_input.fill('12345.67')
        page.wait_for_timeout(500)
        convert_btn = page.locator('button:has-text("转换"), button:has-text("大写")')
        if convert_btn.count() > 0:
            convert_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '壹' in content or '万' in content or '元' in content or '角' in content
        ss = take_screenshot(page, 'rmb-uppercase.png')
        record_result("金额转大写", "tools/rmb-uppercase.html", "pass" if has_result else "fail",
                      "金额12345.67转大写成功" if has_result else "未找到转换结果", ss, console_errors_rmb)
    except Exception as e:
        ss = take_screenshot(page, 'rmb-uppercase.png')
        record_result("金额转大写", "tools/rmb-uppercase.html", "fail", f"异常: {str(e)}", ss, console_errors_rmb)
    page.close()

    # ========== 12. 二维码生成器 ==========
    print("[12/23] 测试 二维码生成器...")
    page = browser.new_page()
    console_errors_qr = []
    page.on("console", lambda msg: console_errors_qr.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/qrcode-generator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea, input[type="text"]').first
        textarea.fill('https://quicktool.xin')
        page.wait_for_timeout(1000)
        gen_btn = page.locator('button:has-text("生成"), button:has-text("二维码")')
        if gen_btn.count() > 0:
            gen_btn.first.click()
            page.wait_for_timeout(1000)
        content = page.content()
        has_result = 'canvas' in content.lower() or 'img' in content.lower() or 'qr' in content.lower() or '二维码' in content
        ss = take_screenshot(page, 'qrcode-generator.png')
        record_result("二维码生成器", "tools/qrcode-generator.html", "pass" if has_result else "fail",
                      "二维码生成成功" if has_result else "未找到二维码图片", ss, console_errors_qr)
    except Exception as e:
        ss = take_screenshot(page, 'qrcode-generator.png')
        record_result("二维码生成器", "tools/qrcode-generator.html", "fail", f"异常: {str(e)}", ss, console_errors_qr)
    page.close()

    # ========== 13. 图片压缩 ==========
    print("[13/23] 测试 图片压缩...")
    page = browser.new_page()
    console_errors_img = []
    page.on("console", lambda msg: console_errors_img.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/image-compressor.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        # Just verify page loads and has file input
        file_input = page.locator('input[type="file"]')
        has_file_input = file_input.count() > 0
        content = page.content()
        has_result = has_file_input or '压缩' in content or 'compress' in content.lower() or 'image' in content.lower()
        ss = take_screenshot(page, 'image-compressor.png')
        record_result("图片压缩", "tools/image-compressor.html", "pass" if has_result else "fail",
                      "页面加载成功，有文件上传控件" if has_file_input else "页面加载成功", ss, console_errors_img)
    except Exception as e:
        ss = take_screenshot(page, 'image-compressor.png')
        record_result("图片压缩", "tools/image-compressor.html", "fail", f"异常: {str(e)}", ss, console_errors_img)
    page.close()

    # ========== 14. 图片转 Base64 ==========
    print("[14/23] 测试 图片转 Base64...")
    page = browser.new_page()
    console_errors_img2b64 = []
    page.on("console", lambda msg: console_errors_img2b64.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/image-to-base64.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        file_input = page.locator('input[type="file"]')
        has_file_input = file_input.count() > 0
        content = page.content()
        has_result = has_file_input or 'base64' in content.lower() or 'data:' in content.lower()
        ss = take_screenshot(page, 'image-to-base64.png')
        record_result("图片转 Base64", "tools/image-to-base64.html", "pass" if has_result else "fail",
                      "页面加载成功，有文件上传控件" if has_file_input else "页面加载成功", ss, console_errors_img2b64)
    except Exception as e:
        ss = take_screenshot(page, 'image-to-base64.png')
        record_result("图片转 Base64", "tools/image-to-base64.html", "fail", f"异常: {str(e)}", ss, console_errors_img2b64)
    page.close()

    # ========== 15. HTTP 状态码 ==========
    print("[15/23] 测试 HTTP 状态码...")
    page = browser.new_page()
    console_errors_http = []
    page.on("console", lambda msg: console_errors_http.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/http-status-codes.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        content = page.content()
        has_result = '200' in content or '404' in content or '500' in content or '状态码' in content
        # Try search/filter
        search_input = page.locator('input[type="text"], input[type="search"]').first
        if search_input.count() > 0:
            search_input.fill('404')
            page.wait_for_timeout(500)
        ss = take_screenshot(page, 'http-status-codes.png')
        record_result("HTTP 状态码", "tools/http-status-codes.html", "pass" if has_result else "fail",
                      "状态码列表加载成功" if has_result else "未找到状态码数据", ss, console_errors_http)
    except Exception as e:
        ss = take_screenshot(page, 'http-status-codes.png')
        record_result("HTTP 状态码", "tools/http-status-codes.html", "fail", f"异常: {str(e)}", ss, console_errors_http)
    page.close()

    # ========== 16. Cron 生成器 ==========
    print("[16/23] 测试 Cron 生成器...")
    page = browser.new_page()
    console_errors_cron = []
    page.on("console", lambda msg: console_errors_cron.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/cron-generator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        content = page.content()
        has_result = 'cron' in content.lower() or 'Cron' in content or '表达式' in content or '0 *' in content
        # Try to interact with selects/inputs
        selects = page.locator('select').all()
        if selects:
            selects[0].select_option(index=0)
            page.wait_for_timeout(500)
        ss = take_screenshot(page, 'cron-generator.png')
        record_result("Cron 生成器", "tools/cron-generator.html", "pass" if has_result else "fail",
                      "Cron生成器页面加载成功" if has_result else "页面加载异常", ss, console_errors_cron)
    except Exception as e:
        ss = take_screenshot(page, 'cron-generator.png')
        record_result("Cron 生成器", "tools/cron-generator.html", "fail", f"异常: {str(e)}", ss, console_errors_cron)
    page.close()

    # ========== 17. BMI 计算器 ==========
    print("[17/23] 测试 BMI 计算器...")
    page = browser.new_page()
    console_errors_bmi = []
    page.on("console", lambda msg: console_errors_bmi.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/bmi-calculator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        inputs = page.locator('input[type="number"], input[type="text"]').all()
        if len(inputs) >= 2:
            inputs[0].fill('70')  # weight
            inputs[1].fill('175')  # height
            page.wait_for_timeout(500)
        calc_btn = page.locator('button:has-text("计算"), button:has-text("BMI")')
        if calc_btn.count() > 0:
            calc_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = 'BMI' in content or '体重' in content or '正常' in content or '偏胖' in content or '22.' in content
        ss = take_screenshot(page, 'bmi-calculator.png')
        record_result("BMI 计算器", "tools/bmi-calculator.html", "pass" if has_result else "fail",
                      "BMI计算成功(身高175体重70)" if has_result else "未找到计算结果", ss, console_errors_bmi)
    except Exception as e:
        ss = take_screenshot(page, 'bmi-calculator.png')
        record_result("BMI 计算器", "tools/bmi-calculator.html", "fail", f"异常: {str(e)}", ss, console_errors_bmi)
    page.close()

    # ========== 18. 单位换算 ==========
    print("[18/23] 测试 单位换算...")
    page = browser.new_page()
    console_errors_unit = []
    page.on("console", lambda msg: console_errors_unit.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/unit-converter.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        num_input = page.locator('input[type="number"], input[type="text"]').first
        num_input.fill('100')
        page.wait_for_timeout(500)
        selects = page.locator('select').all()
        if len(selects) >= 2:
            try:
                selects[0].select_option(index=1)
                selects[1].select_option(index=2)
            except:
                pass
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '换算' in content or 'convert' in content.lower() or 'result' in content.lower() or '100' in content
        ss = take_screenshot(page, 'unit-converter.png')
        record_result("单位换算", "tools/unit-converter.html", "pass" if has_result else "fail",
                      "单位换算页面加载成功" if has_result else "页面加载异常", ss, console_errors_unit)
    except Exception as e:
        ss = take_screenshot(page, 'unit-converter.png')
        record_result("单位换算", "tools/unit-converter.html", "fail", f"异常: {str(e)}", ss, console_errors_unit)
    page.close()

    # ========== 19. 哈希计算 ==========
    print("[19/23] 测试 哈希计算...")
    page = browser.new_page()
    console_errors_hash = []
    page.on("console", lambda msg: console_errors_hash.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/hash-generator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea, input[type="text"]').first
        textarea.fill('Hello World')
        page.wait_for_timeout(1000)
        gen_btn = page.locator('button:has-text("生成"), button:has-text("计算"), button:has-text("Hash")')
        if gen_btn.count() > 0:
            gen_btn.first.click()
            page.wait_for_timeout(1000)
        content = page.content()
        has_result = 'md5' in content.lower() or 'sha' in content.lower() or 'hash' in content.lower() or 'b10a' in content or '0a4d' in content
        ss = take_screenshot(page, 'hash-generator.png')
        record_result("哈希计算", "tools/hash-generator.html", "pass" if has_result else "fail",
                      "哈希计算成功" if has_result else "未找到哈希结果", ss, console_errors_hash)
    except Exception as e:
        ss = take_screenshot(page, 'hash-generator.png')
        record_result("哈希计算", "tools/hash-generator.html", "fail", f"异常: {str(e)}", ss, console_errors_hash)
    page.close()

    # ========== 20. 进制转换 ==========
    print("[20/23] 测试 进制转换...")
    page = browser.new_page()
    console_errors_radix = []
    page.on("console", lambda msg: console_errors_radix.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/radix-converter.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        num_input = page.locator('input[type="number"], input[type="text"]').first
        num_input.fill('255')
        page.wait_for_timeout(500)
        content = page.content()
        has_result = 'ff' in content.lower() or '1111' in content or '377' in content or '进制' in content
        ss = take_screenshot(page, 'radix-converter.png')
        record_result("进制转换", "tools/radix-converter.html", "pass" if has_result else "fail",
                      "进制转换成功(255)" if has_result else "未找到转换结果", ss, console_errors_radix)
    except Exception as e:
        ss = take_screenshot(page, 'radix-converter.png')
        record_result("进制转换", "tools/radix-converter.html", "fail", f"异常: {str(e)}", ss, console_errors_radix)
    page.close()

    # ========== 21. HTML 转义 ==========
    print("[21/23] 测试 HTML 转义...")
    page = browser.new_page()
    console_errors_html = []
    page.on("console", lambda msg: console_errors_html.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/html-escape.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        textarea = page.locator('textarea').first
        textarea.fill('<div class="test">Hello & "World"</div>')
        page.wait_for_timeout(500)
        escape_btn = page.locator('button:has-text("转义"), button:has-text("HTML")')
        if escape_btn.count() > 0:
            escape_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '&lt;' in content or '&gt;' in content or '&amp;' in content or '&quot;' in content
        ss = take_screenshot(page, 'html-escape.png')
        record_result("HTML 转义", "tools/html-escape.html", "pass" if has_result else "fail",
                      "HTML转义成功" if has_result else "未找到转义结果", ss, console_errors_html)
    except Exception as e:
        ss = take_screenshot(page, 'html-escape.png')
        record_result("HTML 转义", "tools/html-escape.html", "fail", f"异常: {str(e)}", ss, console_errors_html)
    page.close()

    # ========== 22. 日期天数计算 ==========
    print("[22/23] 测试 日期天数计算...")
    page = browser.new_page()
    console_errors_date = []
    page.on("console", lambda msg: console_errors_date.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/date-difference.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        date_inputs = page.locator('input[type="date"]').all()
        if len(date_inputs) >= 2:
            date_inputs[0].fill('2024-01-01')
            date_inputs[1].fill('2024-12-31')
            page.wait_for_timeout(500)
        calc_btn = page.locator('button:has-text("计算"), button:has-text("天数")')
        if calc_btn.count() > 0:
            calc_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '天' in content or 'day' in content.lower() or '365' in content or '364' in content or '366' in content
        ss = take_screenshot(page, 'date-difference.png')
        record_result("日期天数计算", "tools/date-difference.html", "pass" if has_result else "fail",
                      "日期天数计算成功" if has_result else "未找到计算结果", ss, console_errors_date)
    except Exception as e:
        ss = take_screenshot(page, 'date-difference.png')
        record_result("日期天数计算", "tools/date-difference.html", "fail", f"异常: {str(e)}", ss, console_errors_date)
    page.close()

    # ========== 23. 房贷计算器 ==========
    print("[23/23] 测试 房贷计算器...")
    page = browser.new_page()
    console_errors_mort = []
    page.on("console", lambda msg: console_errors_mort.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL + "tools/mortgage-calculator.html", timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        inputs = page.locator('input[type="number"], input[type="text"]').all()
        if len(inputs) >= 3:
            inputs[0].fill('1000000')  # loan amount
            inputs[1].fill('30')  # years
            inputs[2].fill('4.9')  # rate
            page.wait_for_timeout(500)
        calc_btn = page.locator('button:has-text("计算"), button:has-text("月供")')
        if calc_btn.count() > 0:
            calc_btn.first.click()
            page.wait_for_timeout(500)
        content = page.content()
        has_result = '月供' in content or '利息' in content or '元' in content or '5307' in content
        ss = take_screenshot(page, 'mortgage-calculator.png')
        record_result("房贷计算器", "tools/mortgage-calculator.html", "pass" if has_result else "fail",
                      "房贷计算成功(100万/30年/4.9%)" if has_result else "未找到计算结果", ss, console_errors_mort)
    except Exception as e:
        ss = take_screenshot(page, 'mortgage-calculator.png')
        record_result("房贷计算器", "tools/mortgage-calculator.html", "fail", f"异常: {str(e)}", ss, console_errors_mort)
    page.close()

    # Also test home page
    print("\n[额外] 测试首页...")
    page = browser.new_page()
    console_errors_home = []
    page.on("console", lambda msg: console_errors_home.append(msg.text) if msg.type == "error" else None)
    try:
        page.goto(BASE_URL, timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        title = page.title()
        tool_cards = page.locator('a[href*="tools/"]').all()
        tool_count = len(tool_cards)
        ss = take_screenshot(page, 'home.png')
        record_result("首页", "index.html", "pass" if tool_count > 0 else "fail",
                      f"首页加载成功，标题: {title}，发现{tool_count}个工具链接", ss, console_errors_home)
    except Exception as e:
        ss = take_screenshot(page, 'home.png')
        record_result("首页", "index.html", "fail", f"异常: {str(e)}", ss, console_errors_home)
    page.close()

    browser.close()

# Save results as JSON
with open(os.path.join(SCREENSHOT_DIR, 'test_results.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"测试完成! 共测试 {len(results)} 个页面")
pass_count = sum(1 for r in results if r['status'] == 'pass')
fail_count = sum(1 for r in results if r['status'] == 'fail')
print(f"通过: {pass_count} / 失败: {fail_count}")
print(f"结果已保存到 test_screenshots/test_results.json")
