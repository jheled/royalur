## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#
from __future__ import absolute_import

import unittest

from royalur.urcore import *

class TestCore(unittest.TestCase):

  def test_i2bbug(self) :
    with self.assertRaises(ValueError) :
      getBoard(2285375536)

if __name__ == '__main__':
  unittest.main()
        
  
