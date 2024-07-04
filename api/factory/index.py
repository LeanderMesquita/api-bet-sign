from api.src.tasks.multiple_inject import MultipleInjection
from api.src.tasks.single_injection import SingleInjection

from api.src.tasks.dataframe_injection import DataframeInjection
from api.src.tasks.json_injection import JSONInjection
class TaskFactory:
    @staticmethod
    def create_task(task_type, data, page):
        if task_type == 'multiple_injection':
            return MultipleInjection(data, page)
        elif task_type == 'single_injection':
            return SingleInjection(data, page)
        elif task_type == 'dataframe_injection':
            return DataframeInjection(data, page)
        elif task_type == 'json_injection': 
            return JSONInjection(data, page)