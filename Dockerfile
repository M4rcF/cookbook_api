# Use uma imagem base oficial leve do Python
FROM python:3.10-slim

# Variável para desabilitar o buffer do Python (útil para logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Defina variáveis de ambiente para o Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Crie e defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências para o container
COPY requirements.txt /app/

# Atualize o pip e instale as dependências sem cache
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o container
COPY . /app/

# Exponha a porta 5000 (porta padrão do Flask)
EXPOSE 5000

# Comando para iniciar o servidor Flask, ouvindo em todas as interfaces
CMD ["flask", "run", "--host=0.0.0.0"]
