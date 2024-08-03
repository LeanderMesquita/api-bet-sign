from time import sleep
from api.src.utils.functions.adjust_username import adjust_username
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.format_password import formatar_senha
from api.src.utils.functions.split_date import split_date
from api.src.utils.functions.validate_and_format_cpf import validate_and_format_cpf
from api.src.utils.logger.index import log
from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
import re
import random
import pandas as pd
import string

class DataframeInjection(BaseTask):
    def __init__(self, row, page):
        self.row = row
        self.page = page

    def execute(self) -> None:
        
        try:
            nome = self.row['Nome']
            cpf = self.row['CPF']
            nascimento = self.row['Nascimento']
            endereco = self.row['Endereço']
            cidade = self.row['Cidade']
            cep = self.row['CEP']
            telefone = self.row['Telefone']
            email = self.row['E-mail']
            nome_usuario = adjust_username(email)
            password_not_formatted = self.row['Senha']
            senha = formatar_senha(password_not_formatted)

            log.info(f'Registering account ({nome}).')

            log.debug('Accepting cookies')
            self.page.get_by_role("button", name="Aceitar todos os cookies").click()

            ## first step
            day, month, year = split_date(nascimento)
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

            # Validate and format CPF
            cpf = validate_and_format_cpf(cpf)
            
            click_and_fill(self.page, selector="CPF", value=cpf, press="Enter", after_delay=1.5)
            
            # Second step
            click_and_fill(self.page, selector="endereço", value=endereco)

            self.page.get_by_label("cidade", exact=True).click()
            sleep(1)
            log.debug(f'Filling selector: "cidade" with value: {cidade}')
            self.page.get_by_label("cidade", exact=True).fill(cidade)

            click_and_fill(self.page, selector="cep", value=cep)
            click_and_fill(self.page, selector="Número de telefone", value=telefone, press="Enter")

            # Third step
            click_and_fill(self.page, selector="E-mail", value=email)
            click_and_fill(self.page, selector="nome de usuário", value=nome_usuario)
            click_and_fill(self.page, selector="senha", value=senha)

            self.page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
            sleep(1)
            self.page.get_by_label("Tenho 18 anos ou mais de").press("Enter")
            sleep(5)

            if self.page.locator('.activate-account__content-notice').is_visible():
                log.success(f'Account ({nome}) was registered successfully!')
                return True
            
            raise ValueError("Not created account")
        except Exception as e:
            log.error(f'The current account {nome} was not registered. {e}')
            error_report(cpf, nome, error=e)