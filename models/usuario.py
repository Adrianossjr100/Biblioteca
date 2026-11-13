from database import conectar

from utils import validar_cpf, limpar_cpf

def cadastrar_usuario(nome, cpf, telefone, email):
    if not validar_cpf(cpf):
        print("CPF inválido! Usuário não cadastrado.")
        return
    cpf = limpar_cpf(cpf)
    with conectar() as conn:
        conn.execute(
            "INSERT INTO usuarios (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)",
            (nome, cpf, telefone, email),
        )
    print(f"Usuário '{nome}' cadastrado!")

def listar_usuarios():
    with conectar() as conn:
        return conn.execute(
            "SELECT id, nome, cpf, telefone FROM usuarios ORDER BY nome"
        ).fetchall()

def buscar_usuario(termo):
    with conectar() as conn:
        return conn.execute(
            "SELECT id, nome, cpf FROM usuarios WHERE nome LIKE ? OR cpf = ?",
            (f"%{termo}%", termo),
        ).fetchall()

def remover_usuario(usuario_id):
    with conectar() as conn:
        aberto = conn.execute(
            "SELECT 1 FROM emprestimos WHERE usuario_id = ? AND data_devolucao IS NULL",
            (usuario_id,),
        ).fetchone()
        if aberto:
            print("Não dá para remover: o usuário tem livro emprestado.")
            return
        conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    print("Usuário removido.")