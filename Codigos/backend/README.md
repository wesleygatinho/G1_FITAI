# FitAI - Backend

Este é o backend do projeto FitAI, uma API RESTful desenvolvida com FastAPI para fornecer todos os serviços necessários para o aplicativo móvel. A API é responsável pelo gerenciamento de usuários, autenticação, registro de progresso, análise de exercícios com IA e muito mais.

## 🌟 Funcionalidades

* **Autenticação de Usuários**: Sistema completo de registro e login com tokens JWT.
* **Gerenciamento de Usuários**: Endpoints para ler e atualizar informações do usuário.
* **Análise de Exercícios com IA**: Processamento de vídeo em tempo real para contar repetições e fornecer feedback sobre a execução de exercícios como agachamentos, flexões e rosca martelo.
* **Registro de Progresso**: Salve o histórico de peso, medidas corporais e sessões de cardio.
* **Sessões de Treino**: Guarde um histórico detalhado de todas as sessões de treino, incluindo os exercícios realizados.
* **Gerador de Dicas e Planos com IA**: Utilize a API do Google Gemini para gerar dicas de fitness e planos de treino personalizados.
* **Gerenciamento de Exercícios**: Endpoints para listar exercícios e obter instruções detalhadas.

## 🛠️ Tecnologias Utilizadas

* **Framework**: FastAPI
* **Banco de Dados**: PostgreSQL com SQLAlchemy
* **Segurança**: `passlib[bcrypt]` para hashing de senhas e `python-jose[cryptography]` para tokens JWT.
* **Visão Computacional**: OpenCV e MediaPipe para análise de pose.
* **Inteligência Artificial**: `google-generativeai` para geração de conteúdo.
* **Validação de Dados**: Pydantic
* **Servidor ASGI**: Uvicorn

## 🚀 Começando

Siga estas instruções para configurar e executar o projeto localmente.

### Pré-requisitos

* Python 3.9+
* PostgreSQL
* Um ambiente virtual (recomendado)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/wesleygatinho/G1_FITAI.git
    cd G1_FITAI/Codigos/backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Windows, use: .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz da pasta `backend` e adicione as seguintes variáveis:
    ```env
    DATABASE_URL="postgresql://seu_usuario:sua_senha@localhost/fitai_db"
    SECRET_KEY="sua_chave_secreta_super_longa_e_segura"
    GOOGLE_API_KEY="sua_chave_da_api_do_google"
    ```
    Certifique-se de que o banco de dados `fitai_db` exista no seu servidor PostgreSQL.

### Executando o Servidor

Com o ambiente virtual ativado e as variáveis de ambiente configuradas, execute o seguinte comando:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em ```http://localhost:8000```. A documentação interativa (Swagger UI) pode ser acessada em ```http://localhost:8000/docs```.

## 📁 Estrutura do Projeto

* ```app/api/v1/```: Contém os roteadores e endpoints da API.
* ```app/core/```: Configurações, segurança e lógica de banco de dados.
* ```app/models/```: Modelos de tabelas do SQLAlchemy.
* ```app/schemas/```: Schemas do Pydantic para validação de dados.
* ```app/services/```: Lógica de negócio (CRUD, serviços de IA, etc.).
* ```exercises/```: Módulos para a lógica de análise de cada exercício.
* ```main.py```: Ponto de entrada da aplicação FastAPI.

## 📄 Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [README.md](#https://github.com/wesleygatinho/G1_FITAI) na raiz do projeto para mais detalhes.

## 🧑‍💻 Autores

* **André Luis Aguiar do Nascimento**
* **Hugo Samuel de Lima Oliveira**
* **Leonardo Sampaio Serra**
* **Lucas Emanoel Amaral Gomes**
* **Wesley dos Santos Gatinho**