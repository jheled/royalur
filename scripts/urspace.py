#! /usr/bin/env python
## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

""" This script generates two binary files, seen and reached.

Reached[pos] is the shortest game-path from the starting position to *pos*. The
game-path is a path [p_0 d_0 p_1 p_1 ... d_n pos], where p_{k+1} is reached by a
legal move from p_k with dice d_k. p_o is the start position, and the path
length is n+1. (Note that for implementationm reasons the stored number is one
greater, whereas 0 is reserved for unreachable positions.

The seen is similar, only the path follows best play only, that is p_{k+1} is
the position reached from p_k by making the best move with d_k.

WARNING: This will take some time. You can download the files from XXXX.
"""
from __future__ import print_function
from __future__ import absolute_import

import os.path

from royalur import *

def main():
  db = PositionsWinProbs(os.path.join(royalURdataDir, "db16.bin"))
  ishtar = getDBplayer(db)

  if not os.path.exists(os.path.join(royalURdataDir, "iplay-levels.bin")):
    bseen = bytearray(b'\x00') * totalPositions
    bseen[board2Index(startPosition())] = 1
    tot = 1
    level = 1
    while True:
      added = 0
      for i in range(totalPositions) :
        assert bseen[i] <= level+1
        if bseen[i] == level:
          board = index2Board(i)
          if not gameOver(board):
            for dice in range(5) :
              am = allMoves(board, dice)
              mv = ishtar(am);         assert len(mv) == 1
              b,e = mv[0]
              ib = board2Index(b)
              if not bseen[ib]:
                bseen[ib] = level + 1
                added += 1
      print(level,tot,added)
      if added == 0 :
        break
      tot += added
      level += 1

    f = open(os.path.join(royalURdataDir, "iplay-levels.bin"), 'wb')
    f.write(bseen)
    f.close()
    del bseen

  if not os.path.exists(os.path.join(royalURdataDir, "ireached-levels.bin")):
    breached = bytearray(b'\x00') * totalPositions
    breached[board2Index(startPosition())] = 1
    tot = 1
    level = 1
    while True:
      added = 0
      for i in range(totalPositions) :
        assert breached[i] <= level+1
        if breached[i] == level:
          board = index2Board(i)
          if not gameOver(board):
            for dice in range(5) :
              for mv in allMoves(board, dice) :
                b,e = mv
                ib = board2Index(b)
                if not breached[ib]:
                  breached[ib] = level + 1
                  added += 1
      print(level,tot,added)
      if added == 0 :
        break
      tot += added
      level += 1

    f = open(os.path.join(royalURdataDir, "ireached-levels.bin"), 'wb')
    f.write(breached)
    f.close()
    del breached

if __name__ == "__main__":
  main()
