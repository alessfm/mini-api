from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from migration import User, Post
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()

# Buscar Postagens
@app.route("/postagens", methods=["GET"])
def getUsersWithPosts():
  try:
    stmt = db.select(User).order_by(User.name)
    busca = db.session.execute(stmt).scalars().all()

    usuarios = []
    for usuario in busca:
      u = usuario.to_json()
      
      stmt = db.select(Post.title).where(Post.user_id == u["id"]).order_by(Post.created_at)
      postagens = db.session.execute(stmt).scalars().all()
      
      usuarios.append({"user": u["nome"], "posts": postagens if len(postagens) else "Nenhuma postagem"})
    
    return mensagem(201, None, usuarios)
  except Exception as e:
    print("Erro: ", e)
    return mensagem(404, "Nenhuma postagem encontrada")

# Criar Usuário
@app.route("/usuarios", methods=["POST"])
def addUser():
  body = request.get_json()

  try:
    db.one_or_404(db.select(User).filter_by(email=body["email"]))
    return mensagem(401, "E-mail já cadastrado")
  except:
    usuario = User(
      name = body["nome"], 
      email = body["email"]
    )

    try:
      db.session.add(usuario)
      db.session.commit()
      return mensagem(201, "Criado com sucesso")
    except Exception as e:
      print("Erro: ", e)
      return mensagem(400, "Erro no cadastro")


# Criar Postagem
@app.route("/postagens", methods=["POST"])
def addPost():
  body = request.get_json();

  try:
    db.get_or_404(User, body["idUsuario"])
  except Exception as e:
    print("Erro: ", e)
    return mensagem(404, "Usuário não encontrado")

  postagem = Post(
    user_id = body["idUsuario"], 
    title = body["titulo"], 
    content = body["conteudo"]
  )

  try:
    db.session.add(postagem)
    db.session.commit()
    return mensagem(201, "Criada com sucesso")
  except Exception as e:
    print("Erro: ", e)
    return mensagem(400, "Erro no cadastro")


# Deletar Usuário
@app.route("/usuarios/<int:id>", methods=["DELETE"])
def deleteUser(id):
  try:
    usuario = db.get_or_404(User, id)
  except Exception as e:
    print("Erro: ", e)
    return mensagem(404, "Usuário não encontrado")

  try:
    db.session.delete(usuario)
    db.session.commit()
    return mensagem(201, "Deletado com sucesso")
  except Exception as e:
    print("Erro: ", e)
    return mensagem(400, "Erro na exclusão")


# Formatar Response
def mensagem(status:int, msg:str, conteudo={}) -> Response:
  body = {}
  body["retorno"] = conteudo
  body["mensagem"] = msg
  return Response(json.dumps(body), status=status, mimetype="application/json")