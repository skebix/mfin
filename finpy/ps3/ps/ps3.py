# -*- coding: utf-8 -*-
"""
Problem Set 3
"""

from finpylib.yield_curves import crea_curva, interpola_tasa


def tasa_fwd(plazo_larga, valor_larga, plazo_corta, valor_corta):
    """
    Retorna una tasa forward expresada en términos anuales.
    Parámetros:
        plazo_larga : plazo de la tasa larga expresado en fracción días / 365
        valor_larga : valor de la tasa larga (efectiva anual)
        plazo_corta : plazo de la tasa corta expresado en fracción días / 365
        valor_corta : valor de la tasa corta (efectiva anual)
    """
    larga = (1 + valor_larga) ** (plazo_larga / 365)
    corta = (1 + valor_corta) ** (plazo_corta / 365)
    return (larga / corta) ** (365 / (plazo_larga - plazo_corta)) - 1


def estructura_tasas_fwd(curva):
    """
    Retorna un dict {plazo_dentro_de : {plazo_para_los_siguientes : tasa_fwd} }
    Parámetros:
        curva : list -> (plazo, tasa) ordenada por plazo en fracción días / 365
    """
    return {round(curva[i][0] * 365):
            {round(plazo_larga * 365 - curva[i][0] * 365):
            tasa_fwd(plazo_larga, tasa_larga, curva[i][0], curva[i][1])
            for plazo_larga, tasa_larga in curva[i+1:]}
            for i in range(0, len(curva) - 1)}


def fx_future(spot, plazo, curva_ars, curva_usd):
    """
    Retorna el precio de arbitraje teórico de un futuro FX
    Parámetros:
        spot      : tasa spot ARS/USD
        plazo     : el plazo del contrato (en días)
        curva_ars : list -> (plazo, tasa) ordenada por plazo en días / 365
        curva_usd : list -> (plazo, tasa) ordenada por plazo en días / 365
    """
    tasa_ars = 1 + interpola_tasa(curva_ars, plazo / 365)
    tasa_usd = 1 + interpola_tasa(curva_usd, plazo / 365)
    return spot * (tasa_ars / tasa_usd) ** (plazo / 365)


def compara_futuros(spot, curva_ars, curva_usd, fx_futures):
    """
    Imprime reglas de trading que exploten un potencial desarbitraje
    Parámetros:
        spot       : tasa spot ARS/USD
        curva_ars  : list -> (plazo, tasa) ordenada por plazo en días / 365
        curva_usd  : list -> (plazo, tasa) ordenada por plazo en días / 365
        fx_futures : dict -> { ticker : { precio : precio, plazo: plazo } }
    NOTA: los valores del plazo en el dict fx_futures son en días
    """
    for ticker, data in fx_futures.items():
        mercado = data['precio']
        teorico = fx_future(spot, data['plazo'], curva_ars, curva_usd)
        diff = (mercado - teorico) * 100 / mercado
        action = "Vender" if mercado > teorico else "Comprar"
        message = (
            f"{ticker} -> "
            f"Mkt: {mercado:.4f} / "
            f"Mod: {teorico:.4f} -> "
            f"Dif: {diff:.2f}% -> "
            f"{action}"
        )
        print(message)


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
    forward_structure_ars_curve = estructura_tasas_fwd(curva_ars)
    print('Forward Structure ARS Curve')
    pretty_print_fwd(forward_structure_ars_curve)
    print()

    curva_usd = crea_curva(data['letras']['USD'])
    forward_structure_usd_curve = estructura_tasas_fwd(curva_usd)
    print('Forward Structure USD Curve')
    pretty_print_fwd(forward_structure_usd_curve)
    print()

    print('FX Futures Arbitrage')
    compara_futuros(data['fx_spot'], curva_ars, curva_usd, data['fx_futures'])
