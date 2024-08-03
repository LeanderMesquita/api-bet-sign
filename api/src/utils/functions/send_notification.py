import os
import sys
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
base_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env') 
load_dotenv(env_path)

def send_whatsapp_report(cpf:str, account_email:str, account_password:str, account_name:str, activation_link:str):
    url_api_wp = os.getenv('URL_API_WP')
    instance = os.getenv('INSTANCE')
    id_group_send = os.getenv('ID_GROUP_SEND')
    api_key_wp = os.getenv('API_KEY_WP')

    # Verificação das variáveis de ambiente
    if not url_api_wp:
        raise ValueError("URL_API_WP environment variable not set")
    if not instance:
        raise ValueError("INSTANCE environment variable not set")
    if not id_group_send:
        raise ValueError("ID_GROUP_SEND environment variable not set")
    if not api_key_wp:
        raise ValueError("API_KEY_WP environment variable not set")
    
    message_report = f'''🚨 Conta Criada - Superbet 🚨

🙋🏻‍♂️ *Nome:* {account_name} 
🙋🏻‍♂️ *CPF:* {cpf}
📧 *Email:* {account_email}
🔑 *Senha:* {account_password}
🔗 *Link de Ativação:* {activation_link}
'''
    url = f"{url_api_wp}{instance}"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key_wp
    }
    payload = {
        "number": id_group_send,
        "options": {
            "delay": 1200,
            "presence": "composing",
            "linkPreview": True
        },
        "textMessage": {
            "text": message_report
        }
    }

    requests.post(url=url, headers=headers, data=json.dumps(payload))

# send_whatsapp_report(cpf='53531418149',account_name= 'SILVIA SATO', account_email='lynellesche95@outlook.com', account_password='DxbvL432j5', broker='00020126890014BR.GOV.BCB.PIX2567api-pix.bancobs2.com.br/spi/v2/a2f2cb84-48e6-40a6-b31c-aaeaece4d18752040000530398654041.005802BR5925Pay Brokers Cobranca E Se6014Belo Horizonte61083038040362070503***630442C9')