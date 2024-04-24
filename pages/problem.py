from genetic import optimize
from typing import List, Tuple
import math
import numpy as np

class Problem:

  def optimize (self, tries: int = 5, n_pop: int = 10, n_gens: int = 100):

    tried = 0

    while True:

      if tried == tries:

        raise Exception ('can not optimize this calendar')

      best, bestval = optimize (self.f, bounds = self.bounds, n_pop = n_pop, n_gens = n_gens)

      if bestval != math.inf:

        break
      else:

        tried = tried + 1

    return best, bestval

  def __init__ (self, M: int, N: int, F: List[List[List[int]]], V: List[List[Tuple[int, int]]], K: List[List[int]], Di: List[int]):

    assert (M == 1)

    def kc (x: np.ndarray, i: int):

      return np.sum ([ 0 if x [i, a] != x [i, b] else K [i][a] + K [i][b] for a in range (N) for b in range (N) ])

    def ke (x: np.ndarray, i: int):

      values = [ K [i][j] / (1 + abs (x [i, j] - V [i][j] [0])) for j in range (x.shape [1]) ]

      return np.sum ([ 0 if k >= x [i, j] else value for j, value in enumerate (values) for k in range (Di [i]) ])

    def kp (x: np.ndarray, i: int):

      return np.sum ([ (K [i][a] + K [i][b]) / (1 + abs (x [i, a] - x [i, b])) for a in range (x.shape [1]) for b in range (x.shape [1]) ])

    def f (x: np.ndarray):

      if any ([ x [i, j] in F [i][j] for i in range (M) for j in range (N) ]):

        return np.inf

      return np.sum ([ kc (x, i) + ke (x, i) + kp (x, i) for i in range (x.shape [0]) ])

    bound_l = np.array ([ [ V [i][j][0] for j in range (N) ] for i in range (M) ])
    bound_u = np.array ([ [ V [i][j][1] for j in range (N) ] for i in range (M) ])

    self.bounds = (bound_l, bound_u)
    self.f = f
