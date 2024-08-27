'''
Aplicação do gerenciamento da Biblioteca.
'''


from typing import Final, Any
import os
import platform
from sqlite3 import Connection, IntegrityError

from src.db.conexao_db import get_conexao_db
from src.db.carga_db import carregar_banco_de_dados
from src.db.listar_livros import listar_livros
from src.db.livro_db import (
    get_livros_emprestado_count,
    get_livros_by_autor_nome,
    get_livro_by_titulo,
)
from src.db.emprestimo_db import (
   get_emprestimos_atrasados,
   get_emprestimo_by_id,
   update_emprestimo_devolucao,
)
from src.db.exemplar_db import (
   verificar_copias_disponiveis,
   update_exemplar,
)

from src.db.autor_db import (
    delete_autor,
    get_autor_by_nome,
)



COR_BRANCA: Final[str] = '\033[0;0m'
COR_BRIGHT_AMARELA: Final[str] = '\033[93m'
COR_VERDE: Final[str] = '\033[32m'
COR_BRIGHT_VERMELHA: Final[str] = '\033[91m'
LINHA_TRACEJADA: Final[str] = '-' * 31
LINHA_PONTILHADA: Final[str] = '-' * 61

OPCOES:  Final[dict[str, str ]] = {
    'C': 'Criação das Tabelas e  Inserção de Dados',
    '1': 'Listar todos os livros disponíveis',
    '2': 'Encontrar todos os livros emprestados no momento',
    '3': 'Localizar os livros escritos por um autor específico',
    '4': 'Verificar o número de cópias disponíveis de um determinado livro',
    '5': 'Mostrar os empréstimos em atraso',
    '6': 'Marcar um livro como devolvido',
    '7': 'Remover um autor',
    'S': 'Sair'    
}

OPCOES_SIM_NAO:  Final[dict[str, str ]] = {
    'S': 'Sim',    
    'N': 'Não',    
}

###########################################################
                  # INFRAESTRUTURA #
###########################################################

# Habilita os caracteres ANSI escape no terminal Windows.
os.system("")

def bright_amarelo(conteudo: Any) -> Any:
    '''
    Colore o texto informado em amarelo brilhante.
    Retorna o texto colorido.
    '''
    return f"{COR_BRIGHT_AMARELA}{conteudo}{COR_BRANCA}"

def verde(conteudo: Any) -> Any:
    '''
    Colore o texto informado em verde.
    Retorna o texto colorido.
    '''
    return f"{COR_VERDE}{conteudo}{COR_BRANCA}"

def bright_vermelho(conteudo: Any) -> Any:
    '''
    Colore o texto informado em vermelho brilhante.
    Retorna o texto colorido.
    '''
    return f"{COR_BRIGHT_VERMELHA}{conteudo}{COR_BRANCA}"

def limpar_console():
    '''
    Limpa o console de acordo com a plataforma.
    '''
    if platform.system() == 'Windows':
        os.system('cls')
    if platform.system() == 'Linux':
        os.system('clear')

def get_input(msg: str) -> str:
    '''
    Encapsula as chamadas dos inputs.
    Confecionda para poder testar os inputs.
    '''
    return input(msg)

def input_int(msg: str) -> int:
    '''
    Obtem número inteiro informado pelo usuário.
    Retorna o número.
    '''
    while True:
        try:
            return int(get_input(msg))
        except ValueError:
            print(bright_vermelho('\n\tApenas números inteiros são aceitos. Por favor, tente novamente.\n')) # pylint: disable=line-too-long

def input_opcoes(msg: str, opcoes: dict[str]) -> str:
    '''
    Obtem a opção válida.
    Retorna a opção.
    '''
    while True:
        opcao = get_input(msg).upper()
        if opcao in opcoes:
            return opcao
        print(f"\n\t'{bright_vermelho(opcao)}' opção inválida! As opções válidas são: {verde(', '.join(opcoes))}") # pylint: disable=line-too-long

def exibir_menu(opcoes: dict[str, str]) -> None:
    '''
    Exibi o menu de opções.
    '''
    print('')
    print(verde(f'\t{LINHA_TRACEJADA}'))
    cabecalho = 'MENU DE OPÇÕES \n'
    print(verde(cabecalho.center(50)))

    for key, value in opcoes.items():
        opcao = '|' + key + '|' + "  "  + value
        print(f"\t\t{verde(opcao)} ")
    print(verde(f'\t{LINHA_TRACEJADA}'))

def escolher_uma_opcao_do_menu_entrada(opcoes_menu_dict: dict[str, str]) -> str:
    '''
    Escolhe uma opção do menu.
    Retorna uma das opções do menu.
    '''
    exibir_menu(opcoes_menu_dict)
    siglas: list[str] = list(opcoes_menu_dict)
    escolher_opcao = input_opcoes('\n\tEntre com a opção desejada: ', siglas).upper() # pylint: disable=line-too-long
    while escolher_opcao not in siglas:
        escolher_opcao = input_opcoes(
            '\n\tEntre com a opção desejada: ',
             siglas
        ).upper()
    return escolher_opcao

######################################################
             # ENTRADA DE DADOS #
######################################################

def get_dado_str(msg_tipo_de_dado: str) -> str:
    '''
    obtem dado tipo str 
    Retorna o dado
    '''
    while True:
        tipo = get_input(f'\n\t{msg_tipo_de_dado}').lower()
        if tipo == '':
            print(bright_vermelho(f'\tValor inválido. O campo {tipo} deve ser preenchido.'))
        return tipo

def get_id(msg: str) -> int:
    '''
    obtem o id.
    Retorna id
    '''
    while True:
        identificacao = input_int(f'\n\t{msg}')
        if identificacao > 0:
            return identificacao
        print(bright_vermelho('\tValor  inválido. O identificador deve ser maior que zero.'))


######################################################
    # FUNÇÕES PARA EXIBIR RESULTADOS #
######################################################

def exibir_livro_escrito_por_autor( autor: str, livros: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''
    qtd = len(livros)
    if qtd > 1:
        print(bright_amarelo(f'\n\t{autor.capitalize()} possui {qtd} livros escritos na biblioteca:')) # pylint: disable=line-too-long
    else:
        print(bright_amarelo(f'\n\t{autor.capitalize()} possui {qtd} livro escrito na biblioteca:')) # pylint: disable=line-too-long

    for livro in livros:
        titulo = livro['titulo']
        print(bright_amarelo(f"\n\tLivro de título '{titulo}'"))

def exibir_emprestimos_em_atraso(emprestimos: list[dict[str, str]]) -> None:
    '''
    Exibe o resultado número de exemplares de um determinado livro.
    '''
    print(bright_amarelo('\n\tEmpréstimos em atraso:'))
    print(bright_amarelo("\n\t.................................................."))
    for emprestimo in emprestimos:
        identificado_emprestimo = emprestimo['id']
        usuario_nome = emprestimo['usuario_nome']
        titulo = emprestimo['livro_titulo']
        editora = emprestimo['editora_nome']
        identificado_exemplar = emprestimo['exemplar_id']
        data_emprestimo = emprestimo['data_emprestimo']
        data_para_devolucao = emprestimo['data_para_devolucao']
        data_devolucao = emprestimo['data_devolucao']

        print(bright_amarelo(f"\n\tEmpréstimo de identificação: |{identificado_emprestimo}|"))
        print(bright_amarelo(f"\n\tUsuário: {usuario_nome}"))
        print(bright_amarelo(f"\n\tTitulo: {titulo}"))
        print(bright_amarelo(f"\n\tEditora: {editora}"))
        print(bright_amarelo(f"\n\tData do empréstimo: {data_emprestimo}"))
        print(bright_amarelo(f"\n\tData para devolução: {data_para_devolucao}"))
        print(bright_amarelo(f"\n\tData de devolução: {data_devolucao if data_devolucao else '-'}"))
        print(bright_amarelo(f"\n\tExemplar de identificado: |{identificado_exemplar}|"))
        print(bright_amarelo("\n\t.................................................."))


######################################################
             # FUNCIONALIDADES DA APLICAÇÃO #
######################################################
def encontar_todos_livros_emprestados(conexao: Connection) -> list[dict[str, str]]:
    '''
    Obtem todos os livros emprestados no momento.
    '''
    livros = get_livros_emprestado_count(conexao)

    if not livros:
        print(bright_amarelo('\n\tSem Livros emprestados no momento.'))
        return

    print(bright_amarelo('\n\tLivros emprestados'))
    for livro in livros:
        titulo = livro['titulo']
        qtd = livro['qtd']
        if qtd > 1:
            print(bright_amarelo(f"\n\tO livro de título '{titulo}' possui {qtd} exemplares emprestados.")) # pylint: disable=line-too-long
        else:
            print(bright_amarelo(f"\n\tO livro de título '{titulo}' possui {qtd} exemplar emprestado.")) # pylint: disable=line-too-long

def localizar_livros_do_autor(conexao: Connection) -> list[dict[str, str]]:
    '''
    Localizar os livros escritos por um autor específico
    '''
    nome = get_dado_str("Nome do autor: ")
    livros = get_livros_by_autor_nome(conexao, nome)
    if livros:
        exibir_livro_escrito_por_autor(nome, livros)
    else:
        print(bright_vermelho(f"\n\t A biblioteca não possui livros do autor '{nome}'."))

def verificar_numero_de_exemplares_disponiveis_do_livro(
    conexao: Connection
) -> list[dict[str, str]]:
    '''
    Verifica o número de cópias disponíveis de um determinado livro
    '''
    titulo = get_dado_str("Título do livro: ")
    livro =  get_livro_by_titulo(conexao, titulo)
    if not livro:
        print(bright_vermelho(f'\n\t {titulo} não encontrado na base de dados.'))
    else:
        quantidade = verificar_copias_disponiveis(conexao, livro['id'])
        if quantidade > 1:
            print(bright_amarelo(f"\n\tO livro de título '{livro['titulo']}' possui {quantidade} exemplares disponíveis")) # pylint: disable=line-too-long
        else:
            print(bright_amarelo(f"\n\tO livro de título '{livro['titulo']}' possui {quantidade} exemplar disponível")) # pylint: disable=line-too-long

def mostrar_emprestimos_em_atraso(conexao: Connection)  -> list[dict[str, str]]:
    '''
    Mostra os empréstimos em atraso
    '''
    emprestimo = get_emprestimos_atrasados(conexao)
    exibir_emprestimos_em_atraso(emprestimo)

def devolver(conexao: Connection, identificacao_emprestimo: int) -> dict[str, Any]:
    '''
    Devolve o empréstimo  de id 
    Retorna o Emprestimo como DEVOLVIDO.
    '''
    emprestimo = get_emprestimo_by_id(conexao, identificacao_emprestimo)
    if not emprestimo:
        raise ValueError (bright_vermelho(f'\n\tO empréstimo de identificação |{identificacao_emprestimo}| não existe na base de dados'))  # pylint: disable=line-too-long
    if emprestimo['estado'] == 'DEVOLVIDO':
        raise ValueError (bright_vermelho("\n\tEmpréstimo já foi devolvido."))

    update_emprestimo_devolucao(
        conexao,
        identificacao= identificacao_emprestimo,
        estado='DEVOLVIDO',
    )
    update_exemplar(
        conexao,
        disponivel = 1,
        identificacao = emprestimo['exemplar_id'],
    )
    return get_emprestimo_by_id(conexao, identificacao_emprestimo)

def devolver_livro(conexao: Connection) -> dict[str, Any]:
    '''
    Marca um livro como devolvido
    '''
    try:
        identificacao = get_id("Identificação do empréstimo: ")
        devolver(conexao, identificacao)
        print(bright_amarelo(f'\n\tEmpréstimo de identificação |{identificacao}| Devolvido com sucesso!')) # pylint: disable=line-too-long
    except ValueError as erro:
        print(bright_vermelho(str(erro)))

def deletar_um_autor(conexao: Connection) -> dict[str, Any]:
    '''
    Remover um autor
    '''
    try:
        autor_nome = get_dado_str('\n\tNome do autor: ')
        autor = get_autor_by_nome(conexao, autor_nome)
        if not autor:
            raise ValueError(bright_vermelho(f"\n\tAutor {autor_nome} não cadastrado."))
        delete_autor(conexao, autor['id'])
        print(bright_amarelo(f'\n\tAutor {autor_nome} excluido com sucesso!'))
    except ValueError as erro:
        print(bright_vermelho(str(erro)))
    except IntegrityError:
        print(bright_vermelho(f"\n\tO autor {autor_nome} não pode ser excluído porque possui livros associados.")) # pylint: disable=line-too-long

###########################################################
                  # CARREGAR BANCO DE DAODS #
###########################################################
def carregar_db(conexao: Connection) -> None:
    '''
    Fluxo da carga do banco de dados.
    '''
    try:
        while True:
            opcao = escolher_uma_opcao_do_menu_entrada(OPCOES_SIM_NAO)
            if opcao == 'S':
                carregar_banco_de_dados(conexao)
                print(bright_amarelo('\n\tCarga da base de dados realizada com sucesso!'))
                break
            if opcao == 'N':
                break
    except Exception as erro:  # pylint: disable=broad-exception-caught
        print(bright_vermelho('\n\tNão foi possível realizar a carga da base de dados.'))
        print(bright_vermelho(f'\n\t{str(erro)}'))


###########################################################
                  # Biblioteca - DB #
###########################################################
def biblioteca_db() -> None:
    '''
    Fluxo Principal do Programa.
    '''
    try:
        conexao: Connection = get_conexao_db()
        limpar_console()
        print(verde('\t*** Biblioteca & Banco de Dados***\n '))
        while True:
            opcao = escolher_uma_opcao_do_menu_entrada(OPCOES)
            if opcao == 'C':
                carregar_db(conexao)
            if opcao == '1':
                print('\n\tListando todos os exemplares disponíveis...')
                listar_livros(conexao)
            if opcao == '2':
                encontar_todos_livros_emprestados(conexao)
            if opcao == '3':
                localizar_livros_do_autor(conexao)
            if opcao == '4':
                verificar_numero_de_exemplares_disponiveis_do_livro(conexao)
            if opcao == '5':
                mostrar_emprestimos_em_atraso(conexao)
            if opcao == '6':
                devolver_livro(conexao)
            if opcao == '7':
                deletar_um_autor(conexao)
            if opcao == "S":
                print(bright_amarelo('\n\tVocê saiu do sistema!'))
                break
    except Exception as erro:
        print('ERRO!!!')
        print(bright_vermelho(erro))
        raise erro
    finally:
        conexao.close()
