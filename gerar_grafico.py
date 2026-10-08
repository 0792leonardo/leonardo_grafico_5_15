#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gráfico 5.15 – MP2,5 – Evolução das concentrações médias anuais – RMSP
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações médias anuais de MP₂,₅ (material particulado fino) com
a faixa de variabilidade representada pelos percentis 10 e 90.

O gráfico exibe:
- Linha da média anual de MP₂,₅ com rótulos de valores
- Faixa sombreada branca entre os percentis 10 e 90
- Período de 2017 a 2025
- Layout limpo e minimalista (sem linhas de grade)

Autor: Leonardo Rocha
Data: 2026-09-11
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
# O arquivo deve estar na mesma pasta do script
CSV = Path("Dd_grafico_5_15.csv")

# Lê o arquivo CSV usando codificação UTF-8 com BOM (comum em arquivos do Windows)
# O parâmetro encoding="utf-8-sig" remove automaticamente o BOM do início do arquivo
df = pd.read_csv(CSV, encoding="utf-8-sig")


# =============================================================================
# LIMPEZA E PREPARAÇÃO DOS DADOS
# =============================================================================

# --- Colunas de médias e percentis (med_int, Per_90, Per_10) ---
# Essas colunas podem conter valores com vírgula como separador decimal (padrão brasileiro)
# Exemplo: "12,5" em vez de "12.5"
# O código abaixo:
#   1. Converte para string
#   2. Substitui vírgulas por pontos (padrão internacional)
#   3. Converte para numérico, transformando erros em NaN
for c in ["med_int", "Per_90", "Per_10"]:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"
    )

# --- Coluna de Ano ---
# Converte para numérico e depois para inteiro (anos não têm casas decimais)
df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype(int)


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()


# -----------------------------------------------------------------------------
# TRAÇO 1: PERCENTIL 90 (BASE PARA PREENCHIMENTO)
# -----------------------------------------------------------------------------

# Este traço é adicionado primeiro para servir como base para o preenchimento
# da área entre os percentis. Ele não é visível (width=0) e não aparece na legenda.
# 
# Nota: usa rgba(255,255,255,0) como cor, que é branco totalmente transparente
# (alternativa ao "width=0" para garantir invisibilidade)
fig.add_trace(go.Scatter(
    x=df["ano"],                                  # Eixo X: anos
    y=df["Per_90"],                               # Eixo Y: valores do percentil 90
    mode="lines",                                 # Modo: apenas linhas
    line=dict(
        color="rgba(255,255,255,0)",              # Branco transparente (invisível)
        width=0                                   # Largura zero
    ),
    showlegend=False,                             # Não mostra na legenda
    hoverinfo="skip"
))


# -----------------------------------------------------------------------------
# TRAÇO 2: PERCENTIL 10 (ÁREA SOMBREADA)
# -----------------------------------------------------------------------------

# Este traço cria a área sombreada entre P10 e P90 usando fill="tonexty"
# Isso preenche a área entre este traço e o anterior (Per_90)
# 
# A cor branca com 88% de opacidade cria um efeito de "névoa" sobre o fundo
# azul claro, destacando a faixa de variabilidade dos dados
fig.add_trace(go.Scatter(
    x=df["ano"],                                  # Eixo X: anos
    y=df["Per_10"],                               # Eixo Y: valores do percentil 10
    mode="lines",                                 # Modo: apenas linhas
    line=dict(
        color="rgba(255,255,255,0)",              # Branco transparente
        width=0                                   # Largura zero
    ),
    fill="tonexty",                               # Preenche entre este traço e o anterior
    fillcolor="#dce6f2",           # Branco com 88% de opacidade
    name="Percentis 10/90",                       # Nome na legenda
    # Dados customizados para o tooltip (valores do P90)
    # Permite exibir tanto P10 quanto P90 no mesmo tooltip
    customdata=df["Per_90"],
    
    # Template personalizado do tooltip
    # %{customdata} acessa os valores customizados (P90)
    hovertemplate=(
        "<b>Percentis 10/90</b><br>"          # Título em negrito
        "P10: %{y:.0f} µg/m³<br>"             # Valor do P10 com 1 decimal
        "P90: %{customdata:.0f} µg/m³<extra></extra>"  # Valor do P90
)))


# -----------------------------------------------------------------------------
# TRAÇO 3: MÉDIA DE MP₂,₅ (LINHA PRINCIPAL)
# -----------------------------------------------------------------------------

# Este traço mostra a média de MP₂,₅ com linha preta, marcadores circulares
# com borda azul, e rótulos de texto com os valores arredondados
fig.add_trace(go.Scatter(
    x=df["ano"],                                  # Eixo X: anos
    y=df["med_int"],                              # Eixo Y: valores da média
    mode="lines+markers+text",                    # Modo: linha + marcadores + texto
    name="Média",                                 # Nome na legenda
    
    # Configuração da linha
    line=dict(
        color="#111111",                          # Cor preta (quase puro)
        width=3                                   # Linha mais grossa para destaque
    ),
    
    # Configuração dos marcadores
    marker=dict(
        color="#111111",                          # Preenchimento preto
        size=9,                                   # Tamanho do marcador
        symbol="circle",                          # Forma: círculo
        line=dict(
            color="#1D6FA5",                      # Borda azul (destaque)
            width=2                               # Espessura da borda
        )
    ),
    
    # Rótulos de texto nos pontos (valores arredondados para inteiro)
    text=df["med_int"].round(0).astype(int).astype(str),
    textposition="top center",                    # Posição: acima do ponto
    
    # Estilo da fonte dos rótulos
    textfont=dict(
        color="#333333",                          # Cinza escuro
        size=13                                   # Tamanho da fonte
    ),
    
    # Template do tooltip ao passar o mouse
    hovertemplate="<b>Média</b><br>%{y:.0f} µg/m³<extra></extra>"
))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

fig.update_layout(
    # Tema claro do Plotly (fundo branco com linhas suaves)
    template="plotly_white",
    
    # Altura da figura em pixels (mais compacto que os anteriores)
    height=590,
    
    # Margens ao redor do gráfico (esquerda, direita, topo, base)
    # Margem inferior (110px) para acomodar a legenda horizontal
    margin=dict(l=95, r=40, t=20, b=110),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#ffffff",                      # Azul muito claro
    
    # Cor de fundo da área do gráfico (onde os dados são plotados)
    plot_bgcolor="#ffffff",                       # Mesma cor para consistência
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    # quando o mouse passa sobre um ano específico
    hovermode="x unified",
    
    # Configuração da fonte global
    font=dict(
        family="Arial, sans-serif",               # Fonte sans-serif limpa
        size=14,                                  # Tamanho padrão
        color="#555555"                           # Cinza médio
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        tickmode="linear",                        # Ticks em intervalos regulares
        dtick=1,                                  # Intervalo de 1 em 1 ano
        range=[2017, 2025],                       # Limites: 2017 a 2025
        showgrid=False,                           # ⚠️ SEM linhas de grade verticais
        zeroline=False,                           # Sem linha no zero do eixo X
        showline=True,                            # ⚠️ MOSTRA a linha do eixo X
        linecolor="#B8B8B8",                       # Cor da linha do eixo (cinza claro)
        ticks="inside"                            # Marcadores dentro do eixo
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="MP₂,₅ (µg/m³)",                    # Título do eixo (MP2.5)
        range=[0, 25],                            # Limites: 0 a 25 µg/m³
        dtick=5,                                  # Intervalo de 5 em 5 µg/m³
        showgrid=False,                           # ⚠️ SEM linhas de grade horizontais
        zeroline=False,                           # Sem linha no zero do eixo Y
        showline=True,                            # ⚠️ MOSTRA a linha do eixo Y
        linecolor="#B8B8B8",                       # Cor da linha do eixo (cinza claro)
        ticks="outside"                           # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                          # Horizontal
        yanchor="top",                            # Âncora no topo
        y=-0.115,                                 # Posicionada abaixo do gráfico
        xanchor="center",                         # Centralizada horizontalmente
        x=0.5,                                    # Centro do eixo X
        font=dict(size=13)                        # Tamanho da fonte
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                                 # Nome do arquivo de saída
    include_plotlyjs=True,                        # Inclui a biblioteca Plotly (offline)
    full_html=True,                               # Gera um documento HTML completo
    config={                                      # Configurações do gráfico
        "responsive": True,                       # Adapta-se ao tamanho da tela
        "displaylogo": False,                     # Remove o logo da Plotly
        "scrollZoom": True                        # Permite zoom com scroll
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO DE MP₂,₅ GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📅 Período: {min(df['ano'])} a {max(df['ano'])}")
print(f"📉 Média MP₂,₅: {df['med_int'].min():.1f} a {df['med_int'].max():.1f} µg/m³")
print(f"📊 Percentis 10/90: faixa de variabilidade incluída")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")