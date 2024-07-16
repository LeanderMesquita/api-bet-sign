from api.src.utils.functions.format_date import format_date
import pandas as pd
def split_date(date_str: str):
    """
    Divide uma data no formato 'YYYY-MM-DD HH:MM:SS' em dia, mês e ano.
    
    Args:
    date_str (str): A data a ser dividida.
    
    Returns:
    tuple: Contendo dia, mês e ano.
    """
    try:
        date = pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S', errors='raise')
        return date.day, date.month, date.year
    except ValueError:
        raise ValueError(f"Data inválida: {date_str}")


