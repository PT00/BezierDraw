import numpy as np


def bezier_curve(points, num=200):
    n = len(points) - 1
    return np.array([sum([comb(n, i) * (1 - t)**(n - i) * t**i * np.array(points[i]) for i in range(n + 1)]) for t in np.linspace(0, 1, num)])

def comb(n, k):
    return np.math.factorial(n) // (np.math.factorial(k) * np.math.factorial(n - k))
