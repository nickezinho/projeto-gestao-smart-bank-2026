import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import io

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Smart Bank - Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILO
# =========================================================


st.markdown("""
<style>
/* FUNDO */
.stApp {
    background-color: #0f172a;
}

/* ÁREA PRINCIPAL */
.main {
    background-color: #0f172a;
}

/* TÍTULOS */
h1 {
    color: white !important;
    font-size: 42px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: white !important;
}

p {
    color: #cbd5e1;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* CARDS */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e293b, #172033);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.25);
}

div[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 14px !important;
}

div[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 27px !important;
    font-weight: 800 !important;
}

/* TABELA */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* BOTÕES */
.stButton button {
    border-radius: 10px;
}

/* DIVISÓRIAS */
hr {
    border-color: #334155;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOCALIZAÇÃO DO EXCEL
# =========================================================

ARQUIVO_EXCEL = (
    Path(__file__).resolve().parent
    / "Planilha dos Investidores.xlsx"
)

df = pd.read_excel(ARQUIVO_EXCEL)
# =========================================================
# TRATAMENTO DOS DADOS
# =========================================================

df.columns = df.columns.str.strip().str.upper()

colunas_obrigatorias = [
    "ID", "NOME", "PERFIL", "ESTADO", "CIDADE", "SEXO",
    "TIPO DE INVESTIMENTO", "VALOR INVESTIDO", "VALOR ATUAL",
    "RENTABILIDADE", "RENDA MENSAL", "IDADE"
]

colunas_faltantes = [
    coluna for coluna in colunas_obrigatorias
    if coluna not in df.columns
]

if colunas_faltantes:
    st.error(f"Colunas ausentes na planilha: {colunas_faltantes}")
    st.stop()

for coluna in [
    "VALOR INVESTIDO", "VALOR ATUAL",
    "RENTABILIDADE", "RENDA MENSAL", "IDADE"
]:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# Trata rentabilidade em formato percentual inteiro
if df["RENTABILIDADE"].dropna().abs().median() > 1:
    df["RENTABILIDADE"] = df["RENTABILIDADE"] / 100

# =========================================================
# TÍTULO
# =========================================================

st.title("🏦 SMART BANK")

st.markdown(
    """
    <p style="
        font-size:18px;
        color:#94a3b8;
        margin-top:-20px;
    ">
    Dashboard de Análise de Investimentos
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Filtros")

st.sidebar.markdown("### Perfil")

perfis = [
    "Todos"
] + sorted(
    df["PERFIL"].dropna().unique().tolist()
)

filtro_perfil = st.sidebar.selectbox(
    "Perfil do investidor",
    perfis
)

st.sidebar.markdown("### Estado")

estados = [
    "Todos"
] + sorted(
    df["ESTADO"].dropna().unique().tolist()
)

filtro_estado = st.sidebar.selectbox(
    "Estado",
    estados
)
st.sidebar.markdown("### Cidade")

cidades_disponiveis = df.copy()

if filtro_estado != "Todos":
    cidades_disponiveis = cidades_disponiveis[
        cidades_disponiveis["ESTADO"] == filtro_estado
    ]

cidades = ["Todas"] + sorted(
    cidades_disponiveis["CIDADE"].dropna().unique().tolist()
)

filtro_cidade = st.sidebar.selectbox(
    "Cidade do investidor",
    cidades
)

st.sidebar.markdown("### Investimento")

tipos = [
    "Todos"
] + sorted(
    df["TIPO DE INVESTIMENTO"].dropna().unique().tolist()
)

filtro_tipo = st.sidebar.selectbox(
    "Tipo de investimento",
    tipos
)

st.sidebar.markdown("### Sexo")

sexos = [
    "Todos"
] + sorted(
    df["SEXO"].dropna().unique().tolist()
)

filtro_sexo = st.sidebar.selectbox(
    "Sexo",
    sexos
)

# =========================================================
# APLICAÇÃO DOS FILTROS
# =========================================================

df_filtrado = df.copy()

if filtro_perfil != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["PERFIL"] == filtro_perfil
    ]

if filtro_estado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["ESTADO"] == filtro_estado
    ]

if filtro_tipo != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["TIPO DE INVESTIMENTO"] == filtro_tipo
    ]

if filtro_sexo != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["SEXO"] == filtro_sexo
    ]

# =========================================================
# INDICADORES
# =========================================================

total_investidores = len(df_filtrado)

total_investido = (
    df_filtrado["VALOR INVESTIDO"].sum()
)

valor_atual = (
    df_filtrado["VALOR ATUAL"].sum()
)

rentabilidade_media = (
    df_filtrado["RENTABILIDADE"].mean() * 100
    if len(df_filtrado) > 0
    else 0
)

lucro_total = valor_atual - total_investido
# =========================================================
# RENTABILIDADE TOTAL PONDERADA
# =========================================================

rentabilidade_ponderada = (
    (valor_atual - total_investido) / total_investido * 100
    if total_investido > 0
    else 0
)

crescimento = (
    (lucro_total / total_investido) * 100
    if total_investido > 0
    else 0
)

# =========================================================
# CARDS PRINCIPAIS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👥 Investidores",
        total_investidores
    )

with col2:

    st.metric(
        "💰 Total Investido",
        f"R$ {total_investido:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

with col3:

    st.metric(
        "📈 Patrimônio Atual",
        f"R$ {valor_atual:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

with col4:

    st.metric(
        "📊 Rentabilidade Média",
        f"{rentabilidade_media:.2f}%"
    )

# =========================================================
# SEGUNDA LINHA DE INFORMAÇÕES
# =========================================================

st.markdown("")

col5, col6, col7 = st.columns(3)

with col5:

    st.metric(
        "💵 Resultado Financeiro",
        f"R$ {lucro_total:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

with col6:

    st.metric(
        "🚀 Crescimento",
        f"{crescimento:.2f}%"
    )

with col7:

    maior_investimento = (
        df_filtrado["VALOR INVESTIDO"].max()
        if len(df_filtrado) > 0
        else 0
    )

    st.metric(
        "🏆 Maior Investimento",
        f"R$ {maior_investimento:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

# =========================================================
# GRÁFICOS PRINCIPAIS
# =========================================================

st.markdown("---")

col_grafico1, col_grafico2 = st.columns(2)

# =========================================================
# GRÁFICO 1
# INVESTIMENTOS POR TIPO
# =========================================================

with col_grafico1:

    st.subheader("💰 Investimentos por Tipo")

    valor_por_tipo = (
        df_filtrado
        .groupby("TIPO DE INVESTIMENTO")
        ["VALOR INVESTIDO"]
        .sum()
        .reset_index()
        .sort_values(
            "VALOR INVESTIDO",
            ascending=True
        )
    )

    grafico_investimentos = px.bar(
        valor_por_tipo,
        x="VALOR INVESTIDO",
        y="TIPO DE INVESTIMENTO",
        orientation="h",
        text="VALOR INVESTIDO",
        title="Valor Total Investido"
    )

    grafico_investimentos.update_traces(
        texttemplate="R$ %{text:,.0f}",
        textposition="outside"
    )

    grafico_investimentos.update_layout(
        height=500,
        template="plotly_dark",
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        grafico_investimentos,
        use_container_width=True
    )

# =========================================================
# GRÁFICO 2
# PERFIL
# =========================================================

with col_grafico2:

    st.subheader("👥 Perfil dos Investidores")

    perfil_contagem = (
        df_filtrado["PERFIL"]
        .value_counts()
        .reset_index()
    )

    perfil_contagem.columns = [
        "PERFIL",
        "QUANTIDADE"
    ]

    grafico_perfil = px.pie(
        perfil_contagem,
        names="PERFIL",
        values="QUANTIDADE",
        hole=0.55,
        title="Distribuição por Perfil"
    )

    grafico_perfil.update_traces(
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Investidores: %{value}"
            "<br>Percentual: %{percent}"
        )
    )

    grafico_perfil.update_layout(
        height=500,
        template="plotly_dark",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        grafico_perfil,
        use_container_width=True
    )
    # =========================================================
# GRÁFICO - DISTRIBUIÇÃO POR SEXO
# =========================================================

st.markdown("---")
st.subheader("👤 Distribuição de Investidores por Sexo")

sexo_contagem = (
    df_filtrado["SEXO"]
    .value_counts()
    .reset_index()
)

sexo_contagem.columns = ["SEXO", "QUANTIDADE"]

grafico_sexo = px.pie(
    sexo_contagem,
    names="SEXO",
    values="QUANTIDADE",
    hole=0.5,
    title="Distribuição por Sexo"
)

grafico_sexo.update_traces(
    textinfo="percent+label"
)

grafico_sexo.update_layout(
    height=450,
    template="plotly_dark"
)

st.plotly_chart(
    grafico_sexo,
    use_container_width=True
)

# =========================================================
# GRÁFICO 3
# INVESTIDO X ATUAL
# =========================================================

st.markdown("---")

st.subheader("📈 Evolução Patrimonial")

comparacao = pd.DataFrame({
    "Categoria": [
        "Valor Investido",
        "Valor Atual"
    ],

    "Valor": [
        total_investido,
        valor_atual
    ]
})

grafico_comparacao = px.bar(
    comparacao,
    x="Categoria",
    y="Valor",
    text="Valor",
    title="Valor Investido × Patrimônio Atual"
)

grafico_comparacao.update_traces(
    texttemplate="R$ %{text:,.2f}",
    textposition="outside"
)

grafico_comparacao.update_layout(
    height=450,
    template="plotly_dark",
    yaxis_title="Valor (R$)",
    xaxis_title="",
    showlegend=False
)

st.plotly_chart(
    grafico_comparacao,
    use_container_width=True
)

# =========================================================
# GRÁFICO 4
# RANKING DE RENTABILIDADE
# =========================================================

st.markdown("---")

st.subheader("🏆 Ranking de Rentabilidade")

ranking = (
    df_filtrado[
        [
            "NOME",
            "TIPO DE INVESTIMENTO",
            "VALOR INVESTIDO",
            "RENTABILIDADE"
        ]
    ]
    .sort_values(
        "RENTABILIDADE",
        ascending=True
    )
)

grafico_rentabilidade = px.bar(
    ranking,
    x="RENTABILIDADE",
    y="NOME",
    orientation="h",
    text="RENTABILIDADE",
    color="RENTABILIDADE",
    color_continuous_scale="Teal",
    hover_data=[
        "TIPO DE INVESTIMENTO",
        "VALOR INVESTIDO"
    ],
    title="Rentabilidade por Investidor"
)

grafico_rentabilidade.update_traces(
    texttemplate="%{text:.2%}",
    textposition="outside"
)

grafico_rentabilidade.update_layout(
    height=600,
    template="plotly_dark",
    xaxis_title="Rentabilidade",
    yaxis_title="Investidor",
    coloraxis_showscale=False
)

st.plotly_chart(
    grafico_rentabilidade,
    use_container_width=True
)

# =========================================================
# TABELA
# =========================================================

st.markdown("---")

st.subheader("📋 Base de Investidores")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)
# =========================================================
# RENDA X VALOR INVESTIDO
# =========================================================

st.markdown("---")

st.subheader("💰 Relação entre Renda e Valor Investido")

grafico_renda = px.scatter(
    df_filtrado,
    x="RENDA MENSAL",
    y="VALOR INVESTIDO",
    size="VALOR INVESTIDO",
    color="PERFIL",
    hover_name="NOME",
    hover_data=[
        "IDADE",
        "TIPO DE INVESTIMENTO",
        "RENTABILIDADE"
    ],
    title="Renda Mensal × Valor Investido"
)

grafico_renda.update_layout(
    height=550,
    template="plotly_dark",
    xaxis_title="Renda Mensal (R$)",
    yaxis_title="Valor Investido (R$)",
    legend_title="Perfil"
)

st.plotly_chart(
    grafico_renda,
    use_container_width=True
)
# =========================================================
# GRÁFICO - INVESTIMENTOS POR ESTADO
# =========================================================

st.markdown("---")

st.subheader("📍 Investimentos por Estado")

investimentos_estado = (
    df_filtrado
    .groupby("ESTADO")["VALOR INVESTIDO"]
    .sum()
    .reset_index()
    .sort_values("VALOR INVESTIDO", ascending=False)
)

grafico_estado = px.bar(
    investimentos_estado,
    x="ESTADO",
    y="VALOR INVESTIDO",
    text="VALOR INVESTIDO",
    title="Valor Total Investido por Estado"
)

grafico_estado.update_traces(
    texttemplate="R$ %{text:,.0f}",
    textposition="outside"
)

grafico_estado.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Estado",
    yaxis_title="Valor Investido (R$)",
    showlegend=False
)

st.plotly_chart(
    grafico_estado,
    use_container_width=True
)

# =========================================================
# GRÁFICO 8 - INVESTIMENTOS POR CIDADE
# =========================================================

st.markdown("---")
st.subheader("🌆 Ranking de Investimentos por Cidade")

investimentos_cidade = (
    df_filtrado
    .groupby("CIDADE", as_index=False)
    .agg(
        Total_Investido=("VALOR INVESTIDO", "sum"),
        Quantidade_Investidores=("ID", "count"),
        Patrimonio_Atual=("VALOR ATUAL", "sum")
    )
    .sort_values("Total_Investido", ascending=False)
)

grafico_cidade = px.bar(
    investimentos_cidade,
    x="CIDADE",
    y="Total_Investido",
    color="Total_Investido",
    text="Total_Investido",
    hover_data=[
        "Quantidade_Investidores",
        "Patrimonio_Atual"
    ],
    color_continuous_scale="Teal",
    title="Cidades com Maior Volume de Investimentos"
)

grafico_cidade.update_traces(
    texttemplate="R$ %{text:,.2f}",
    textposition="outside"
)

grafico_cidade.update_layout(
    height=500,
    template="plotly_dark",
    xaxis_title="Cidade",
    yaxis_title="Total Investido (R$)",
    coloraxis_showscale=False
)

st.plotly_chart(
    grafico_cidade,
    use_container_width=True
)


# =========================================================
# GRÁFICO 9 - DISTRIBUIÇÃO POR IDADE
# =========================================================

st.markdown("---")
st.subheader("🎂 Perfil Etário dos Investidores")

grafico_idade = px.histogram(
    df_filtrado,
    x="IDADE",
    nbins=10,
    color_discrete_sequence=["#14b8a6"],
    title="Distribuição de Investidores por Idade"
)

grafico_idade.update_layout(
    height=450,
    template="plotly_dark",
    xaxis_title="Idade",
    yaxis_title="Quantidade de Investidores",
    bargap=0.10
)

st.plotly_chart(
    grafico_idade,
    use_container_width=True
)
# =========================================================
# GRÁFICO - LUCRO POR TIPO DE INVESTIMENTO
# =========================================================

st.markdown("---")
st.subheader("💹 Resultado Financeiro por Investimento")

lucro_tipo = (
    df_filtrado
    .groupby("TIPO DE INVESTIMENTO", as_index=False)
    .agg(
        Investido=("VALOR INVESTIDO", "sum"),
        Atual=("VALOR ATUAL", "sum")
    )
)

lucro_tipo["LUCRO"] = (
    lucro_tipo["Atual"] - lucro_tipo["Investido"]
)

grafico_lucro = px.bar(
    lucro_tipo,
    x="TIPO DE INVESTIMENTO",
    y="LUCRO",
    color="LUCRO",
    text="LUCRO",
    color_continuous_scale="Teal",
    title="Lucro ou prejuízo por tipo de investimento"
)

grafico_lucro.update_traces(
    texttemplate="R$ %{text:,.2f}",
    textposition="outside"
)

grafico_lucro.update_layout(
    height=450,
    template="plotly_dark",
    xaxis_title="Tipo de Investimento",
    yaxis_title="Resultado Financeiro (R$)",
    coloraxis_showscale=False
)

st.plotly_chart(
    grafico_lucro,
    use_container_width=True
)

# =========================================================
# TABELA - RESUMO POR TIPO DE INVESTIMENTO
# =========================================================

st.markdown("---")
st.subheader("📊 Resumo Estratégico por Investimento")

resumo_investimentos = (
    df_filtrado
    .groupby("TIPO DE INVESTIMENTO", as_index=False)
    .agg(
        Investidores=("ID", "count"),
        Total_Investido=("VALOR INVESTIDO", "sum"),
        Patrimonio_Atual=("VALOR ATUAL", "sum"),
        Rentabilidade_Media=("RENTABILIDADE", "mean")
    )
)

resumo_investimentos["Resultado_Financeiro"] = (
    resumo_investimentos["Patrimonio_Atual"]
    - resumo_investimentos["Total_Investido"]
)

resumo_investimentos = resumo_investimentos.sort_values(
    "Total_Investido",
    ascending=False
)

resumo_exibicao = resumo_investimentos.rename(columns={
    "TIPO DE INVESTIMENTO": "Tipo de Investimento",
    "Investidores": "Quantidade de Investidores",
    "Total_Investido": "Total Investido (R$)",
    "Patrimonio_Atual": "Patrimônio Atual (R$)",
    "Rentabilidade_Media": "Rentabilidade Média",
    "Resultado_Financeiro": "Resultado Financeiro (R$)"
})

st.dataframe(
    resumo_exibicao.style.format({
        "Total Investido (R$)": "R$ {:,.2f}",
        "Patrimônio Atual (R$)": "R$ {:,.2f}",
        "Rentabilidade Média": "{:.2%}",
        "Resultado Financeiro (R$)": "R$ {:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# EXPORTAR DADOS
# =========================================================

st.markdown("---")
st.subheader("📥 Exportar Relatórios")

col_download1, col_download2 = st.columns(2)

with col_download1:
    csv_investidores = df_filtrado.to_csv(
        index=False,
        sep=";",
        decimal=","
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Baixar investidores filtrados",
        data=csv_investidores,
        file_name="smart_bank_investidores.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_download2:
    csv_resumo = resumo_exibicao.to_csv(
        index=False,
        sep=";",
        decimal=","
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Baixar resumo dos investimentos",
        data=csv_resumo,
        file_name="smart_bank_resumo_investimentos.csv",
        mime="text/csv",
        use_container_width=True
    )
# =========================================================
# EXPORTAR RELATÓRIO COMPLETO EM EXCEL
# =========================================================

import io

buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:

    df_filtrado.to_excel(
        writer,
        sheet_name="Investidores",
        index=False
    )

    resumo_exibicao.to_excel(
        writer,
        sheet_name="Resumo",
        index=False
    )

st.download_button(
    label="📊 Baixar relatório completo em Excel",
    data=buffer.getvalue(),
    file_name="Smart_Bank_Relatorio.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)
# =========================================================
# RODAPÉ
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748b;
        padding:15px;
    ">
        🏦 <b>SMART BANK</b> — Dashboard de Análise de Investimentos
        <br>
        Projeto acadêmico de Análise de Dados
    </div>
    """,
    unsafe_allow_html=True
)
