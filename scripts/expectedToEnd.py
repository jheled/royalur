## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

""" This script generates a data file with the expected number of turns to game
end for every ROGOUR position.
"""

from royalur import *
from royalur.humanStrategies import totPips2s, totPips1s

import os.path
import sys
from functools import reduce

db = PositionsWinProbs(os.path.join(royalURdataDir, "db16.bin"))
ishtar = getDBplayer(db)

def ballPark(b) :
  a1, a2 = 0.91335123,  0.401785
  n1, n2 = totPips1s(b), totPips1s(reverseBoard(b))
  return a1 * min(n1, n2) + a2 * (n1+n2)
  
def unpackl1(l) :
  return (l >> 24, (l >> 16) & 0xff, (l >> 8) & 0xff, l & 0xff)

def packl1(bf) :
  return (bf[0] << 24) + (bf[1] << 16) + (bf[2] << 8) + bf[3]

def setv(buf, pos, val) :
  assert 0 <= val < 1024
  v = int(round(2**21 * val))
  buf[pos*4:pos*4+4] = unpackl1(v)

def getv(buf, pos) :
  v = packl1(buf[pos*4:pos*4+4])
  return float(v)/2**21
  
def hasv(buf, pos) :
  return buf[pos*4:pos*4+4] != bytearray(b'\xff')*4

def halfList(added, exvals) :
  supdateList = set()
  updateList = []
  for k in reversed(added) :
    assert k not in supdateList
    b = index2Board(k)

    r = board2Index(reverseBoard(b))
    if r not in supdateList:
      updateList.append((k,r))
      supdateList.add(k)

  return updateList

def packRcpt(longs) :
  return bytearray(reduce(lambda x,y : x+y, [unpackl1(l) for l in longs]))

def unpackRcpt(buf) :
  return [packl1(buf[i:i+4]) for i in range(0, len(buf), 4)]

def getRcpt(key, rkey) :
  board = index2Board(key)
  bf = []
  for dice in range(1,5) :
    am = allMoves(board, dice)
    mv = ishtar(am);         assert len(mv) == 1
    b,e = mv[0]
    v = board2Index(b)
    #if e:
    #  v |= (0x1 << 31)
    bf.append(v)

  board = reverseBoard(board)
  for dice in range(1,5) :
    am = allMoves(board, dice)
    mv = ishtar(am);         assert len(mv) == 1
    b,e = mv[0]
    v = board2Index(b)
    #if e:
    #  v |= (0x1 << 31)
    bf.append(v)
  return bf

def evalBoth(key, rkey, rcpt, exvals) :
  #vk = [(getv(exvals, v & ~(0x1<<31)), v & (0x1<<31)) for v in rcpt[:4]]
  vk = [getv(exvals, v) for v in rcpt[:4]]
  a1 = sum([v*p for v,p in zip(vk, (4,6,4,1))]) + 15
  
  #vr = [(getv(exvals, v & ~(0x1<<31)), v & (0x1<<31)) for v in rcpt[4:]]
  vr = [getv(exvals, v) for v in rcpt[4:]]        
  a2 = sum([v*p for v,p in zip(vr, (4,6,4,1))]) + 15

  # 16 X = a1 + 1 * ( 1 + Y ) = a1 + 1 + Y = a1 + 1 + (a2 + 1 + X)/16
  # 16 Y = a2 + 1 * ( 1 + X ) = a2 + 1 + X
  # 256 X = 16 a1 + 16 + a2 + 1 + X
  # X = (16 a1 + 16 + a2 + 1) / 255
  # Y = (a2 + 1 + X) / 16
  
  X = (16 * a1 + 16 + a2 + 1) / 255.
  Y = (a2 + 1 + X) / 16.
  return X,Y

def playr(b, N) :
  res = []
  for _ in range(N) :
    r = [] ;
    play.playGame(ishtar, ishtar, startingBoardAndSide = (b, 1), record = r);
    res.append(len(r) - 1)
  return res

def main():
  exvals = bytearray(b'\xff') * 4*totalPositions

  for g in range(7) :
    for b in positionsIterator(7,g):
      setv(exvals, board2Index(b), 0.0)
      rb = reverseBoard(b)
      setv(exvals, board2Index(rb), 0.0)

  frct = None

  fnbase = "ex.02"
  gm = 0
  for rm in range(gm, -1, -1) :
    del frct
    added = []
    print(gm,rm)
    for b in positionsIterator(gm, rm):
      #if (b[12] + b[13] > 0 and b[19] + b[20] < 0) :
      #  continue
      key = board2Index(b)
      added.append(key)
      if not hasv(exvals, key):
        setv(exvals, key, ballPark(b)) 

      rk = board2Index(reverseBoard(b))
      if not hasv(exvals, rk):
        setv(exvals, rk, ballPark(b))

    updateList = halfList(added, exvals)
    print(len(updateList),"position pairs.")
    del added
    updateList = sorted(updateList, key = lambda x : totPips2s(getBoard(x[0])))

    frct = [None]*len(updateList)
    k = 0
    for key,rkey in updateList:
      frct[k] = packRcpt(getRcpt(key, rkey))
      k += 1
      if k % (36*1024) == 0 :
        print("%.0f" % (k*100./len(updateList)), end = '')
        sys.stdout.flush()
    print()

    rnd = 0
    maxe = 1
    while maxe > 1e-5:
      rnd += 1
      print("round",rnd,'(',gm,rm,')')
      if 1:
        dif,maxe,mkey = 0.0, -1, None
        tot = len(updateList)

        cnt = 0
        for key,rkey in updateList :
          cnt += 1
          if cnt % (36*1024) == 0 :
            print(cnt,int((100.*cnt)/tot),"%.3g" % maxe, '.')
            sys.stdout.flush()

          e1, e2 = evalBoth(key, rkey, unpackRcpt(frct[cnt-1]), exvals)

          e = getv(exvals, key)
          er1 = abs(e - e1)

          e = getv(exvals, rkey)
          er2 = abs(e - e2)
          dif += er1 + er2
          if max(er1,er2) > maxe:
            maxe = max(er1,er2)
            mkey = key,er1,er2
          setv(exvals,  key, e1)
          setv(exvals, rkey, e2)
        print()
        print(maxe, dif, dif/(2*tot))

    f = open(fnbase + ".inpro.bin", "wb")
    f.write(exvals)
    f.close()


if __name__ == "__main__":
  main()
