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
    def __init__(self, option_type, strike):
        self.__type = option_type
        self.__strike = strike

    def __repr__(self):
        return f'{self.__type} @ {self.__strike:.2f}'


class Call(VanillaOption):
    def __init__(self, strike):
        super().__init__('Call', strike)

    def payoff(self, terminal_price):
        return max(terminal_price - self._VanillaOption__strike, 0)


class Put(VanillaOption):
    def __init__(self, strike):
        super().__init__('Put', strike)

    def payoff(self, terminal_price):
        return max(self._VanillaOption__strike - terminal_price, 0)


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


if __name__ == '__main__':

    c = Call(10)
    print(c.payoff(28))
    p = Put(15)
    print(p.payoff(17))