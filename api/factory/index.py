from api.src.tasks.multiple_inject import MultipleInjection
from api.src.tasks.single_injection import SingleInjection

class TaskFactory:
    @staticmethod
    def create_task(task_type, row):
        if task_type == 'multiple_injection':
            return MultipleInjection(row)
        elif task_type == 'single_injection':
            return SingleInjection(row)