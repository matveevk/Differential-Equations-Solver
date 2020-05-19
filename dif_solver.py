import math
from parse import parse
from typing import Sequence
import numpy as np
from matplotlib.pyplot import show, plot, title


# DifSolver class solves differential equation
# stated as in Cauchy problem (e. g. y' = x^2y, y(0.5) = 20)
# using The Runge–Kutta method
# (see https://en.wikipedia.org/wiki/Runge-Kutta_methods)


class DifSolver:

    """
    - derivative - derivative derivative (e. g. lambda (x, y): x^2 * y)
    - condition - pair of condition values (x0, y0), so y(x0) = y0
    - func_name - name of the function variable (e. g. 'y')
    - var_name - name of the respect-variable (e. g. 'x')
    - raw - pair of strings with initial equation
                    and condition (e. g. y' = x^2y, y(0.5) = 20)
    """

    def __init__(self, equation: str, condition: str):
        """
        :param equation: string, format of either dy/dx = x^2y, or y' = x^2 * y
        :param condition: string, format of y(0.5) = 20
        Note: function name and variable should be a single latin letter each
        """
        equation = equation.replace(' ', '')
        condition = condition.replace(' ', '')
        self.raw = [equation, condition]

        self.func_name, self.var_name = self.parse_name(equation)
        self.derivative = self.parse_derivative(equation)
        self.condition = self.parse_condition(condition)

    def solve(
            self,
            step: float = 0.01,
            order: int = 4,
            breadth: float = 10,
            a: Sequence[Sequence[float]] = [[],
                                            [0.5],
                                            [0, 0.5],
                                            [0, 0, 1]],
            b: Sequence[float] = np.array((1/6, 1/3, 1/3, 1/6)),
            c: Sequence[float] = np.array((0, 0.5, 0.5, 1)),
            visualize: bool = False
    ):
        """
        :param step: parameter of method
        :param order: number of stages
        :param breadth: how much of x-axis to calculate
        :param a: Runge–Kutta matrix
        :param b: weights
        :param c: nodes
        :param visualize: shows plt graph if True
        :return: returns pair of lists (x, y) such that y_i = y(x_i)
        Note indexing (0 to order-1)
        """

        xs = np.arange(self.condition[0], self.condition[0] + breadth, step)
        ys = np.zeros(len(xs))
        ys[0] = self.condition[1]

        for i, x in enumerate(xs[1:], start=1):
            k = np.zeros(order)
            for j in range(order):
                x_par = xs[i - 1] + step * c[j]
                y_par = ys[i - 1] + step * np.dot(a[j], k[:j])
                k[j] = self.derivative(x_par, y_par)

            ys[i] = ys[i - 1] + step * np.dot(b, k)

        if visualize:
            plot(xs, ys)
            title(self.raw)
            show()
        return xs, ys

    def parse_name(self, equation: str):
        """
        :param equation: string, format of either dy/dx = x^2y, or y' = x^2 * y
        :return: pair of letters matching function and variable (e. g. ('y', 'x'))
        """
        r1 = parse('d{}/d{}={}', equation, case_sensitive=True)
        r2 = parse('{}\'={}', equation, case_sensitive=True)
        if r1 is not None:
            return r1.fixed[:2]
        elif r2 is not None:
            func_name = r2.fixed[0]
            derivative = r2.fixed[1]
            for name in sorted(self.reserved_names.keys(), key=len, reverse=True):
                derivative = derivative.replace(name, '')
            for ch in derivative:
                if ch.isalpha() and ch != func_name:
                    return func_name, ch
            return func_name, ('x' if func_name != 'x' else 't')
        raise ValueError('Wrong equation input format for ' + equation)

    def parse_derivative(self, equation: str):
        """
        :param equation: string, format of either dy/dx = x^2*y, or y'=x^2*y
        :return: lambda-function corresponding to input
        """
        func = equation.split('=')[1]
        func = func.replace('^', '**')

        # TODO: surround vars with * (2a -> 2*a; xcos(y) -> x*cos(y))

        return lambda t, f: eval(func,
                                 {self.func_name: f, self.var_name: t},
                                 self.reserved_names)

    @staticmethod
    def parse_condition(condition: str):
        """
        :param condition: string, format of y(0.5)=20
        :return:
        """
        return tuple(map(float, parse('{}({})={}', condition, case_sensitive=True).fixed[1:]))

    def __str__(self):
        return 'raw: {}\nfunc_name: {}, var_name: {}, condition: {}({}) = {}'.format(
            self.raw, self.func_name, self.var_name, self.func_name,
            self.condition[0], self.condition[1]
        )

    reserved_names = {
        'cos': math.cos,
        'sin': math.sin,
        'sqrt': math.sqrt,
        'fact': math.factorial,
        'log': math.log,
        'ln': math.log,
        'log10': math.log10,
        'tan': math.tan,
        'tg': math.tan,
        'ctg': lambda x: 1 / math.tan(x),
        'cot': lambda x: 1 / math.tan(x),
        'arcsin': math.asin,
        'asin': math.asin,
        'arccos': math.acos,
        'acos': math.acos,
        'arctan': math.atan,
        'arctg': math.atan,
        'atan': math.atan,
        'arcctg': lambda x: math.atan(1 / x),
        'arccot': lambda x: math.atan(1 / x),
        'acot': lambda x: math.atan(1 / x),
        'pi': math.pi,
        'e': math.e,
        # TODO: add Hyperbolic functions, Abs, Floor, Ceil, Sign, Logarithms
    }


if __name__ == '__main__':
    cosxy = 'cos(x)*y'
    xp1 = '2*x+1'

    foo = xp1

    equation = 'dy/dx = ' + foo
    condition = "y(0) = 2"
    ds = DifSolver(equation, condition)
    ds.solve()

    equation = "y' = " + foo
    condition = "y(0) = 2"
    DifSolver(equation, condition).solve(visualize=True)

    print(ds)
