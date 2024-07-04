from api.src.tasks.multiple_inject import MultipleInjection
from api.src.tasks.single_injection import SingleInjection

class TaskFactory:
    @staticmethod
    def create_task(task_type, row, page):
        if task_type == 'multiple_injection':
            return MultipleInjection(row, page)
        elif task_type == 'single_injection':
            return SingleInjection(row, page)