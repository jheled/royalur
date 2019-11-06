## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

"""
==========================
Play and rollout functions
==========================

Functions to play ROGOUR games and positions, using different strategies for X and O.
"""

__all__ = ["rollout", "getDBplayer", "ply1", "prob"]

import random

if __package__ is None or __package__ == '':
  from urcore import *
  from humanStrategies import bestHumanStrategySoFar as hplay
  from probsdb import PositionsWinProbs
else:
  from .urcore import *
  from .humanStrategies import bestHumanStrategySoFar as hplay
  from .probsdb import PositionsWinProbs

def showBoard(b) :
  """ Print board ``b`` on stdout (debug). """
  
  print(boardAsString(b))
  
def playGame(playerX = lambda x : x, playerO = lambda x : x,
             startingBoardAndSide = None, record = None) :
  """ Play one game from start to finish. Report who won.
  
  Use playerX/playerO to determine X/O moves. Use a random player if unspecified. Start at
  ``startingBoardAndSide`` if given. If ``record`` is not None fill it with a record of the game,
  each move specified as a triplet (board-code, side-to-play, pips (the dice)).

  Return last board and the side on move, i.e. the loser.
  """
  
  if startingBoardAndSide:
    b,side = startingBoardAndSide
  else :
    b,side = startPosition(), 1
  
  while not gameOver(b) :
    pips = getPips()

    if record is not None:
      record.append((board2Code(b),"OX"[side],pips))
      
    am = allMoves(b, pips);                                         assert am

    if len(am) == 1:
      m,e = am[0]
    else :
      le = (playerX if side else playerO)(am)
        
      if len(le) == 1:
        m,e = le[0]
      else :
        m,e = random.choice(le)
    
    b = m
    if not e :
      side = 1 - side
      
  if record is not None:
    record.append((board2Code(b),"OX"[side],None))
    
  return b,"OX"[side]

def showGame(record) :
  """ Print game record on stdout (debug) """
  
  nm = 1
  for board,side,pips in record:
    print(nm,": ","OX"[side] + " pips:",pips)
    nm += 1
    board = code2Board(board)
    showBoard(board if side == 1 else reverseBoard(board))
    print()

def pitStrategies(playerX, playerO, N, sEvery = -1) :
  """ Play ``N`` games games between two strategies, report number of wins for X and O. """
  Xs,Ys = 0,0    
  for k in range(N//2) :
    b,t = playGame(playerX, playerO)
    Xs += t == 'O'
    Ys += t == 'X'
    b,t = playGame(playerO, playerX)
    Xs += t == 'X'
    Ys += t == 'O'
    if sEvery > 0 and (k % sEvery == 0):
      print(Xs,Ys)
      
  return Xs,Ys

# A default player when there is nothing else. 

def getDBmove(moves, db) :
  """ Get best move among ``moves`` according to DB. Fallback to human-like player if necessary. """
  
  if not db :
    return hplay(moves)
    
  mvs = [(db.aget(b),b,e) for b,e in moves]
  if not all([p is not None for p,b,e in mvs]) :
    return hplay(moves)
    
  p,b,e = max([(p if e else 1 - p,b,e) for p,b,e in mvs])
  return [(b,e)]

def getDBplayer(db) :
  """ Return a player using probabilities from ``db``.
  
  Fall back to default human player if position has no DB entry.
  """
  
  if isinstance(db, str) :
    db = PositionsWinProbs(db)

  return lambda moves : getDBmove(moves, db)
  
def rolloutPlay(b, side, playerX = hplay, playerO = hplay, evaluator = None) :
  """ Play ``b`` to completion. Report who won.
  
  Use playerX/playerO to determine X/O moves. If unspecified, use the best human-like player. If
  ``evaluator`` is given, truncate the game at the first position with a valid probability, and
  return it.
  """
  
  while not gameOver(b) :
    pips = getPips()
    am = allMoves(b, pips);                     assert am
    if len(am) == 1:
      m,e = am[0]
    else :
      le = (playerX if side else playerO)(am)
      if len(le) == 1:
        m,e = le[0]
      else :
        m,e = random.choice(le)
    
    b = m
    if not e :
      side = 1 - side
    if evaluator:
      p = evaluator(b)
      if p is not None:
        return side, p
        
  return 1-side,1

def rollout(board, nTrials, playerX = None, playerO = None, evaluator = None) :
  """ Play ``board`` ``nTrials`` times. Report percentage of wins.
  
  Use playerX/playerO to determine X/O moves. If unspecified, use the best human-like player. If
  ``evaluator`` is given, truncate the rollout at the first position with a valid probability.
  """
  
  wc = 0
  for _ in range(nTrials) :
    side,p = rolloutPlay(getBoard(board), 1, playerX or hplay, playerO or hplay, evaluator)
    wc += p if side == 1 else 1-p
  return float(wc)/nTrials

def ply1(board, db) :
  """ Win probability of ``board`` at 1-ply. """
  
  pWin = 0
  for pr,pips in (((1./16), 0), ((1./4), 1), ((3./8), 2), ((1./4), 3), ((1./16),4)) :
    am = allMoves(board, pips)
    maxp = -1
    for b,e in am:
      if gameOver(b) :
        maxp = 1
        break

      p = db.aget(b);             assert p is not None;
      if not e:
        p = 1 - p
      if p > maxp :
        maxp = p
        
    assert 0 <= maxp <= 1
    pWin += pr * maxp
    
  assert 0 <= pWin <= 1
  return pWin

def prob(board, ply, db) :
  """ Win probability of ``board`` at ``ply``-ply. """

  if ply == 0 :
    return db.aget(board)
  if ply == 1:
    return ply1(board, db)
  
  pWin = 0
  for pr,pips in (((1./16), 0), ((1./4), 1), ((3./8), 2), ((1./4), 3), ((1./16),4)) :
    am = allMoves(board, pips)
    maxp = -1
    for b,e in am:
      if gameOver(b) :
        maxp = 1
        break

      p = prob(b, ply-1, db)
      if not e:
        p = 1 - p
      if p > maxp :
        maxp = p
        
    assert 0 <= maxp <= 1
    pWin += pr * maxp
    
  assert 0 <= pWin <= 1
  return pWin
  
#  LocalWords:  rollout evaluator
