import re
from playwright.sync_api import Page, expect
from time import sleep
from dotenv import load_dotenv
import os
from api.src.utils.logger.index import log
from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.functions.split_date import split_date


class MultipleInjection(BaseTask):
    def __init__(self, row, page):
        self.row = row
        self.page = page

    def execute(self) -> None:
        
        
        log.debug('Accepting cookies')
        self.page.get_by_role("button", name="Aceitar todos os cookies").click()

        ## first step
        
        day, month, year = split_date(self.row['Nascimento'])#self.row['Nascimento']
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

        click_and_fill(self.page, selector="CPF", value="229.126.063-49", press="Enter")#self.row['CPF']
        
        #second step
        click_and_fill(self.page, selector="endereço", value="Rua teste")#self.row['Endereço']
    
        
        self.page.get_by_label("cidade", exact=True).click()
        sleep(1)
        log.debug(f'Filling selector: "cidade" with value: {"?CIDADE"}')
        self.page.get_by_label("cidade", exact=True).fill("fortaleza")#self.row['Cidade']

        click_and_fill(self.page, selector="cep", value="60000-600")#self.row['CEP']
        click_and_fill(self.page, selector="Número de telefone", value="940028922", press="Enter")#self.row['Telefone']

        #third step
        click_and_fill(self.page, selector="E-mail", value="emailteste@gmail.com")#self.row['Email']
        click_and_fill(self.page, selector="nome de usuário", value="testebet2")#self.row['Nome Usuario]
        click_and_fill(self.page, selector="senha", value="Edra36Edra")#self.row['Senha']

        self.page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
        sleep(1)
        self.page.get_by_label("Tenho 18 anos ou mais de").press("Enter")
        