from numpy import array
import math

# Runge-Kutta 4th order method constants:

RK4_A = [[],
         [0.5],
         [0, 0.5],
         [0, 0, 1]]
RK4_B = array((1/6, 1/3, 1/3, 1/6))
RK4_C = array((0, 0.5, 0.5, 1))

# Euler method constants (RK order of 1):

EULER_A = [[]]
EULER_B = array(1)
EULER_C = array(0)

# 3/8 rule method constants:

TE_A = [[],
         [1/3],
         [-1/3, 1],
         [1, -1, 1]]
TE_B = array((1/8, 3/8, 3/8, 1/8))
TE_C = array((0, 1/3, 2/3, 1))

METHODS = {
    'RK4': (RK4_A, RK4_B, RK4_C),
    'EULER': (EULER_A, EULER_B, EULER_C),
    '3/8': (TE_A, TE_B, TE_C),
}

RESERVED_NAMES = {
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
