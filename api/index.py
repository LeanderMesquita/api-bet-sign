from time import sleep
from api.configs.index import Configure
from api.factory.index import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log


class Starter:
    def __init__(self):
        self.configure = Configure()

    def start_JSON_injection(self, data, selected_task:str = 'json_injection'):
        try:
            log.info('Starting JSON injection')
            self.injection(data, selected_task)

        except Exception as e:
            log.critical(f'An critical error ocurred!: {e}') 
    
    def start_dataframe_injection(self, data, selected_task:str = 'dataframe_injection'):
        try:
            if not data.empty: log.success('Dataframe create successfully!')

            for index, row in data.iterrows():
                log.info('Starting dataframe automation')
                self.injection(row, selected_task)
                if index >= len(data) - 1: log.warning(f'All accounts are readed, please verify the reports. Iterate qtn: {len(data)}')
        except Exception as e:
            log.critical(f'An critical error ocurred!: {e}') 

    def injection(self, data, selected_task): 
        page, p = self.configure.construct_browser(self, server=data['Proxy'], username='odFzSl36zp', password='87478941')#server = row['Proxy']
        task = TaskFactory.create_task(selected_task, data, page)
        task.execute()
        sleep(5)
        p.stop()