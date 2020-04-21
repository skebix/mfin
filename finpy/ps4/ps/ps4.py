# -*- coding: utf-8 -*-
"""
Problem Set 4
"""

from math import exp, sqrt
from random import gauss


class EuroDerivative:
    def get_price(self, s0, rfr, volatilidad, plazo, simulaciones, seed=None):
        pass

    def plot_payoff(self, min, max):
        pass


class Strategy(EuroDerivative):
    def __init__(self, name):
        pass

    def __repr__(self):
        pass


class VanillaOption(EuroDerivative):
    def __init__(self, type, strike):
        pass

    def __repr__(self):
        pass


class Call(VanillaOption):
    def __init__(self, strike):
        pass

    def payoff(self, terminal_price):
        pass


class Put(VanillaOption):
    def __init__(self, strike):
        pass

    def payoff(self, terminal_price):
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
