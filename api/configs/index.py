import sys
from playwright.sync_api import sync_playwright
from api.src.utils.logger.index import log
from dotenv import load_dotenv
import os 

import sys
from playwright.sync_api import sync_playwright
from api.src.utils.logger.index import log
from dotenv import load_dotenv
import os

class Configure:
    @staticmethod
    def construct_browser(self, use_proxy: str, proxy_server: str = None, proxy_username: str = None, proxy_password: str = None, is_headless: bool = False):
        try:
            p = sync_playwright().start()
            
            if use_proxy.lower() == 'sim' and proxy_server:
                proxy_options = {
                    "server": proxy_server,
                    "username": proxy_username,
                    "password": proxy_password
                }

                log.debug(f'Launching browser with proxy settings')
                log.debug(f'Server: {proxy_options["server"]} - Username: {proxy_options["username"]} - Password: {proxy_options["password"]}')

                browser = p.chromium.launch(headless=is_headless, proxy={"server": "per-context"})
                context = browser.new_context(proxy=proxy_options, locale='pt-BR')
            else:
                log.debug(f'Launching browser without proxy')
                browser = p.chromium.launch(headless=is_headless)
                context = browser.new_context(locale='pt-BR')

            page = context.new_page()
            
            base_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
            env_path = os.path.join(base_dir, '.env') 
            load_dotenv(env_path)

            base_url = os.getenv('BASE_URL')
            log.debug(f"Filling URL: {base_url}")
            page.goto(base_url, timeout=9000000)

            return page, p
        
        except Exception as e:
            log.error(f'Error in browser construction: {e}')

    def get_credentials(self):
        base_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(base_dir, '.env') 
        load_dotenv(env_path)
        
        username = os.getenv('BASE_USERNAME')
        password = os.getenv('BASE_PASSWORD')
        return username, password
