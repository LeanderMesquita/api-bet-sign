import os
import re
import playwright
from api.src.tasks.base_task import BaseTask
from playwright.sync_api import sync_playwright, Playwright, expect

class VerifyAccount(BaseTask):
    def __init__(self, row, page):
        self.row = row
        self.page = page

    def execute(self) -> None:
      page = self.page
      
      url_email = os.getenv('URL_EMAIL')
      page.goto(url_email)

      page.get_by_test_id("i0116").fill('')
      page.get_by_role("button", name="Avançar").click()
      page.get_by_test_id("i0118").fill('')
      page.get_by_test_id("i0118").press("Enter")
      page.get_by_test_id("checkboxField").check()
      page.get_by_label("Continuar conectado?").click()
      page.wait_for_timeout(3000)
      page.get_by_text("Caixa de Entrada").click()
      page.wait_for_timeout(3000)
      page.locator("div").filter(has_text=re.compile(r"^SUPERBET - Ative sua conta$")).click()
      page.wait_for_timeout(10000)
      with page.expect_popup() as page2_info:
          page.get_by_role("link", name="Ative sua conta").click()
      page3 = page2_info.value
      print('Info page2', page2_info)
      page3.goto("https://superbet.com/pt-br/")
      page3.get_by_role("button", name="Aceitar todos os cookies").click()
      expect(page3.locator("body")).to_contain_text("Parabéns!")
      page3.get_by_role("button", name="RESGATE SEU BÔNUS").click()

      # Lógica de quando a conta não ativar o bônus:
      if page3.locator("text=Bônus cancelado").is_visible():
          print("Conta com o bônus cancelado.") 
          #aqui temos que mandar para o excel de report e adicionar alguma coluna para colocar essa info
          # de que a conta foi criada porem o bonus nao foi ativado.
        
      else:
          # Seguir fluxo normal
          # falta pegar uma conta que o bonus tenha ficado ativo, escolher o esporte e depois ve no 
          # link do pix se tem as seguintes pagadoras Okto ou Global... Exemplo de link:
          # https://00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/d9051056188541ff907b78c95fbcbd075204000053039865802BR5920Okto%20Pagamentos%20S.A.6009Sao%20Paulo62070503***6304AD5B
          page3.get_by_role("button", name="depositar", exact=True).click()
          page3.get_by_role("button", name=" COPIAR CÓDIGO").click()  # Copia o código PIX
          # Obter o código PIX copiado e imprimir no console
          codigo_pix = page3.evaluate('navigator.clipboard.readText()')
          print(f"Código PIX copiado: {codigo_pix}")