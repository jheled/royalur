## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the files LICENCE and gpl.txt for copying conditions.
#
import unittest

import random, sympy

from royalur.urcore import *
from royalur.urcore import nPositionsOff, bitsIterator

class TestCore(unittest.TestCase):

  def test_bititer(self) :
    for _ in range(10) :
      k = random.randint(1, 10)
      n = random.randint(k, 15)
      iall = set()
      for b in bitsIterator(k,n) :
        self.assertEqual(len(b), n)
        self.assertEqual(sum(b), k)
        self.assertTrue(tuple(b) not in iall)
        iall.add(tuple(b))
      self.assertEqual(sympy.binomial(n, k), len(iall))
      
  def test_counts(self) :
    # We'll take the larger cases on faith :)
    for g in range(7, 2, -1) :
      for r in range(7, 2, -1) :
        n = 0
        allb = set()
        for b in positionsIterator(g,r):
          n += 1
          allb.add(board2Code(b))
        self.assertEqual(nPositionsOff[g,r], n, (g,r,n,nPositionsOff[g,r]))
        self.assertEqual(len(allb), n, (g,r,n,len(allb)))

if __name__ == '__main__':
  unittest.main()
        
