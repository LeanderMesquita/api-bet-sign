from time import sleep
from api.configs.index import Configure
from api.factory.index import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log


class Starter:
    def __init__(self):
        self.configure = Configure()

    def start_injection(self, data, selected_task:str):
        try:
            
            log.info('Starting automation')
            self.injection(data, selected_task)

        except Exception as e:
            log.critical(f'An critical error ocurred!: {e}') 

    def injection(self, data, selected_task):
        
        page, p = self.configure.construct_browser(self, server='http://43.159.29.83:21836', username='odFzSl36zp', password='87478941')#server = row['Proxy']
        task = TaskFactory.create_task(selected_task, data, page)
        task.execute()
        sleep(5)
        p.stop()
        

        
