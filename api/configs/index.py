from playwright.sync_api import sync_playwright
from api.src.utils.logger.index import log
from dotenv import load_dotenv
import os 

class Configure:
    @staticmethod
    def construct_browser(self, server: str, username: str = None, password: str = None, is_headless: bool = False):
    
        try:
            
            proxy_options = {
                "server": server,
                "username": username,
                "password": password
            }

            p = sync_playwright().start()

            log.debug(f'Launching browser with proxy settings - {proxy_options["server"]}')
            browser = p.chromium.launch(headless=is_headless, proxy={"server": "per-context"})
            context = browser.new_context(proxy=proxy_options)
            page = context.new_page()
            
            load_dotenv()
            base_url = os.getenv('BASE_URL')
            log.debug(f"Filling URL: {base_url}")
            page.goto(base_url, timeout=9000000)

            return page, p
        
        except Exception as e:
            log.error(f'Error in browser construction: {e}')