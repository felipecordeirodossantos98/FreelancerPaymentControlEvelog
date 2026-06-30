import pandas as pd
import streamlit as st

from parser import montar_objeto
from calculos import (
    calcular_pagamentos,
    calcular_jornadas
)

st.set_page_config(
    page_title="Controle de Freelancers",
    layout="wide"
)

st.title("Controle de Pagamento de Freelancers")

col1, _ = st.columns([1, 2])

with col1:

    arquivo = st.file_uploader(
        "Selecione a planilha",
        type=["xls", "xlsx"]
    )

if arquivo:

    dados = montar_objeto(arquivo)

    pagamentos = calcular_pagamentos(dados)

    col2, _ = st.columns([1, 2])

    with col2:

        st.info(
            f"{dados['periodo']['inicio']} até {dados['periodo']['fim']}"
        )

        pesquisa = st.text_input(
            "Pesquisar funcionário"
        )

    for funcionario in pagamentos:

        if (
            pesquisa
            and pesquisa.lower() not in funcionario["nome"].lower()
        ):
            continue

        if not funcionario["marcacoes"]:
            continue

        with st.container(border=True):

            st.subheader(f"👤 {funcionario['nome']}")

            marcacoes = funcionario["marcacoes"]

            if len(marcacoes) == 1:

                periodo = (
                    marcacoes[0],
                    marcacoes[0]
                )

            else:

                periodo = st.select_slider(
                    "Período",
                    options=marcacoes,
                    value=(
                        marcacoes[0],
                        marcacoes[-1]
                    ),
                    format_func=lambda dt:
                        dt.strftime("%d/%m/%Y %H:%M"),
                    key=f"slider_{funcionario['id']}"
                )

            inicio, fim = periodo

            marcacoes_filtradas = [

                m

                for m in marcacoes

                if inicio <= m <= fim

            ]

            jornadas = calcular_jornadas(
                marcacoes_filtradas
            )

            total = sum(
                j["valor"]
                for j in jornadas
            )

            st.metric(
                "Valor a Receber",
                f"R$ {total:.2f}"
            )

            tabela = []

            for jornada in jornadas:

                tabela.append({

                    "Entrada":
                        jornada["entrada"].strftime("%d/%m/%Y %H:%M"),

                    "Saída":
                        jornada["saida"].strftime("%d/%m/%Y %H:%M"),

                    "Horas":
                        jornada["horas"],

                    "Valor":
                        f"R$ {jornada['valor']:.2f}"

                })

            if tabela:

                st.dataframe(
                    pd.DataFrame(tabela),
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "Nenhuma jornada encontrada para o período selecionado."
                )