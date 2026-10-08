# Gráfico 5.15 — MP2,5

Gráfico interativo em Python + Plotly baseado no CSV fornecido.

## Dados

Arquivo: `Dd_grafico_5_15.csv`

Campos utilizados:

- `ano`
- `med_int` — Média
- `Per_90` — percentil 90
- `Per_10` — percentil 10

Os percentis com vírgula decimal são convertidos automaticamente.

## Configuração

- Período: 2017–2025.
- Eixo Y: 0–25 µg/m³.
- Intervalo do eixo Y: 5 µg/m³.
- Faixa branca: Percentis 10/90.
- Linha preta: Média.
- Marcadores circulares.
- Rótulos numéricos da média.
- Fundo `#DDE9F4`.
- HTML autocontido.
- Zoom e tooltip interativos.

## Arquivos

- `index.html`
- `Dd_grafico_5_15.csv`
- `gerar_grafico.py`
- `.github/workflows/pages.yml`
- `.nojekyll`
- `publicar_github.bat`
- `README.md`

## Instalação

```bash
pip install pandas plotly
```

## Gerar

```bash
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico 5.15 MP2.5"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

URL:

```text
https://SEU_USUARIO.github.io/SEU_REPOSITORIO/
```
