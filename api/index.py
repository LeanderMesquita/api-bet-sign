from time import sleep
from dotenv import load_dotenv
import os 
from api.factory.index import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log
from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright

def start_injection(df, selected_task:str):
    try:
        log.info('Starting automation')
        if not df.empty: log.success('Dataframe create successfully!')
        for index, row in df.iterrows():    
            try:
                log.info(f'Registering account ({row['Nome']}).')
                
                page, p = construct_browser(server='http://43.159.29.83:21836', username='odFzSl36zp', password='87478941')#server = row['Proxy']
                task = TaskFactory.create_task(selected_task, row, page)
                task.execute()

                log.success(f'Account ({row['Nome']}) was registered successfully!')
                successfully_report(row['CPF'], row['Nome'])
                sleep(5)
                p.stop()
                if index >= len(df) - 1: log.warning(f'All accounts are readed, please verify the reports. Iterate qtn: {len(df)}')
                
            except Exception as e:
                log.error(f'The current account {row['Nome']} was not registered. {e}')
                error_report(row['CPF'], row['Nome'], error=e)

    except Exception as e:
        log.critical(f'An critical error ocurred!: {e}') 


def construct_browser(server: str, username: str = None, password: str = None, is_headless: bool = False):
 
    try:
        
        proxy_options = {
            "server": server,
            "username": username,
            "password": password
        }

        p = sync_playwright().start()

        log.debug('Launching browser with proxy settings')
        browser = p.chromium.launch(headless=is_headless, proxy={"server": "per-context"})
        context = browser.new_context(proxy=proxy_options)
        page = context.new_page()
        
        load_dotenv()
        base_url = os.getenv('BASE_URL')
        log.debug(f"Filling URL: {base_url}")
        page.goto(base_url, timeout=60000)

        return page, p
    
    except Exception as e:
        log.error(f'Error in browser construction: {e}')
        
