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
                task = TaskFactory.create_task(selected_task)
                task.execute(page=construct_browser(server='', username='odFzSl36zp', password='87478941'))

                log.success(f'Account ({row['Nome']}) was registered successfully!')
                successfully_report(row['CPF'], row['Nome'])
                if index >= len(df) - 1: log.warning(f'All accounts are readed, please verify the reports. Iterate qtn: {len(df)}')
                
            except Exception as e:
                log.error(f'The current account {row['Nome']} was not registered. {e}')
                error_report(row['CPF'], row['Nome'], error=e)

    except Exception as e:
        log.critical(f'An critical error ocurred!: {e}') 


def construct_browser(server:str, username:str, password:str, is_headless:bool = False) -> Page:
    
    load_dotenv()
    
    proxy_options = {
        "server": server,
        "username": username,
        "password": password
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={"server": "per-context"}, headless=is_headless)
        context = browser.new_context(proxy=proxy_options)
        page = context.new_page()
        page.goto(os.getenv('BASE_URL'))
        page.get_by_role("button", name="Aceitar todos os cookies").click()