# API Gerenciador de Finanças

API REST desenvolvida com **FastAPI** para gerenciamento financeiro pessoal. O projeto permite cadastrar, listar, atualizar e remover movimentações financeiras, utilizando **SQLite** como banco de dados e autenticação **HTTP Basic**.

## Tecnologias Utilizadas

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Docker
* Docker Compose

---

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* Docker
* Docker Compose

Verifique as instalações:

```bash
docker --version
docker-compose --version
```

---

## Clonando o Repositório

Clone o projeto para sua máquina:

```bash
git clone https://github.com/JoaoHardman/Gerenciador_de_financas.git
```

Acesse o diretório do projeto:

```bash
cd Gerenciador_de_financas
```

---

## Executando a Aplicação com Docker Compose

### 1. Construir e iniciar os contêineres

Execute o comando abaixo para construir as imagens e iniciar os serviços em segundo plano:

```bash
docker-compose up --build -d
```

Após a execução, a API estará disponível em:

```text
http://localhost:8000
```

---

### 2. Acessar a documentação automática

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

### 3. Verificar os logs da aplicação

Para acompanhar os logs em tempo real:

```bash
docker-compose logs -f
```

---

### 4. Parar os contêineres

Para interromper a execução dos serviços:

```bash
docker-compose down
```

---

### 5. Reconstruir a aplicação após alterações

Caso realize mudanças no código:

```bash
docker-compose up --build -d
```

---

## Autenticação

A API utiliza autenticação HTTP Basic.

Credenciais padrão:

```text
Usuário: admin
Senha: admin
```

---

## Endpoints Disponíveis

### Listar movimentações

```http
GET /movimentacoes
```

### Cadastrar movimentação

```http
POST /movimentacoes
```

Exemplo de corpo da requisição:

```json
{
  "descricao": "Salário",
  "valor": 5000,
  "tipo": "receita",
  "categoria": "Trabalho"
}
```

### Atualizar movimentação

```http
PUT /movimentacoes/{id}
```

### Remover movimentação

```http
DELETE /movimentacoes/{id}
```

---

## Estrutura do Projeto

```text
.
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── financas.db
└── README.md
```

---

## Autor

João Pedro

GitHub: https://github.com/JoaoHardman
