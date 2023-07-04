from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas

app = Flask(__name__)
api = Api(app)


class Pessoa(Resource):
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


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/listaPessoas/')


if __name__ == '__main__':
    app.run(debug=True)