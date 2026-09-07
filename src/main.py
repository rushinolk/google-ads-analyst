import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging
from etl_pipeline import main_data


load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "postgres_db")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB")



file_path = "data/GoogleAds_DataAnalytics_Sales_Uncleaned.csv"
table_name = "staging_ads"

# Cria a engine usando as variaveis do container
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

# Configurando o logging

console_handler = logging.StreamHandler()

# 2. Configura para mandar para o arquivo
file_handler = logging.FileHandler('log/pipeline.log', encoding='utf-8')

#logging configuration
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[console_handler, file_handler]
)


main_data(file_path,table_name,engine)

# Comentario para corrigir push