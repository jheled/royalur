#!/usr/bin/env python
## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

"""
===============================
Print and Annotate ROGOUR Games
===============================

"""
from __future__ import print_function
from __future__ import absolute_import

import argparse, sys, os.path
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import math
from math import log

from royalur import *

db = None

def halfValid(b) :
  ok1 = all([b[i] == 0 or b[i] == 1 for i in (0,1,2,3,12,13)])
  ok2 = all([-1 <= b[i] <= 1 or b[i] == 1 for i in range(4,12)])
  ok3 = sum([b[i] == 1 for i in range(14)]) + b[14] <= 7
  return ok1 and ok2 and ok3

def validBoard(b) :
  return halfValid(b) and halfValid(reverseBoard(b))

def massageBoardString(bs, mvFrom = None, bCode = "") :
  bs = "".join([c.lower() if c in "OX" else c for c in bs])
  if mvFrom is None or mvFrom.lower() == 'e':
    top,mid,low = bs.split('\n')
    if mvFrom and mvFrom.isupper():
      top = top[:8] + 'O' + top[9:]
    if bCode:
      mid = mid + " "*9 + bCode
    if mvFrom and mvFrom.islower():
      low = low[:8] + 'X' + low[9:]
    bs = "\n".join((top,mid,low))
  else :
    top,mid,low = bs.split('\n')
    if mvFrom.isdigit() :
      i = 4 + ord(mvFrom) - ord('1')
      mid = mid[:i] + mid[i].upper() + mid[i+1:]
    elif mvFrom.islower() :
      if mvFrom in "abcd" :
        i = 7 - (ord(mvFrom) - ord('a'))
      else :
        i = 10 + (ord('z')- ord(mvFrom))
      low = low[:i] + low[i].upper() + low[i+1:]
    else :
      if mvFrom in "ABCD" :
        i = 7 - (ord(mvFrom) - ord('A'))
      else :
        i = 10 + (ord('Z')- ord(mvFrom))
      top = top[:i] + top[i].upper() + top[i+1:]

    if bCode :
      mid = mid + " "*9 + bCode
    bs = "\n".join((top,mid,low))
  return bs

def diceLuck(board, dice) :
  am = allMoves(board, dice)
  ps = [db.aget(b) if e else 1 - db.aget(b) for b,e in am]
  pw = max(ps)
  e = pw - db.aget(board)
  return e

def diceLuckStr(e) :
  e = 100*e

  if e > 7 : return "!!"  #98%
  if e > 4 : return "!"   #94%
  if e < -7 : return "~~"
  if e < -4 : return "~"
  return ""

def pr2ELOdif(p) :
  assert 0 < p < 1

  return - 400*log(1/p - 1, 10)

def dice2str(dice) :
  dice = int(dice)

  return ((4-dice)*'=' + '@'*dice)


def main():
  global db
  parser = argparse.ArgumentParser(description="""Print and optionally annotate a ROGOUR game.""")

  parser.add_argument("--annotate", "-a",
                      help = "Annotate the moves", action = "store_true", default = False)

  parser.add_argument("--codes", "-c",
                      help="Show board codes.", action = "store_true", default = False)

  parser.add_argument("--highlights", "-H",
                      help="Show only highlights: lucky, unlucky and misplays. (implies annotate)",
                      action = "store_true", default = False)

  parser.add_argument("--header",
                      help="Show board layout.", action = "store_true", default = False)

  parser.add_argument("--database", "-d", metavar="FILE", help="Probabilities database.")

  parser.add_argument('match', metavar='FILE', help="Match log file")

  options = parser.parse_args()
  URFileName = options.match
  try :
    urMatchLog = file(URFileName)
  except IOError as e:
    # report error
    print("Can't open match:", e, file=sys.stderr)
    sys.exit(1)

  highlights =  options.highlights

  annotate = options.annotate or highlights
  if annotate:
    try:
      if options.database:
        db = PositionsWinProbs(options.database)
      else :
        db = PositionsWinProbs(royalURdataDir + "/db16.bin")
    except:
      print("Error: no dababase, can't annotate.", file=sys.stderr)
      sys.exit(1)

  gameBoard = startPosition()
  xName,oName = 'X', 'O'
  outFile = sys.stdout

  if options.header :
    print("[H] DCBA  ZY (F)", file=outFile)
    print("    12345678    ", file=outFile)
    print("[h] dcba  zy (f)", file=outFile)
    print("", file=outFile)

    print("H - Home. F - Finish.", file=outFile)
    print("'e' and 'E' denote Entering, i.e. moving a new piece from home to board.", file=outFile)
    print("""'!' is lucky and '!!' very lucky. '~' is unlucky and '~~' very unlucky.""", file=outFile)
    print("", file=outFile)
  bcode = None

  if annotate:
    luckTotals = [0, 0]
    equityLose = [0, 0]

  for line in urMatchLog:
    line = line.strip()
    if line[0] == '#':
      continue
      #  print(line, file=outFile)

    if "wins" in line.lower() and line[1] == ':' :
      who = "XO".index(line[0])
      print([xName,oName][who],"Wins.", file=outFile)
      print("", file=outFile)

      if gameOver(gameBoard) and annotate :
        print("Skill: %s %.2f  %s %.2f" % (xName, equityLose[0], oName, equityLose[1]), file=outFile)
        px = .5 + equityLose[0]/100.
        eloX = ("%.0f" % (2000 + pr2ELOdif(px))) if px > 0 else "Dreadful beyond words."
        po = .5 + equityLose[1]/100.
        eloO = ("%.0f" % (2000 +  pr2ELOdif(po))) if po > 0 else "Dreadful beyond words."

        print("ELO:   %s  %s   %s  %s" % (xName, eloX, oName, eloO), file=outFile)
        print("", file=outFile)

        print("Luck: %s %.2f  %s %.2f" % (xName, 100*luckTotals[0], oName, 100*luckTotals[1]), file=outFile)
        p = 0.5 + (luckTotals[0] - luckTotals[1])
        if 0 < p < 1 :
          xOverO = pr2ELOdif(p)
          if luckTotals[0] > luckTotals[1] :
            print("Luck equivalence: %.0f ELO points to" % xOverO, xName + ".", file=outFile)
          else :
            print("Luck equivalence: %.0f ELO points to" % -xOverO, oName + ".", file=outFile)
        else :
          print([oName,xName][luckTotals[0] > luckTotals[1]],"go to Las Vegas *Immediately*!!", file=outFile)
        print("", file=outFile)

      continue

    if line.startswith("Board:") :
      if annotate:
        luckTotals = [0, 0]
        equityLose = [0, 0]
      gameBoard = code2Board(line[len("Board:"):].strip().strip('"'))
      continue

    if line.startswith("X is ") :
      w = line.split(" ")
      xName,oName = w[2].strip(","),w[5]
      print(line)
      continue

    if line.startswith("X: ") or line.startswith("O: "):
      showPositon = True

      who = "XO".index(line[0])

      if options.codes:
        if not gameOver(gameBoard):
          bcode = board2Code(gameBoard)
        else :
          bcode = None

      action = line[3:].split(' ')
      if len(action) == 1:
        pips = action[0];                         assert pips in "01234"

        assert len(allMoves(gameBoard if who == 0 else reverseBoard(gameBoard), int(pips))) == 1,(line,gameBoard,who)

        if annotate :
          p = db.aget(gameBoard if who == 1 else reverseBoard(gameBoard))
          if p is not None:
            dlucke = diceLuck(gameBoard if who == 0 else reverseBoard(gameBoard), int(pips))
            luckTotals[who] += dlucke
            dluck = diceLuckStr(dlucke)
            if dluck or not highlights:
              print('='*18, file=outFile)
              print("XO"[who] + ':', dice2str(pips)+' '+dluck, "%4.2f" % (100*(1-p)), file=outFile)
              showPositon = True
            else :
              showPositon = False
        else :
          print('='*18, file=outFile)
          print("XO"[who] + ':', dice2str(pips), file=outFile)
        if showPositon:
          print(massageBoardString(boardAsString(gameBoard), None, bcode), file=outFile)
      else:
        pips = int(action[0])
        square = action[1][0]

        luck = ""
        if annotate :
          showPositon = not highlights

          boardOnMoveSide = gameBoard if who == 0 else reverseBoard(gameBoard)
          p = db.aget(boardOnMoveSide)
          if p is not None:
            lucke = diceLuck(boardOnMoveSide, pips)
            luckTotals[who] += lucke

            luck = diceLuckStr(lucke)
            if luck : showPositon = True
            #luck = ' '*4 + "%.3f" % dluck

        positionOutput = StringIO.StringIO()
        print >> positionOutput, '='*18
        print >> positionOutput, "XO"[who] + ':', dice2str(pips)+' '+luck, square
        c = square.lower() if who == 0 else  square.upper()
        print >> positionOutput, massageBoardString(boardAsString(gameBoard), c, bcode)

        if who == 1:
          gameBoard = reverseBoard(gameBoard)

        moveFrom = boardCHmap[square.lower()]
        moveTo = moveFrom + pips

        if annotate:
          if db.aget(gameBoard) is not None:
            print >> positionOutput, ""
            froms = []
            ams = allMoves(gameBoard, pips, froms);          assert len(froms) == len(ams)
            ps, codes = [], []
            for b,e in ams:
              p = db.aget(b)
              if not e:
                p = 1 - p
              ps.append(p)
              codes.append(board2Code(b) if options.codes else None)

            sps = sorted(zip(ps,froms,codes), reverse=1)
            for p,frm,code in sps:
              ploss = 0
              if frm == moveFrom:
                strt = " ** "
                if p != sps[0][0] :
                  ploss = (p - sps[0][0])*100
                  equityLose[who] += ploss
                  fin = code or ""
                  showPositon = True
                else :
                  fin = " "*8 + code if code else ""
              else :
                strt = " "*4
                fin = " "*8 + code if code else ""
              lt = boardPos2CH[frm]
              if who == 1:
                lt = lt.upper()
              print >> positionOutput, strt + lt, "%4.2f" % (100*p), \
                " (%.2f)" % ploss if ploss != 0 else "", fin

        if showPositon:
          print(positionOutput.getvalue().strip(), file=outFile)
        positionOutput.close()

        if moveFrom >= 0:
          gameBoard[moveFrom] = 0
        if moveTo == 14:
          gameBoard[moveTo] += 1
        else:
          gameBoard[moveTo] = 1

        assert validBoard(gameBoard)

        if who == 1:
          gameBoard = reverseBoard(gameBoard)
      if showPositon:
        print("", file=outFile)


  urMatchLog.close()


if __name__ == "__main__":
  main()
