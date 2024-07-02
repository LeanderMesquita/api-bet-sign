from api.src.tasks.base_task import BaseTask


class MultipleInjection(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self):
        return super().execute()
        