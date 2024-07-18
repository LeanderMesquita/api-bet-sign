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
            log.debug("Clicking to email")
            self.page.locator("div").filter(has_text=re.compile(r"^SUPERBET - Ative sua conta$")).click()
            return True
        except:
            log.debug("Not Find Email in Actual Folder")
            return False
        
    def get_payment_provider(link: str) -> str:
        payment_providers = ["Okto", "Global"]
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
            
            log.debug("Logging in")
            page.get_by_test_id("i0116").fill(email)
            page.get_by_role("button", name="Avançar").click()
            page.get_by_test_id("i0118").fill(password)
            page.get_by_test_id("i0118").press("Enter")
            page.get_by_test_id("checkboxField").check()
            page.get_by_label("Continuar conectado?").click()
            log.debug("Wait for dom content load...")
            page.wait_for_timeout(20000)
            log.debug("Find activation email in Inbox")
            if not self.find_and_click_email():
                log.debug("Find activation email in Junk")
                page.get_by_text("Lixo Eletrônico").click()
                page.wait_for_timeout(20000)
                if not self.find_and_click_email():
                    raise ValueError("Email não encontrado.")
                else:
                    page.get_by_role("button", name="Mostrar conteúdo bloqueado e").click()
                
            page.wait_for_timeout(50000)

            log.debug('Clicking the link activation to account')
            activation_link = page.locator("a:has-text('Ative sua conta')").get_attribute('href')
            page.goto(activation_link, timeout=1000000)
            page.wait_for_timeout(50000)
            log.debug('Accepting Cookies')
            page.get_by_role("button", name="Aceitar todos os cookies").click()
            expect(page.locator("body")).to_contain_text("Parabéns!")
            log.debug('Clicking in bonus redemption')
            page.get_by_role("button", name="RESGATE SEU BÔNUS").click()

            # Lógica de quando a conta não ativar o bônus:
            if page.locator("text=Bônus cancelado").is_visible():
                log.error("Account with canceled bonus.") 
                raise ValueError(f'The current account was created but without bonus') 
                
            else:
                page.get_by_role("button", name="Sim, quero").click()
                page.get_by_role("button", name="selecione o bônus de esporte").click()
                log.debug('Making a deposit')
                page.get_by_role("button", name="depositar", exact=True).click()
                
                page.get_by_role("button", name=" COPIAR CÓDIGO").click()  # Copia o código PIX
                codigo_pix = page.evaluate('navigator.clipboard.readText()')
                provider = self.get_payment_provider(codigo_pix)
                if provider:
                    log.info(f'Account Verified Successfully with payment provider: {provider}')
                    print(f"Código PIX copiado: {codigo_pix}")
                    print(f"Pagadora encontrada: {provider}")
                else:
                    log.info("Account Verified Successfully, but the payment provider is not Okto or Global.")
                    print(f"Código PIX copiado: {codigo_pix}")
                    print("Código PIX não contém as pagadoras Okto ou Global.")
                    
        except Exception as e:
            error_report(cpf=self.row["CPF"],account_name=self.row["Nome"], error=e)
            log.error(f"Error in account verification: {e}")