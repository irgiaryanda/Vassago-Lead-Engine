import re
import urllib.parse
from playwright.async_api import async_playwright

async def run_lead_scan(keyword: str, max_results: int = 3) -> list[dict]:
    leads = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(f"https://html.duckduckgo.com/html/?q={keyword}", timeout=10000)
            
            # Extract search result URLs
            url_elements = await page.locator("a.result__url").all()
            
            urls_to_visit = []
            for element in url_elements:
                if len(urls_to_visit) >= max_results:
                    break
                href = await element.get_attribute("href")
                if href:
                    if href.startswith("//duckduckgo.com/l/?uddg="):
                        qs = urllib.parse.parse_qs(urllib.parse.urlparse("http:" + href).query)
                        if "uddg" in qs:
                            href = urllib.parse.unquote(qs["uddg"][0])
                    if href.startswith(("http://", "https://")):
                        urls_to_visit.append(href)
                    
            # Visit each URL
            for url in urls_to_visit:
                try:
                    await page.goto(url, timeout=10000)
                    title = await page.title()
                    content = await page.content()
                    
                    # Regex to find email
                    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
                    contact_email = email_match.group(0) if email_match else ""
                    
                    leads.append({
                        "company_name": title.strip() if title else "Unknown",
                        "contact_email": contact_email,
                        "website_url": url
                    })
                except Exception:
                    continue
        except Exception:
            pass
        finally:
            await browser.close()
            
    return leads
