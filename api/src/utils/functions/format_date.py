from datetime import datetime

def format_date(raw_date:str) -> str:
    """ raw -> str -> datetime -> format -> str"""
    try:
        return str(datetime.strptime(str(raw_date), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y'))
    except ValueError as e:
        print(e)

