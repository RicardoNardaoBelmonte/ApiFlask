from flask import Flask, jsonify, request, make_response
from EstruturaApi import Autor, Postagem, app, db
import jwt
from datetime import datetime, timedelta 
from functools import wraps

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token nao foi incluido'}, 401)
        try:
            resultado = jwt.decode(token,app.config['SECRET_KEY'], algorithms=['HS256'])
            autor = Autor.query.filter_by(id_autor= resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token invalido'},401)
        return f(autor,  *args, **kwargs)
    return decorated

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic Realm=:"login obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario: 
        return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic Realm=:"login obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic Realm=:"login obrigatório"'})


#endpoints para classe Postagem
@app.route('/')
@token_obrigatorio
def obter_postagens(autor):
    postagem  = Postagem.query.all()
    lista_de_postagens = []
    for postagens in postagem:
        postagem_atual = {}
        postagem_atual['id_postagem'] = postagens.id_postagem
        postagem_atual['titulo'] = postagens.titulo
        postagem_atual['id_autor'] = postagens.id_autor
        lista_de_postagens.append(postagem_atual)
    
    return jsonify({'Postagens': lista_de_postagens})

@app.route('/postagem/<int:id_postagem>', methods = ['GET'])
@token_obrigatorio
def obter_postagem_por_indice(autor,id_postagem):
    postagem_existente = Postagem.query.filter_by(id_postagem = id_postagem).first()
    if not postagem_existente:
        return jsonify({'mensagem': 'Postagem não encontrada!'})
    postagem_atual = {}
    postagem_atual['id_postagem'] = postagem_existente.id_postagem
    postagem_atual['titulo'] = postagem_existente.titulo
    postagem_atual['id_autor'] = postagem_existente.id_autor

    return jsonify({'Postagem': postagem_atual})


@app.route('/postagem', methods = ['POST'])
@token_obrigatorio
def nova_postagem(autor):
    postagem = request.get_json()
    nova_postagem = Postagem(id_postagem = postagem['id_postagem'], titulo= postagem['titulo'], id_autor = postagem['id_autor'])
    db.session.add(nova_postagem)
    db.session.commit()
    return jsonify({'mensagem':'Postagem criada com sucesso!'}, 200)

@app.route('/postagem/<int:id_postagem>', methods = ['PUT'])
@token_obrigatorio
def alterar_postagem(autor,id_postagem):
    postagem_para_alterar = request.get_json()
    postagem_existente = Postagem.query.filter_by(id_postagem = id_postagem).first()
    if not postagem_existente:
        return jsonify({'mensagem': 'Postagem não encontrada!'})
    try:
        if postagem_para_alterar['id_postagem']:
            postagem_existente.id_postagem = postagem_para_alterar['id_postagem']
    except:
        pass
    try:
        if postagem_para_alterar['titulo']:
            postagem_existente.titulo = postagem_para_alterar['titulo']
    except:
        pass
    try:
        if postagem_para_alterar['id_autor']:
            postagem_existente.id_autor = postagem_para_alterar['id_autor']
    except:
        pass
    db.session.commit()
    return jsonify({'mensagem': 'Postagem alterada com sucesso!'}, 200)

@app.route('/postagem/<int:id_postagem>', methods= ['DELETE'])
@token_obrigatorio
def excluir_postage(autor,id_postagem):
    Postagem_existente = Postagem.query.filter_by(id_postagem = id_postagem).first()
    if not Postagem_existente:
        return jsonify({'mensagem': 'Postagem não encontrada!'})
    db.session.delete(Postagem_existente)
    db.session.commit()
    return jsonify({'mensagem': 'Postagem excluida com sucesso!'}, 200)

#endpoints para classe Autor
@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor   
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)

    return jsonify({'Autores': lista_de_autores})

@app.route('/autores/<int:id_autor>', methods = ['GET'])
@token_obrigatorio
def obter_autor_por_id(autor,id_autor):
   autor =  Autor.query.filter_by(id_autor = id_autor).first()
   if not autor:
       return jsonify({'Mensagem': 'Autor nao encontrado'})
   autor_atual = {}
   autor_atual['id_autor'] = autor.id_autor   
   autor_atual['nome'] = autor.nome
   autor_atual['email'] = autor.email

   return jsonify({'Autor': autor_atual})

@app.route('/autores', methods = ['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor =  request.get_json()
    autor = Autor(nome= novo_autor['nome'],senha= novo_autor['senha'], email= novo_autor['email'] )
    db.session.add(autor)
    db.session.commit()
    return jsonify({'mensagem': 'Usuario criado com sucesso'}, 200)

@app.route('/autores/<int:id_autor>', methods = ['PUT'])
@token_obrigatorio
def alterar_autor(autor,id_autor):
    usuario_para_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor =  id_autor).first()
    if not autor:
        return jsonify({'mensagem': 'Autor nao encontrado'}, 404)
    try:
        if usuario_para_alterar['nome']:
            autor.nome = usuario_para_alterar['nome']
    except:
        pass
    try:
        if usuario_para_alterar['email']:
            autor.email = usuario_para_alterar['email']
    except:
        pass
    try:
        if usuario_para_alterar['senha']:
            autor.senha = usuario_para_alterar['senha']
    except:
        pass
    
    db.session.commit()
    return jsonify({'mensagem': 'Usuario alterado com sucesso'}, 200)

@app.route('/autores/<int:id_autor>', methods = ['DELETE'])
@token_obrigatorio
def excluir_autor(autor,id_autor):
    autor = Autor.query.filter_by(id_autor = id_autor).first()
    if not autor:
        return jsonify({'mensagem': 'Autor não encontrado!'})
    
    db.session.delete(autor)
    db.session.commit()
    return jsonify({'mensagem': 'Autor excluido com sucesso!'}, 200)


app.run(port=5000, host='localhost', debug=True)

