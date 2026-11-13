from datetime import date, timedelta
from database import conectar
from config import PRAZO_DIAS, MULTA_POR_DIA, LIMITE_LIVROS_POR_USUARIO

def calcular_multa(data_prevista, data_devolucao):
    atraso = (data_devolucao - data_prevista).days
    return max(0, atraso) * MULTA_POR_DIA

def emprestar(usuario_id, livro_id):
    with conectar() as conn:
        livro = conn.execute(
            "SELECT titulo, qtd_disponivel FROM livros WHERE id = ?", (livro_id,)
        ).fetchone()
        if not livro:
            print("Livro não encontrado.")
            return
        if livro[1] <= 0:
            print(f"Sem exemplares disponíveis de '{livro[0]}'.")
            return

        abertos = conn.execute(
            "SELECT COUNT(*) FROM emprestimos WHERE usuario_id = ? AND data_devolucao IS NULL",
            (usuario_id,),
        ).fetchone()[0]
        if abertos >= LIMITE_LIVROS_POR_USUARIO:
            print("Usuário atingiu o limite de empréstimos.")
            return

        hoje = date.today()
        prevista = hoje + timedelta(days=PRAZO_DIAS)
        conn.execute(
            """INSERT INTO emprestimos (usuario_id, livro_id, data_emprestimo, data_prevista)
               VALUES (?, ?, ?, ?)""",
            (usuario_id, livro_id, hoje.isoformat(), prevista.isoformat()),
        )
        conn.execute(
            "UPDATE livros SET qtd_disponivel = qtd_disponivel - 1 WHERE id = ?", (livro_id,)
        )
    print(f"'{livro[0]}' emprestado! Devolver até {prevista.strftime('%d/%m/%Y')}.")

def devolver(emprestimo_id, data_devolucao=None):
    data_devolucao = data_devolucao or date.today()
    with conectar() as conn:
        emp = conn.execute(
            "SELECT livro_id, data_prevista FROM emprestimos WHERE id = ? AND data_devolucao IS NULL",
            (emprestimo_id,),
        ).fetchone()
        if not emp:
            print("Empréstimo não encontrado ou já devolvido.")
            return

        prevista = date.fromisoformat(emp[1])
        multa = calcular_multa(prevista, data_devolucao)
        conn.execute(
            "UPDATE emprestimos SET data_devolucao = ?, multa = ? WHERE id = ?",
            (data_devolucao.isoformat(), multa, emprestimo_id),
        )
        conn.execute(
            "UPDATE livros SET qtd_disponivel = qtd_disponivel + 1 WHERE id = ?", (emp[0],)
        )
    if multa > 0:
        print(f"Devolvido com atraso. Multa: R$ {multa:.2f}")
    else:
        print("Devolvido no prazo. Sem multa!")