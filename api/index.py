from api.factory.index import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log

def start_injection(df, selected_task:str):
    try:
        log.info('Starting automation')
        if not df.empty: log.success('Dataframe create successfully!')
        for index, row in df.iterrows():
            try:
                log.info(f'Registering account ({row['Nome']}).')
                task = TaskFactory.create_task(selected_task)
                task.execute()

                log.success(f'Account ({row['Nome']}) was registered successfully!')
                successfully_report(row['CPF'], row['Nome'])
                if index >= len(df) - 1: log.warning(f'All accounts are readed, please verify the reports. Iterate qtn: {len(df)}')
                
            except Exception as e:
                log.error(f'The current account {row['Nome']} was not registered. {e}')
                error_report(row['CPF'], row['Nome'], error=e)

    except Exception as e:
        log.critical(f'An critical error ocurred!: {e}') 
