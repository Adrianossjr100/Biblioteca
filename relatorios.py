from datetime import date
from database import conectar
from models.emprestimo import calcular_multa

def resumo_acervo():
    with conectar() as conn:
        titulos, total, disponiveis = conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(qtd_total),0), COALESCE(SUM(qtd_disponivel),0) FROM livros"
        ).fetchone()
    print(f"Títulos: {titulos} | Exemplares: {total} | "
          f"Disponíveis: {disponiveis} | Emprestados: {total - disponiveis}")

def livros_emprestados():
    with conectar() as conn:
        linhas = conn.execute("""
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_prevista
            FROM emprestimos e
            JOIN livros l   ON l.id = e.livro_id
            JOIN usuarios u ON u.id = e.usuario_id
            WHERE e.data_devolucao IS NULL
            ORDER BY e.data_prevista
        """).fetchall()
    if not linhas:
        print("Nenhum livro emprestado.")
    for emp_id, titulo, nome, saiu, prevista in linhas:
        print(f"[{emp_id}] '{titulo}' com {nome} | desde {saiu} | devolver até {prevista}")

def atrasados():
    hoje = date.today()
    with conectar() as conn:
        linhas = conn.execute("""
            SELECT l.titulo, u.nome, u.telefone, e.data_prevista
            FROM emprestimos e
            JOIN livros l   ON l.id = e.livro_id
            JOIN usuarios u ON u.id = e.usuario_id
            WHERE e.data_devolucao IS NULL AND e.data_prevista < ?
        """, (hoje.isoformat(),)).fetchall()
    if not linhas:
        print("Nenhum atraso. 👍")
    for titulo, nome, tel, prevista in linhas:
        multa = calcular_multa(date.fromisoformat(prevista), hoje)
        print(f"'{titulo}' com {nome} ({tel}) | venceu {prevista} | multa até hoje: R$ {multa:.2f}")