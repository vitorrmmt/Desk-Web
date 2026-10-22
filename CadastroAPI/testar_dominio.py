# =============================================================================
#  testar_dominio.py  —  o dominio provado sem interface nenhuma
#  Encontro 7 · Programacao para Desktop e Web · ADS · 2026/2
# =============================================================================

from dominio.livro import Livro
from dominio.usuario import Usuario
from dominio.emprestimo import Emprestimo

print("--- testando o dominio, sem tela nenhuma ---")

livro = Livro("Dom Casmurro", "Machado de Assis", 1899)
print("livro criado:", livro)

# o teste tem que provar que o ERRADO tambem e barrado
try:
    Livro("Sem ano", "Alguem", 3000)
    print("FALHOU: o ano 3000 passou")
except ValueError as erro:
    print("ok, barrou:", erro)

ana = Usuario("Ana Souza", "2026001")
emp = Emprestimo(livro, ana, "24/08/2026")
print("emprestimo:", emp)

emp.devolver()
print("depois de devolver:", emp)

try:
    emp.devolver()
    print("FALHOU: devolveu duas vezes")
except ValueError as erro:
    print("ok, barrou:", erro)

# uma lista pode guardar OBJETOS: cada posicao tem um Livro inteiro
acervo = [
    livro,
    Livro("Iracema", "Jose de Alencar", 1865),
]
print("livros no acervo:", len(acervo))
print("o autor do primeiro:", acervo[0].autor)

# buscar e percorrer e comparar. nao tem magica
procurado = "iracema"
escolhido = None
for item in acervo:
    if item.titulo.lower() == procurado.lower():
        escolhido = item
print("escolhido:", escolhido)

# colchete com for dentro = filtro
# leia: "os emprestimos, um por um, os que NAO foram devolvidos"
emprestimos = [emp, Emprestimo(acervo[1], ana, "24/08/2026")]
em_aberto = [e for e in emprestimos if not e.devolvido]
print("emprestimos:", len(emprestimos), "- em aberto:", len(em_aberto))

print("--- fim ---")
