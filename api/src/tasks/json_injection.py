from time import sleep
from api.src.utils.functions.validate_and_format_cpf import validate_and_format_cpf
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
            log.debug(f'Trimming birthdate {self.obj['dob']}'+' 00:00:00')
            day, month, year = split_date(self.obj['dob']+' 00:00:00')
            self.page.get_by_placeholder("dd").click()
            sleep(1)
            log.debug(f'Filling selector: "dd" with value: {day}')
            self.page.get_by_placeholder("dd").fill(str(day))
            sleep(1)
            log.debug(f'Filling selector: "mm" with value: {month}')
            self.page.get_by_placeholder("mm").fill(str(month))
            sleep(1)
            log.debug(f'Filling selector: "yyyy" with value: {year}')
            self.page.get_by_placeholder("yyyy").fill(str(year))

            cpf = validate_and_format_cpf(self.obj['cpf'])
            click_and_fill(self.page, selector="CPF", value=cpf, press="Enter")
            
            #second step
            
            click_and_fill(self.page, selector="endereço", value=self.obj['address'])
        
            self.page.get_by_label("cidade", exact=True).click()
            sleep(1)
            log.debug(f'Filling selector: "cidade" with value: {self.obj['city']}')
            self.page.get_by_label("cidade", exact=True).fill(self.obj['city'])

            click_and_fill(self.page, selector="cep", value=self.obj['zipcode'])
            click_and_fill(self.page, selector="Número de telefone", value=self.obj['phone'], press="Enter")

            #third step
            click_and_fill(self.page, selector="E-mail", value=self.obj['email'])
            click_and_fill(self.page, selector="nome de usuário", value=self.obj['username'])
            click_and_fill(self.page, selector="senha", value=self.obj['password'])

            self.page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
            sleep(1)
            self.page.get_by_label("Tenho 18 anos ou mais de").press("Enter")
            log.success(f'Account ({self.obj['name']}) was registered successfully!')

        except Exception as e:
            log.error(f'The current account {self.obj['name']} was not registered. {e}')
            