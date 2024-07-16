from api.src.tasks.dataframe_injection import DataframeInjection
from api.src.tasks.json_injection import JSONInjection
from api.src.tasks.verify_account import VerifyAccount

class TaskFactory:
    @staticmethod
    def create_task(task_type, data, page):
        if task_type == 'dataframe_injection':
            return DataframeInjection(data, page)
        elif task_type == 'json_injection': 
            return JSONInjection(data, page)
        elif task_type == 'verify_account':
            return VerifyAccount(data, page)