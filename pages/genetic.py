from numpy.random import rand
from numpy.random import randint
from typing import Callable, List, Tuple
import numpy as np

def cross (p1: list, p2: list, r_cross: float):

  c1, c2 = p1.copy (), p2.copy ()

  if rand () < r_cross:

    pt = randint (1, len (p1) - 2)

    c1 = p1 [:pt] + p2 [pt:]
    c2 = p2 [:pt] + p1 [pt:]

  return [ c1, c2 ]

def mutate (bitstring: str, r_muta: float):

  for i in range (len (bitstring)):

    if rand () < r_muta:

      bitstring [i] = 1 - bitstring [i]

  return bitstring

def selection (scores: List[float], pop: List[List[int]], k = 3):

  selection_ix = randint (len (pop))

  for ix in randint (0, len (pop), k - 1):

    if scores [ix] < scores [selection_ix]:

      selection_ix = ix

  return pop [selection_ix]

def optimize (f: Callable[[np.ndarray], float], bounds: Tuple[np.ndarray, np.ndarray], n_pop: int = 10, n_gens: int = 100):

  shape = bounds[0].shape
  flats = [ bound.flatten () for bound in bounds ]

  n_bits = 16
  r_cross = 0.9

  n_vars = len (bounds[0].flatten ())
  r_muta = 1.0 / (float (n_bits) * n_vars)

  def decode (bitstring) -> np.ndarray:

    decoded = [ ]
    largest = 2 ** n_bits

    for i in range (n_vars):

      start, end = i * n_bits, (i + 1) * n_bits

      sub = bitstring [start : end]
      chars = ''.join ([ str (s) for s in sub ])
      integer = int (chars, 2)

      value = round (flats [0][i] + (integer / largest) * (flats [1][i] - flats [0][i]))

      decoded.append (value)

    return np.array (decoded).reshape (shape)

  pop = [ randint (0, 2, n_bits * n_vars).tolist () for _ in range (n_pop) ]

  best, bestval = pop [0], f (decode (pop [0]))
  static = 0

  while (static < n_gens):

    scores = [ f (decode (p)) for p in pop ]
    static = 1 + static

    for p, score in zip (pop, scores):

      if score < bestval:

        best, bestval, static = p, score, 0

        #print (f' new best: f({decode (p)}) = {score}')

    children = [ ]
    selected = [ selection (scores, pop) for _ in range (n_pop) ]

    for i in range (0, n_pop, 2):

      p1, p2 = selected [i], selected [i + 1]

      for c in cross (p1, p2, r_cross):

        children.append (mutate (c, r_muta))

    pop = children

  return decode (best), bestval
