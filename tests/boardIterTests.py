## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the files LICENCE and gpl.txt for copying conditions.
#
import unittest

from royalur.urcore import *
from royalur.urcore import nPositionsOff

class TestCore(unittest.TestCase):

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
        
