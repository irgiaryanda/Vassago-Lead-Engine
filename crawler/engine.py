import re
import urllib.parse
from playwright.async_api import async_playwright

async def run_lead_scan(keyword: str, max_results: int = 3) -> list[dict]:
    leads = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            print(f"\n[CRAWLER] Initiating search for: {keyword}")
            encoded_keyword = urllib.parse.quote_plus(keyword)
            search_url = f"https://html.duckduckgo.com/html/?q={encoded_keyword}"
            await page.goto(search_url, timeout=30000)
            await page.wait_for_timeout(2000)
            print(f"[CRAWLER] Page loaded. Title: {await page.title()}")
            
            # Extract search result URLs
            url_elements = await page.locator("a.result__url, a.result__snippet, a.result__a, a").all()
            print(f"[CRAWLER] Found {len(url_elements)} raw link elements on search page")
            
            urls_to_visit = []
            for element in url_elements:
                href = await element.get_attribute("href")
                if not href:
                    continue
                    
                actual_url = ""
                if "uddg=" in href:
                    actual_url = urllib.parse.unquote(href.split("uddg=")[1].split("&")[0])
                elif href.startswith("http"):
                    actual_url = href
                else:
                    continue
                    
                if "duckduckgo.com" in actual_url:
                    continue
                    
                if actual_url and actual_url.startswith("http") and actual_url not in urls_to_visit:
                    urls_to_visit.append(actual_url)
                    print(f"[CRAWLER] ✅ Valid Target Acquired: {actual_url}")
                    
                if len(urls_to_visit) >= max_results:
                    break
                    
            # Visit each URL
            for url in urls_to_visit:
                try:
                    print(f"[CRAWLER] 🌐 Scanning Website: {url}")
                    await page.goto(url, timeout=10000)
                    title = await page.title()
                    content = await page.content()
                    
                    # Regex to find email
                    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
                    contact_email = email_match.group(0) if email_match else ""
                    if contact_email:
                        print(f"[CRAWLER] 📧 SUCCESS! Email found: {contact_email}")
                    
                    leads.append({
                        "company_name": title.strip() if title else "Unknown",
                        "contact_email": contact_email,
                        "website_url": url
                    })
                except Exception:
                    print(f"[CRAWLER] ❌ Skipped (Error/Timeout): {url}")
                    continue
        except Exception as e:
            print(f"[CRAWLER] ❌ FATAL ERROR during search: {e}")
        finally:
            await browser.close()
            
    return leads
