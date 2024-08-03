import random
import string

def formatar_senha(senha):
    # Verifica se a senha contém números
    tem_numero = any(char.isdigit() for char in senha)
    
    # Verifica se a senha contém caracteres maiúsculos
    tem_maiusculo = any(char.isupper() for char in senha)
    
    # Verifica se a senha contém caracteres minúsculos
    tem_minusculo = any(char.islower() for char in senha)
    
    # Verifica se a senha tem pelo menos 8 caracteres
    tamanho_suficiente = len(senha) >= 8

    # Se não contém caracteres maiúsculos, transforma um caractere em maiúsculo
    if not tem_maiusculo:
        senha += random.choice(string.ascii_uppercase)

    # Se não contém caracteres minúsculos, transforma um caractere em minúsculo
    if not tem_minusculo:
        senha += random.choice(string.ascii_lowercase)

    # Se não tem 8 ou mais caracteres, adiciona caracteres até completar 8
    while len(senha) < 8:
        senha += random.choice(string.ascii_letters + string.digits)

    return senha