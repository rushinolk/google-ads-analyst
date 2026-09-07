FROM python:3.13.15

WORKDIR /app

# Copia e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY . .

# Executa o ponto de entrada principal
CMD ["python", "src/main.py"]