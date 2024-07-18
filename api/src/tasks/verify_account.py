import os
import re
from time import time
import playwright
from api.src.tasks.base_task import BaseTask
from playwright.sync_api import sync_playwright, Playwright, expect
from api.src.utils.functions.error_report import error_report
from api.src.utils.logger.index import log

class VerifyAccount(BaseTask):
    def __init__(self, row, page):
        self.row = row
        self.page = page

    def find_and_click_email(self):
        try:
            self.page.locator("div").filter(has_text=re.compile(r"^SUPERBET - Ative sua conta$")).click()
            return True
        except Exception as e:
            log.debug(f"Exception in find_and_click_email: {e}")
            return False
        
    def get_payment_provider(link: str) -> str:
        payment_providers = ["Okto", "Global", "Pay By SB GLOBAL", "Pay Brokers Cobranca E Se"]
        for provider in payment_providers:
            if re.search(provider, link, re.IGNORECASE):
                return provider
        return None  
    
    def execute(self) -> None:
        try:
            page = self.page
            email = self.row['E-mail']
            password = self.row['Senha']

            log.info("Starting account validation")
            
            url_email = os.getenv('URL_EMAIL')
            page.goto(url_email)
            
            log.info("Logging in")
            log.debug(f"Filling email address: {email}")
            page.get_by_test_id("i0116").fill(email)
            page.get_by_role("button", name="Avançar").click()
            log.debug("Filled email and clicked 'Avançar'")

            log.debug(f"Filling password: {password}")
            page.get_by_test_id("i0118").fill(password)
            page.get_by_test_id("i0118").press("Enter")
            log.debug("Filled password and pressed 'Enter'")
            
            log.debug("Checking if the 'Ignore for now' link is visible.")
            if page.locator("a#iShowSkip").is_visible():
                log.debug("'Ignore for now' link is visible, clicking it.")
                page.locator("a#iShowSkip").click()

            page.get_by_test_id("checkboxField").check()
            page.get_by_label("Continuar conectado?").click()
            log.debug("Checked 'Stay signed in' and clicked 'Yes'")

            log.debug("Wait for dom content load...")
            page.wait_for_timeout(20000)
            
            log.info("Searching for activation email in Inbox")
            if not self.find_and_click_email():
                log.info("Activation email not found in Inbox, checking Junk folder")
                page.get_by_text("Lixo Eletrônico").click()
                page.wait_for_timeout(20000)
                if not self.find_and_click_email():
                    raise ValueError("Activation email not found in Junk folder either.")
                else:
                    log.debug("Activation email found in Junk folder, clicking 'Show blocked content'")
                    page.get_by_role("button", name="Mostrar conteúdo bloqueado e").click()

            log.debug("Waiting for the email content to load...")    
            page.wait_for_timeout(50000)

            log.info("Clicking the account activation link")
            activation_link = page.locator("a:has-text('Ative sua conta')").get_attribute('href')
            if activation_link:
                page.goto(activation_link, timeout=1000000)
                page.wait_for_timeout(50000)
                log.info("Navigated to the account activation link")
            else:
                raise ValueError("Activation link not found in the email.")
                
            log.info("Checking for 'Accept cookies' button")
            if page.get_by_role("button", name="Aceitar todos os cookies").is_visible():
                log.info("Accepting cookies")
                page.get_by_role("button", name="Aceitar todos os cookies").click()
                log.info("Cookies accepted")
            else:
                log.info("'Accept cookies' button not found, continuing without accepting cookies")

            expect(page.locator("body")).to_contain_text("Parabéns!")
            log.info("'Parabéns!' text found")

            log.info("Clicking 'RESGATE SEU BÔNUS' button")
            page.get_by_role("button", name="RESGATE SEU BÔNUS").click()

            if page.locator("text=Bônus cancelado").is_visible():
                log.error("Account with canceled bonus.") 
                raise ValueError("The current account was created but without bonus")
                
            else:
                log.info("Clicking 'Sim, quero'")
                page.get_by_role("button", name="Sim, quero").click()
                log.info("Selecting sports bonus")
                page.get_by_role("button", name="selecione o bônus de esporte").click()
                log.debug('Making a deposit')
                page.get_by_role("button", name="depositar", exact=True).click()
                
                log.info("Clicking 'COPIAR CÓDIGO' button")
                page.get_by_role("button", name=" COPIAR CÓDIGO").click()  # Copia o código PIX
                
                log.info("Handling clipboard permission dialog")
                page.on("dialog", lambda dialog: dialog.accept())

                log.info("Reading PIX code from clipboard")
                codigo_pix = page.evaluate('navigator.clipboard.readText()')
                log.debug(f'Value pix code: {codigo_pix}') 

                provider = self.get_payment_provider(codigo_pix)
                if provider:
                    log.info(f'Account Verified Successfully with payment provider: {provider}')
                    log.debug(f"Código PIX copiado: {codigo_pix}")
                    log.debug(f"Pagadora encontrada: {provider}")
                else:
                    log.info("Account Verified Successfully, but the payment provider is not Okto or Global.")
                    log.debug(f"Código PIX copiado: {codigo_pix}")
                    log.debug("Código PIX não contém as pagadoras Okto ou Global.")
                    
        except Exception as e:
            error_report(cpf=self.row["CPF"],account_name=self.row["Nome"], error=e)
            log.error(f"Error in account verification: {e}")