import pandas as pd
import logging
from sqlalchemy import create_engine



def extract_data(file_path):

    try:
        data = pd.read_csv(file_path)
        return data
    
    except FileNotFoundError:
        logging.error(f"Error: The file at {file_path} was not found.")
        return None


    
def clean_cost_and_sale_amount(df):

    if df is None:
        logging.error("Error: No data to clean.")
        return None

    coluns_replace = ['Cost','Sale_Amount']

    for col in coluns_replace:
        if col in df.columns:
            df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
        else:
            logging.warning(f"Warning: Column '{col}' not found in DataFrame.")

    return df

def clean_ad_date(df):
    # 1. Padroniza todos os separadores para hífen '-' em toda a coluna
    ad_date_clean = df['Ad_Date'].astype(str).str.replace('/', '-', regex=False)

    # 2. Tenta fazer a conversão rápida dos dois padrões principais (AAAA-MM-DD e DD-MM-AAAA)
    s1 = pd.to_datetime(ad_date_clean, format='%Y-%m-%d', errors='coerce')
    s2 = pd.to_datetime(ad_date_clean, format='%d-%m-%Y', errors='coerce')

    # 3. Preenche as lacunas combinando as conversões
    df['Ad_Date'] = s1.fillna(s2)

    # 4. (Opcional - Fallback) Se ainda sobrar algum formato exótico que virou NaT,
    # usa o parâmetro 'mixed' do Pandas 2.0+ apenas nas linhas restantes:
    if df['Ad_Date'].isna().any():
        mask = df['Ad_Date'].isna()
        df.loc[mask, 'Ad_Date'] = pd.to_datetime(
            ad_date_clean[mask], 
            format='mixed', 
            dayfirst=True, 
            errors='coerce'
        )

    return df



def convert_columns_to_numeric(df):

    if df is None:
        logging.error("Error: No data to convert columns.")
        return None
    
    columns_convert = ['Clicks', 'Impressions', 'Leads', 'Conversions']

    for col in columns_convert:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            logging.warning(f"Warning: Column '{col}' not found in DataFrame.")


    return df


def drop_columns(df, columns_to_drop):
    if df is None:
        logging.error("Error: No data to drop columns from.")
        return None

    for col in columns_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col])
        else:
            logging.warning(f"Warning: Column '{col}' not found in DataFrame.")

    return df


def clean_data(df):

    if df is not None:
        df = clean_cost_and_sale_amount(df)
        df = clean_ad_date(df)
        df = convert_columns_to_numeric(df)
        df = drop_columns(df, ['Conversion Rate'])
        logging.info("Data cleaning completed successfully.")
    else:
        logging.error("Data cleaning failed due to extraction error.")

    return df



def load_data(df,table_name,engine):

    if df is None:
        logging.error("Error: No data to load.")
        return None

    try:
        df.to_sql( 
                name=table_name, 
                con=engine, 
                if_exists='replace', 
                index=False
        )
        logging.info(f"Data loaded successfully into table '{table_name}'.")

    except Exception as e:
        logging.error(f"Error loading data into database: {e}")
        return None


def main_data(file_path,table_name,engine):
    
    # 1. Extract
    df = extract_data(file_path)

    # 2. Clean
    df = clean_data(df)

    # 3. Load
    load_data(df,table_name,engine)