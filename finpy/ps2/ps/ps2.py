# -*- coding: utf-8 -*-
"""
Problem Set 2
"""


def crea_shift_func(bps_short, bps_long):
    """
    Crea función desplazamiento.
    Parámetros:
        bps_short : Puntós Básicos deplazamiento en tasa 0 días (parte corta)
        bps_long  : Puntós Básicos deplazamiento en tasa 365 días (parte larga)

    NOTA: 100 Puntos Básicos = 1.00 %
    """
    def shift_func(plazo):
        """
        Devuelve la magnitud del cambio de yield para un plazo determinado.
        Parámetros:
            plazo : Plazo expresado en días.

        NOTA: Realiza interpolación lineal. De sólo uso entre 0 y 365 días.
        """
        return ((bps_long - bps_short) * (plazo / 365.) + bps_short) / 10000.

    return shift_func


def tea(precio, capital, plazo):
    """
    Calcula la TEA de una letra.
    Parámetros:
        precio  : Precio de la letra cada 100 VN.
        capital : Monto de capital que devuelve la letra cada 100 VN.
        plazo   : Plazo residual en días.
    """
    return (capital / precio) ** (365. / plazo) - 1.


def tna(precio, capital, plazo):
    """
    Calcula la TNA de una letra.
    Parámetros:
        precio  : Precio de la letra cada 100 VN.
        capital : Monto de capital que devuelve la letra cada 100 VN.
        plazo   : Plazo residual en días.
    """
    return ((capital / precio) - 1.) * (365. / plazo)


def tir(precio, capital, plazo, flag=True):
    """
    Calcula la TIR de una letra.
    Parámetros:
        precio  : Precio de la letra cada 100 VN.
        capital : Monto de capital que devuelve la letra cada 100 VN.
        plazo   : Plazo residual en días.
        flag    : bool True utiliza TIR como T.E.A. y False como T.N.A
    """
    return tea(precio, capital, plazo) if flag else tna(precio, capital, plazo)


def precio_letra(tir, capital, plazo, flag=True):
    """
    Calcula el precio de una letra.
    Parámetros:
        tir     : TIR de la letra.
        capital : Monto de capital que devuelve la letra cada 100 VN.
        plazo   : Plazo residual en días.
        flag    : bool True utiliza TIR como T.E.A. y False como T.N.A
    """
    if flag:
        return capital / (tir + 1) ** (plazo / 365)
    else:
        return capital / (tir / (365 / plazo) + 1)


def tir_promedio_ponderada(mercado, portfolio, flag=True):
    """
    Calcula la TIR promedio ponderada para un portfolio.
    Parámetros:
        mercado   : dict, keys tickers y values data (precio, capital, plazo).
        portfolio : dict, keys tickers y values weights.
        flag      : bool True utiliza TIR como T.E.A. y False como T.N.A
    """
    return sum([tir(**mercado[ticker], flag=flag) * weight
                for ticker, weight in portfolio.items()])


def plazo_promedio_ponderado(mercado, portfolio):
    """
    Calcula la duration para un portfolio.
    Parámetros:
        mercado   : dict, keys tickers y values data (precio, capital, plazo).
        portfolio : dict, keys tickers y values weights.
    """
    return sum([mercado[ticker]['plazo'] * weight
                for ticker, weight in portfolio.items()])


def total_return(mercado, portfolio, horizon, shift_func, flag=True):
    """
    Calcula el total return para un portfolio.
    Parámetros:
        mercado    : dict, keys tickers y values data (precio, capital, plazo).
        portfolio  : dict, keys tickers y values weights.
        horizon    : int, horizonte de tiempo en días.
        shift_func : función de cambio de curva, para desplazar la tir
        flag       : bool True utiliza TIR como T.E.A. y False como T.N.A
    """
    retorno_tickers = 0

    for ticker, weight in portfolio.items():
        # Tomo los datos de mercado para el ticker actual
        data = mercado[ticker]
        precio, capital, plazo = data['precio'], data['capital'], data['plazo']

        # El plazo es menor porque estoy en el horizon, la tir se desplaza
        plazo_futuro = plazo - horizon
        tir_estimada = tir(**data, flag=flag) + shift_func(plazo_futuro)
        precio_futuro = precio_letra(tir_estimada, capital, plazo_futuro)

        retorno = precio_futuro / precio - 1
        retorno_ponderado = retorno * weight
        retorno_tickers += retorno_ponderado

    return retorno_tickers


if __name__ == '__main__':
    # Importo json, cargo la data para mercado y portfolio
    import json
    data = json.load(open('data/c3_mkt_data.json'))
    mercado = data['mercado']
    portfolio = data['portfolio']

    # Creo mi función de cambio de curva, calculo tir, duration y total return
    shift_func = crea_shift_func(-500, -500)
    tir_portfolio = tir_promedio_ponderada(mercado, portfolio, True)
    plazo_portfolio = plazo_promedio_ponderado(mercado, portfolio)
    total_return_portfolio = total_return(mercado, portfolio, 15, shift_func)

    # Imprimo los stats de mi portfolio en formato de tabla
    print("Portfolio Stats:\n(valores promedio)\n-------------------")
    print(f'TIR    = {tir_portfolio:5.2%}')
    print(f'Plazo  = {plazo_portfolio:3}')
    print(f'TotRet = {total_return_portfolio:5.2%}')
