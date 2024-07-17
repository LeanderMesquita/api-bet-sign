from concurrent.futures import ThreadPoolExecutor
from time import sleep
from api.configs.index import Configure
from api.factory.index import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

class Starter:
    def __init__(self):
        self.configure = Configure()

    def start_JSON_injection(self, data, selected_task:str = 'json_injection'):
        try:
            log.info('Starting JSON injection')
            username, password = self.configure.get_credentials()
            proxy_ip = data['ipProxy']  
            proxy_url = f'http://{proxy_ip}'
            page, p = self.configure.construct_browser(self, server=proxy_url, username=username, password=password, is_headless=data['headless'])
            task = TaskFactory.create_task(selected_task, data, page)
            task.execute()
            sleep(3)
        except Exception as e:
            log.critical(f'An critical error ocurred!: {e}') 
        finally:
            p.stop()
            log.info(f'Browser closed for {data["name"]}')
        
    
    def start_dataframe_injection(self, data, headless, selected_task:str = 'dataframe_injection'):
        try:
            log.info('Starting automation')

            for index, row in data.iterrows():
                def str_to_bool(s):
                    return s.lower() == 'true'

                proxy_ip = row['Proxy']  
                proxy_url = f'http://{proxy_ip}'
                username, password = self.configure.get_credentials()
                proxy = {'server': proxy_url, 'username': username, 'password': password}

                try:
                    page, p = self.configure.construct_browser(self, server=proxy['server'], username=proxy['username'], password=proxy['password'], is_headless=str_to_bool(headless))
                    task = TaskFactory.create_task(selected_task, row, page)
                    task.execute()
                    task_verify_account = TaskFactory.create_task(task_type='verify_account', data=row, page=page)
                    task_verify_account.execute()
                    sleep(5)
                finally:
                    p.stop()
                    log.info(f'Browser closed for {row["Nome"]}')
                    

        except Exception as e:
            log.critical(f'A critical error occurred!: {e}')
