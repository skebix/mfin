# -*- coding: utf-8 -*-
"""
Problem Set 4
"""

from math import exp, sqrt
from random import gauss, seed


class EuroDerivative:
    def get_price(self, s0, rfr, volatilidad, plazo, simulaciones, sd=None):
        pass

    def plot_payoff(self, min, max):
        pass


class Strategy(EuroDerivative):

    def __init__(self, name):
        self.__name = name
        self.__options = []

    def __repr__(self):
        pos = '\n'.join(f'{"Long" if q > 0 else "Short":5} {abs(q)} {o}'
                        for q, o in self.__options)
        return '\n'.join([f'Strategy: {self.__name}', '-' * 20, pos, '-' * 20])

    def add_position(self, cantidad, opcion):
        self.__options.append((cantidad, opcion))

    def payoff(self, terminal_price):
        pass


class VanillaOption(EuroDerivative):
    def __init__(self, option_type, strike):
        self._type = option_type
        self._strike = strike

    def __repr__(self):
        return f'{self._type} @ {self._strike:.2f}'


class Call(VanillaOption):
    def __init__(self, strike):
        super().__init__('Call', strike)

    def payoff(self, price):
        return price - self._strike if price > self._strike else 0


class Put(VanillaOption):
    def __init__(self, strike):
        super().__init__('Put', strike)

    def payoff(self, price):
        return self._strike - price if self._strike > price else 0


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

    strategy = Strategy('Butterfly')
    strategy.add_position(1, Call(10))
    strategy.add_position(-2, Call(12))
    strategy.add_position(1, Call(14))
    print(strategy)

    # price = strategy.get_price(10, 0.05, 0.15, 180, 100000, 123)
    # print(price)
