# -*- coding: utf-8 -*-
"""
Problem Set 3
"""

from finpylib.yield_curves import crea_curva, interpola_tasa


def tasa_fwd(plazo_larga, valor_larga, plazo_corta, valor_corta):
    larga = (1 + valor_larga) ** (plazo_larga / 365)
    corta = (1 + valor_corta) ** (plazo_corta / 365)
    return (larga / corta) ** (365 / (plazo_larga - plazo_corta)) - 1


def estructura_tasas_fwd(curva):
    return {round(curva[i][0] * 365):
            {round(plazo_larga * 365 - curva[i][0] * 365):
            tasa_fwd(plazo_larga, tasa_larga, curva[i][0], curva[i][1])
            for plazo_larga, tasa_larga in curva[i+1:]}
            for i in range(0, len(curva) - 1)}


def compara_futuros(spot, curva_ars, curva_usd, fx_futures):
    for ticker, data in fx_futures.items():
        mercado = data['precio']
        teorico = fx_future(spot, data['plazo'], curva_ars, curva_usd)
        diff = (mercado - teorico) * 100 / mercado
        action = "Vender" if mercado > teorico else "Comprar"
        print(f'{ticker} -> Mkt: {mercado} / Mod: {teorico} -> Dif: {diff} -> {action}')


def fx_future(spot, plazo, curva_ars, curva_usd):
    tasa_ars = 1 + interpola_tasa(curva_ars, plazo / 365)
    tasa_usd = 1 + interpola_tasa(curva_usd, plazo / 365)
    return spot * (tasa_ars / tasa_usd) ** (plazo / 365)


def pretty_print_fwd(fwd_struct):
    """
    Arma cuadro para visualizar una estructura forward.
    Parámetros:
        fwd_struct : Estructura de tasas forward
    """
    for t, fwds in fwd_struct.items():
        fwds_txt = ', '.join(f'{tt:3}: {r:6.2%}' for tt, r in fwds.items())
        print(f'{t:3}: {{', fwds_txt, '}')


if __name__ == '__main__':
    import json
    data = json.load(open('data/c4_mkt_data.json'))
    curva_ars = crea_curva(data['letras']['ARS'])
    tfars = estructura_tasas_fwd(curva_ars)
    pretty_print_fwd(tfars)
    curva_usd = crea_curva(data['letras']['USD'])
    tfusd = estructura_tasas_fwd(curva_usd)
    pretty_print_fwd(tfusd)
    compara_futuros(data['fx_spot'], curva_ars, curva_usd, data['fx_futures'])