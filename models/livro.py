from database import conectar

def cadastrar_livro(titulo, autor, isbn, ano, quantidade):
    with conectar() as conn:
        conn.execute(
            """INSERT INTO livros (titulo, autor, isbn, ano, qtd_total, qtd_disponivel)
            VALUES(?, ?, ?, ?, ?, ?)""",
            (titulo, autor, isbn, ano, quantidade, quantidade),
        )
    print(f"Livro '{titulo}' cadastrado com sucesso")
    
def listar_livros():
    with conectar() as conn:
        return conn.execute(
            "SELECT id, titulo, autor, qtd_total, qtd_disponivel From livros Order BY titulo"
        ).fetchall()
        
def buscar_livro(termo):
    with conectar() as conn:
        return conn.execute(
            "Select id, titulo, autor, qtd_total, qtd_disponivel FROM livros WHERE titulo LIKE ? OR autor LIKE ?",
            (f"%{termo}%", f"%{termo}%"),
        ).fetchall()
        
def remover_livro(livro_id):
    with conectar() as conn:
        return conn.execute(
            "SELECT 1 FROM emprestimos WHERE livro_id = ? AND data_devolucao IS NULL",
            (livro_id,),
        ).fetchone()
        if aberto:
            print("Não da para remover: o livro está emprestado")
            return
        conn.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        print("Livro removido.")