# =============================================================================
#  janela.py  —  a janela ligada ao banco (encontro 12)
#  A janela e o api.py usam o mesmo dominio e o mesmo banco.
# =============================================================================

import tkinter as tk

from dominio.livro import Livro
from dominio.usuario import Usuario
from dominio.emprestimo import Emprestimo
from dados.repositorio_livro import RepositorioLivro

# o acervo nao mora mais aqui: ele mora no banco, e quem fala com ele e este objeto
repositorio = RepositorioLivro()

# o que a Listbox esta mostrando agora, na mesma ordem da tela
livros_na_tela = []

emprestimos = []
usuario = Usuario("Aluno", "0000")

janela = tk.Tk()
janela.title("Biblioteca")
janela.geometry("460x600")

tk.Label(janela, text="Acervo", font=("Arial", 14)).pack(pady=6)

lista = tk.Listbox(janela, width=52, height=6)
lista.pack(padx=10)

campo = tk.Entry(janela, width=34)
campo.pack(pady=8)

resultado = tk.Label(janela, text="", fg="blue")


def emprestar():
    procurado = campo.get()

    escolhido = None
    for item in repositorio.listar():
        if item.titulo.lower() == procurado.lower():
            escolhido = item

    if escolhido is None:
        resultado.config(text="Nao esta no acervo.", fg="red")
        return

    emprestimo = Emprestimo(escolhido, usuario, "14/09/2026")
    emprestimos.append(emprestimo)
    resultado.config(text="Emprestado: " + str(emprestimo), fg="blue")


def devolver():
    if not emprestimos:
        resultado.config(text="Nao ha emprestimo.", fg="red")
        return

    emprestimo = emprestimos[-1]

    try:
        emprestimo.devolver()
        resultado.config(text="Devolvido: " + str(emprestimo), fg="blue")
    except ValueError as erro:
        resultado.config(text=str(erro), fg="red")


tk.Button(janela, text="Emprestar", command=emprestar).pack()
tk.Button(janela, text="Devolver", command=devolver).pack(pady=4)

resultado.pack(pady=6)

# ---------------------------------------------------------------- cadastro

titulo_secao = tk.Label(janela, text="Cadastrar livro", font=("Arial", 12))
titulo_secao.pack(pady=(10, 4))

formulario = tk.Frame(janela)
formulario.pack()

tk.Label(formulario, text="Titulo:").grid(row=0, column=0, sticky="e")
campo_titulo = tk.Entry(formulario, width=28)
campo_titulo.grid(row=0, column=1, pady=2)

tk.Label(formulario, text="Autor:").grid(row=1, column=0, sticky="e")
campo_autor = tk.Entry(formulario, width=28)
campo_autor.grid(row=1, column=1, pady=2)

tk.Label(formulario, text="Ano:").grid(row=2, column=0, sticky="e")
campo_ano = tk.Entry(formulario, width=28)
campo_ano.grid(row=2, column=1, pady=2)


def atualizar_lista():
    lista.delete(0, tk.END)

    # a tela nao guarda nada: ela mostra o que o repositorio devolveu agora
    livros_na_tela.clear()

    for livro in repositorio.listar():
        livros_na_tela.append(livro)
        lista.insert(tk.END, str(livro))


def livro_selecionado():
    selecionados = lista.curselection()

    if not selecionados:
        resultado.config(text="Selecione um livro na lista.", fg="red")
        return None

    # a posicao na tela nao e o id do banco -- ela so serve para achar o objeto
    posicao = selecionados[0]
    return livros_na_tela[posicao]


def cadastrar():
    titulo = campo_titulo.get()
    autor = campo_autor.get()
    ano = campo_ano.get()

    try:
        livro = Livro(titulo, autor, int(ano))

        # antes: acervo.append(livro), e sumia ao fechar a janela
        repositorio.salvar(livro)

        atualizar_lista()
        campo_titulo.delete(0, tk.END)
        campo_autor.delete(0, tk.END)
        campo_ano.delete(0, tk.END)
        resultado.config(text="Cadastrado: " + str(livro), fg="blue")
    except ValueError as erro:
        # a mensagem e a que a SUA classe escreveu no raise
        resultado.config(text=str(erro), fg="red")


def excluir():
    livro = livro_selecionado()

    if livro is None:
        return

    # quem some do banco e o id, nao a linha da tela
    repositorio.excluir(livro.id)
    atualizar_lista()
    resultado.config(text="Excluido: " + livro.titulo, fg="blue")


def alterar():
    livro = livro_selecionado()

    if livro is None:
        return

    try:
        # aqui a regra do dominio entra em acao antes do banco: ano invalido
        # nem chega no SQLite, porque o setter da classe recusa
        livro.titulo = campo_titulo.get()
        livro.autor = campo_autor.get()
        livro.ano = int(campo_ano.get())

        repositorio.atualizar(livro)
        atualizar_lista()
        resultado.config(text="Alterado: " + str(livro), fg="blue")
    except ValueError as erro:
        resultado.config(text=str(erro), fg="red")


tk.Button(janela, text="Cadastrar", command=cadastrar).pack(pady=6)

botoes = tk.Frame(janela)
botoes.pack()

tk.Button(botoes, text="Excluir", command=excluir).pack(side="left", padx=4)
tk.Button(botoes, text="Alterar", command=alterar).pack(side="left", padx=4)

# a primeira carga da tela: ela nasce vazia e o banco a preenche
atualizar_lista()

janela.mainloop()

repositorio.fechar()
