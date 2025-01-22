from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

with app.app_context():
  class User(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      name = db.Column(db.String(150), nullable = False)
      email = db.Column(db.String(100), unique = True, nullable = False)
      created_at = db.Column(db.DateTime(timezone = True), server_default = func.now())
      posts = db.relationship("Post", backref="user", cascade = "all, delete")

      def __repr__(self):
          return f"<User {self.name}>"


  class Post(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
      title = db.Column(db.String(50))
      content = db.Column(db.Text)
      created_at = db.Column(db.DateTime(timezone = True), server_default = func.now())

      def __repr__(self):
          return f"<Post {self.title}>"


  db.drop_all()
  db.create_all()