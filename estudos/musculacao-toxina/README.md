# Musculação depois da toxina botulínica — fontes do PDF

Arquivos que geram a revisão de evidência em PDF (A4, 14 páginas) sobre treinar
musculação após aplicação de toxina botulínica.

## Arquivos

| Arquivo | O que é |
|---|---|
| `gerar-pdf.py` | Script que monta o PDF do começo ao fim |
| `capa.html` | Capa em página cheia. O marcador `__EMBLEMA__` é trocado pelo brasão em base64 na hora de gerar |
| `miolo.html` | Corpo do documento: 10 seções, fichas de estudo, gráfico em SVG, tabela do protocolo e as 13 referências |
| `print-base.css` | Folha de estilo de impressão: escala tipográfica em pt, medidas em mm, controle de quebra de página |

O brasão vem de `emblema.png`, na raiz do repositório — não há cópia aqui.

## Gerar o PDF

```bash
pip install playwright pypdf
playwright install chromium      # se ainda não houver Chromium na máquina

cd estudos/musculacao-toxina
python3 gerar-pdf.py
```

Sai um `HermesIA-musculacao-e-toxina-botulinica.pdf` no diretório atual. Para
mudar o destino, use `-s caminho/do/arquivo.pdf`.

Se o Chromium estiver num lugar que o script não encontre, aponte para ele:

```bash
CHROMIUM_PATH=/usr/bin/chromium python3 gerar-pdf.py
```

## Como o documento é montado

O PDF é renderizado em duas passadas e depois juntado, porque capa e miolo têm
regras de página diferentes:

- **capa** — margem zero, fundo sangrando até a borda, sem cabeçalho nem número
  de página;
- **miolo** — margens de 24 mm, cabeçalho corrente com filete dourado e rodapé
  numerado a partir de 1.

As três famílias tipográficas (Playfair Display, Inter e IBM Plex Mono) são
baixadas do Google Fonts e **embutidas como data URI** em um `fonts.css`
temporário. Por isso o script precisa de rede na primeira vez, e por isso o PDF
resultante não depende de nenhuma fonte instalada na máquina de quem abrir.

Os arquivos intermediários (`fonts.css`, `capa-final.html` e os dois PDFs
parciais) vão para um diretório temporário e são apagados no fim. Nada disso
está versionado.

## Sobre o conteúdo

Levantamento feito em 4 de setembro de 2026, com 13 fontes — 8 internacionais e
5 do acervo SciELO.

**Nenhum texto completo foi acessado.** O ambiente onde a pesquisa foi feita
bloqueia ScienceDirect, PubMed, PMC, o site do *JAAD* e o SciELO; todos os
números vieram de resumos e de sínteses de busca. A seção 09 do documento
registra essa e as demais limitações. Confira na fonte primária antes de
publicar qualquer cifra daqui.

O documento é um levantamento de literatura e não constitui orientação médica
individual.
