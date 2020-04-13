"""
Problem Set 1
"""

from math import exp, sqrt
from random import gauss, seed


def crear_gmb(precio_inicial, media, volatilidad):
    """
    Crea un generador de valores de un Geometric Brownian Motion.
    """
    precio_simulado = precio_inicial

    def generador_precio():
        """
        Dado el precio t-1, la media y volatilidad, retorna el siguiente valor
        de un Geometric Brownian Motion.
        """
        nonlocal precio_simulado
        drift = media - pow(volatilidad, 2) / 2
        dt = 1 / 365
        incremento_browniano = volatilidad * sqrt(dt) * gauss(0, 1)
        precio_simulado *= exp(drift * dt + incremento_browniano)
        return precio_simulado
    return generador_precio


if __name__ == '__main__':

    seed(1234)
    generar_precio = crear_gmb(100, 0.1, 0.05)

    for i in range(1000):
        precio_simulado = generar_precio()
        if precio_simulado >= 130:
            print(i, 'Target alcanzado. Toma de Ganancia.')
            break
        else:
            print(i, 'Target no alcanzado.')
        print(precio_simulado)
    print(precio_simulado)
