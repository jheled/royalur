## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

"""
=============================
Human-like Players for ROGOUR
=============================

Human-like players are built upon the basic core principles of ROGOUR: hitting,
not getting hit, extra moves and bearing off. Such core principles (or
strategies) are captured in a *move filter*. A move filter takes a set of
positions (all possible moves for some position and dice in our case), and
filters out undesirable positions. It may filter none at all or all but one. For
example :py:func:`hitAny` keeps the positions with the highest number of pieces
in the opponents home, and so effectively prefers positions with hits over
positions without hits.

More advanced players are built on top of those core principles by creating a
*compound filter*, which is a list of core filters which are executed in
order, from first to last.
"""
from __future__ import absolute_import

import random

from .urcore import homes, GR_OFF, RD_OFF, reverseBoard

__all__ = ["bestHumanStrategySoFar"]

def prHit(board) :
  """ Probability that Green (to move) will hit a Red piece.

  'Optimized' for speed.
  """

  hitsOn = [False]*4
  for i in range(4,12) :
    if board[i] == -1 and i != 7:
      for pips in (1,2,3,4) :
        if board[i-pips] == 1:
          hitsOn[pips-1] = True
  return sum([p for h,p in zip(hitsOn, (4,6,4,1)) if h])/16.
      
def totPips1s(board) :
  """ Total pip count for green. """
  tot = 0
  for i in range(14):
    if board[i] == 1:
      tot += 14 - i
  tot += 15*homes(board)[0]
  return tot

def totPips2s(board) :
  """ Total pip count for both sides. """
  
  tot, totG, totR = 0,0,0
  for i in range(14):
    v = board[i]
    if v != 0:
      tot += 14 - i
      if v == 1:
        totG += 1
      else:
        totR += 1
  for i in (15,16,17,18):
    if board[i] == -1 :
      tot += 29 - i
      totR += 1
  for i in (19,20):
    if board[i] == -1 :
      tot += 21 - i
      totR += 1
  tot += 15*(7 - (board[14] + totG) + 7 - (board[21] + totR))

  return tot
  
## Donkey
def greedyExtraTurn(moves) :
  """ Prefer moves which give an extra move. """
  
  return  [(b,e) for b,e in moves if e] or moves

## Extra
def greedyExtraTurnPlus(moves) :
  """ Prefer moves which give an extra move and have the highest probability of hitting an opponent
  piece on the next move.
  """
  
  we = [(b,e) for b,e in moves if e]
  if we:
    wp = [(prHit(b),b,e) for b,e in we]
    mp = max(wp)[0]
    moves = [(b,e) for p,b,e in wp if p == mp]

  return moves

## bear  
def greedyOff(moves) :
  """ Prefer moves which bear-off a piece. """
  we = [(b[GR_OFF if e else RD_OFF],b,e) for b,e in moves]
  mo = max(we)[0]
  return [(b,e) for o,b,e in we if mo == o]

## hit
def hitAny(moves) :
  """ Prefer moves which hit enemy pieces. """
  a = [(homes(b)[1 if e else 0],b,e) for b,e in moves]
  v = max(a)[0]
  return [(b,e) for h,b,e in a if h == v]

## Chuck
def hitAdvanced(moves) :
  """ Prefer moves which increase opponent pip total. """
  a = [(totPips1s(reverseBoard(b) if e else b),b,e) for b,e in moves]
  v = max(a)[0]
  return [(b,e) for h,b,e in a if h == v]

## Frank
def minHitPr(moves) :
  """ Prefer moves which lower the probability of getting hit """
  wp = [(prHit(b if not e else reverseBoard(b)),b,e) for b,e in moves]
  mp = min(wp)[0]
  return [(b,e) for p,b,e in wp if p == mp]

## safe
def protected(moves) :
  """ Prefer moves with a piece on protected square. """
  return [(b,e) for b,e in moves if b[7] == (1 if e else -1)] or moves

## homestretch
def safety(moves) :
  """ Prefer moves with put more pieces on the homestretch (yz) for safety."""
  
  a1 = [(sum(b[12:15]) if e else (-sum(b[19:21])+b[21]),b,e) for b,e in moves]
  m = max(a1)[0]
  return [(b,e) for c,b,e in a1 if c == m]

def greenAtHome(board) :
  gOnBoard = sum([i == 1 for i in board[0:14]])
  gTotInPlay = 7 - board[GR_OFF]
  return gTotInPlay - gOnBoard
  
def enter(moves) :
  """ Give preference to add another piece to the board. """
  mvs = [(greenAtHome(b),(b,e)) for b,e in moves]
  m = min(mvs)[0]
  return [be for g,be in mvs if g == m]

strategies = [greedyExtraTurn, greedyExtraTurnPlus, greedyOff, hitAny, hitAdvanced, minHitPr,
              protected, safety, enter]

nicks = ["Donkey", "Extra", "bear", "hit", "Chuck", "Frank", "safe", "homestretch", "party"]

def getByNicks(spec) :
  ns = [strategies[nicks.index(nick)] for nick in spec.split(';')]
  return lambda m: chainFilt(m, ns)
  
def chainFilt(moves, chain) :
  """ A compound filter: apply all filters in ``chain`` in order. """
  
  for c in chain:
    moves = c(moves)
    if len(moves) == 1:
      return moves
  return moves

bestHumanStrategySoFar = lambda m: chainFilt(m, [strategies[i] for i in (3, 6, 1, 8, 2, 7, 5, 4, 0)])
##(3, 1, 6, 5, 2, 4, 0, 7)])

#  LocalWords:  ROGOUR
