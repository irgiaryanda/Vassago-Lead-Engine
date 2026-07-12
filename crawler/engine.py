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
            search_url = f"https://search.yahoo.com/search?p={encoded_keyword}"
            await page.goto(search_url, timeout=30000)
            await page.wait_for_timeout(2000)
            print(f"[CRAWLER] Page loaded. Title: {await page.title()}")
            
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            
            # Extract search result URLs
            url_elements = await page.locator("a").all()
            print(f"[CRAWLER] Found {len(url_elements)} raw link elements on search page")
            
            urls_to_visit = []
            for element in url_elements:
                if len(urls_to_visit) >= max_results:
                    break
                    
                href = await element.get_attribute("href")
                if not href or not href.startswith("http"):
                    continue
                    
                if any(domain in href for domain in ["yahoo.com", "bing.com", "microsoft.com", "duckduckgo.com"]):
                    continue
                    
                actual_url = href
                
                if actual_url not in urls_to_visit:
                    urls_to_visit.append(actual_url)
                    print(f"[CRAWLER] ✅ Valid Target Acquired: {actual_url}")
                    
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
                        "website_url": page.url
                    })
                except Exception:
                    print(f"[CRAWLER] ❌ Skipped (Error/Timeout): {url}")
                    continue
        except Exception as e:
            print(f"[CRAWLER] ❌ FATAL ERROR during search: {e}")
        finally:
            await browser.close()
            
    return leads
