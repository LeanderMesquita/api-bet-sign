import pandas as pd
import os 

def read_dataframe(path: str):
    try:
        if not path:
            raise FileNotFoundError(f'Arquivo não encontrado')

        file_extension = os.path.splitext(path)[1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(path, dtype=str)    
        elif file_extension == '.xlsx':
            df = pd.read_excel(path, dtype=str)
             
        return df
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None