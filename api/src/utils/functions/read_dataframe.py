import pandas as pd
import os 

def read_dataframe(path: str):
    try:
        if not path:
            raise FileNotFoundError(f'File not found')

        file_extension = os.path.splitext(path.filename)[1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(path, dtype=str)    
        elif file_extension == '.xlsx':
            df = pd.read_excel(path, dtype=str)
             
        return df
    
    except Exception as e:
        print(f"An error has ocurred while reading path: {e}")
        return None