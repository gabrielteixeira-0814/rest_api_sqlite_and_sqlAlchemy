from models import Pessoas

def insere_pessoas():
    pessoa = Pessoas(nome='Daniel', idade=26)
    pessoa.save()
    print(pessoa)

def consulta_pessoa():
    pessoa = Pessoas.query.all()
    # pessoa = Pessoas.query.filter_by(nome='Gabriel').first()
    print(pessoa)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Gabriel').first()
    pessoa.idade = 10
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Daniel').first()
    pessoa.delete()


if __name__ == '__main__':
    # insere_pessoas()
    # altera_pessoa()
    exclui_pessoa()
    consulta_pessoa()