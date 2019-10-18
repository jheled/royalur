## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#
import unittest
import random

from royalur.urcore import *

class TestCore(unittest.TestCase):

  def oneBoard(self, b) :
    self.assertEqual(code2Board(board2Code(b)), b)
    self.assertEqual(index2Board(board2Index(b)), b)
    
  def test_basic(self) :
    b = startPosition()
    self.oneBoard(b)

  def test_boards(self) :
    for _ in range(100) :
      i = random.randint(0, totalPositions-1)
      self.oneBoard(getBoard(i))

  def test_rev(self) :
    for _ in range(5000) :
      i = random.randint(0, totalPositions-1)
      b = getBoard(i)
      self.assertEqual(reverseBoard(reverseBoard(b)), b)

  def test_cov_bug(self) :
    l = bytearray(b'\x00') * totalPositions
    for r in range(7) :
      for b in positionsIterator(7,r):
        i = board2Index(b)
        self.assertEqual(l[i], 0)
        l[i] = 1
    for g in range(7) :
      for b in positionsIterator(g,7):
        i = board2Index(b)
        self.assertEqual(l[i], 0, str(i) + ',' + repr(b))
        l[i] = 1

  def test_cov_full(self) :
    l = bytearray(b'\x00') * totalPositions
    for g in range(7) :
      for r in range(7) :
        for b in positionsIterator(g,r):
          i = board2Index(b)
          self.assertEqual(l[i], 0, str(i) + ',' + repr(b))
          l[i] = 1
          self.assertEqual(index2Board(i), b, str(i) + ',' + repr(b))
    
if __name__ == '__main__':
  unittest.main()
