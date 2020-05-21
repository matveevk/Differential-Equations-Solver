# Differential-Equations-Solver
Solver for Initial value problem implementing The Runge–Kutta method.

See details of the method: https://en.wikipedia.org/wiki/Runge-Kutta_methods

## In Russian (русский):
Класс, решающий ОДУ Коши: `DifSolver` в файле `dif_solver.py`. Класс содержит описание методов.

### Примеры использования
Нарисовать график методом Рунге-Кутты 4-го порядка:
```
simple_rk4 = DifSolver("dy/dt = 2 * (t+1)", "y(0) = 1")
simple_rk4.solve(visualize=True)
```
Нарисовать график методом Эйлера, от 1 до 21 на оси абцисс, с шагом 0.02:
```
simple_euler = DifSolver("y' = 2 * (t+1)", "y(1) = 2")
simple_euler.solve(visualize=True, method='EULER', breadth=20, step=0.02)
```
Получить значения функции с пользовательскими параметрами метода. 

`a` — матрица Бутчера

`b` — нижняя строка таблицы Бутчера (веса коэффициентов рекурренты)

`c` — левый столбец таблицы Бутчера (прирост абцисс в пересчёте коэффициентов)
```
custom = DifSolver("y' = y * x, y(0) = 0")
xs, ys = custom.solve(a=[[], [2/3]], b=[1/4, 3/4], c=[0, 2/3])
# печатаем полученные значения:
print(('y({}) = {}'.format(xs[i], ys[i]) for i in range(len(xs)))
```

## In English:
*TODO*
