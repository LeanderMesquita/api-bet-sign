from time import sleep
from api.configs.index import Configure
from api.factory.index import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log
from concurrent.futures import ThreadPoolExecutor

class Starter:
    def __init__(self):
        self.configure = Configure()

    def start_injection(self, data, selected_task: str):
        try:
            log.info('Starting automation')
            self.injection(data, selected_task)
        except Exception as e:
            log.critical(f'A critical error occurred!: {e}')

    def injection(self, data, selected_task):
        def process_row(row):
            proxy = {'server':'http://43.159.29.83:21836', "username":'odFzSl36zp', "password":'87478941'}
            page, p = self.configure.construct_browser(self, server=proxy['server'], username=proxy['username'], password=proxy['password'])
            task = TaskFactory.create_task(selected_task, row, page)
            task.execute()
            sleep(5)
            p.stop()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            for _, row in data.iterrows():
                executor.submit(process_row, row)
