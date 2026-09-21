import pandas as pd
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError



def extract_data(file_path):

    try:
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.lower()
        return data
    
    except FileNotFoundError:
        logging.error(f"Error: The file at {file_path} was not found.")
        return None


    
def clean_cost_and_sale_amount(df):

    if df is None:
        logging.error("Error: No data to clean.")
        return None

    columns_replace = ['cost','sale_amount']

    for col in columns_replace:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r'[^\d.,-]', '', regex=True)  
                .str.replace(',', '', regex=False)          
                .replace('', pd.NA)                         
                .astype(float)
            )
        else:
            logging.warning(f"Warning: Column '{col}' not found in DataFrame.")

    return df

def clean_ad_date(df):
    # 1. Padroniza todos os separadores para hífen '-' em toda a coluna
    # NaN vira 'nan' string e é convertido para NaT pelo errors='coerce'
    ad_date_clean = df['ad_date'].astype(str).str.replace('/', '-', regex=False)

    # 2. Tenta fazer a conversão rápida dos dois padrões principais (AAAA-MM-DD e DD-MM-AAAA)
    s1 = pd.to_datetime(ad_date_clean, format='%Y-%m-%d', errors='coerce')
    s2 = pd.to_datetime(ad_date_clean, format='%d-%m-%Y', errors='coerce')

    # 3. Preenche as lacunas combinando as conversões
    df['ad_date'] = s1.fillna(s2)

    # 4. (Opcional - Fallback) Se ainda sobrar algum formato exótico que virou NaT,
    # usa o parâmetro 'mixed' do Pandas 2.0+ apenas nas linhas restantes:
    if df['ad_date'].isna().any():
        mask = df['ad_date'].isna()
        df.loc[mask, 'ad_date'] = pd.to_datetime(
            ad_date_clean[mask], 
            format='mixed', 
            dayfirst=True, 
            errors='coerce'
        )

    n_nat = df['ad_date'].isna().sum()
    if df['ad_date'].isna().all():
        raise ValueError("Nenhuma data convertida — verificar formatos em clean_ad_date")
    if n_nat > 0:
        logging.warning(f"{n_nat} datas não convertidas (NaT)")

    return df


def convert_columns_to_numeric(df):

    if df is None:
        logging.error("Error: No data to convert columns.")
        return None
    
    columns_convert = ['clicks', 'impressions', 'leads', 'conversions']

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
        df = drop_columns(df, ['conversion rate'])
        logging.info("Data cleaning completed successfully.")
    else:
        logging.error("Data cleaning failed due to extraction error.")

    return df



def load_data(df, table_name, engine):
    if df is None:
        logging.error("Error: No data to load.")
        return None
    try:
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name}"))
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        logging.info(f"Data loaded successfully into table '{table_name}'.")
    except SQLAlchemyError as e:
        logging.error(f"Error loading data into database: {e}")
        return None


def main_data(file_path,table_name,engine):
    
    df = extract_data(file_path)
    df = clean_data(df)
    load_data(df,table_name,engine)

    return df