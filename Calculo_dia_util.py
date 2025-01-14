import pandas as pd
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

vdata = "05-08-2023" #Coloque a data desejada
vdias = 7 #Quantos dias Posterior/Anterior a data desejada
dap = 1 # 1 caso deseja jogar para o proximo dia util <-> 0 caso deseja o dia util anterior

def calcular_carnaval(ano):
    # Calcula a data da Páscoa para o ano fornecido
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes_pascoa = (h + l - 7 * m + 114) // 31
    dia_pascoa = ((h + l - 7 * m + 114) % 31) + 1

    # Calcula a data do Carnaval (47 dias antes da Páscoa)
    data_pascoa = date(ano, mes_pascoa, dia_pascoa)
    data_carnaval = data_pascoa - relativedelta(days=47)

    return data_carnaval


def calcula_vencimento(vdata,vdias,dap:bool):
    
    
    #ano = datetime.now().year
    #region Formatacao data
    if "-" in vdata or "_" in vdata:
            vdata =  re.sub(r"['-','_']", '/', vdata)
    
            if "//" in vdata: vdata = re.sub(r'\/\/{1,}','/',vdata)
    #endregion


    PadraoBrasileiro = re.search(r'\d{2}.\d{2}.\d{4}',vdata)
    PadraoAmericano = re.search(r'\d{4}.\d{2}.\d{2}',vdata)

    if PadraoBrasileiro != None:
        calculodata = datetime.strptime(vdata,'%d/%m/%Y') + relativedelta(days=vdias)
        ano = calculodata.year

    if PadraoAmericano != None:
        calculodata = datetime.strptime(vdata,'%Y/%m/%d') + relativedelta(days=vdias)
        ano = calculodata.year

    feriados = {    "Ano novo": date(ano,1,1), "Aniversario SP":date(ano,1,25),
                    "Carnanval" : calcular_carnaval(ano),
                    "Paixao de Cristo":date(ano,4,7), "Tiradentes":(date(ano,4,21)),
                    "Dia do Trabalho":date(ano,5,1), "Corpos Christi":date(ano,6,8),
                    "Data Magna SP":date(ano,7,9),"Independencia":date(ano,9,7),
                    "Dia das criancas":date(ano,10,12),"Proclamacao":date(ano,11,15),
                    "Consciencia Negra":date(ano,11,20),"Natal":date(ano,12,25)
                    }

    if calculodata.weekday() >= 5 or calculodata.date() in feriados.values():
        
        match calculodata.weekday():
            case 5: #Sabado
                if dap == 1:
                    calculodata = calculodata + relativedelta(days=2)
                else:
                    calculodata = calculodata - relativedelta(days=1)

            case 6 : #Domingo
                if dap == 1:
                    calculodata = calculodata + relativedelta(days=1)
                else:
                    calculodata = calculodata - relativedelta(days=2)
            case 4: #Feriado na sexta
                    if dap == 1:
                        calculodata = calculodata + relativedelta(days=3)
                    else:
                        calculodata = calculodata - relativedelta(days=1)
            case _: #Feriado na semana
                print("Feriado na semana")
                if dap == 1:
                    calculodata = calculodata + relativedelta(days=1)
                else:
                    if (calculodata).weekday() == 0:
                        print("Entrou")
                        calculodata = calculodata - relativedelta(days=3)
                    else:
                        calculodata = calculodata - relativedelta(days=1)
    print(f"Data retorno {calculodata.date()}")



print(calcula_vencimento(vdata,vdias,dap))
