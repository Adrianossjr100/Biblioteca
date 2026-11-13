import sqlite3
from database import criar_tabelas
from models.livro import cadastrar_livro, listar_livros, buscar_livro
from models.usuario import cadastrar_usuario, listar_usuarios
from models.emprestimo import emprestar, devolver
from relatorios import resumo_acervo, livros_emprestados, atrasados
from utils import validar_cpf

def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número válido.")

def menu():
    print("""
===== BIBLIOTECA =====
1 - Cadastrar livro
2 - Listar livros
3 - Buscar livro
4 - Cadastrar usuário
5 - Listar usuários
6 - Emprestar livro
7 - Devolver livro
8 - Resumo do acervo
9 - Livros emprestados
10 - Atrasados
0 - Sair""")
    return input("Escolha: ").strip()

def main():
    criar_tabelas()
    while True:
        op = menu()
        try:
            if op == "1":
                cadastrar_livro(input("Título: "), input("Autor: "), input("ISBN: "),
                                ler_int("Ano: "), ler_int("Quantidade: "))
            elif op == "2":
                for id_, titulo, autor, total, disp in listar_livros():
                    print(f"[{id_}] {titulo} - {autor} ({disp}/{total} disponíveis)")
            elif op == "3":
                for l in buscar_livro(input("Título ou autor: ")):
                    print(l)
            elif op == "4":
                nome = input("Nome: ")
                cpf = input("CPF: ")
                while not validar_cpf(cpf):
                    print("CPF inválido! Digite 11 números (ex: 529.982.247-25).")
                    cpf = input("CPF: ")
                cadastrar_usuario(nome, cpf, input("Telefone: "), input("E-mail: "))
            elif op == "5":
                for id_, nome, cpf, tel in listar_usuarios():
                    print(f"[{id_}] {nome} - CPF {cpf} - {tel}")
            elif op == "6":
                emprestar(ler_int("ID do usuário: "), ler_int("ID do livro: "))
            elif op == "7":
                livros_emprestados()
                devolver(ler_int("ID do empréstimo: "))
            elif op == "8":
                resumo_acervo()
            elif op == "9":
                livros_emprestados()
            elif op == "10":
                atrasados()
            elif op == "0":
                print("Até logo!")
                break
            else:
                print("Opção inválida.")
        except sqlite3.IntegrityError:
            print("Erro: ISBN ou CPF já cadastrado.")

if __name__ == "__main__":
    main()