# -*- coding: utf-8 -*-
"""
Problem Set 4
"""

from math import exp, sqrt
from matplotlib.pyplot import plot
from random import gauss, seed


class EuroDerivative:
    def get_price(self, s0, rfr, volatilidad, plazo, simulaciones, sd=None):
        """
        El precio del derivado, calculado con simulaciones Monte Carlo, cada
        precio es parte del path de una GBM.
        Parámetros:
            s0           : Precio inicial del activo subyacente
            rfr          : Tasa libre de riesgo de capitalización contínua
            volatilidad  : Diaria anualizada de capitalización contínua
            plazo        : En días
            simulaciones : Cantidad de precios a simular
            sd           : Semilla para el generador de números de random
        """
        seed(sd)
        tv = sum(self.payoff(sim_gbm(s0, rfr, volatilidad, plazo))
                 for _ in range(simulaciones))
        return tv * exp(-rfr * plazo / 365.0) / simulaciones

    def plot_payoff(self, min, max):
        """
        Muestra el gráfico de payoffs entre dos precios determinados.
        Parámetros:
            min: int, precio mínimo menor al strike más pequeño de las opciones
            max: int, precio máximo mayor al strike más grande de las opciones
        """
        pr = range(min * 2, max * 2 + 1)
        plot([p / 2 for p in pr], [self.payoff(p / 2) for p in pr])


class Strategy(EuroDerivative):
    def __init__(self, name):
        """
        Inicializo una estrategia con cierto nombre y sin opciones.
        """
        self.__name = name
        self.__options = []

    def __repr__(self):
        pos = '\n'.join(f'{"Long" if q > 0 else "Short":5} {abs(q)} {o}'
                        for q, o in self.__options)
        return '\n'.join([f'Strategy: {self.__name}', '-' * 20, pos, '-' * 20])

    def add_position(self, cantidad, opcion):
        """
        Agrego cantidad de opciones a mi estrategia.
        Parámetros:
            cantidad: int, positivo si es Long o negativo si es un Short
            opcion  : Call o Put, con cierto strike price
        """
        self.__options.append((cantidad, opcion))

    def payoff(self, market_price):
        """
        El payoff de la estrategia es la suma de los payoff de sus opciones
        Parámetros:
            market_price: El precio de mercado en el día del ejercicio
        """
        return sum(q * opt.payoff(market_price) for q, opt in self.__options)


class VanillaOption(EuroDerivative):
    def __init__(self, option_type, strike):
        """
        Inicializa la opción con un tipo (call o put) y el strike
        """
        self._type = option_type
        self._strike = strike

    def __repr__(self):
        return f'{self._type} @ {self._strike:.2f}'


class Call(VanillaOption):
    def __init__(self, strike):
        """
        Usa el constructor de VanillaOption para inicializar un Call con strike
        """
        super().__init__('Call', strike)

    def payoff(self, price):
        """
        Calcula el payoff del Call, si el precio del mercado es menor o igual
        al strike, no se ejerce la opción, siendo 0 el payoff
        Parámetros:
            price : Precio de mercado del activo subyacente
        """
        return price - self._strike if price > self._strike else 0


class Put(VanillaOption):
    def __init__(self, strike):
        """
        Usa el constructor de VanillaOption para inicializar un Put con strike
        """
        super().__init__('Put', strike)

    def payoff(self, price):
        """
        Calcula el payoff del Put, si el precio del mercado es mayor o igual al
        strike, no se ejerce la opción, siendo 0 el payoff
        Parámetros:
            price : Precio de mercado del activo subyacente
        """
        return self._strike - price if self._strike > price else 0


def sim_gbm(s0, drift, sigma, plazo):
    """
    Simula precio terminal de un Geometric Brownian Motion al cabo de un plazo.
    Parámetros:
        s0    : Precio inicial del stock
        drift : Drift (Tasa diaria anualizada / Cap. contínua)
        sigma : Volatidad (Diaria anualizada / Cap. contínua)
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

    strategy.plot_payoff(9, 15)

    params = {'s0': 10, 'rfr': 0.05, 'volatilidad': 0.15,
              'plazo': 180, 'simulaciones': 100000, 'sd': 123}
    strategy_price = strategy.get_price(**params)
    print("The price for this strategy is", strategy_price)
