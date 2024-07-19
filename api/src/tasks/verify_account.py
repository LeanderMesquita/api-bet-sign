import os
import re
from time import time
import playwright
from api.src.tasks.base_task import BaseTask
from playwright.sync_api import sync_playwright, Playwright, expect
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.send_notification import send_whatsapp_report
from api.src.utils.functions.successfully_report import successfully_report
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
            log.error(f"Exception in find_and_click_email: {e}")
            return False
        
    def get_payment_provider(self, link: str) -> str:
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
            name = self.row['Nome']
            cpf = self.row['CPF']
           

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
            if page.get_by_role("link", name="Ignorar por enquanto").is_visible():
                log.debug("'Ignore for now' link is visible, clicking it.")
            page.get_by_role("link", name="Ignorar por enquanto").click()
            page.get_by_role("link", name="Ignorar por enquanto").click()

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
                    log.debug("Activation email found in Junk folder, checking if button 'Show blocked content' is visible")
                    if page.get_by_role("button", name="Mostrar conteúdo bloqueado e").is_visible():
                        log.debug("Clicking 'Show blocked content'")
                        page.get_by_role("button", name="Mostrar conteúdo bloqueado e").click()

            log.debug("Waiting for the email content to load...")    
            page.wait_for_timeout(50000)

            log.debug("Clicking the account activation link")
            activation_link = page.locator("a:has-text('Ative sua conta')").get_attribute('href')
            if activation_link:
                page.goto(activation_link, timeout=10000000)
                page.wait_for_timeout(20000)
                log.debug("Navigated to the account activation link")
            else:
                raise ValueError("Activation link not found in the email.")
                
            log.debug("Checking for 'Accept cookies' button")
            if page.get_by_role("button", name="Aceitar todos os cookies").is_visible():
                log.debug("Accepting cookies")
                page.get_by_role("button", name="Aceitar todos os cookies").click()
                log.debug("Cookies accepted")
            else:
                log.debug("'Accept cookies' button not found, continuing without accepting cookies")

            expect(page.locator("body")).to_contain_text("Parabéns!")
            log.debug("'Parabéns!' text found")

            log.debug("Clicking 'RESGATE SEU BÔNUS' button")
            page.get_by_role("button", name="RESGATE SEU BÔNUS").click()

            if page.locator("text=Bônus cancelado").is_visible():
                log.error("Account with canceled bonus.") 
                raise ValueError("The current account was created but without bonus")
                
            else:

                log.debug("Clicking 'Sim, quero'")
                page.get_by_role("button", name="Sim, quero").click()
                log.debug("Selecting sports bonus")
                page.get_by_role("button", name="selecione o bônus de esporte").click()
                log.debug('Making a deposit')
                page.get_by_role("button", name="depositar", exact=True).click()
                

                def handle_dialog(dialog):
                    if "área de transferência" in dialog.message or "copiados para a área de transferência" in dialog.message:
                        log.debug(f'clicking "Permitir" to {dialog.message}')
                        dialog.accept()  # press "Permitir"
                    else:
                        dialog.dismiss()  # press "Bloquear"
                
                page.on("dialog", handle_dialog)

                log.debug("Clicking 'COPIAR CÓDIGO' button")
                page.get_by_role("button", name=" COPIAR CÓDIGO").click()  # Copia o código PIX


                log.debug("Reading PIX code from clipboard")
                # Resolver a Promise para obter o valor do clipboard
                codigo_pix = page.evaluate('''navigator.clipboard.readText().then(text => text)''')
                log.debug(f'Value pix code: {codigo_pix}') 

                log.success(f'Account - [{name}] - Verified Successfully with payment provider: \n{codigo_pix}')
                send_whatsapp_report(cpf=cpf, account_name=name, account_email=email, account_password=password, broker=codigo_pix )
                log.success(f'Report send to Whatsapp Group')
                successfully_report(cpf=cpf, account_name=name, account_email=email, account_password=password, provider_payment=codigo_pix)
                
                    
        except Exception as e:
            error_report(cpf=self.row["CPF"],account_name=self.row["Nome"], error=e)
            log.error(f"Error in account verification: {e}")