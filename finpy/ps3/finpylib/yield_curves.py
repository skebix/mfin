"""
Clase 4: Trabajando con Curvas
"""
# Recuerden copiar clase3.py en la carpeta finpylib (paquete) y renombrarlo
# como calc_fin.py para que este import funcione.
from finpylib.calc_fin import tea


def crea_curva(mkt_data):
    """
    Genera lista con tuplas (plazo, tasa) para una curva ordenada por plazo.
    Parámetros:
        mkt_data : dict -> codigo: {precio, capital, plazo}
    """
    # Debajo en vez de mktData.items() uso .values() porque los códigos de las
    # letras no me interesan. Sólo me focalizao en la parte de los datos;
    # .values() sólo me devuelve los contenidos del dict, no las etiquetas.
    curva = [(ld['plazo'] / 365., tea(**ld)) for ld in mkt_data.values()]

    # Este lambda permite seleccionar para cada tupla el primer elemento que
    # en nuestro caso es el plazo; criterio por el cual quiero ordenar.
    curva.sort(key=lambda t: t[0])

    return curva


def interpola_tasa(curva, plazo_obj):
    """
    Realiza interpolación lineal de tasas a partir de datos de mercado.
    Parámetros:
        curva     : Lista de tuplas (plazo, tasa) ordenada por plazo.
        plazo_obj : Plazo para el cual se desea calcular la tasa.
    """
    if plazo_obj < curva[0][0] or plazo_obj > curva[-1][0]:
        raise RuntimeError('Plazo objetivo fuera de los datos de la curva !!!')

    # Este sum busca encontrar cuál es el elemento en la lista que es un plazo
    # inmediatamente mayor al plazo_obj. Esto se necesita para encontrar el
    # intervalo sobre el cual vamos a interpolar.
    ind_prox = sum(1 for a, b in curva if a < plazo_obj)

    # Este if retorna el resultado si justo plazo_obj coincide con alguno de
    # los puntos de la curva ya que no se necesita interpolar.
    if plazo_obj == curva[ind_prox][0]:
        return curva[ind_prox][1]

    prev, prox = curva[ind_prox - 1], curva[ind_prox]

    diff_tasa = prox[1] - prev[1]
    diff_plazo = prox[0] - prev[0]

    return prev[1] + (plazo_obj - prev[0]) / diff_plazo * diff_tasa


if __name__ == '__main__':
    import json
    from matplotlib.pyplot import scatter, plot

    data = json.load(open('data/c4_mkt_data.json'))

    # Vamos a usar de ejemplo la curva de ARS pero podría hacerse todo para la
    # curva de USD también.
    curva_ars = crea_curva(data['letras']['ARS'])

    # scatter se utiliza pasando una lista primero con los valores de x (plazo
    # de cada tasa), y luego otra lista con las y (valores de cada tasa)
    scatter([x for x, y in curva_ars], [y for x, y in curva_ars])

    # Para plot lo mismo, pero ahora vamos a crear valores interpolados para
    # todos los puntos intermedios. Uso try para controlar los potenciales
    # errores en interpola_curva.
    try:
        c_interp = [(t / 365., interpola_tasa(curva_ars, t / 365.)) for
                    t in range(14, 490)]  # 14 y 490-1 son min/max de curva_ars

        # Prueben números fuera de los límites y verán como se captura el
        # error.

    except RuntimeError as e:
        print('No se pudo completar la interpolación.')
        print(f'Error: {str(e)}')

    else:
        plot([x for x, y in c_interp], [y for x, y in c_interp])
