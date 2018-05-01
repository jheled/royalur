## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the files LICENCE and gpl.txt for copying conditions.
#

"""
=======================================
Core functionality for classical ROGOUR
=======================================

The player are named Green (to move) and Red. Each board square is assigned a character.

::

  D C B A     Z Y
  1 2 3 4 5 6 7 8         
  d c b a     z y

Green pieces move through abcd12345678yz, while Red pieces move ABCD12345678YZ. Internally the
board is represented as an array of length 22, indexed thus,

::

  18 17 16 15   [21] 20 19
   4  5  6  7  8  9  10 11
   3  2  1  0   [14] 13 12

Positions 14 and 21 respectively store the number of Green/Red pieces out of play (born-off). The
number of pieces at home is implicit (total must sum to 7). You may find it easier to picture the
game and internal representation like that:

::

 Red   15 16 17 18+                    19 20+ 21
                    4 5 6 7& 8 9 10 11 
 Green  0  1  2  3+                    12 13+ 14

The plus sign indicates the square bestows an extra roll. The ampersand provide protection from hits
as well.

The board can be encoded as either a *code* or an *index*. Codes are printable strings (of length 5)
intended for "human interaction" and light usage, i.e. copy/paste for sharing or when the number of
boards is relativly small. The index is tighter representation mapping the board to an unique
integer in the range [0,137913936), the total number of Ur positions. Indices are computationally
slower than codes, but enable storing per-board values in one contiguous memory block, indexed by
the board index, for the full game space. Given the ridiculous overhead of Python lists, and even
the supposedly efficient arrays, the only viable option is to work with low-level bytearrays indexed
by the board index.

"""

import random

__all__ = [
  "startPosition",
  "allActualMoves", "allMoves", "getPips",
  "reverseBoard", "homes", "gameOver", "typeBearOff", "totalPositions",
  "getIndex", "getBoard", "getCode",
  "boardAsString", "board2Code", "code2Board", "board2Index", "index2Board",
  "positionsIterator",
  "boardCHmap", "reverseBoardIndex", "boardPos2CH"
]

GR_OFF = 14
RD_OFF = 21

def reverseBoard(board) :
  """ Reverse roles of Red and Green. """
  
  r = [0]*22
  for i in range(4):
    opp = 15+i
    r[i] = -board[opp]
    r[opp] = -board[i]
  for i in range(4, 12):
    r[i] = -board[i]
  for i in range(12, 15):
    opp = 7+i
    r[i] = -board[opp]
    r[opp] = -board[i]
  r[14] = board[21]
  r[21] = board[14]
  return r

# Squares bestowing an extra roll. 
extraTurn = [3, 7, 13, 18, 20]
# In indexed array form, for speed
extraTurnA = [False]*22
for i in extraTurn:
  extraTurnA[i] = True

boardCHmap = {'a' :  0, 'b' : 1, 'c' : 2, 'd' : 3, 'y' : 12, 'z' : 13,
              'A' :  15, 'B' : 16, 'C' : 17, 'D' : 18, 'Y' : 19, 'Z' : 20,
              '1' : 4, '2' :  5, '3' : 6, '4' : 7, '5' : 8, '6' : 9, '7' : 10, '8' : 11,
              'e' : -1, 'E' : -1}
boardPos2CH = "abcd12345678yz ABCDYZ e"

def reverseBoardIndex(i) :
  if 0 <= i <= 3:
    return 15 + i
  if 15 <= i <= 18:
    return i - 15
  if 12 <= i <= 14:
    return i + 7
  if 19 <= i <= 21:
    return i - 7
  if 4 <= i < 4 + 8:
    return i
  assert False

def allActualMoves(board, pips, froms = None) :
  """Return a list of all **actual** moves by Green given the dice.

  *actual* here means omitting the cases where Green can't move. Each returned move is a ``(b,e)``
  pair, where ``e`` is True when Green has an extra turn (and thus the board has not been flipped),
  or False and thus this is Red turn and the board is flipped.
  """
  assert not gameOver(board)
  if pips == 0:
    return []
    
  gOnBoard = sum([i == 1 for i in board[0:14]])
  totPiecesMe = 7 - board[GR_OFF];                    assert totPiecesMe != 0
  atHome = totPiecesMe - gOnBoard
  
  moves = []
  if atHome:
    to = pips-1
    if board[to] == 0:
      b = list(board)
      b[to] = 1
      moves.append((b, extraTurnA[to]))
      if froms is not None:
        froms.append(-1)
  for i in range(14):
    if board[i] == 1:
      to = i + pips
      if to < 14 and board[to] != 1:
        if board[to] == 0 or to != 7:
          b = list(board)
          b[i] = 0
          b[to] = 1
          moves.append((b, extraTurnA[to]))
          if froms is not None:
            froms.append(i)
      elif to == 14:
        b = list(board)
        b[i] = 0
        b[14] += 1
        moves.append((b,False))
        if froms is not None:
          froms.append(i)
          
  for k,(b,e) in enumerate(moves) :
    if not e:
      moves[k] = (reverseBoard(b),e)
  return moves

def allMoves(board, pips, froms = None) :
  """ Return a list of all moves by Green given the dice.

  Same format as :py:func:`allActualMoves`, but including the "no-move" board from 0 pips. 
  """
  
  aam = allActualMoves(board, pips, froms)
  if aam:
    return aam
    
  if froms is not None:
    froms.append(None)
  return [(reverseBoard(board),False)]
  
def startPosition() :
  """ Staring position. """
  
  return [0]*22

def homes(board) :
  """ Helper returning a (numberOfGreenMenAtHome, numberOfRedMenAtHome) pair. """
  
  gOnBoard = sum([i == 1 for i in board[0:14]])
  gTotInPlay = 7 - board[GR_OFF]
  gHome = gTotInPlay - gOnBoard
  
  rOnBoard = sum([i == -1 for i in board[15:19] + board[4:12] + board[19:21]])
  rTotInPlay = 7 - board[RD_OFF]
  rHome = rTotInPlay - rOnBoard
  return gHome, rHome
  
def boardAsString(board) :
  """ Board as a printable string (debug). """
  
  board = getBoard(board)
  
  o = sum([i == 1 for i in board[0:14]])
  totPiecesMe = 7 - board[GR_OFF]
  atHome = totPiecesMe - o
  
  oo = sum([i == -1 for i in board[15:19] + board[4:12] + board[19:21]])
  ototPiecesOff = 7 - board[RD_OFF]
  oatHome = ototPiecesOff - oo
  
  top = "".join(['O' if board[i] == -1 else '.' for i in range(18,14,-1)]) + \
        '  ' + "".join(['O' if board[i] == -1 else '.' for i in (20,19)]) + \
        (" (%1d)" % (board[RD_OFF]))
  mid = "".join(['O.X'[board[i]+1] for i in range(4,12)])
  bot = "".join(['X' if board[i] == 1 else '.' for i in range(3,-1,-1)]) + \
        '  ' + "".join(['X' if board[i] == 1 else '.' for i in (13,12)]) + \
        (" (%1d)" % (board[GR_OFF]))
  s = "[%1d] " % oatHome + top + '\n' + ' '*4 + mid + '\n' + "[%1d] " % atHome + bot
  return s

z85s = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
rz85 = dict([(c,k) for k,c in enumerate(z85s)])

def b2a(sbits) :
  """Encode 31 bits (represented by a 0/1 string) as a length 5 string made of printable characters
     (ASCII85 i.e. base 85).
  """
  
  l = long(sbits, 2)
  a = ''
  for _ in range(5) :
    c = l % 85
    a += z85s[c]
    l = (l - c) // 85
  return a
  
def a2b(s) :
  """ Decode the base 95 string back to a string of 0/1 bits. """
  
  l = 0
  for x in s[::-1]:
    l = l*85 + rz85[x]
  return format(l, '031b')
  
def board2Code(board) :
  """Encode board as a string.

  First the board is encoded as 31 bits: 2x3 bits for number of pieces at home, 2x6 bits pieces on
  abcdyz/ABCDYZ, and 13 bits for squares 1-8. The middle strip squares are taken as representing an
  8 digit base-3 number, which is converted to an integer in the range [0 - 3**8-1], which in turn
  is encoded as 13 bits (6+12+13 = 31). The 31 bits are encodes as string of 5 printable characters
  (2**31 < 85**5).
  """
  
  o = sum([i == 1 for i in board[0:14]])
  totPiecesMe = 7 - board[GR_OFF]
  atHome = totPiecesMe - o
  s = format(atHome, '03b') + "".join(['1' if i else '0' for i in board[:4] + board[12:14]])
  
  oo = sum([i == -1 for i in board[15:19] + board[4:12] + board[19:21]])
  ototPiecesOff = 7 - board[RD_OFF]
  oatHome = ototPiecesOff - oo
  
  s = s + (format(oatHome, '03b') + "".join(['1' if i else '0' for i in  board[15:19] + board[19:21]]))
  x = board[4] + 1
  for i in board[5:12]:
    x = 3*x + i + 1
  s1 = format(x, '013b')
  s = s + s1
  r = b2a(s)
  assert a2b(r) == s
  return r
  
def code2Board(e) :
  """Decode board code back to internal representation."""
  assert len(e) == 5 and all([c in rz85 for c in e])
  
  s = a2b(e);                                             assert len(s) == 31
  atHome, oAtHome = int(s[:3], 2),int(s[9:12], 2);        assert 0 <= atHome <= 7 and 0 <= oAtHome <= 7
  
  board = [0]*22
  for b,k in ((3,0),(4,1),(5,2),(6,3),(7,12),(8,13)) :
    if s[b] == '1' :
      board[k] = 1
  for b,k in ((12,15),(13,16),(14,17),(15,18),(16,19),(17,20)) :
    if s[b] == '1' :
      board[k] = -1
  mid = s[18:];                        assert len(mid) == 13
  mid = int(mid, 2);                   assert 0 <= mid < 3**8
  for i in range(11,3,-1) :
    x = mid % 3
    board[i] = x - 1
    mid = (mid - x) // 3
  board[14] = 7 - (atHome + sum([i == 1 for i in board[0:14]]))
  board[21] = 7 - (oAtHome + sum([i == -1 for i in board[15:19] + board[4:12] + board[19:21]]))
  return board

def gameOver(board) :
  """ True if game on board is over, False otherwise. """
  
  return board[14] == 7 or board[21] == 7

def typeBearOff(board) :
  """ True if board is in *bear-off* mode. (i.e. no more contact possible). """
  
  return sum(board[12:15]) == 7 or -sum(board[19:21]) + board[21] == 7
  
def getPips() :
  """ Get a "dice" roll. """
  
  return [0,1,1,1,1,2,2,2,2,2,2,3,3,3,3,4][random.randint(0, 15)]

# Board iterators

def bitsIterator(k, n) :
  """ Iterate over all placements of *k* identical pieces in *n* locations. """
  
  if k == 0:
    yield (0,)*n
  elif k == n :
    yield (1,)*n
  else :
    for v in bitsIterator(k-1, n-1) :
      yield (1,) + v
    for v in bitsIterator(k, n-1) :
      yield (0,) + v

def gIterator(gOff = 0) :
  """ Iterate over all green pieces positions with *gOff* pieces off board. """
  
  gMen = 7-gOff
  b = [0]*22
  b[GR_OFF] = gOff
  for gHome in range(gMen, -1, -1) :
    gOnBoard = gMen - gHome
    for gOnMine in range(min(6,gOnBoard), -1, -1) :
      for onMine in bitsIterator(gOnMine, 6) :
        b[:4] = onMine[:4]
        b[12:14] = onMine[4:]
        for onStrip in bitsIterator(gOnBoard - gOnMine, 8) :
          b[4:12] = onStrip
          yield list(b)

def rIterator(board, rOff = 0) :
  """ Iterate over all red pieces positions with *rOff* pieces off board, conditional on present
  green pieces as given in *board*. """
  
  b = list(board)
  b[RD_OFF] = rOff
  rMen = 7-rOff
  bStrip = b[4:12]
  for rHome in range(rMen, -1, -1) :
     rOnBoard = rMen - rHome
     for rOnMine in range(min(6,rOnBoard), -1, -1) :
       for onMine in bitsIterator(rOnMine, 6) :
         b[15:19] = [-x for x in onMine[:4]]
         b[19:21] = [-x for x in onMine[4:]]
         for onStrip in bitsIterator(rOnBoard - rOnMine, 8) :
           if any([x == 1 and y == 1 for x,y in zip(onStrip, bStrip)]) :
             continue
           b[4:12] = [-1 if x else y for x,y in zip(onStrip, bStrip)]
           yield list(b)
             
def positionsIterator(gOff = 0, rOff = 0) :
  """ Iterate over all positions with *gOff*/*rOff* Green/Red pieces (respectively) off. """
  
  for b in gIterator(gOff) :
    for b1 in rIterator(b, rOff) :
      yield list(b1)


from binomhack import bmap
    
# m on one side, n on the other
def countPosOnBoard(m, n) :
  assert m >= n
  tot = 0
  for m1 in range(min(m,6)+1) :
    m2 = m - m1
    tot += bmap[6,m1] * bmap[8,m2] * bmap[14-m2, n]
  return tot

nPositionsOnBoard = dict()
for m in range(8) :
  for n in range(m+1) :
    nPositionsOnBoard[m,n] = countPosOnBoard(m, n)
    if m != n :
      nPositionsOnBoard[n,m] = nPositionsOnBoard[m,n]

def countOff(gOff, yOff) :
  tot = 0
  gAvail = 7 - gOff
  for gHome in range(gAvail+1) :
    gOnBoard = gAvail - gHome
    yAvail = 7 - yOff
    for yHome in range(yAvail+1) :
      yOnBoard = yAvail - yHome
      tot += nPositionsOnBoard[gOnBoard, yOnBoard]
  return tot

nPositionsOff = dict()
for m in range(8) :
  for n in range(m+1) :
    nPositionsOff[m,n] = countOff(m, n)
    if m != n :
       nPositionsOff[n,m] = nPositionsOff[m,n]

totalPositions = sum(nPositionsOff.values())
assert totalPositions == sum([(8-i)*nPositionsOnBoard[i,j]*(8-j) for i,j in nPositionsOnBoard])

# 0 <= Men on board <= 7
def startPoint(gOff, rOff, gHome, rHome) :
  n = 0
  for i in range(gOff) :
    for j in range(7+1) :
      n += nPositionsOff[i,j]
  for j in range(rOff) :
    n += nPositionsOff[gOff,j]

  n1 = 0
  for k in range(gHome) :
    for l in range((7-rOff) + 1) :
      g,r = 7 - (k + gOff), 7 - (l + rOff)
      n1 += nPositionsOnBoard[g, r]
    
  for l in range(rHome) :
    g,r = 7 - (gHome + gOff), 7 - (l + rOff)
    n1 += nPositionsOnBoard[g, r]
  return n + n1

def partialSums(gMen, rMen) :
  tot = 0
  ps = [tot]
  for m1 in range(min(gMen,6)+1) :
    m2 = gMen - m1
    tot += bmap[6,m1] * bmap[8,m2] * bmap[14-m2, rMen]
    ps.append(tot)
  return ps

def bitsIndex(bits) :
  k = sum(bits)
  N = len(bits)
  i = 0
  for b in bits :
    if b :
      i += bmap[N-1, k]
      k -= 1
    N -= 1
  return i

def i2bits(i, k, N) :
  bits = [0]*N
  j = 0
  while N > 0:
    bnk = bmap[N-1, k]
    if i >= bnk:
      bits[j] = 1
      i -= bnk
      k -= 1
    N -= 1
    j += 1
  return bits
  
# Ur positions are laid in 64 main blocks. the i*8+j block contains all positions with 'i' Green men
# and 'j' Red men (respectively) off the board (i.e. not at home or on the board). (i,j) pairs are
# sorted lexicographicaly. (0,0),(0,1)...,(0,7),(1,0),(1,1)...(7,7)
#
# The (i,j) block is dividied into (7-i)*(7-j) subblocks. the subblock 'k * (7-j) + l' contains all
# positions with k Green men at home and (and i off), and l Green men home (j off). Again (k,l)
# subblocks are sorted lexicographicaly.
#
# The subblock with g (= 7-i-k) Green men and r (= 7-j-l) on board (respectively) has size
#  P_(g,r) = sum m=0..min(6,g) B(6,m) * B(8,g - m) * B(14 - (g-m), r)
#

startings = [(startPoint(gOff, rOff, gHome, rHome), gOff, rOff, gHome, rHome)
             for gOff in range(8) for rOff in range(8)
             for gHome in range(8-gOff) for rHome in range(8-rOff)]
assert len(set([x[0] for x in startings])) == len([x[0] for x in startings])
spoints = [x[0] for x in startings]
spMap = dict([(tuple(x[1:]),x[0]) for x in startings])
pSums = dict([((gMen,rMen), partialSums(gMen, rMen)) for gMen in range(8) for rMen in range(8)])

def __board2Index(board) :
  b = getBoard(board)

  gOff = b[GR_OFF]
  rOff = b[RD_OFF]
  
  gSafe = b[:4] + b[12:14]
  m = sum(gSafe)
  partSafeG = bitsIndex(gSafe)
  bits = [x == 1 for x in b[4:12]]
  gStrip = bitsIndex(bits)
  gMen = sum(bits) + m
  bits = [x == -1 for x in (b[15:19] + b[4:12] + b[19:21]) if x != 1]
  partR = bitsIndex(bits)
  rMen = sum(bits)
  gHome, rHome = 7 - (gMen + gOff), 7 - (rMen + rOff)
  
  i0 = spMap[gOff, rOff, gHome, rHome]

  ps = pSums[gMen, rMen]
  i1 = ps[m]
  i2 = partSafeG * bmap[8,gMen - m] + gStrip
  i3 = i2 * bmap[14 - (gMen-m), rMen] + partR;         assert i3 < ps[m+1] - ps[m]
  ##print i1,i2,i3,len(bits), partR, bits
  return i0 + i1 + i3
  
from bisect import bisect
  
def __index2Board(index) :
  i = bisect(spoints, index)
  assert startings[i-1][0] <= index < (startings[i][0] if i < len(startings) else totalPositions)
  
  gOff, rOff, gHome, rHome = startings[i-1][1:]

  index -= startings[i-1][0];                               assert index >= 0

  gMen, rMen = 7 - (gOff + gHome), 7 - (rOff + rHome)
  ps = pSums[gMen, rMen]
  m = 0
  while not (ps[m] <= index < ps[m+1]) :
    m += 1
  index -= ps[m]
  u = bmap[14 - (gMen-m), rMen]
  i2 = index // u
  partR = index - i2 * u
  u = bmap[8,gMen - m]
  partSafeG = i2 // u
  gStrip = i2 - u * partSafeG
  
  gSafe = i2bits(partSafeG, m ,6)
  b4_12 = i2bits(gStrip, gMen - m, 8)
  bOther = i2bits(partR, rMen, 14 - (gMen-m))
  
  b = [0]*22
  b[14],b[21] = gOff, rOff
  b[:4] = gSafe[:4]
  b[12:14] = gSafe[4:]
  b[4:12] = b4_12
  b[15:19] = [-x for x in bOther[:4]]

  i = 4
  for k in range(4,12) :
    if b[k] == 0 :
      if bOther[i] :
        b[k] = -1
      i += 1
  b[19:21] = [-x for x in bOther[i:]]
  return b

import irogaur

def index2Board(index) :
  i = bisect(spoints, index)
  #assert startings[i-1][0] <= index < (startings[i][0] if i < len(startings) else totalPositions)
  st = startings[i-1]
  gOff, rOff, gHome, rHome = st[1:]

  return irogaur.index2Board(index - st[0], gOff, rOff, gHome, rHome, pSums)

def board2Index(board) :
  return irogaur.board2Index(board, spMap, pSums)
  
def getIndex(board) :
  """ Get board index from either a board, code, or index (convenience) """
  
  if isinstance(board, int) :
    return board
  if isinstance(board, str) :
    return board2Index(code2Board(board))
  if isinstance(board, list) :
    return board2Index(board)
  assert False
  
def getCode(board) :
  """ Get board code from either a board, code, or index (convenience) """
  if isinstance(board, str) :
    assert len(board) == 5 and all([x in rz85 for x in board])
    return board
  if isinstance(board, int) :
    return board2Code(index2Board(board))
  if isinstance(board, list) :
    return board2Code(board)
  assert False
  
def getBoard(key) :
  """ Get internal representation of board from either a board, code, or index (convenience) """
  if isinstance(key, str) :
   return code2Board(key)
  elif isinstance(key, int) :
    return index2Board(key)
  elif isinstance(key, list) :
    return key
  assert False

#  LocalWords:  bytearrays
