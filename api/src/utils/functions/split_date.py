from api.src.utils.functions.format_date import format_date

def split_date(raw_date: str):
    formatted_date = format_date(raw_date)

    if '/' not in formatted_date:
        raise ValueError('Invalid format. Date must be: "DD/MM/YYYY"') 
        
    day, month, year = formatted_date.split('/')
    return day, month, year

