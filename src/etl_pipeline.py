import pandas as pd
import logging



def extract_data(file_path):

    try:
        data = pd.read_csv(file_path)
        return data
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None


    
def clean_cost_and_sale_amount(df):

    if df is None:
        print("Error: No data to clean.")
        return None

    coluns_replace = ['Cost','Sale_Amount']

    for col in coluns_replace:
        if col in df.columns:
            df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")

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
    columns_convert = ['Clicks', 'Impressions', 'Leads', 'Conversions']
    for col in columns_convert:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")


    return df


def drop_columns(df, columns_to_drop):
    if df is None:
        print("Error: No data to drop columns from.")
        return None

    for col in columns_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col])
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")

    return df


def clean_data(file_path):

    df = extract_data(file_path)

    if df is not None:
        df = clean_cost_and_sale_amount(df)
        df = clean_ad_date(df)
        df = convert_columns_to_numeric(df)
        df = drop_columns(df, ['Conversion Rate'])
    return df


def load_data(df,table_name, engine):

    if df is None:
        print("Error: No data to load.")
        return None

    try:
        df.to_sql( 
                name=table_name, 
                con=engine, 
                if_exists='replace', 
                index=False
        )

    except Exception as e:
        print(f"Error loading data into database: {e}")
        return None


