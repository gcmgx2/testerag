# Base Python image
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos essenciais primeiro para instalar dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o conteúdo do projeto para dentro do container
COPY . .

# Expõe a porta padrão do Uvicorn
EXPOSE 8000

# Define variável de ambiente para produção (opcional)
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
