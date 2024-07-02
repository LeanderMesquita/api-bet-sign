import re
from playwright.sync_api import Page, expect
from time import sleep

from api.src.tasks.base_task import BaseTask
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.functions.split_date import split_date


class MultipleInjection(BaseTask):
    def __init__(self, row):
        self.row = row

    def execute(self, page: Page) -> None:
        ## going to superbet register page
        page.goto("https://superbet.com/pt-br/register?utm_source=google&utm_medium=ppc&utm_campaign=ppc-bet-acq-ext-sitelink_onboard-brand-all-sup&gad_source=1&gclid=CjwKCAjwp4m0BhBAEiwAsdc4aIvP-ORBTZXG7hDmPVNE6OS3i3lVBSnfOx9V-RbIy8OUS6Z2DcDj1RoCT3kQAvD_BwE")

        ## first step
        page.get_by_role("button", name="Aceitar todos os cookies").click()

        day, month, year = split_date(self.row['Data de Nascimento'])
        page.get_by_placeholder("dd").click()
        page.get_by_placeholder("dd").fill(day)
        page.get_by_placeholder("mm").fill(month)
        page.get_by_placeholder("yyyy").fill(year)

        click_and_fill(page, selector="CPF", value="229.126.063-49_", press="Enter")#self.row['CPF']
        
        #second step
        click_and_fill(page, selector="endereço", value="Rua teste")#self.row['Endereço']
    
        page.get_by_label("cidade", exact=True).click()
        page.get_by_label("cidade", exact=True).fill("fortaleza")#self.row['Cidade']

        click_and_fill(page, selector="cep", value="60000-600")#self.row['CEP']
        click_and_fill(page, selector="Número de telefone", value="940028922", press="Enter")#self.row['Telefone']

        #third step
        click_and_fill(page, selector="E-mail", value="emailteste@gmail.com")#self.row['Email']
        click_and_fill(page, selector="nome de usuário", value="testebet2")#self.row['Nome Usuario]
        click_and_fill(page, selector="senha", value="davi_chefinho_aumenta_meu_salario")#self.row['Senha']

        page.locator("label").filter(has_text="Tenho 18 anos ou mais de").click()
        page.get_by_label("Tenho 18 anos ou mais de").press("Enter")
        