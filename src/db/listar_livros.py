'''
Módulo Listar livros
'''

from sqlite3 import Connection

def listar_livros (conexao: Connection):
    '''
    Listar livros
    '''
    cursor = conexao.cursor()
    lista = cursor.execute('SELECT titulo FROM livros INNER JOIN exemplares ON livros.id = exemplares.livro_id WHERE disponivel IS 1') # pylint: disable=line-too-long

    for livro in lista:
        print (livro)
