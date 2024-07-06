from time import sleep
from api.src.utils.logger.index import log
from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.functions.split_date import split_date


class JSONInjection(BaseTask):
    def __init__(self, json, page):
        self.obj = json
        self.page = page

    def execute(self) -> None:
        
        try:
            if not isinstance(self.obj, dict):
                raise TypeError(f'the parameter passed is not JSON.')

            log.debug('Accepting cookies')
            self.page.get_by_role("button", name="Aceitar todos os cookies").click()

            ## first step
            log.debug(f'Trimming birthdate {self.obj['Nascimento']}')
            day, month, year = split_date(self.obj['Nascimento'])
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

            click_and_fill(self.page, selector="CPF", value=self.obj['CPF'], press="Enter")
            
            #second step
            click_and_fill(self.page, selector="endereço", value=self.obj['Endereço'])
        
            
            self.page.get_by_label("cidade", exact=True).click()
            sleep(1)
            log.debug(f'Filling selector: "cidade" with value: {self.obj['Cidade']}')
            self.page.get_by_label("cidade", exact=True).fill(self.obj['Cidade'])

            click_and_fill(self.page, selector="cep", value=self.obj['CEP'])
            click_and_fill(self.page, selector="Número de telefone", value=self.obj['Telefone'], press="Enter")

            #third step
            click_and_fill(self.page, selector="E-mail", value=self.obj['Email'])
            click_and_fill(self.page, selector="nome de usuário", value=self.obj['Nome Usuario'])
            click_and_fill(self.page, selector="senha", value=self.obj['Senha'])

            self.page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
            sleep(1)
            self.page.get_by_label("Tenho 18 anos ou mais de").press("Enter")
            log.success(f'Account ({self.obj['Nome']}) was registered successfully!')

        except Exception as e:
            log.error(f'The current account {self.obj['Nome']} was not registered. {e}')
            