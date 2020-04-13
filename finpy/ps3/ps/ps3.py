# -*- coding: utf-8 -*-
"""
Problem Set 3
"""

from finpylib.yield_curves import crea_curva


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
    tf = estructura_tasas_fwd(curva_ars)
    pretty_print_fwd(tf)
