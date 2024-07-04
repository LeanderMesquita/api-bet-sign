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
        if not self.dataframe.empty: log.success('Dataframe create successfully!')
        for index, row in self.dataframe.iterrows():    
            try:
    
                log.info(f'Registering account ({row['Nome']}).')
                
                log.debug('Accepting cookies')
                self.page.get_by_role("button", name="Aceitar todos os cookies").click()

                ## first step
                
                day, month, year = split_date(row['Nascimento'])#row['Nascimento']
                self.page.get_by_placeholder("dd").click()
                sleep(1)
                log.debug(f'Filling selector: "dd" with value: {day}')
                self.page.get_by_placeholder("dd").fill("28")#day
                sleep(1)
                log.debug(f'Filling selector: "mm" with value: {month}')
                self.page.get_by_placeholder("mm").fill("09")#month
                sleep(1)
                log.debug(f'Filling selector: "yyyy" with value: {year}')
                self.page.get_by_placeholder("yyyy").fill("1963")#year

                click_and_fill(self.page, selector="CPF", value="229.126.063-49", press="Enter")#row['CPF']
                
                #second step
                click_and_fill(self.page, selector="endereço", value="Rua teste")#row['Endereço']
            
                
                self.page.get_by_label("cidade", exact=True).click()
                sleep(1)
                log.debug(f'Filling selector: "cidade" with value: {"?CIDADE"}')
                self.page.get_by_label("cidade", exact=True).fill("fortaleza")#row['Cidade']

                click_and_fill(self.page, selector="cep", value="60000-600")#row['CEP']
                click_and_fill(self.page, selector="Número de telefone", value="940028922", press="Enter")#row['Telefone']

                #third step
                click_and_fill(self.page, selector="E-mail", value="emailteste@gmail.com")#row['Email']
                click_and_fill(self.page, selector="nome de usuário", value="testebet2")#row['Nome Usuario]
                click_and_fill(self.page, selector="senha", value="Edra36Edra")#row['Senha']

                self.page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
                sleep(1)
                self.page.get_by_label("Tenho 18 anos ou mais de").press("Enter")

                log.success(f'Account ({row['Nome']}) was registered successfully!')
                successfully_report(row['CPF'], row['Nome'])
                if index >= len(self.dataframe) - 1: log.warning(f'All accounts are readed, please verify the reports. Iterate qtn: {len(self.dataframe)}')
                
            except Exception as e:
                    log.error(f'The current account {row['Nome']} was not registered. {e}')
                    error_report(row['CPF'], row['Nome'], error=e)
