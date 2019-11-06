## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

# Small binomial coefficients values: Use a direct mapping for minimal overhead.

__all__ = ["bmap"]

class memorize(dict):
  def __init__(self, func):
    self.func = func

  def __call__(self, *args):
    return self[args]

  def __missing__(self, key):
    result = self[key] = self.func(*key)
    return result

@memorize
def _binomial(n,k) :
  if n < k: return 0
  if k == 0:
    return 1
  if n == k :
    return 1
  return _binomial(n-1,k) + _binomial(n-1,k-1)

bmap = dict()
for _n in range(20) :
  for _k in range(20) :
    bmap[_n,_k] = _binomial(_n,_k)
