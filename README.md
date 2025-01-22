# mini-api
Atividade da Pós-graduação na UniFAP, uma mini-api em Flask.

## Requisitos

- [Python ^3.7](https://www.python.org/downloads/)

## Instruções

### Instalar Dependências

_(Opcional)_ Crie um ambiente virtual para instalar as dependências separadamente do seus outros projetos em Python:

  ```bash
  # Windows:
  python -m venv env
  .\env\Scripts\activate

  # Unix:
  python3 -m venv env
  source env/bin/activate
  ```

Agora, realize a instalação das dependências:

  ```bash
  pip install -r requirements.txt
  ```

### Executar Projeto

Rode o arquivo `migration.py` para criar o banco de dados (instance/database.db);

Com as tabelas criadas no seu ambiente, execute na raiz do projeto:
  
  ```bash
  flask --app app run
  # ou
  python -m flask --app app run
  ```

Pronto! A API estará disponível em [localhost:5000](localhost:5000)

## Rotas

1. POST - localhost:5000/usuarios
2. DELETE - localhost:5000/usuarios/{id}
3. GET - localhost:5000/postagens
4. POST - localhost:5000/postagens
