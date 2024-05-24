#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23
# необходимо организовать конвейер, в котором сначала
# в отдельном потоке вычисляется значение первой функции,
# после чего результаты вычисления должны передаваться второй функции,
# вычисляемой в отдельном потоке. Потоки для вычисления значений двух
# функций должны запускаться одновременно.


from math import cos, fabs, log, pi, sin
from threading import Barrier, Lock, Thread

EPS = 10e-7

lock = Lock()
barrier = Barrier(3)


# 11 Вариант
def sum_1(results, x):

    a = sin(x)
    S, k = a, 2
    # Найти сумму членов ряда.
    while fabs(a) > EPS:
        coef = 2 * k - 1
        a = sin(coef * x) / coef
        S += a
        k += 1

    with lock:
        results[0] = S
    barrier.wait()


# 12 Вариант
def sum_2(results, x):

    a = cos(x)
    S, k = a, 2
    # Найти сумму членов ряда.
    while fabs(a) > EPS:
        a = cos(k * x) / k
        S += a
        k += 1

    with lock:
        results[1] = S
    barrier.wait()


def show_results(results):
    barrier.wait()
    with lock:
        sum1, sum2 = results[0], results[1]
        control_value1 = pi / 4
        control_value2 = -log(2 * sin(pi / 2))

        print(f"x1 = {pi/2}")
        print(f"Сумма ряда 1: {round(sum1, 4)}")
        print(f"Контрольное значение ряда 1: {round(control_value1, 4)}")
        print(f"Проверка 1: {round(sum1, 4) == round(control_value1, 4)}")

        print(f"x2 = {pi}")
        print(f"Сумма ряда 2: {round(sum2, 4)}")
        print(f"Контрольное значение ряда 2: {round(control_value2, 4)}")
        print(f"Проверка: {round(sum2, 4) == round(control_value2, 4)}")


def main():
    part_of_rows = [0, 0]

    th1 = Thread(target=sum_1, args=(part_of_rows, pi / 2))
    th2 = Thread(target=sum_2, args=(part_of_rows, pi))
    th3 = Thread(target=show_results, args=(part_of_rows,))

    th1.start()
    th2.start()
    th3.start()


if __name__ == "__main__":
    main()
