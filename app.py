from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    render_template_string
)

import os
import sqlite3
import random
from datetime import datetime

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()


# ============================================================
# CONFIGURAÇÃO
# ============================================================

app = Flask(__name__)

app.secret_key = "casamento-izabella-anderson-2026"

# Quantidade máxima de fotos permitidas por envio
MAX_FOTOS_POR_ENVIO = 10


# ------------------------------------------------------------
# PASTA ONDE AS FOTOS SERÃO SALVAS
# ------------------------------------------------------------
#
# Por enquanto:
# C:\Users\ander\eclipse-workspace\casamento\uploads
#
# Quando colocarmos o SSD/pendrive, basta trocar esta linha.
#
# Exemplo:
#
# UPLOAD_FOLDER = r"E:\CASAMENTO\fotos"
#
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)
UPLOAD_FOLDER = "/Volumes/CASAMENTO/fotos"


# Banco SQLite
DATABASE = os.path.join(
    BASE_DIR,
    "casamento.db"
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# BANCO DE DADOS
# ============================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS fotos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            local TEXT NOT NULL,

            arquivo TEXT NOT NULL,

            data_hora TEXT NOT NULL

        )
    """)

    conn.commit()

    conn.close()


# Inicializa banco
init_db()


# ============================================================
# ESTILOS
# ============================================================

STYLE = """
<style>

    * {
        box-sizing: border-box;
    }

    body {

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Arial,
            sans-serif;

        max-width: 600px;

        margin: auto;

        padding: 20px;

        background: #fafafa;

        color: #333;
    }


    .container {

        background: white;

        padding: 25px;

        border-radius: 18px;

        box-shadow:
            0 2px 15px rgba(0,0,0,0.08);
    }


    .coracao {

        font-size: 48px;

        text-align: center;

        margin-bottom: 5px;
    }


    h1 {

        text-align: center;

        margin: 5px 0;

        font-size: 28px;
    }


    h2 {

        margin-top: 10px;
    }


    .subtitulo {

        text-align: center;

        color: #777;

        margin-bottom: 30px;
    }


    .titulo {

        font-size: 18px;

        font-weight: bold;

        margin-top: 20px;

        margin-bottom: 12px;
    }


    input[type="text"],
    input[type="password"] {

        width: 100%;

        padding: 14px;

        border: 1px solid #ccc;

        border-radius: 10px;

        font-size: 17px;

        margin-bottom: 12px;
    }


    input[type="file"] {

        width: 100%;

        padding: 12px;

        margin-bottom: 20px;

        font-size: 15px;
    }


    .chips {

        display: flex;

        flex-wrap: wrap;

        gap: 8px;

        justify-content: center;

        margin-bottom: 15px;
    }


    .chip {

        border: 1px solid #ddd;

        background: white;

        padding: 10px 14px;

        border-radius: 22px;

        font-size: 14px;

        cursor: pointer;
    }


    .chip.selecionado {

        background: #222;

        color: white;

        border-color: #222;
    }


    .botao {

        width: 100%;

        padding: 16px;

        border: none;

        border-radius: 10px;

        background: #222;

        color: white;

        font-size: 18px;

        cursor: pointer;
    }


    .botao-galeria {
        margin-top: 30px !important;
    }


    .rodape-casamento {
        text-align: center;
        margin-top: 45px;
        padding-top: 25px;
        border-top: 1px solid #eee;
        color: #888;
        font-size: 13px;
        line-height: 1.7;
    }


    .rodape-casamento .bandeira {
        font-size: 30px;
        margin-top: 5px;
    }


    .botao-secundario {

        display: block;

        width: 100%;

        padding: 13px;

        margin-top: 10px;

        border-radius: 10px;

        border: 1px solid #ddd;

        background: white;

        color: #333;

        text-align: center;

        text-decoration: none;

        font-size: 16px;
    }


    .mensagem {

        margin-top: 20px;

        padding: 16px;

        border-radius: 10px;

        background: #e8ffe8;

        text-align: center;

        font-size: 16px;
    }


    .erro {

        margin-bottom: 20px;

        padding: 14px;

        border-radius: 10px;

        background: #ffe8e8;

        color: #a00000;

        text-align: center;
    }


    .estatisticas {

        display: grid;

        grid-template-columns: 1fr 1fr;

        gap: 12px;

        margin: 20px 0;
    }


    .card {

        background: #f5f5f5;

        padding: 18px;

        border-radius: 12px;

        text-align: center;
    }


    .numero {

        font-size: 30px;

        font-weight: bold;
    }


    .legenda {

        color: #777;

        font-size: 14px;
    }


    .ranking {

        margin-top: 20px;
    }


    .ranking-item {

        display: flex;

        justify-content: space-between;

        padding: 12px 5px;

        border-bottom: 1px solid #eee;

        font-size: 16px;
    }


    .galeria {

        display: grid;

        grid-template-columns: repeat(2, 1fr);

        gap: 8px;

        margin-top: 20px;
    }


    .galeria img {

        width: 100%;

        aspect-ratio: 1 / 1;

        object-fit: cover;

        border-radius: 8px;

        cursor: pointer;
    }


    .foto-info {

        font-size: 12px;

        color: #777;

        margin-top: 3px;
    }


    .admin-topo {

        display: flex;

        justify-content: space-between;

        align-items: center;
    }


    .admin-topo a {

        color: #555;

        text-decoration: none;

        font-size: 14px;
    }

</style>
"""


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/", methods=["GET", "POST"])
def index():

    mensagem = ""

    local_inicial = ""

    nome_inicial = ""


    if request.method == "POST":

        nome = request.form.get(
            "nome",
            ""
        ).strip()


        local = request.form.get(
            "local",
            ""
        ).strip()


        fotos = [
            foto
            for foto in request.files.getlist("foto")
            if foto and foto.filename
        ]


        nome_inicial = nome

        local_inicial = local


        if not nome:

            mensagem = "Digite seu nome."


        elif not local:

            mensagem = "Informe onde aconteceu o momento."


        elif not fotos:

            mensagem = "Escolha pelo menos uma foto."


        elif len(fotos) > MAX_FOTOS_POR_ENVIO:

            mensagem = (
                f"Você pode enviar no máximo "
                f"{MAX_FOTOS_POR_ENVIO} fotos por vez."
            )


        else:

            conn = get_db()
            quantidade_enviada = 0

            try:

                for foto in fotos:

                    agora = datetime.now().strftime(
                        "%Y%m%d_%H%M%S_%f"
                    )


                    extensao = os.path.splitext(
                        foto.filename
                    )[1].lower()


                    # HEIC/HEIF não é renderizado de forma confiável
                    # pelos navegadores. Convertemos para JPEG e
                    # guardamos somente o JPEG.
                    if extensao in [".heic", ".heif"]:

                        nome_arquivo = f"{agora}.jpg"

                        caminho = os.path.join(
                            UPLOAD_FOLDER,
                            nome_arquivo
                        )

                        imagem = Image.open(foto)

                        # Corrige a orientação que vem nos metadados
                        # das fotos tiradas pelo iPhone.
                        imagem = ImageOps.exif_transpose(imagem)

                        if imagem.mode != "RGB":
                            imagem = imagem.convert("RGB")

                        imagem.save(
                            caminho,
                            "JPEG",
                            quality=85,
                            optimize=True
                        )

                    else:

                        if not extensao:
                            extensao = ".jpg"

                        nome_arquivo = (
                            f"{agora}{extensao}"
                        )

                        caminho = os.path.join(
                            UPLOAD_FOLDER,
                            nome_arquivo
                        )

                        foto.save(caminho)


                    conn.execute(
                        """
                        INSERT INTO fotos
                        (
                            nome,
                            local,
                            arquivo,
                            data_hora
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            nome,
                            local,
                            nome_arquivo,
                            datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S"
                            )
                        )
                    )

                    quantidade_enviada += 1


                conn.commit()

            except Exception:

                conn.rollback()
                raise

            finally:

                conn.close()


            return redirect(
                url_for(
                    "index",
                    sucesso="1",
                    quantidade=quantidade_enviada
                )
            )


    # O sucesso é mostrado somente na página GET após o redirect.
    if request.args.get("sucesso") == "1":

        try:
            quantidade = int(
                request.args.get("quantidade", "1")
            )
        except ValueError:
            quantidade = 1

        if quantidade == 1:
            mensagem = (
                "❤️ Foto recebida! "
                "Obrigado por participar!"
            )
        else:
            mensagem = (
                f"❤️ {quantidade} fotos recebidas! "
                "Obrigado por participar!"
            )


    return render_template_string(
        """
        <!DOCTYPE html>

        <html lang="pt-BR">

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >

            <title>
                Izabella & Anderson ❤️
            </title>

            {{ style|safe }}

        </head>


        <body>

        <div class="container">


            <div class="coracao">
                ❤️
            </div>


            <h1>
                Izabella & Anderson
            </h1>


            <p class="subtitulo">
                Compartilhe um momento
                do nosso casamento!
            </p>


            {% if mensagem %}

                <div
                    id="modalMensagem"
                    class="modal-overlay"
                >

                    <div class="modal">

                        <div class="modal-icone">
                            {% if mensagem.startswith("❤️") %}
                                ❤️
                            {% else %}
                                ⚠️
                            {% endif %}
                        </div>

                        <h2>
                            {% if mensagem.startswith("❤️") %}
                                {% if "fotos" in mensagem %}
                                    Fotos enviadas!
                                {% else %}
                                    Foto enviada!
                                {% endif %}
                            {% else %}
                                Atenção
                            {% endif %}
                        </h2>

                        <p>
                            {{ mensagem }}
                        </p>

                        <button
                            class="modal-botao"
                            onclick="fecharModal()"
                        >
                            OK
                        </button>

                    </div>

                </div>

            {% endif %}


            <form
                id="formUpload"
                method="POST"
                enctype="multipart/form-data"
                onsubmit="prepararEnvio()"
            >


                <div class="titulo">
                    👤 Seu nome
                </div>


                <input
                    id="nome"
                    type="text"
                    name="nome"
                    placeholder="Como podemos identificar você?"
                    value="{{ nome }}"
                    autocomplete="name"
                    required
                >


                <div class="titulo">
                    📸 Onde aconteceu?
                </div>


                <div class="chips">


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '💍 Entrada dos noivos')"
                    >
                        💍 Entrada
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '⛪ Cerimônia')"
                    >
                        ⛪ Cerimônia
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '❤️ Dança dos noivos')"
                    >
                        ❤️ Dança
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '🎸 Show da banda')"
                    >
                        🎸 Banda
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '💃 Pista de dança')"
                    >
                        💃 Pista
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '🥂 Brinde')"
                    >
                        🥂 Brinde
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '🍰 Bolo')"
                    >
                        🍰 Bolo
                    </button>


                    <button
                        type="button"
                        class="chip"
                        onclick="selecionarLocal(this, '😂 Momentos diversos')"
                    >
                        😂 Diversos
                    </button>


                </div>


                <input
                    id="local"
                    type="text"
                    name="local"
                    placeholder="Ou digite outro momento..."
                    value="{{ local }}"
                    required
                >


                <div class="titulo">
                    📷 Escolha uma ou no maximo 10 fotos
                </div>


                <input
                    id="fotos"
                    type="file"
                    name="foto"
                    accept="image/*,.heic,.heif"
                    multiple
                    required
                    onchange="atualizarQuantidadeFotos()"
                >


                <div
                    id="contadorFotos"
                    style="
                        text-align:center;
                        color:#777;
                        font-size:13px;
                        margin-top:-10px;
                        margin-bottom:15px;
                    "
                >
                    Você pode enviar até {{ max_fotos }} fotos por vez.
                </div>


                <button
                    id="botaoEnviar"
                    class="botao"
                    type="submit"
                >
                    ❤️ Enviar foto
                </button>


            </form>
 
           

            <p
                style="
                    text-align:center;
                    color:#999;
                    font-size:12px;
                    margin-top:25px;
                "
            >
                Cada foto ajuda a guardar
                esse momento para sempre ❤️
            </p>

           <div class="rodape-casamento">

    <strong>3 de outubro de 2026</strong>

    <br>

    Belo Horizonte - Minas Gerais - Brasil

    <div class="bandeiras">🇧🇷</div>

    <div class="botoes-rodape">
        <a href="/galeria" class="botao-rodape">
            📸 Veja o que já rolou
        </a>

        <a href="/galeriaEspecial" class="botao-rodape botao-rodape--especial">
            ✨ Galeria especial
        </a>
    </div>

</div>


<style>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 20px;
}

.modal {
    width: 100%;
    max-width: 340px;
    background: white;
    border-radius: 18px;
    padding: 28px 22px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
    animation: aparecerModal 0.25s ease;
}

.modal-icone {
    font-size: 48px;
    margin-bottom: 10px;
}

.modal h2 {
    margin: 5px 0 10px;
    color: #333;
}

.modal p {
    color: #666;
    font-size: 14px;
    line-height: 1.5;
}

.modal-botao {
    margin-top: 15px;
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 10px;
    background: #222;
    color: white;
    font-size: 15px;
    cursor: pointer;
}

@keyframes aparecerModal {
    from {
        opacity: 0;
        transform: scale(0.92);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}
.spinner {
    display: inline-block;
    width: 14px;
    height: 14px;
    margin-right: 7px;
    border: 2px solid rgba(255,255,255,0.4);
    border-top-color: white;
    border-radius: 50%;
    animation: girar 0.8s linear infinite;
    vertical-align: middle;
}

@keyframes girar {
    to {
        transform: rotate(360deg);
    }
}
.rodape-casamento {
    text-align: center;
    font-family: 'Georgia', serif;
    color: #444;
}

.botoes-rodape {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.botao-rodape {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 18px;
    border-radius: 999px;
    border: 1px solid #d9c9a3;
    background: #fffaf1;
    color: #6b5b3e;
    text-decoration: none;
    font-size: 14px;
    font-family: 'Georgia', serif;
    transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.botao-rodape:hover {
    background: #f3e6c8;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
}

.botao-rodape--especial {
    background: #fdf1f1;
    border-color: #e8c4c4;
    color: #8a4b4b;
}

.botao-rodape--especial:hover {
    background: #f8dede;
}
.bandeira {
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
    font-size: 20px;
    margin-top: 4px;
}
</style>


        </div>


        <script>

        function fecharModal() {

            var modal =
                document.getElementById("modalMensagem");

            if (modal) {
                modal.remove();
            }

        }


        // Depois de exibir o sucesso, limpa o parâmetro da URL.
        // Assim, se o usuário voltar da galeria, a página inicial
        // não volta a considerar a foto como recém-enviada.
        document.addEventListener(
            "DOMContentLoaded",
            function() {

                if (window.location.search.indexOf("sucesso=1") !== -1) {

                    window.history.replaceState(
                        {},
                        document.title,
                        window.location.pathname
                    );

                }

            }
        );


        // Safari/iPhone e outros navegadores podem restaurar
        // a página anterior diretamente do cache de navegação.
        // Nesse caso, remove o modal que já foi exibido.
        window.addEventListener(
            "pageshow",
            function(event) {

                if (event.persisted) {
                    fecharModal();
                }

            }
        );


            function selecionarLocal(
                botao,
                local
            ) {

                document.getElementById(
                    "local"
                ).value = local;


                document
                    .querySelectorAll(".chip")
                    .forEach(function(chip) {

                        chip.classList.remove(
                            "selecionado"
                        );

                    });


                botao.classList.add(
                    "selecionado"
                );

            }


            // Lembra o nome neste celular.
            // Não usa banco, login ou sessão.
            document.addEventListener(
                "DOMContentLoaded",
                function() {

                    var campoNome =
                        document.getElementById("nome");

                    var nomeSalvo =
                        localStorage.getItem(
                            "casamento_nome"
                        );

                    if (
                        campoNome &&
                        !campoNome.value &&
                        nomeSalvo
                    ) {
                        campoNome.value = nomeSalvo;
                    }

                }
            );


            function atualizarQuantidadeFotos() {

                var campoFotos =
                    document.getElementById("fotos");

                var contador =
                    document.getElementById("contadorFotos");

                var botao =
                    document.getElementById("botaoEnviar");

                if (!campoFotos) {
                    return;
                }

                var quantidade = campoFotos.files.length;

                if (quantidade === 0) {

                    if (contador) {
                        contador.innerHTML =
                            "Você pode enviar até {{ max_fotos }} fotos por vez.";
                    }

                    if (botao) {
                        botao.innerHTML = "❤️ Enviar foto";
                    }

                    return;
                }

                if (quantidade > {{ max_fotos }}) {

                    if (contador) {
                        contador.innerHTML =
                            "⚠️ Você selecionou " +
                            quantidade +
                            " fotos. O limite é {{ max_fotos }}.";
                        contador.style.color = "#a00000";
                    }

                    if (botao) {
                        botao.innerHTML =
                            "⚠️ Limite de {{ max_fotos }} fotos";
                    }

                    return;
                }

                if (contador) {
                    contador.style.color = "#777";
                    contador.innerHTML =
                        "📸 " + quantidade +
                        (quantidade === 1
                            ? " foto selecionada"
                            : " fotos selecionadas");
                }

                if (botao) {
                    botao.innerHTML =
                        "❤️ Enviar " + quantidade +
                        (quantidade === 1 ? " foto" : " fotos");
                }
            }


            // Mostra um "aguarde" durante o upload
            // e evita o envio duplicado.
            function prepararEnvio() {

                var campoNome =
                    document.getElementById("nome");

                var botao =
                    document.getElementById("botaoEnviar");

                if (campoNome && campoNome.value.trim()) {

                    localStorage.setItem(
                        "casamento_nome",
                        campoNome.value.trim()
                    );

                }

                if (botao) {

                    botao.disabled = true;

                    botao.innerHTML =
                        "⏳ Enviando foto... aguarde";
                    botao.innerHTML =
                        '<span class="spinner"></span> ⏳  Enviando foto... aguarde';

                    botao.style.opacity = "0.65";
                    botao.style.cursor = "wait";

                }

            }

        </script>


        </body>

        </html>
        """,

        style=STYLE,

        max_fotos=MAX_FOTOS_POR_ENVIO,

        nome=nome_inicial,

        local=local_inicial,

        mensagem=mensagem
    )


# ============================================================
# GALERIA
# ============================================================

@app.route("/galeria")
def galeria():

    local_filtro = request.args.get(
        "local",
        ""
    ).strip()


    # Paginação da galeria.
    # Mantemos a página leve mesmo quando houver muitas fotos.
    try:
        pagina = int(request.args.get("pagina", "1"))
    except ValueError:
        pagina = 1

    if pagina < 1:
        pagina = 1

    fotos_por_pagina = 20

    conn = get_db()


    locais = conn.execute(
        """
        SELECT DISTINCT local
        FROM fotos
        WHERE local IS NOT NULL
          AND local <> ''
        ORDER BY local
        """
    ).fetchall()


    if local_filtro:

        total_fotos = conn.execute(
            """
            SELECT COUNT(*)
            FROM fotos
            WHERE local = ?
            """,
            (local_filtro,)
        ).fetchone()[0]

    else:

        total_fotos = conn.execute(
            """
            SELECT COUNT(*)
            FROM fotos
            """
        ).fetchone()[0]


    total_paginas = max(
        1,
        (total_fotos + fotos_por_pagina - 1)
        // fotos_por_pagina
    )


    if pagina > total_paginas:
        pagina = total_paginas


    offset = (pagina - 1) * fotos_por_pagina


    if local_filtro:

        fotos = conn.execute(
            """
            SELECT *
            FROM fotos
            WHERE local = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (
                local_filtro,
                fotos_por_pagina,
                offset
            )
        ).fetchall()

    else:

        fotos = conn.execute(
            """
            SELECT *
            FROM fotos
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (
                fotos_por_pagina,
                offset
            )
        ).fetchall()


    conn.close()


    return render_template_string(
        """
        <!DOCTYPE html>

        <html lang="pt-BR">

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >

            <title>
                Fotos ❤️
            </title>

            {{ style|safe }}

        </head>


        <body>

        <div class="container">


            <div class="coracao">
                ❤️
            </div>


            <h1>
                Fotos do casamento
            </h1>


            <p class="subtitulo">
                Momentos compartilhados
            </p>


            <form
                method="GET"
                style="margin-top:20px;"
            >

                <div class="titulo">
                    🔎 Filtrar por momento
                </div>

                <select
                    name="local"
                    onchange="this.form.submit()"
                    style="
                        width:100%;
                        padding:14px;
                        border:1px solid #ccc;
                        border-radius:10px;
                        font-size:16px;
                        background:white;
                    "
                >

                    <option value="">
                        Todos os momentos
                    </option>

                    {% for item in locais %}

                        <option
                            value="{{ item['local'] }}"
                            {% if local_filtro == item['local'] %}
                                selected
                            {% endif %}
                        >
                            {{ item['local'] }}
                        </option>

                    {% endfor %}

                </select>

            </form>


            <div class="galeria">

                {% for foto in fotos %}

                    <div>

                        <a
                            href="/foto/{{ foto['arquivo'] }}"
                            target="_blank"
                        >

                            <img
                                src="/foto/{{ foto['arquivo'] }}"
                                loading="lazy"
                            >

                        </a>


                        <div class="foto-info">

                            {{ foto['nome'] }}
                            ·
                            {{ foto['local'] }}

                        </div>

                    </div>

                {% endfor %}

            </div>


            {% if not fotos %}

                <p style="text-align:center;">

                    {% if local_filtro %}
                        Nenhuma foto encontrada nesse momento. 📸
                    {% else %}
                        Ainda não temos fotos.
                        Seja o primeiro! 📸
                    {% endif %}

                </p>

            {% endif %}


            {% if total_paginas > 1 %}

                <div
                    style="
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        gap:10px;
                        margin-top:25px;
                        flex-wrap:wrap;
                    "
                >

                    {% if pagina > 1 %}

                        <a
                            href="{{ url_for('galeria', local=local_filtro, pagina=pagina-1) }}"
                            class="botao-secundario"
                            style="
                                width:auto;
                                margin-top:0;
                                padding:10px 14px;
                            "
                        >
                            ← Anteriores
                        </a>

                    {% endif %}


                    <span
                        style="
                            color:#777;
                            font-size:14px;
                            padding:8px 4px;
                        "
                    >
                        Página {{ pagina }} de {{ total_paginas }}
                    </span>


                    {% if pagina < total_paginas %}

                        <a
                            href="{{ url_for('galeria', local=local_filtro, pagina=pagina+1) }}"
                            class="botao-secundario"
                            style="
                                width:auto;
                                margin-top:0;
                                padding:10px 14px;
                            "
                        >
                            Próximas →
                        </a>

                    {% endif %}

                </div>

            {% endif %}


            <a
                class="botao-secundario"
                href="/"
            >
                📸 Enviar outra foto
            </a>


        </div>

        </body>

        </html>
        """,

        style=STYLE,

        fotos=fotos,

        locais=locais,

        local_filtro=local_filtro,

        pagina=pagina,

        total_paginas=total_paginas
    )


# ============================================================
# GALERIA ESPECIAL
# ============================================================

@app.route("/galeriaEspecial")
def galeria_especial():

    conn = get_db()

    fotos = conn.execute(
        """
        SELECT *
        FROM fotos
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    # Cinco estilos diferentes.
    # Sem parâmetro, começa no mosaico.
    # O botão "Ver outra composição" avança para o próximo.
    formatos = [
        "mosaico",
        "coracao",
        "polaroid",
        "destaques",
        "artistica"
    ]

    try:
        indice_formato = int(
            request.args.get("formato", "0")
        ) % len(formatos)
    except ValueError:
        indice_formato = 0

    formato = formatos[indice_formato]

    proximo_formato = (
        (indice_formato + 1) % len(formatos)
    )

    return render_template_string(
        """
        <!DOCTYPE html>

        <html lang="pt-BR">

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >

            <title>
                Izabella & Anderson ❤️
            </title>

            <style>

                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    padding: 18px;
                    background: #f7f5f2;
                    color: #333;
                    font-family:
                        -apple-system,
                        BlinkMacSystemFont,
                        "Segoe UI",
                        Arial,
                        sans-serif;
                }

                .especial {
                    max-width: 1100px;
                    margin: auto;
                }

                .especial-cabecalho {
                    text-align: center;
                    padding: 15px 10px 25px;
                }

                .especial-cabecalho .coracao {
                    font-size: 48px;
                    line-height: 1;
                }

                .especial-cabecalho h1 {
                    margin: 8px 0;
                    font-family: Georgia, serif;
                    font-size: clamp(28px, 5vw, 48px);
                }

                .especial-cabecalho p {
                    color: #777;
                    margin: 8px 0;
                    font-size: 15px;
                }

                .especial-grade {
                    display: grid;
                    grid-template-columns: repeat(6, 1fr);
                    grid-auto-rows: 105px;
                    gap: 7px;
                }

                .especial-foto {
                    overflow: hidden;
                    border-radius: 12px;
                    background: #ddd;
                    position: relative;
                }

                .especial-foto a {
                    display: block;
                    width: 100%;
                    height: 100%;
                }

                .especial-foto img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    display: block;
                }

                .especial-foto.grande {
                    grid-column: span 3;
                    grid-row: span 3;
                }

                .especial-foto.medio {
                    grid-column: span 2;
                    grid-row: span 2;
                }

                .especial-foto.pequena {
                    grid-column: span 1;
                    grid-row: span 1;
                }

                .especial-coracao {
                    position: relative;
                    width: min(94vw, 760px);
                    aspect-ratio: 1 / 0.92;
                    margin: 30px auto;
                    display: grid;
                    grid-template-columns: repeat(10, 1fr);
                    grid-auto-rows: 1fr;
                    gap: 5px;
                    padding: 12px;
                    overflow: hidden;
                    clip-path: polygon(
                        50% 96%,
                        4% 45%,
                        4% 25%,
                        10% 12%,
                        22% 5%,
                        34% 6%,
                        43% 13%,
                        50% 23%,
                        57% 13%,
                        66% 6%,
                        78% 5%,
                        90% 12%,
                        96% 25%,
                        96% 45%
                    );
                    background: white;
                }

                .especial-coracao .especial-foto {
                    min-width: 0;
                    min-height: 0;
                    border-radius: 7px;
                    overflow: hidden;
                }

                .especial-coracao .especial-foto img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    display: block;
                }

                .especial-polaroids {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: center;
                    gap: 18px;
                    padding: 20px 5px;
                }

                .polaroid {
                    width: min(43%, 280px);
                    background: white;
                    padding: 10px 10px 35px;
                    box-shadow: 0 3px 14px rgba(0,0,0,.16);
                    transform: rotate(-2deg);
                }

                .polaroid:nth-child(3n) {
                    transform: rotate(2deg);
                }

                .polaroid:nth-child(4n) {
                    transform: rotate(-4deg);
                }

                .polaroid img {
                    width: 100%;
                    aspect-ratio: 1 / 1;
                    object-fit: cover;
                    display: block;
                }

                .especial-destaques {
                    display: grid;
                    grid-template-columns: 2fr 1fr;
                    gap: 8px;
                }

                .especial-destaques .principal {
                    min-height: 520px;
                    border-radius: 14px;
                    overflow: hidden;
                }

                .especial-destaques .lateral {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 8px;
                }

                .especial-destaques .lateral .especial-foto {
                    min-height: 150px;
                }

                .especial-artistica {
                    columns: 3 220px;
                    column-gap: 8px;
                }

                .especial-artistica .especial-foto {
                    display: inline-block;
                    width: 100%;
                    height: auto;
                    margin: 0 0 8px;
                    break-inside: avoid;
                }

                .especial-artistica .especial-foto img {
                    height: auto;
                    max-height: 450px;
                    object-fit: cover;
                }

                .especial-botoes {
                    text-align: center;
                    padding: 28px 10px 10px;
                }

                .especial-botoes a {
                    display: inline-block;
                    margin: 6px;
                    padding: 13px 18px;
                    border-radius: 10px;
                    text-decoration: none;
                    background: #222;
                    color: white;
                }

                .especial-botoes .secundario {
                    background: white;
                    color: #333;
                    border: 1px solid #ddd;
                }

                .especial-rodape {
                    text-align: center;
                    margin-top: 35px;
                    padding: 25px 10px 10px;
                    border-top: 1px solid #ddd;
                    color: #777;
                }

                .especial-rodape .bandeiras {
                    font-size: 34px;
                    margin-top: 10px;
                    letter-spacing: 5px;
                }

                @media (max-width: 650px) {

                    body {
                        padding: 10px;
                    }

                    .especial-grade {
                        grid-template-columns: repeat(4, 1fr);
                        grid-auto-rows: 80px;
                    }

                    .especial-foto.grande {
                        grid-column: span 2;
                        grid-row: span 2;
                    }

                    .especial-foto.medio {
                        grid-column: span 2;
                        grid-row: span 2;
                    }

                    .polaroid {
                        width: 43%;
                        padding-bottom: 25px;
                    }

                    .especial-destaques {
                        grid-template-columns: 1fr;
                    }

                    .especial-destaques .principal {
                        min-height: 360px;
                    }

                    .especial-destaques .lateral {
                        grid-template-columns: repeat(3, 1fr);
                    }

                    .especial-destaques .lateral .especial-foto {
                        min-height: 110px;
                    }

                }

            </style>

        </head>


        <body>

        <div class="especial">

            <div class="especial-cabecalho">

                <div class="coracao">
                    ❤️
                </div>

                <h1>
                    Izabella & Anderson
                </h1>

                <p>
                    Nossos melhores momentos, em muitas formas
                </p>

                <p>
                    Cada atualização pode mostrar uma nova composição. 📸
                </p>

            </div>


            {% if formato == "mosaico" %}

                <div class="especial-grade">

                    {% for foto in fotos %}

                        {% if loop.index % 7 == 1 %}
                            {% set tamanho = "grande" %}
                        {% elif loop.index % 3 == 0 %}
                            {% set tamanho = "medio" %}
                        {% else %}
                            {% set tamanho = "pequena" %}
                        {% endif %}

                        <div class="especial-foto {{ tamanho }}">

                            <a
                                href="/foto/{{ foto['arquivo'] }}"
                                target="_blank"
                            >

                                <img
                                    src="/foto/{{ foto['arquivo'] }}"
                                    loading="lazy"
                                >

                            </a>

                        </div>

                    {% endfor %}

                </div>


            {% elif formato == "coracao" %}

                <div class="especial-coracao">

                    {% for foto in fotos %}

                        <div class="especial-foto">

                            <a
                                href="/foto/{{ foto['arquivo'] }}"
                                target="_blank"
                            >

                                <img
                                    src="/foto/{{ foto['arquivo'] }}"
                                    loading="lazy"
                                >

                            </a>

                        </div>

                    {% endfor %}

                </div>


            {% elif formato == "polaroid" %}

                <div class="especial-polaroids">

                    {% for foto in fotos %}

                        <div class="polaroid">

                            <a
                                href="/foto/{{ foto['arquivo'] }}"
                                target="_blank"
                            >

                                <img
                                    src="/foto/{{ foto['arquivo'] }}"
                                    loading="lazy"
                                >

                            </a>

                        </div>

                    {% endfor %}

                </div>


            {% elif formato == "destaques" %}

                {% if fotos %}

                    <div class="especial-destaques">

                        <div class="especial-foto principal">

                            <a
                                href="/foto/{{ fotos[0]['arquivo'] }}"
                                target="_blank"
                            >

                                <img
                                    src="/foto/{{ fotos[0]['arquivo'] }}"
                                    loading="lazy"
                                >

                            </a>

                        </div>

                        <div class="lateral">

                            {% for foto in fotos[1:] %}

                                <div class="especial-foto">

                                    <a
                                        href="/foto/{{ foto['arquivo'] }}"
                                        target="_blank"
                                    >

                                        <img
                                            src="/foto/{{ foto['arquivo'] }}"
                                            loading="lazy"
                                        >

                                    </a>

                                </div>

                            {% endfor %}

                        </div>

                    </div>

                {% endif %}


            {% else %}

                <div class="especial-artistica">

                    {% for foto in fotos %}

                        <div class="especial-foto">

                            <a
                                href="/foto/{{ foto['arquivo'] }}"
                                target="_blank"
                            >

                                <img
                                    src="/foto/{{ foto['arquivo'] }}"
                                    loading="lazy"
                                >

                            </a>

                        </div>

                    {% endfor %}

                </div>

            {% endif %}


            {% if not fotos %}

                <p style="text-align:center;">
                    Ainda não temos fotos. 📸
                </p>

            {% endif %}


            <div class="especial-botoes">

                <a href="/galeria">
                    🖼️ Voltar para galeria
                </a>

                <a
                    class="secundario"
                    href="/galeriaEspecial?formato={{ proximo_formato }}"
                >
                    🔄 Ver outra composição
                </a>

            </div>


            <div class="especial-rodape">

                <strong>
                    3 de outubro de 2026
                </strong>

                <br>

                Belo Horizonte - Minas Gerais - Brasil

                <div class="bandeiras">
                    🇧🇷
                </div>

            </div>


        </div>

        </body>

        </html>
        """,

        fotos=fotos,

        formato=formato,

        indice_formato=indice_formato,

        proximo_formato=proximo_formato
    )


# ============================================================
# SERVIR FOTO
# ============================================================

@app.route("/foto/<nome_arquivo>")
def foto(nome_arquivo):

    return send_from_directory(
        UPLOAD_FOLDER,
        nome_arquivo
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    erro = ""


    if request.method == "POST":

        usuario = request.form.get(
            "usuario"
        )


        senha = request.form.get(
            "senha"
        )


        if (
            usuario == "anderson"
            and senha == "123"
        ):

            session["admin"] = True

            return redirect(
                url_for("admin")
            )


        erro = "Usuário ou senha inválidos."


    if not session.get("admin"):

        return render_template_string(
            """
            <!DOCTYPE html>

            <html lang="pt-BR">

            <head>

                <meta charset="UTF-8">

                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                >

                <title>
                    Administração
                </title>

                {{ style|safe }}

            </head>


            <body>

            <div class="container">

                <div class="coracao">
                    🔐
                </div>

                <h1>
                    Administração
                </h1>

                <p class="subtitulo">
                    Casamento Izabella & Anderson
                </p>


                {% if erro %}

                    <div class="erro">
                        {{ erro }}
                    </div>

                {% endif %}


                <form method="POST">


                    <input
                        type="text"
                        name="usuario"
                        placeholder="Usuário"
                        required
                    >


                    <input
                        type="password"
                        name="senha"
                        placeholder="Senha"
                        required
                    >


                    <button
                        class="botao"
                        type="submit"
                    >
                        Entrar
                    </button>


                </form>


            </div>

            </body>

            </html>
            """,

            style=STYLE,

            erro=erro
        )


    # ========================================================
    # ESTATÍSTICAS
    # ========================================================

    conn = get_db()


    total = conn.execute(
        """
        SELECT COUNT(*)
        FROM fotos
        """
    ).fetchone()[0]


    total_convidados = conn.execute(
        """
        SELECT COUNT(
            DISTINCT nome
        )
        FROM fotos
        """
    ).fetchone()[0]


    ranking = conn.execute(
        """
        SELECT
            nome,
            COUNT(*) AS quantidade

        FROM fotos

        GROUP BY nome

        ORDER BY quantidade DESC, nome

        LIMIT 20
        """
    ).fetchall()


    fotos = conn.execute(
        """
        SELECT *
        FROM fotos
        ORDER BY id DESC
        """
    ).fetchall()


    conn.close()


    return render_template_string(
        """
        <!DOCTYPE html>

        <html lang="pt-BR">

        <head>

            <meta charset="UTF-8">

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >

            <title>
                Admin - Casamento
            </title>

            {{ style|safe }}

        </head>


        <body>

        <div class="container">


            <div class="admin-topo">

                <h1>
                    ❤️ Admin
                </h1>

                <a href="/admin/logout">
                    Sair
                </a>

            </div>


            <p class="subtitulo">
                Izabella & Anderson
            </p>


            <div class="estatisticas">


                <div class="card">

                    <div class="numero">
                        {{ total }}
                    </div>

                    <div class="legenda">
                        📸 Fotos
                    </div>

                </div>


                <div class="card">

                    <div class="numero">
                        {{ total_convidados }}
                    </div>

                    <div class="legenda">
                        👥 Convidados
                    </div>

                </div>


            </div>


            <h2>
                🏆 Ranking
            </h2>


            <div class="ranking">

                {% for pessoa in ranking %}

                    <div class="ranking-item">

                        <span>

                            {% if loop.index == 1 %}
                                🥇
                            {% elif loop.index == 2 %}
                                🥈
                            {% elif loop.index == 3 %}
                                🥉
                            {% else %}
                                {{ loop.index }}º
                            {% endif %}

                            {{ pessoa['nome'] }}

                        </span>


                        <strong>
                            {{ pessoa['quantidade'] }}
                            📸
                        </strong>

                    </div>

                {% endfor %}

            </div>


            <h2>
                🖼️ Fotos
            </h2>


            <div class="galeria">

                {% for foto in fotos %}

                    <div>

                        <a
                            href="/foto/{{ foto['arquivo'] }}"
                            target="_blank"
                        >

                            <img
                                src="/foto/{{ foto['arquivo'] }}"
                                loading="lazy"
                            >

                        </a>


                        <div class="foto-info">

                            <strong>
                                {{ foto['nome'] }}
                            </strong>

                            <br>

                            {{ foto['local'] }}

                            <br>

                            {{ foto['data_hora'] }}

                        </div>
                        <form
                            method="POST"
                            action="/admin/apagar-foto/{{ foto['id'] }}"
                            onsubmit="return confirm(
                                '⚠️ Tem certeza que deseja apagar esta foto do álbum?\\n\\nO arquivo original será mantido no PDrive.'
                            );"
                        >
                            <button
                                type="submit"
                                style="
                                    margin-top:10px;
                                    background:#b91c1c;
                                    color:white;
                                    border:none;
                                    padding:8px 12px;
                                    border-radius:8px;
                                    cursor:pointer;
                                "
                            >
                                🗑️ Apagar foto
                            </button>
                        </form>

                    </div>

                {% endfor %}

            </div>


            {% if not fotos %}

                <p style="text-align:center;">
                    Nenhuma foto recebida ainda.
                </p>

            {% endif %}


            <a
                class="botao-secundario"
                href="/"
            >
                📸 Página de envio
            </a>


        </div>

        </body>

        </html>
        """,

        style=STYLE,

        total=total,

        total_convidados=total_convidados,

        ranking=ranking,

        fotos=fotos
    )



@app.route("/admin/apagar-foto/<int:id>", methods=["POST"])
def admin_apagar_foto(id):

    if not session.get("admin"):
        return redirect(url_for("admin"))

    conn = get_db()

    conn.execute(
        "DELETE FROM fotos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

# ============================================================
# LOGOUT
# ============================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("admin")
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )