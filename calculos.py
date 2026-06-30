from datetime import datetime, time

VALOR_ATE_9H = 100
VALOR_ACIMA_9H = 200
LIMITE_HORAS = 9


def formatar_horas(horas_decimais):

    horas = int(horas_decimais)
    minutos = round((horas_decimais - horas) * 60)

    if minutos == 60:
        horas += 1
        minutos = 0

    return f"{horas:02d}:{minutos:02d}"


def converter_data_hora(data, hora):

    if isinstance(hora, time):

        return datetime.combine(
            datetime.strptime(data, "%Y-%m-%d").date(),
            hora
        )

    hora = str(hora).strip()

    if len(hora) >= 8:
        hora = hora[:5]

    return datetime.strptime(
        f"{data} {hora}",
        "%Y-%m-%d %H:%M"
    )


def calcular_jornadas(marcacoes):

    jornadas = []

    i = 0

    while i + 1 < len(marcacoes):

        entrada = marcacoes[i]
        saida = marcacoes[i + 1]

        horas = (saida - entrada).total_seconds() / 3600

        valor = (
            VALOR_ATE_9H
            if horas <= LIMITE_HORAS
            else VALOR_ACIMA_9H
        )

        jornadas.append({
            "entrada": entrada,
            "saida": saida,
            "horas_decimal": horas,
            "horas": formatar_horas(horas),
            "valor": valor
        })

        i += 2

    return jornadas


def calcular_pagamentos(dados):

    funcionarios = {}

    for dia in dados["dias"].values():

        data = dia["data"]

        for funcionario in dia["funcionarios"]:

            fid = funcionario["id"]

            if fid not in funcionarios:

                funcionarios[fid] = {
                    "id": fid,
                    "nome": funcionario["nome"],
                    "marcacoes": []
                }

            for horario in funcionario["horarios"]:

                funcionarios[fid]["marcacoes"].append(
                    converter_data_hora(data, horario)
                )

    resultado = []

    for funcionario in funcionarios.values():

        funcionario["marcacoes"].sort()

        jornadas = calcular_jornadas(
            funcionario["marcacoes"]
        )

        resultado.append({
            "id": funcionario["id"],
            "nome": funcionario["nome"],
            "marcacoes": funcionario["marcacoes"],
            "jornadas": jornadas,
            "total": sum(
                j["valor"]
                for j in jornadas
            )
        })

    resultado.sort(
        key=lambda x: x["nome"]
    )

    return resultado