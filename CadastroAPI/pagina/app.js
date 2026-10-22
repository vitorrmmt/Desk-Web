const API = "http://127.0.0.1:8000";

async function listarLivros() {
    const resposta = await fetch(API + "/livros");
    const livros = await resposta.json();

    const lista = document.getElementById("lista");

    lista.innerHTML = "";

    for (const livro of livros) {
        const item = document.createElement("li");

        item.textContent = `${livro.id} - ${livro.titulo} (${livro.ano})`;
        lista.appendChild(item);
    }
}

async function buscarLivro() {
    const codigo = document.getElementById("codigo").value;
    const resultado = document.getElementById("resultado");

    const resposta = await fetch(API + "/livros/" + codigo);
    const livro = await resposta.json();

    if (!resposta.ok) {
        resultado.textContent = livro.detail;
        return;
    }

    resultado.textContent = `${livro.titulo} - ${livro.autor} (${livro.ano})`;
}

async function cadastrarLivro() {
    const campoTitulo = document.getElementById("titulo");
    const campoAutor = document.getElementById("autor");
    const campoAno = document.getElementById("ano");
    const mensagem = document.getElementById("mensagem");


    const novo = {
        titulo: campoTitulo.value,
        autor: campoAutor.value,
        ano: Number(campoAno.value),
    }; 

    const resposta = await fetch(API + "/livros", {
        method: "POST",
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify(novo), 
    });
    const livro = await resposta.json();

    if (!resposta.ok) {
        mensagem.textContent = livro.detail; 
        return;
    }

    mensagem.textContent = `Cadastrado: ${livro.titulo} (codigo ${livro.id})`;

    campoTitulo.value = "";
    campoAutor.value = "";
    campoAno.value = "";

    listarLivros();
}

const botaoListar = document.getElementById("botao-listar");
botaoListar.addEventListener("click", listarLivros);
const botaoBuscar = document.getElementById("botao-buscar");
botaoBuscar.addEventListener("click", buscarLivro);
const botaoCadastrar = document.getElementById("botao-cadastrar");
botaoCadastrar.addEventListener("click", cadastrarLivro);