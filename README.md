# Cookbook API

**Cookbook API** é o back-end de um projeto de receitas culinárias, desenvolvido em Python (usando Flask, Flask-RESTful, Flask-JWT-Extended, SQLAlchemy, Flasgger, entre outros). A API permite criar, editar, listar e excluir receitas, gerenciar usuários e cadastros de avaliações (reviews). A autenticação é realizada via JWT e a documentação interativa está disponível com Swagger. O projeto utiliza o Redis para gerenciamento da blocklist dos tokens e pode ser executado via Docker.

---

## 🚀 Funcionalidades

- **Recipes Management:**  
  - Criar, editar, listar e excluir receitas.  
  - Cada receita contém nome, origem, categoria, URL da imagem, instruções de preparo, ingredientes (array de strings) e um flag para indicar se é pública.

- **User Authentication:**  
  - Cadastro, login e logout de usuários com autenticação JWT.

- **Reviews:**  
  - Cadastro, edição, visualização e exclusão de avaliações para as receitas.

- **Documentation:**  
  - Documentação interativa via Swagger, acessível em `/apidocs`.

- **Redis Integration:**  
  - Utilizado para gerenciar a blocklist dos tokens JWT.

- **Docker:**  
  - O projeto conta com um Dockerfile e um arquivo Docker Compose para facilitar a execução e orquestração dos containers.

---

## 🛠 Instruções de Instalação

Você pode configurar o ambiente para desenvolvimento local ou executar o projeto via Docker.

### 1. Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://docs.python.org/3/library/venv.html) (opcional, mas recomendado)
- [Git](https://git-scm.com/)
- [Redis](https://redis.io/download) – Importante: instale e inicie o Redis para que o sistema se conecte.
- (Opcional) [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)

---

### 2. Configuração para Desenvolvimento Local

#### a) Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd cookbook_api
```

#### b) Criar e Ativar o Ambiente Virtual

- No Linux/Mac:
```bash
python3 -m venv env
source env/bin/activate
```

- No Windows:
```bash
python -m venv env
.\env\Scripts\activate
```

#### c) Instalar as Dependências

Certifique-se de que o arquivo requirements.txt está na raiz do projeto. Em seguida, execute:
```bash
pip install -r requirements.txt
```

#### d) Iniciar a Aplicação

```bash
python run.py
```

A API ficará disponível em: http://localhost:5000
A documentação interativa via Swagger pode ser acessada em: http://localhost:5000/apidocs

### 3. Executando via Docker

#### a) Dockerfile

Certifique-se de ter o seguinte Dockerfile na raiz do projeto:
```bash
# Dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

WORKDIR /app

# Copia o arquivo de dependências e instala os pacotes
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . /app/

# Exponha a porta 5000
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
```

#### b) docker-compose.yml

Crie (ou verifique) o arquivo docker-compose.yml com o conteúdo abaixo:
```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=development
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

#### c) Construir e Iniciar os Containers

No terminal, execute:
```bash
docker-compose up --build
```

Após a construção, a aplicação ficará disponível em: http://localhost:5000
A documentação Swagger estará em: http://localhost:5000/apidocs

### Comandos Úteis

- Instalar dependências:
```bash
pip install -r requirements.txt
```

- Executar localmente:
```bash
python run.py
```

- Build e run com Docker Compose:
```bash
docker-compose up --build
```

- Parar os containers:
```bash
docker-compose down
```