from time import sleep
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.index import log
from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.functions.split_date import split_date

class DataframeInjection(BaseTask):
    def __init__(self, dataframe, page):
        self.dataframe = dataframe
        self.page = page

    def execute(self) -> None:
        if not self.dataframe.empty: 
            log.success('Dataframe created successfully!')
        for index, row in self.dataframe.iterrows():    
            try:
                log.info(f'Registering account ({row['Nome']}).')
                log.debug('Accepting cookies')
                self.page.get_by_role("button", name="Aceitar todos os cookies").click()
                
                day, month, year = split_date(row['Nascimento'])
                self.page.get_by_placeholder("dd").click()
                sleep(1)
                log.debug(f'Filling selector: "dd" with value: {day}')
                self.page.get_by_placeholder("dd").fill(day)
                sleep(1)
                log.debug(f'Filling selector: "mm" with value: {month}')
                self.page.get_by_placeholder("mm").fill(month)
                sleep(1)
                log.debug(f'Filling selector: "yyyy" with value: {year}')
                self.page.get_by_placeholder("yyyy").fill(year)

                click_and_fill(self.page, selector="CPF", value=row['CPF'], press="Enter")
                
                click_and_fill(self.page, selector="endereço", value=row['Endereço'])
                self.page.get_by_label("cidade", exact=True).click()
                sleep(1)
                log.debug(f'Filling selector: "cidade" with value: {row['Cidade']}')
                self.page.get_by_label("cidade", exact=True).fill(row['Cidade'])

                click_and_fill(self.page, selector="cep", value=row['CEP'])
                click_and_fill(self.page, selector="Número de telefone", value=row['Telefone'], press="Enter")

                click_and_fill(self.page, selector="E-mail", value=row['Email'])
                click_and_fill(self.page, selector="nome de usuário", value=row['Nome Usuario'])
                click_and_fill(self.page, selector="senha", value=row['Senha'])

                self.page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
                sleep(1)
                self.page.get_by_label("Tenho 18 anos ou mais de").press("Enter")

                log.success(f'Account ({row['Nome']}) was registered successfully!')
                successfully_report(row['CPF'], row['Nome'])
                if index >= len(self.dataframe) - 1: 
                    log.warning(f'All accounts processed. Total: {len(self.dataframe)}')
            except Exception as e:
                log.error(f'The current account {row['Nome']} was not registered. {e}')
                error_report(row['CPF'], row['Nome'], error=e)
