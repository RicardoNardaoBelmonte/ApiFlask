# ApiFlask
Api contendo duas classes Autor e Postagem, fornecendo cadastro e postagens de autores e postagens.

## API de Autores e Postagens
Esta API foi desenvolvida utilizando o framework Flask e SQLAlchemy para realizar operações CRUD (Create, Read, Update, Delete) em duas entidades: Autor e Postagem. A API utiliza JWT para autenticação e PostgreSQL como banco de dados.

## Tecnologias Utilizadas
- Python 3.x
- Flask
- Flask-SQLAlchemy
- PostgreSQL (Supabase)
- JWT (JSON Web Tokens)

## Endpoints da API
- Autores
GET /autores Obtém a lista de todos os autores.

GET /autores/<int:id_autor>
Obtém um autor específico pelo seu ID.

POST /autores
Cria um novo autor.

PUT /autores/<int:id_autor>
Altera os dados de um autor.

DELETE /autores/<int:id_autor>
Exclui um autor pelo ID.

- Postagens
GET /
Obtém a lista de todas as postagens.

GET /postagem/<int:id_postagem>
Obtém uma postagem específica pelo ID.

POST /postagem
Cria uma nova postagem.

PUT /postagem/<int:id_postagem>
Altera os dados de uma postagem existente.

DELETE /postagem/<int:id_postagem>
Exclui uma postagem pelo ID.

- Autenticação
A autenticação na API é feita via JWT. Para obter um token, faça login com as credenciais de um autor no endpoint /login.

POST /login
Realiza o login e retorna um token JWT.

Após obter o token, inclua-o nos headers de requisições protegidas utilizando o campo x-access-token.

## Configuração do Banco de Dados
A API usa o banco de dados PostgreSQL hospedado no Supabase. Para configurar o banco de dados, o código já inclui a função inicializar_banco(), que cria as tabelas Autor e Postagem.7

Configure a variável de ambiente SQLALCHEMY_DATABASE_URI para a URL de conexão do seu banco de dados PostgreSQL.

# Dependências 
Instale no terminal o arquivo requirements.txt lá tera todas as dependências que você ira precisar para rodar a API

```bash
pip install -r requirements.txt
