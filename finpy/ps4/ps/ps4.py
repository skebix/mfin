# -*- coding: utf-8 -*-
"""
Problem Set 4
"""

from math import exp, sqrt
from random import gauss


class EuroDerivative:
    pass


class Strategy(EuroDerivative):
    pass


class VanillaOption(EuroDerivative):
    pass


class Call(VanillaOption):
    pass


class Put(VanillaOption):
    pass


def sim_gbm(s0, drift, sigma, plazo):
    """
    Simula precio terminal de un Geometric Brownian Motion al cabo de un plazo.
    Parámetros:
        s0    : Precio inicial del stock
        drift : Drift (Tasa diaria anualizada / Cap. contínua)
        sigma : Volatidad (Diara anualizada / Cap. contínua)
        plazo : Cantidad de días de plazo de la simulación
    """
    st = s0 * exp((drift - .5 * sigma * sigma) * (plazo / 365.) +
                  sigma * sqrt(plazo / 365.) * gauss(0., 1.))
    return st
