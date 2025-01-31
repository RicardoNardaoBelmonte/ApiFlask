from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

#criar uma api flask

app = Flask(__name__)

#criar uma instancia SQLalchemy
app.config['SECRET_KEY'] = 'Ric@rdo#19'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
db:SQLAlchemy

#definir estrutura postagem
class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))

#definir estrutura autor
class Autor (db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')

#comando para criar banco de dadosQQ


#criando usuario Autor
def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        autor = Autor(nome = 'Ricardo', email = 'nardaoricardo@gmail.com', senha = '123', admin = True)
        db.session.add(autor)
        db.session.commit()

if __name__ == '__main__':
    inicializar_banco()