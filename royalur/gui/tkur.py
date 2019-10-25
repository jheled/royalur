#! /usr/bin/env python
## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

# This is not pretty code, and might be buggy. You have been warned

from __future__ import print_function
from __future__ import absolute_import

import random
import logging
import argparse, sys, os.path, time
try:
  import tkinter as tk
except ImportError:
  import Tkinter as tk
from PIL import ImageTk, Image

dir_path = os.path.dirname(os.path.realpath(__file__))

from royalur import *
from royalur.urcore import extraTurnA
from royalur.humanStrategies import getByNicks, bestHumanStrategySoFar

flog = None
options = None
cv = None
foemenu = None

logging.basicConfig(level=logging.DEBUG)


def _create_circle(self, x, y, r, **kwargs):
  return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def dbdPlayer(moves, db) :
  mvs = [(int(db.aget(b)*64)/64.,b,e) for b,e in moves]
  ps = [(p if e else 1 - p,b,e) for p,b,e in mvs]
  mp = max(ps)[0]
  return [(b,e) for p,b,e in ps if p == mp]

# Human  : Green / G / 0 / Bottom
# Machine: Red   / R / 1 / Top

class UrCanvas(tk.Frame) :
  def __init__ (self, master, urBoardImage) :
    self.master = master
    self.loc = self.dragged = 0

    self.lock = True
    self.delay = 0.4

    tk.Frame.__init__(self, master)

    self.boardPhoto = ImageTk.PhotoImage(urBoardImage)

    iWidth, iHeight = urBoardImage.size

    canvas = tk.Canvas(self, width = iWidth, height = iHeight,
                       relief = tk.RIDGE, borderwidth = 1)

    canvas.create_image(0, 0, image = self.boardPhoto, anchor = tk.NW)

    sqaresCoordinates = \
      {
        'a' : (290,267), 'b' : (218, 267), 'c' : (136,267), 'd' : ( 66, 267),
        'y' : (580,267), 'z' : (509, 267),
        '1' : (66, 193), '2' : (136, 193), '3' : (218, 193), '4' : (290, 193),
        '5' : (365,193), '6' : (435, 193), '7' : (509, 193), '8' : (580, 193),
        'A' : (290,120), 'B' : (218, 120), 'C' : (136, 120), 'D' : ( 66, 120),
        'Y' : (580,120), 'Z' : (509, 120),
       }
    self.sqaresCoordinates = sqaresCoordinates

    self.dice1 = Image.open(os.path.join(dir_path, "d41.png"))
    self.d1 = ImageTk.PhotoImage(self.dice1)

    self.dice0 = Image.open(os.path.join(dir_path, "d40.png"))
    self.d0 = ImageTk.PhotoImage(self.dice0)

    dSpacing = max(*(self.dice1.size + self.dice0.size))

    self.pieceLocations = dict()

    self.dices = [[], []]
    for i in range(4) :
      x,y = iWidth - (dSpacing+10), (iHeight - 4*dSpacing)//2 + i * dSpacing
      oid = canvas.create_image(x,y, image = self.d1, anchor = tk.NW, state = 'hidden')
      self.dices[1].append(oid)

      oid = canvas.create_image(x, y, image = self.d0, anchor = tk.NW, state = 'hidden')
      self.dices[0].append(oid)

    def pieceHomeXY(who, i, radius) :
      return 340 - i*(2 * radius + 7), 345 if who == 'G' else 40

    self.radius = 15
    self.gr, self.rd = [], []
    radius, width = self.radius, 3
    for i in range(7) :
      x,y = pieceHomeXY('G', i, self.radius)
      sqaresCoordinates['h' + str(i)] = (x,y)

      c = canvas.create_circle(x, y, radius, fill="green2", outline="black",
                               width=width, state='hidden', tags='GreenPiece')
      self.gr.append(c)
      self.pieceLocations[c] = 'h' + str(i)

      x,y = pieceHomeXY('R', i, self.radius)
      sqaresCoordinates['H' + str(i)] = (x,y)
      c = canvas.create_circle(x, y, radius, fill="red", outline="black",
                               width=width, state='hidden')
      self.rd.append(c)
      self.pieceLocations[c] = 'H' + str(i)

      rdb = (440, 110)
      gdb = (440, 271)

      sqaresCoordinates['F' + str(i)] = (rdb[0],rdb[1] - i*radius)
      sqaresCoordinates['f' + str(i)] = (gdb[0],gdb[1] + i*radius)

    x0,sz = iWidth - (dSpacing+10) - 5, 80
    x = canvas.create_rectangle(x0, sz, x0+60, sz + dSpacing*4 + 20, width = 2, outline = "red", state = 'hidden')
    y = canvas.create_rectangle(x0, sz, x0+60, sz + dSpacing*4 + 20, width = 2, outline = "green2", state='hidden')
    self.diceIndicator = [y,x]

    canvas.pack(expand  = 1, fill = tk.BOTH)

    canvas.tag_bind("GreenPiece", "<Button-1>", self.click)
    canvas.bind_all("<space>", self.space)

    self.c = canvas

  def valid(self) :
    assert validBoard(self.gameBoard)
    assert len(self.pieceLocations) == 14
    gOff, gInPlay, gHome = 0, 0, 0
    for gid in self.gr:
      code = self.pieceLocations[gid]
      assert code[0] in 'hf' or (code in "abcd12345678yz")
      if code[0] == 'f':
        gOff += 1
      elif code[0] == 'h' :
        gHome += 1
      else :
        assert self.gameBoard[boardCHmap[code]] == 1
        gInPlay += 1
    assert gOff == self.gameBoard[14] and gOff+gInPlay+gHome == 7

    rOff, rInPlay, rHome = 0, 0, 0
    for gid in self.rd:
      code = self.pieceLocations[gid]
      assert code[0] in 'HF' or (code in "ABCD12345678YZ")
      if code[0] == 'F':
        rOff += 1
      elif code[0] == 'H' :
        rHome += 1
      else :
        assert self.gameBoard[boardCHmap[code]] == -1
        rInPlay += 1
    assert rOff == self.gameBoard[21] and rOff+rInPlay+rHome == 7

  def space(self, event) :
    if self.lock or gameOver(self.gameBoard) :
      return

    froms = []
    am = allMoves(self.gameBoard, self.pips, froms)
    if len(am) > 1:
      return

    self.lock = True

    frm = froms[0];                       assert frm is not None

    if frm == -1 :
      for pCanvasID,code in self.pieceLocations.iteritems():
        if code[0] == 'h' :
          break
      codeTo = 'abcd'[self.pips - 1]
    else :
      c = boardPos2CH[frm]
      for pCanvasID,code in self.pieceLocations.iteritems():
        if code == c:
          break
      codeTo = boardPos2CH[frm + self.pips]

    ok = self.movePiece('G', pCanvasID, codeTo);       assert ok
    self.afterOppMove(codeTo)

  def afterOppMove(self, codeTo) :
    self.pips = None

    if gameOver(self.gameBoard) :
      self.lock = True
      return

    opTurn = codeTo != ' ' and extraTurnA[boardCHmap[codeTo]]
    logging.debug(opTurn, codeTo)
    self.playLoop(opTurn)

  def playLoop(self, opTurn) :
    while not gameOver(self.gameBoard) :
      if opTurn:
        waiting = self.oppToPlay()
        if waiting :
          return

      self.mePlay()
      self.master.update(); time.sleep( self.delay )
      opTurn = True

  def click(self, event):
    if self.lock :
      return

    self.lock = True

    logging.debug("pips", self.pips)

    pCanvasID = event.widget.find_withtag(tk.CURRENT)[0]
    fromCode = self.pieceLocations[pCanvasID]
    if fromCode[0] == 'h' :
      codeTo = 'abcd'[self.pips - 1]
    else :
      iTo = boardCHmap[fromCode] + self.pips
      if iTo > 14 :
        ## Illegal move
        self.lock = False
        return

      codeTo = boardPos2CH[iTo]

    if not self.movePiece('G', pCanvasID, codeTo) :
      self.lock = False
      return

    self.afterOppMove(codeTo)


  def canvasMovePiece(self, pCanvasID, codeTo) :
    (x,y),r = self.sqaresCoordinates[codeTo], self.radius
    self.c.coords(pCanvasID, x - r, y - r, x + r, y + r)
    self.pieceLocations[pCanvasID] = codeTo

  def movePiece(self, who, pCanvasID, codeTo) :
    logging.debug("movePiece", who, pCanvasID, codeTo)

    codeFrom = self.pieceLocations[pCanvasID]
    logging.debug("codeFrom", codeFrom)

    if codeTo == ' ':
      pre = ('f' if who == 'G' else 'F')
      has = set([pre + str(i) for i in  range(7)])
      for pid,code in self.pieceLocations.iteritems():
        if code[0] == pre :
          has.remove(code)
      codeTo = sorted(has)[0]
      logging.debug(who, has, codeTo)

      self.canvasMovePiece(pCanvasID, codeTo)
      self.c.tag_raise(pCanvasID)
      j = boardCHmap[codeFrom]
      self.gameBoard[j] = 0
      self.gameBoard[14 if who == 'G' else 21] += 1

      self.valid()
      if flog:
        print(codeFrom, file=flog)
        if gameOver(self.gameBoard) :
          print(('X:' if who == 'G' else 'O:'), "wins", file=flog)
        flog.flush()

      return True

    t = boardCHmap[codeTo]

    if codeFrom[0].lower() == 'h' :
      if self.gameBoard[t] != 0 :
        return False
      self.gameBoard[t] = 1 if who == 'G' else -1
    else :
      j = boardCHmap[codeFrom];         assert self.gameBoard[j] == (1 if who == 'G' else -1)
      if self.gameBoard[t] != 0 and (self.gameBoard[j] == self.gameBoard[t] or t == 7) :
        return False

      if self.gameBoard[t] != 0 :
        # hit
        pre = ('H' if who == 'G' else 'h')
        has = set([pre + str(i) for i in  range(7)])
        for pid,code in self.pieceLocations.iteritems():
          if code == codeTo :
            phit = pid
          if code[0] == pre :
            has.remove(code)
        self.canvasMovePiece(phit, list(has)[0])

      self.gameBoard[t] = self.gameBoard[j]
      self.gameBoard[j] = 0

    self.canvasMovePiece(pCanvasID, codeTo)

    logging.debug(self.gameBoard)
    self.valid()

    if flog:
      if codeFrom[0] in "hH" :
        codeFrom = 'e' if who == 'G' else 'E'
      print(codeFrom, file=flog)
      flog.flush()

    #play.showBoard(self.gameBoard)
    return True

  def mePlay(self) :
    while not gameOver(self.gameBoard) :
      pips = self.rollAndShowDice('R')

      froms = []
      am = allMoves(reverseBoard(self.gameBoard), pips, froms)
      #play.showBoard(reverseBoard(self.gameBoard))
      logging.debug("f**",froms)

      self.master.update(); time.sleep( self.delay )

      if pips == 0 or (len(am) == 1 and froms[0] is None) :
        if flog:
          print("", file=flog)
          flog.flush()

        time.sleep( 2*self.delay )
        return

      if len(am) == 1:
        m,e = am[0]
      else :
        pam = self.player(am)
        m,e = random.choice(pam)

      moveFrom = froms[am.index((m,e))]
      logging.debug("moveFrom",moveFrom)
      if moveFrom == -1 :
        for pid,code in self.pieceLocations.iteritems():
          if code[0] == 'H' :
            cto = 'ABCD'[pips - 1]
            break
      else :
        codeFrom = boardPos2CH[reverseBoardIndex(moveFrom)]
        #import pdb; pdb.set_trace()
        for pid,code in self.pieceLocations.iteritems():
          if codeFrom == code :
            cto = boardPos2CH[moveFrom + pips].upper()
            break

      ok = self.movePiece('R', pid, cto);           assert ok

      if not e:
        logging.debug("not extra")
        break

  def rollAndShowDice(self, forWho) :
    d = [random.randint(0,1) for _ in range(4)]
    dc = self.dices
    for k,x in enumerate(d) :
      self.c.itemconfig(dc[x][k],   state='normal')
      self.c.itemconfig(dc[1-x][k], state='hidden')
    for x in self.diceIndicator:
      self.c.itemconfig(x, state="hidden")
    self.c.itemconfig(self.diceIndicator[0 if forWho == 'G' else 1], state = 'normal')

    pips = sum(d)
    if flog :
      print("#", board2Code(self.gameBoard), file=flog)
      print("XO"[forWho == 'R'] + ': ' + str(pips), file=flog)
      flog.flush()

    logging.debug("")
    logging.debug("roll", forWho, sum(d))
    return pips

  def setPlayer(self, name) :
    self.playerName = name.capitalize()
    if name == "sam" :
      self.player = getByNicks("hit;Donkey;safe;homestretch;bear")
    elif name == "joe" :
      self.player = getByNicks('safe;homestretch;hit;Extra;Chuck;Frank;bear;Donkey')
    elif name == "santa" :
      self.player = bestHumanStrategySoFar
    elif name == "expert" or name == "ishtar" :
      db = PositionsWinProbs(royalURdataDir + "/db16.bin")
      if name == "expert" :
        self.player = lambda m : dbdPlayer(m, db)
      else :
        self.player = getDBplayer(db)
    else :
      raise ValueError

  def newGame(self) :
    self.lock = True
    self.gameBoard = startPosition()

    for k,x in enumerate(self.gr):
      self.canvasMovePiece(x, 'h' + str(k))
      self.c.itemconfig(x, state = 'normal')
    for k,x in enumerate(self.rd):
      self.canvasMovePiece(x, 'H' + str(k))
      self.c.itemconfig(x, state = 'normal')

    self.valid()

    if flog:
      print('Board: "' + str(board2Code(self.gameBoard)) + '"', file=flog)
      print("X is %s, O is %s" % (options.name, self.playerName), file=flog)
      flog.flush()

    opTurn = random.randint(0, 1) == 0
    self.playLoop(opTurn)

  def oppToPlay(self) :
    pips = self.rollAndShowDice('G')
    self.master.update(); time.sleep( self.delay )

    froms = []
    am = allMoves(self.gameBoard, pips, froms)

    if pips == 0 or len(am) == 1 and froms[0] is None :
      if flog:
        print("", file=flog)
        flog.flush()

      time.sleep( 2*self.delay )
      return False

    self.pips = pips
    self.lock = False
    return True

def setPlayer(name, k) :
  cv.setPlayer(name)
  for i in range(1,4) :
    foemenu.entryconfigure(i, foreground = "black")
  foemenu.entryconfigure(k, foreground = "blue")




def main():
  global cv, flog, foemenu, options

  parser = argparse.ArgumentParser(description="""Play ROGOUR, Man against the Machine.
  In the GUI you can select the machine strength, start a new match and
  exit. Simply click a piece to move it, or space when there is only one legal move.""")

  parser.add_argument("--record", "-r", metavar="FILE", help = "Record the match in FILE.")

  parser.add_argument("--name", "-n", metavar="STR", default = "Human", help = "Your name.")

  options = parser.parse_args()
  try :
    flog = open(options.record, 'a') if options.record else None
  except:
    logging.error("Error opening match log.")
    sys.exit(1)

  tk.Canvas.create_circle = _create_circle
  root = tk.Tk()
  urBoardImage = Image.open(os.path.join(dir_path, "urBoard.jpg"))
  root.geometry('+%d+%d' % (960 - urBoardImage.size[0]//2,
                            540 - urBoardImage.size[1]//2) )

  root.title("The Royal UR")
  icon = ImageTk.PhotoImage(file=os.path.join(dir_path, "urbicon.png"))
  root.tk.call('wm','iconphoto',root._w,icon)

  cv = UrCanvas(root, urBoardImage)
  cv.pack()

  menu = tk.Menu(root)
  root.config(menu=menu)
  menu.add_command(label = "Play", command = cv.newGame)
  foemenu = tk.Menu(menu)
  menu.add_cascade(label = "Foe", menu = foemenu)
  foemenu.add_command(label = "Sam    (1650)", command = lambda : setPlayer("sam", 1) )
  foemenu.add_command(label = "Joe    (1730)", command = lambda : setPlayer("joe", 2) )
  foemenu.add_command(label = "Santa  (1820)", command = lambda : setPlayer("santa", 3) )
  foemenu.add_command(label = "Expert (1880)", command = lambda : setPlayer("expert", 4) )
  foemenu.add_command(label = "Ishtar (2000)", command = lambda : setPlayer("ishtar", 5) )

  menu.add_separator()
  menu.add_separator()
  menu.add_separator()
  menu.add_command(label = "Exit", command = root.quit)

  setPlayer("santa", 3)

  root.mainloop()

  if flog :
    flog.close()
  root.destroy()



if __name__ == "__main__":
  main()
