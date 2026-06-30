import re
from datetime import datetime, timedelta

import pandas as pd


def montar_objeto(arquivo):

    df = pd.read_excel(
        arquivo,
        header=None
    )

    # ----------------------------
    # Período
    # ----------------------------

    texto_periodo = str(df.iloc[2, 25])

    match = re.search(
        r'(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})',
        texto_periodo
    )

    if not match:
        raise Exception("Período não encontrado na célula Z3.")

    data_inicio = datetime.strptime(
        match.group(1),
        "%Y-%m-%d"
    ).date()

    data_fim = datetime.strptime(
        match.group(2),
        "%Y-%m-%d"
    ).date()

    dados = {}

    linha = 4

    while linha < len(df):

        # Verifica se ainda existe um bloco completo
        if linha + 2 >= len(df):
            break

        linha_dias = linha + 1
        linha_horas = linha + 2

        # ID do funcionário
        id_bruto = df.iloc[linha, 3]

        if pd.isna(id_bruto):
            linha += 3
            continue

        funcionario_id = int(float(id_bruto))

        nome = df.iloc[linha, 11]

        if pd.isna(nome):
            funcionario_nome = ""
        else:
            funcionario_nome = str(nome).replace("Nome:", "").strip()

        data_atual = data_inicio

        # Colunas B até a última existente
        for coluna in range(1, df.shape[1]):

            dia_planilha = df.iloc[linha_dias, coluna]

            if pd.isna(dia_planilha):
                data_atual += timedelta(days=1)
                continue

            # Caso não exista linha de horários
            if linha_horas >= len(df):
                horarios = ""
            else:
                horarios = df.iloc[linha_horas, coluna]

            lista_horarios = []

            if not pd.isna(horarios):

                for hora in str(horarios).split("\n"):

                    hora = hora.strip()

                    if not hora:
                        continue

                    # Remove segundos (08:30:00 -> 08:30)
                    if len(hora) >= 8:
                        hora = hora[:5]

                    lista_horarios.append(hora)

            if coluna not in dados:

                dados[coluna] = {
                    "coluna": coluna,
                    "dia": int(float(dia_planilha)),
                    "data": data_atual.strftime("%Y-%m-%d"),
                    "funcionarios": []
                }

            if lista_horarios:

                dados[coluna]["funcionarios"].append({
                    "id": funcionario_id,
                    "nome": funcionario_nome,
                    "horarios": lista_horarios
                })

            data_atual += timedelta(days=1)

        linha += 3

    return {
        "periodo": {
            "inicio": data_inicio.strftime("%Y-%m-%d"),
            "fim": data_fim.strftime("%Y-%m-%d")
        },
        "dias": dados
    }