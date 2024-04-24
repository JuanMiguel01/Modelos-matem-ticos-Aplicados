from problem import Problem
from typing import Callable, Generator
import numpy as np
import time

def permutate_j (i: int, j: int = 0, maxj: int = 1):

  if j + 1 == maxj:

    for a in range (V [i][j][0], 1 + V [i][j][1]):

      yield [ a ]

  else:

    for a in range (V [i][j][0], 1 + V [i][j][1]):

      for b in permutate_j (i, j + 1, maxj):
      
        yield [ a, *b ]

def permutate_i (i: int = 0, maxi: int = 1, maxj: int = 1):

  if i + 1 == maxi:

    for a in permutate_j (i, 0, maxj = maxj):

      yield [ a ]

  else:

    for a in permutate_j (i, 0, maxj = maxj):

      for b in permutate_i (i + 1, maxi = maxi, maxj = maxj):

        yield [ a, *b ]

def realoptimize (f: Callable[[np.ndarray], float], generator: Generator[np.ndarray, None, None]):

  best, bestval = None, np.inf

  for x in map (lambda x: np.array (x), generator):

    if bestval > (z := f (x)): best, bestval = x, z

  return best, bestval

M = 1 # Número de cursos
N = 5 # Número de asignaturas
F = [[[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]] # Días no válidos para asignar pruebas (feriados, fin de semana)
V = [[(0, 5), (0, 2), (4, 10), (5, 20), (2, 10)]] # Plazos para realizar las pruebas
K = [[1, 2, 4, 3, 1]] # Carga de trabajo de las asignaturas
Di = [21] # Días del curso

def collect (laps: int = 1, n_pop = 10, n_gens = 100):

  problem = Problem (M, N, F, V, K, Di)

  best, bestval = realoptimize (problem.f, permutate_i (maxi = M, maxj = N))

  print (f'realoptimal: f({best}) = {bestval}')

  for _ in range (laps):

    begin = time.perf_counter ()
    best, bestval = problem.optimize (n_pop = n_pop, n_gens = n_gens)
    took = time.perf_counter () - begin

    print (f'optimal: f({best}) = {bestval} (took {took} seconds)')

collect (laps = 50)
