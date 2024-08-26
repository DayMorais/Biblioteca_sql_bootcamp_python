from sqlite3 import Connection

def listar_livros (conexao: Connection):
    cursor = conexao.cursor()
    lista = cursor.execute(f'SELECT titulo FROM livros INNER JOIN exemplares ON livros.id = exemplares.livro_id WHERE disponivel IS 1')
    
    for livro in lista:
        print (livro)
