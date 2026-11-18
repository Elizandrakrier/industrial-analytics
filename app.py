import streamlit as st
import pandas as pd
import plotly.express as px
import io
from src.queries import carregar_dados_financeiros_producao

st.set_page_config(
    page_title="Industrial Analytics - Kari Kari", layout="wide")

st.title("Dashboard de Produção & Custos Industriais")
st.markdown("Projeto demonstrativo integrando **Dados de Chão de Fábrica com Impacto Financeiro** para a vaga de Analista de Dados Júnior.")

df = carregar_dados_financeiros_producao()

st.sidebar.header("Filtros")
linha_selecionada = st.sidebar.selectbox(
    "Selecione a Linha", ["Todas"] + list(df["linha_producao"].unique()))

if linha_selecionada != "Todas":
    df_filtrado = df[df["linha_producao"] == linha_selecionada]
else:
    df_filtrado = df

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

total_produzido = df_filtrado["qtde_produzida"].sum()
perda_total_refugo = df_filtrado["perda_financeira_refugo"].sum()
desvio_custo = df_filtrado["desvio_custo_total"].sum()
media_paradas = df_filtrado["horas_parada"].mean()

col1.metric("Total Produzido", f"{total_produzido:,.0f} un")
col2.metric("Prejuízo com Refugo", f"R$ {perda_total_refugo:,.2f}")
col3.metric("Desvio de Custo Total", f"R$ {desvio_custo:,.2f}")
col4.metric("Média Horas Parada", f"{media_paradas:.1f} h")

st.markdown("---")

st.subheader("📥 Exportação de Relatórios e Indicadores")
st.markdown(
    "Automatize o envio de relatórios gerenciais baixando os dados filtrados abaixo:")

col_exp1, col_exp2 = st.columns(2)


def converter_para_excel(df_export):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False,
                           sheet_name='Indicadores_Producao')
    return output.getvalue()


def converter_para_csv(df_export):
    return df_export.to_csv(index=False).encode('utf-8')


with col_exp1:
    excel_data = converter_para_excel(df_filtrado)
    st.download_button(
        label="📥 Baixar Relatório em Excel (.xlsx)",
        data=excel_data,
        file_name="indicadores_producao_karikari.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_exp2:
    csv_data = converter_para_csv(df_filtrado)
    st.download_button(
        label="📊 Baixar Dados para Google Sheets (.csv)",
        data=csv_data,
        file_name="dados_producao_googlesheets.csv",
        mime="text/csv"
    )

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📉 Perda Financeira por Motivo de Parada")
    fig_parada = px.bar(
        df_filtrado,
        x="motivo_parada",
        y="horas_parada",
        color="linha_producao",
        labels={"motivo_parada": "Motivo da Parada",
                "horas_parada": "Horas Paradas"}
    )
    st.plotly_chart(fig_parada, use_container_width=True)

with col_b:
    st.subheader("💰 Custo Real vs. Impacto do Refugo por Produto")
    fig_custo = px.scatter(
        df_filtrado,
        x="qtde_refugo",
        y="desvio_custo_total",
        color="produto",
        size="horas_parada",
        hover_data=["linha_producao", "data"],
        labels={"qtde_refugo": "Quantidade de Refugo",
                "desvio_custo_total": "Desvio de Custo (R$)"}
    )
    st.plotly_chart(fig_custo, use_container_width=True)

st.subheader("📋 Dados Detalhados da Operação")
st.dataframe(df_filtrado, use_container_width=True)
