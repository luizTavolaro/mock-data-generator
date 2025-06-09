import pandas as pd
import numpy as np
from fastapi import FastAPI
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI()

class RequestData(BaseModel):
    data_inicio: str
    quantidade_dias: int
    lim_inf: Tuple[float, float]
    lim_sup: Tuple[float, float]
    var: Tuple[float, float]

def gerar_dias_uteis_por_quantidade(data_inicio, quantidade_dias):
    data_inicio_format = datetime.strptime(data_inicio, '%Y-%m-%d')
    dias_semana = []
    contador = 0
    dias_adicionados = 0

    while dias_adicionados < quantidade_dias:
        data_atual = data_inicio_format + timedelta(days=contador)
        if data_atual.weekday() < 5:
            dias_semana.append(data_atual)
            dias_adicionados += 1
        contador += 1

    return dias_semana

def gerar_dados(data, lim_inf, lim_sup, var):

    x = np.arange(1, 7)

    if isinstance(data, str):
        data = datetime.strptime(data, '%Y-%m-%d')

    noise =  np.random.uniform(var[0],var[1],len(x)).ravel()

    y_manha = -0.0025*x**4 + 0.0625*x**3 - 0.4445*x**2 + 1.2214*x - 1.0191
    y_manha =  pd.DataFrame(y_manha*noise)

    y_tarde = -0.0011*x**6 + 0.0396*x**5 - 0.5856*x**4 + 4.4158*x**3 - 17.815*x**2 + 35.943*x - 21.982
    y_tarde =  pd.DataFrame(y_tarde*noise)

    y_noite = -0.0003*x**6 + 0.012*x**5 - 0.1995*x**4 + 1.6801*x**3 - 7.5303*x**2 + 16.703*x - 10.637
    y_noite =  pd.DataFrame(y_noite * noise)

    y = pd.concat([y_manha, y_tarde, y_noite], axis=0)

    hora = np.arange(7,25)

    df = pd.DataFrame({
        'Hora': hora,
        'Consumo': y[0].values
    })

    df['Dia_da_Semana'] = data.strftime('%A')

    return df


@app.post("/")
def get_data(request: RequestData):
    dias_uteis = gerar_dias_uteis_por_quantidade(request.data_inicio, request.quantidade_dias)
    lista_dataframes = []
    for dia in dias_uteis:
        df_dia = gerar_dados(dia, request.lim_inf, request.lim_sup, request.var)
        lista_dataframes.append(df_dia)

    df_final = pd.concat(lista_dataframes, ignore_index=True)

    return df_final.to_json()
