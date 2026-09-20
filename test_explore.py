from playwright.sync_api import sync_playwright
import json
import os

screenshot_dir = os.path.join(os.path.dirname(__file__), 'test_screenshots')
os.makedirs(screenshot_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://quicktool.xin/', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    page.screenshot(path=os.path.join(screenshot_dir, 'home.png'), full_page=True)
    
    # Get page title
    title = page.title()
    print(f"Page title: {title}")
    
    # Extract all links and tool-related elements
    content = page.content()
    
    # Find all links
    links = page.locator('a').all()
    tool_links = []
    for link in links:
        href = link.get_attribute('href')
        text = link.inner_text()
        if href and text:
            tool_links.append({'text': text.strip(), 'href': href.strip()})
    
    # Find navigation items
    nav_items = page.locator('nav a, .nav-link, .tool-card, .tool-item, [class*="tool"], [class*="card"]').all()
    nav_texts = []
    for item in nav_items:
        try:
            text = item.inner_text()
            if text.strip():
                nav_texts.append(text.strip())
        except:
            pass
    
    # Find buttons
    buttons = page.locator('button').all()
    button_texts = []
    for btn in buttons:
        try:
            text = btn.inner_text()
            if text.strip():
                button_texts.append(text.strip())
        except:
            pass

    # Try to find tool grid/list items
    # Look for common patterns in tool websites
    all_elements = page.locator('a[href]').all()
    all_hrefs = []
    for el in all_elements:
        href = el.get_attribute('href')
        text = el.inner_text().strip()
        if href and text:
            all_hrefs.append({'text': text, 'href': href})
    
    print("\n=== All Links ===")
    for item in all_hrefs:
        print(f"  {item['text'][:50]} -> {item['href']}")
    
    print(f"\n=== Summary ===")
    print(f"Total links: {len(all_hrefs)}")
    print(f"Total buttons: {len(button_texts)}")
    
    # Save full page content for analysis
    with open(os.path.join(screenshot_dir, 'page_content.html'), 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Save links as JSON
    with open(os.path.join(screenshot_dir, 'tool_links.json'), 'w', encoding='utf-8') as f:
        json.dump(all_hrefs, f, ensure_ascii=False, indent=2)
    
    browser.close()
    print("\nDone! Check screenshots and page_content.html for details.")
