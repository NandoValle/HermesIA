#!/usr/bin/env python3
"""
Gera o PDF da revisão de evidência "Musculação depois da toxina botulínica".

O que este script faz, em ordem:

  1. baixa as três famílias tipográficas do Google Fonts e embute cada face
     como data URI num fonts.css local — o PDF fica autossuficiente e
     renderiza igual em qualquer máquina, sem depender de fonte instalada;
  2. injeta o brasão (emblema.png, na raiz do repositório) na capa em base64;
  3. renderiza capa e miolo em A4 com o Chromium, via Playwright — a capa sem
     margem e sem cabeçalho, o miolo com margens, cabeçalho corrente e rodapé
     com numeração de página;
  4. junta os dois PDFs e grava os metadados do documento.

Uso:
    python3 gerar-pdf.py [-s SAIDA.pdf]

Dependências:
    pip install playwright pypdf

O Chromium é procurado nesta ordem: variável de ambiente CHROMIUM_PATH, os
navegadores que o Playwright instalou em PLAYWRIGHT_BROWSERS_PATH (ou em
/opt/pw-browsers), e por fim o Chromium do próprio Playwright. Se nenhum for
encontrado, rode `playwright install chromium` ou aponte CHROMIUM_PATH para um
binário do Chrome/Chromium já instalado.

Os arquivos intermediários (fonts.css, capa-final.html e os dois PDFs parciais)
são gravados num diretório temporário e descartados no fim.
"""

import argparse
import base64
import os
import pathlib
import re
import shutil
import sys
import tempfile
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent          # raiz do repositório
EMBLEMA = RAIZ / "emblema.png"

# Um User-Agent de navegador é necessário: sem ele o Google Fonts devolve TTF
# em vez de woff2, que é muito maior.
UA = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

FAMILIAS = [
    ("Playfair+Display", "wght@600;700"),   # títulos
    ("Inter",            "wght@300;400;500;600"),  # texto
    ("IBM+Plex+Mono",    "wght@400;500"),   # dados, etiquetas, numeração
]

# Só os subconjuntos que o português precisa. Puxar cyrillic/greek/vietnamese
# triplicaria o tamanho sem servir a nenhum glifo do documento.
SUBCONJUNTOS = ("latin", "latin-ext")

CABECALHO = """
<div style="width:100%;font-family:'Helvetica Neue',Arial,sans-serif;font-size:7px;color:#8A93A6;
            padding:0 90.7px;margin:0;-webkit-print-color-adjust:exact;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;
              border-bottom:0.5px solid #C9A84C;padding-bottom:4px;letter-spacing:.10em;">
    <span style="text-transform:uppercase;">Muscula&ccedil;&atilde;o depois da toxina botul&iacute;nica</span>
    <span style="text-transform:uppercase;color:#8A6B1F;">HermesIA &nbsp;&middot;&nbsp; Revis&atilde;o de evid&ecirc;ncia</span>
  </div>
</div>
"""

RODAPE = """
<div style="width:100%;font-family:'Helvetica Neue',Arial,sans-serif;font-size:7px;color:#8A93A6;
            padding:0 90.7px;margin:0;-webkit-print-color-adjust:exact;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;
              border-top:0.5px solid #D8DEE8;padding-top:5px;letter-spacing:.06em;">
    <span>hermesia.ia.br</span>
    <span>Levantamento de literatura &nbsp;&middot;&nbsp; n&atilde;o &eacute; orienta&ccedil;&atilde;o m&eacute;dica individual</span>
    <span>p&aacute;g. <span class="pageNumber"></span>/<span class="totalPages"></span></span>
  </div>
</div>
"""

METADADOS = {
    "/Title": "Musculação depois da toxina botulínica — revisão de evidência",
    "/Author": "HermesIA",
    "/Subject": "Revisão de evidência sobre treinar musculação após aplicação "
                "de toxina botulínica",
    "/Keywords": "toxina botulínica, botox, musculação, exercício físico, "
                 "evidência, SciELO",
    "/Creator": "HermesIA · hermesia.ia.br",
}


def baixar(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def montar_fontes(destino: pathlib.Path) -> None:
    """Baixa as faces e grava um fonts.css com cada woff2 embutido em data URI."""
    faces = []
    for familia, pesos in FAMILIAS:
        css = baixar(f"https://fonts.googleapis.com/css2?family={familia}:{pesos}&display=swap").decode()
        # O CSS vem como: /* subconjunto */ @font-face{...} repetido.
        blocos = re.split(r"/\*\s*([\w\-\[\]]+)\s*\*/", css)
        for i in range(1, len(blocos) - 1, 2):
            subconjunto, face = blocos[i], blocos[i + 1]
            if subconjunto not in SUBCONJUNTOS:
                continue
            m = re.search(r"url\((https://[^)]+\.woff2)\)", face)
            if not m:
                continue
            b64 = base64.b64encode(baixar(m.group(1))).decode()
            face = face.replace(m.group(1), f"data:font/woff2;base64,{b64}")
            faces.append(re.sub(r"\s+", " ", face).strip())
        print(f"  fontes: {familia.replace('+', ' ')} ok")
    destino.write_text("\n".join(faces), encoding="utf-8")


def montar_capa(destino: pathlib.Path) -> None:
    """Copia a capa trocando o marcador __EMBLEMA__ pelo brasão em base64."""
    if not EMBLEMA.exists():
        sys.exit(f"erro: brasão não encontrado em {EMBLEMA}")
    uri = "data:image/png;base64," + base64.b64encode(EMBLEMA.read_bytes()).decode()
    html = (AQUI / "capa.html").read_text(encoding="utf-8")
    if "__EMBLEMA__" not in html:
        sys.exit("erro: capa.html não tem o marcador __EMBLEMA__")
    destino.write_text(html.replace("__EMBLEMA__", uri), encoding="utf-8")


def achar_chromium() -> str | None:
    if os.environ.get("CHROMIUM_PATH"):
        return os.environ["CHROMIUM_PATH"]
    base = pathlib.Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    if base.is_dir():
        for exe in sorted(base.glob("chromium-*/chrome-linux/chrome")):
            return str(exe)
    return None  # deixa o Playwright resolver sozinho


def renderizar(trabalho: pathlib.Path, saida: pathlib.Path) -> None:
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter

    capa_pdf, miolo_pdf = trabalho / "_capa.pdf", trabalho / "_miolo.pdf"
    args = {}
    exe = achar_chromium()
    if exe:
        args["executable_path"] = exe

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(**args)
        pagina = navegador.new_page()

        # Capa: sangra até a borda, sem cabeçalho nem numeração.
        pagina.goto((trabalho / "capa-final.html").as_uri(), wait_until="load")
        pagina.wait_for_timeout(600)
        pagina.pdf(path=str(capa_pdf), format="A4", print_background=True,
                   prefer_css_page_size=True,
                   margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})

        # Miolo: margens, cabeçalho corrente e rodapé numerado a partir de 1.
        pagina.goto((trabalho / "miolo.html").as_uri(), wait_until="load")
        pagina.wait_for_timeout(600)
        pagina.pdf(path=str(miolo_pdf), format="A4", print_background=True,
                   prefer_css_page_size=True, display_header_footer=True,
                   header_template=CABECALHO, footer_template=RODAPE,
                   margin={"top": "24mm", "right": "24mm",
                           "bottom": "22mm", "left": "24mm"})
        navegador.close()

    escritor = PdfWriter()
    for parcial in (capa_pdf, miolo_pdf):
        for pagina_pdf in PdfReader(str(parcial)).pages:
            escritor.add_page(pagina_pdf)
    escritor.add_metadata(METADADOS)
    with open(saida, "wb") as fh:
        escritor.write(fh)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-s", "--saida", default="HermesIA-musculacao-e-toxina-botulinica.pdf",
                    help="caminho do PDF de saída")
    saida = pathlib.Path(ap.parse_args().saida).resolve()

    trabalho = pathlib.Path(tempfile.mkdtemp(prefix="estudo-toxina-"))
    try:
        # O miolo referencia fonts.css e print-base.css por caminho relativo,
        # então os três precisam conviver no mesmo diretório.
        shutil.copy(AQUI / "miolo.html", trabalho / "miolo.html")
        shutil.copy(AQUI / "print-base.css", trabalho / "print-base.css")

        print("baixando e embutindo as fontes...")
        montar_fontes(trabalho / "fonts.css")
        print("injetando o brasão na capa...")
        montar_capa(trabalho / "capa-final.html")
        print("renderizando em A4...")
        renderizar(trabalho, saida)
    finally:
        shutil.rmtree(trabalho, ignore_errors=True)

    from pypdf import PdfReader
    print(f"\npronto: {saida}")
    print(f"  {len(PdfReader(str(saida)).pages)} páginas · "
          f"{saida.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
