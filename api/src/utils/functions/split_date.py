def split_date(raw_date: str):
    if '/' not in raw_date:
        raise ValueError('Invalid format. Date must be: "DD/MM/YYYY"') 
        
    day, month, year = raw_date.split('/')
    return day, month, year

