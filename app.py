from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades
from flask_httpauth import HTTPBasicAuth

auth =  HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


USUARIO = {
    'gabriel' : '12345',
    'Rafael' : '321'
}


@auth.verify_password
def verificacao(login, senha):
    print('vaidando usuario')
    print(USUARIO.get(login) == senha)
    if not (login, senha):
        return False

    return USUARIO.get(login) == senha

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):

        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()

            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada!'
            }

        return response


    def put(self, nome):
    
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json

            if 'nome' in dados:
                pessoa.nome = dados['nome']

            if 'idade' in dados:
                pessoa.idade = dados['idade']
            
            pessoa.save()

            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não foi possível atualizar o cadastro!'
            }

        return response
    

    def delete(self, nome): 

        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
            pessoa.delete()

            response = {
                    'status': 'Sucesso!',
                    'mensagem': mensagem
                }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não foi possível deleta o cadastro!'
            }

        return response

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):

        try:
            pessoas = Pessoas.query.all()
            response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não foi encontrado registro!'
            }

        return response
    
    def post(self):

        try:
            dados = request.json
            pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
            pessoa.save()

            response = {
                    'nome': pessoa.nome,
                    'idade': pessoa.idade,
                    'id': pessoa.id
                }

        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Não foi possível inserir registro!'
            }
    
        return response
    
class ListaAtividades(Resource):
    @auth.login_required
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]

        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        Atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        Atividade.save()

        response = {
            'id' : Atividade.id,
            'pessoa' : Atividade.pessoa.nome,
            'nome' : Atividade.nome 
        }

        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/listaPessoas/')
api.add_resource(ListaAtividades, '/atividades/')


if __name__ == '__main__':
    app.run(debug=True)