import sqlite3

DB = "biblioteca.db"

def conectar():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    with conectar() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT,
            data_cadastro TEXT DEFAULT (date('now'))
        );
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            isbn TEXT UNIQUE,
            ano INTEGER,
            qtd_total INTEGER NOT NULL DEFAULT 1,
            qtd_disponivel INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
            livro_id INTEGER NOT NULL REFERENCES livros(id),
            data_emprestimo TEXT NOT NULL,
            data_prevista TEXT NOT NULL,
            data_devolucao TEXT,
            multa REAL DEFAULT 0
        );
        """)

if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado!")