import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright





def login_razer_gold(email: str, password: str, region_url: str, session_dir: str) -> bool:
    print("[*] Starting Razer Gold login process...")

    session_path = Path(session_dir)

    # Cleanup old session data
    if session_path.exists():
        print(f"[*] Removing old session data at: {session_path}")
        shutil.rmtree(session_path)

    os.makedirs(session_path, exist_ok=True)
    print(f"[+] New session directory created at: {session_dir}")

    with sync_playwright() as p:
        print("[*] Launching browser...")
        # browser = p.chromium.launch(headless=True)
        browser = p.chromium.launch(headless=False)

        session_file = session_path / "state.json"
        
        if session_file.exists():
            context = browser.new_context(storage_state=str(session_file))
        else:
            context = browser.new_context()
            
        page = context.new_page()

        print(f"[*] Navigating to region URL: {region_url}")
        page.goto(region_url)
        
        try:
            print("[*] Waiting for cookies button to appear...")
            accept_btn = page.get_by_role("button", name="Accept All")
            accept_btn.wait_for(state='visible', timeout=5000)
            print("[*] Accepting cookies...")
            accept_btn.click()
            page.wait_for_timeout(1000)
        except Exception as e:
            print("[!] Cookie banner not found or error:", e)

        try:
            print("[*] Waiting for login button to appear...")
            page.wait_for_selector('a[aria-label*="Log in"]', timeout=10000)
            page.click('a[aria-label*="Log in"]')
            print("[+] Clicked on login button.")
        except Exception as e:
            html = page.content()
            Path("debug_login_page.html").write_text(html)
            print(f"[!] Failed to find or click login button: {e}")
            browser.close()
            return False

        try:
            print("[*] Waiting for email/password input fields...")
            page.wait_for_selector('#input-login-email', timeout=10000)
            page.fill('#input-login-email', email)
            page.fill('#input-login-password', password)
            print("[+] Filled in credentials.")
        except Exception as e:
            print(f"[!] Failed to fill login form: {e}")
            browser.close()
            return False

        try:
            print("[*] Attempting to log in...")
            page.click('#btn-log-in')

            print("[*] Waiting for post-login redirect...")
            page.wait_for_url(lambda url: 'gold.razer.com' in url, timeout=15000)

            context.storage_state(path=session_path / "state.json")
            print("[+] Login successful. Session state saved.")
            return True
        except Exception as e:
            print(f"[!] Login failed or timeout occurred: {e}")
            return False
        finally:
            browser.close()
            print("[*] Browser closed.")
            
            
            
async def scrape_variants(product_url: str, region_url: str):
    try:
        country_code = region_url.split("https://gold.razer.com/")[1].split("/")[0]

        parts = product_url.split('/')
        parts[3] = country_code
        target_url = '/'.join(parts)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(target_url, timeout=60000)

            # First, wait a short time and check for error message
            try:
                await page.wait_for_selector('.rz-alert--danger', timeout=2000)
                alert = await page.query_selector('.rz-alert--danger')
                if alert:
                    text = await alert.inner_text()
                    await browser.close()
                    return {'error': text.strip()}
            except:
                pass  # No error alert found — continue

            # Then try to get variant elements
            try:
                await page.wait_for_selector('.selection-tile__text', timeout=10000)
                elements = await page.query_selector_all('.selection-tile__text')
                variants = [await el.inner_text() for el in elements]
                await browser.close()
                return variants
            except Exception as e:
                await browser.close()
                return {'error': 'No variants found and no error message available.'}

    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}

