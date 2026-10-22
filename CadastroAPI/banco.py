# =============================================================================
#  banco.py  —  cria a tabela e, se ela estiver vazia, guarda três livros
#  Rode uma vez: python banco.py
# =============================================================================

import sqlite3

conexao = sqlite3.connect("biblioteca.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS livro (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT    NOT NULL,
        autor  TEXT,
        ano    INTEGER
    )
""")

# só guarda os três livros se a tabela ainda estiver vazia
cursor.execute("SELECT COUNT(*) FROM livro")
if cursor.fetchone()[0] == 0:
    livros = [
        ("Dom Casmurro", "Machado de Assis", 1899),
        ("Iracema", "Jose de Alencar", 1865),
        ("O Cortico", "Aluisio Azevedo", 1890),
    ]
    for titulo, autor, ano in livros:
        cursor.execute(
            "INSERT INTO livro (titulo, autor, ano) VALUES (?, ?, ?)",
            (titulo, autor, ano),
        )
    conexao.commit()

cursor.execute("SELECT id, titulo, autor, ano FROM livro")
for codigo, titulo, autor, ano in cursor.fetchall():
    print(f"{codigo} - {titulo} - {autor} ({ano})")

conexao.close()
