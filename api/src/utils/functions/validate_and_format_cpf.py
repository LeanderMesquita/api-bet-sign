import re


def validate_and_format_cpf(cpf: str) -> str:
    """
    Valida e formata um CPF.
    
    Args:
    cpf (str): O CPF a ser validado e formatado.
    
    Returns:
    str: O CPF formatado.
    """
    # Remove todos os caracteres não numéricos
    cpf_digits = re.sub(r'\D', '', cpf)
    
    # Verifica se o CPF já está formatado
    if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return cpf
    
    # Formata o CPF
    formatted_cpf = f'{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:11]}'
    return formatted_cpf
