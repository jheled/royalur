## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

""" This script creates the winning probabilities database for ROGOUR.
It will take a veeeeerrrry long time and eat your computer memory.
It is here for educational purposes.
"""
from __future__ import print_function
from __future__ import absolute_import

import sys

from royalur import *
from royalur.humanStrategies import totPips2s


def ply1PartsFullRecpt(board, rboard) :
  pWinOnMove = 0
  prReverse = 0
  rest = []

  #[pWinOnMove, [ [[gside] [rside]] , [[gside] [rside]] , ...      ], pNoMove]
  #                       1                   2                  4
  
  for pr,pips in ((1, 0), (4, 1), (6, 2), (4, 3), (1,4)) :
    am = allMoves(board, pips)
    if pips == 0 or (len(am) == 1 and not am[0][1] and am[0][0] == rboard) :
      prReverse += pr
      if pips > 0 :
        rest.append(None)
      continue
      
    for b,e in am:
      if gameOver(b) :
        assert pWinOnMove == 0
        pWinOnMove = pr
        break
    if pWinOnMove > 0 :
      rest.append(None)
      continue

    brds = [[], []]
    for b,e in am:
      brds[0 if e else 1].append(4*board2Index(b))
    rest.append(brds)
  return [pWinOnMove, prReverse, rest]

def unpackl1(l) :
  return (l >> 24, (l >> 16) & 0xff, (l >> 8) & 0xff, l & 0xff)
  
def packl1(bf) :
  return (bf[0] << 24) + (bf[1] << 16) + (bf[2] << 8) + bf[3]
  
def packOne(hr) :
  emp = 0
  for k,rg in enumerate(hr[2]) :
    r,g = ([],[]) if rg is None else rg
    
    if not r:
      emp |= 1 << (2*k)
    if not g:
      emp |= 1 << (2*k+1)
  l = []
  for rg in hr[2] :
    if rg is None:
      continue
    r,g = rg
    if r :
      for i in r:
        l.extend(unpackl1(i//4))
      assert len(r) <= 7 and (l[-4*len(r)] & 0xf0) == 0
      l[-4*len(r)] |= len(r) << (8-3)
    if g :
      for i in g:
        l.extend(unpackl1(i//4))
      assert len(g) <= 7 and (l[-4*len(g)] & 0xf0) == 0
      l[-4*len(g)] |= len(g) << (8-3)
  
  return [hr[0] + (hr[1] << 4), emp] + l

def restoreOne(buf) :
  emp = buf[1]
  mask = 0x1
  al = []
  i = 2

  while len(al) < 8:
    while (emp & mask) and len(al) < 8:
      al.append([])
      mask <<= 1
    mask <<= 1
    if len(al) == 8 :
      break
    l = (buf[i] & 0xe0) >> 5
    pks = []
    for _ in range(l) :
      pks.append(4*packl1([buf[i] & (~0xe0)] + list(buf[i+1:i+4])))
      i += 4
    al.append(pks)

  z = [ [al[i],al[i+1]] if al[i] or al[i+1] else None for i in (0,2,4,6)]
  return [buf[0] & 0x0f, (buf[0] & 0xf0) >> 4] + [z]
  
def ply1BothFullRecpt(board) :
  r = reverseBoard(board)
  A = ply1PartsFullRecpt(board, r)
  B = ply1PartsFullRecpt(r, board)
  return (A,B)

def condencedPly1BothFullRecpt(board) :
  A,B = ply1BothFullRecpt(board)
  bf1,bf2 = packOne(A), packOne(B)
  l1 = len(bf1)
  return [(l1 & 0xff00) >> 8, l1 & 0xff] + bf1 + bf2

def restorePly1BothFullRecpt(buf) :
  lenbf1 = (buf[0] << 8) + buf[1]
  bf1 = buf[2:lenbf1+2]
  bf2 = buf[lenbf1+2:]
  return restoreOne(bf1), restoreOne(bf2)

def ply1fr(recpt, db) :
  rest = recpt[2]
  sm = 0
  for cans,p in zip(rest, (4,6,4,1)):
    if cans :
      g,r = cans
      if not g:
        m = max([(1-db.get(k)) for k in r])
      elif not r:
        m = max([db.get(k) for k in g])
      else :
        mg = max([db.get(k) for k in g])
        mr = max([(1-db.get(k)) for k in r])
        m = max(mr, mg)
      sm += m * p
  return recpt[0] + sm # (recpt[0] + sm)/16.
  
def ply1bfr(recpt, db) :
  gr,rd = recpt
  A,p1 = ply1fr(gr, db), gr[1]
  B,p2 = ply1fr(rd, db), rd[1]

  X = (16*A + p1 * (16 - B - p2)) / (256. - p1*p2)
  Y = (B + p2 * (1 - X)) / 16.
  if not (0 <= X <= 1 and 0 <= Y <= 1) :
    assert False
  return X,Y
  
def ply1bfrc(buf, db) :
  return ply1bfr(restorePly1BothFullRecpt(buf), db)


def ply1Parts(board, rboard, db) :
  pWin = 0
  prReverse = 0
  for pr,pips in (((1./16), 0), ((1./4), 1), ((3./8), 2), ((1./4), 3), ((1./16),4)) :
    am = allMoves(board, pips)
    maxp = -1
    if pips == 0 or (len(am) == 1 and not am[0][1] and am[0][0] == rboard) :
      prReverse += pr
      continue
      
    for b,e in am:
      if gameOver(b) :
        maxp = 1
        break
      else:
        p = db.aget(b);       assert p is not None
        if p is not None :
          if not e:
            p = 1 - p
      if p > maxp :
        maxp = p
    assert 0 <= maxp <= 1
    pWin += pr * maxp
  assert 0 <= pWin <= 1
  return pWin, prReverse

def ply1GetBoth(board, db) :
  r = reverseBoard(board)
  A,p1 = ply1Parts(board, r, db)
  B,p2 = ply1Parts(r, board, db)
  
  X = (A + p1 * (1 - B - p2)) / (1 - p1*p2)
  Y = B + p2 * (1 - X)
  if not (0 <= X <= 1 and 0 <= Y <= 1) :
    assert False
    X = A + p1 * (1 - db.get(r))
    Y = B + p2 * (1 - X)
  return X,Y,r
  
db = PositionsWinProbs()
assert len(db.b) == 4 * totalPositions

filled = 0

for g in range(7) :
  for b in positionsIterator(7, g):
    db.set(board2Index(b), 1.0)
    db.set(board2Index(reverseBoard(b)), 0.0)
    filled += 2
    
def unpackl(l4) :
  return unpackl1(l4[0]) + unpackl1(l4[1]) + unpackl1(l4[2]) + unpackl1(l4[3]) 

def packl(bf) :
  return packl1(bf[:4]),packl1(bf[4:8]),packl1(bf[8:12]),packl1(bf[12:16])

def halfList(added, db) :
  supdateList = set()
  updateList = []

  for k in reversed(added) :
    assert k not in supdateList
    b = db.key2board(k)

    r = db.board2key(reverseBoard(b))
    if r not in supdateList:
      updateList.append((k,r))
      supdateList.add(k)

  return updateList

frct = None
fnbase = "db"

for gm in range(6, -1, -1) :
  for rm in range(gm, -1, -1) :
    del frct
    added = []
    print(gm,rm)
    for b in positionsIterator(gm, rm):
      #if (b[12] + b[13] > 0 and b[19] + b[20] < 0) :
      #  continue
      key = db.board2key(b)
      added.append(key)
      if db.get(key) is None:
        db.set(key, 0.5)
        filled += 1

      rk = db.board2key(reverseBoard(b))
      if db.get(rk) is None:
        db.set(rk, 0.5)
        filled += 1

    updateList = halfList(added, db)
    print(len(updateList),"position pairs.")
    del added
    updateList = sorted(updateList, key = lambda i2 : totPips2s(db.key2board(i2[0])))

    frct = [None]*len(updateList)
    k = 0
    for key,rkey in updateList:
      frct[k] = bytearray(condencedPly1BothFullRecpt(db.key2board(key)))
      k += 1
      if k % (36*1024) == 0 :
        print("%.0f" % (k*100./len(updateList)), end='')
        sys.stdout.flush()
    print()

    rnd = 0
    maxe = 1
    while maxe > 1e-6:
      rnd += 1
      print("round",rnd,'(',gm,rm,')')
      dif,maxe,mkey = 0.0, -1, None
      tot = len(updateList)
      cnt = 0
      for key,rkey in updateList :
        cnt += 1
        if cnt % (36*1024) == 0 :
          print(cnt,int((100.*cnt)/tot),"%.3g" % maxe, '.')
          sys.stdout.flush()

        p1, p2 = ply1bfrc(frct[cnt-1], db)               ;assert 0 <= p1 <= 1 and 0 <= p2 <= 1

        ##X,Y,r = ply1GetBoth(db.key2board(key), db);           assert X == p1 and Y == p2

        p = db.get(key)                                  ; assert p is not None
        er1 = abs(p - p1)

        p = db.get(rkey)                                 ; assert p is not None
        er2 = abs(p - p2)
        dif += er1 + er2
        if max(er1,er2) > maxe:
          maxe = max(er1,er2)
          mkey = key,er1,er2
        db.set(key,  p1)
        db.set(rkey, p2)
      print()
      print(maxe, dif, dif/(2*tot), tot, filled)
      
    db.save(fnbase + ".inpro.bin")
    #import os
    #assert os.path.getsize(fnbase + ".inpro.bin") == 4*totalPositions
