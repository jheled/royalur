## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

"""
======================
Probabilities Database
======================

Per-Position win probabilities for the full game space.
"""

if __package__ is None or __package__ == '':
  from urcore import totalPositions, getIndex, index2Board, getBoard
else:
  from .urcore import totalPositions, getIndex, index2Board, getBoard

__all__ = ["PositionsWinProbs"]

import os.path, gzip, bz2

def fileFromName(fname) :
  """A Python file object from (possibly compressed) disk file.

  If file has a common suffix (.gz,.bz2) use that as a guide. If fname does
  not exist, look for a compressed file with the same stem.
  
  :param fname: file name 
  """
  
  if os.path.exists(fname) :
    fname = os.path.realpath(fname)
    if fname.endswith(".gz") :
      return gzip.open(fname)
    if fname.endswith(".bz2") :
      return bz2.BZ2File(fname)
    return open(fname, 'rb')
  if os.path.exists(fname + ".gz") :
    return gzip.open(fname + ".gz")
  if os.path.exists(fname + ".bz2") :
    return bz2.BZ2File(fname + ".bz2")
  
  raise IOError("no such file " + fname)

class PositionsWinProbs(object) :
  """ Win probability for Green (on play) for each ROGOUR position. """
  def __init__(self, fname = None) :
    if fname :
      self.load(fname)
    else :
      self.b = bytearray(b'\xff') * (4 * totalPositions)
      self.wsize = 4
      self.tkeys = None

  def load(self, fname) :
    f = fileFromName(fname)
    self.b = bytearray(f.read())
    f.close();
    if len(self.b) == 4 * totalPositions:
      self.wsize = 4
    elif len(self.b) == 2 * totalPositions:
      self.wsize = 2
    else :
      assert False, "corrupt %s, read only %d" % (fname, len(self.b))
    self.tkeys = None
    
  def save(self, fname) :
    f = open(fname, 'wb')
    f.write(self.b)
    f.close()

  def board2key(self, board) :
    """Return the db internal 'position'. This happens to be the offset into one humongus
    byte array.
    """
    return self.wsize * getIndex(board)

  def key2board(self, key) :
    """ Return the key of the board associated with this position. """
    return index2Board(key//self.wsize)
    
  def get(self, bpos) :
    """ Get the win probability associated with position ``bpos``. """
    if self.wsize == 4:
      x1,x2,x3,x4 = self.b[bpos:bpos+4]
      v = (x1 << 24) + (x2 << 16) + (x3 << 8) + x4
      if v == 0xffffffff :
        return None
      return v/2.**31
    elif self.wsize == 2:
      x1,x2 = self.b[bpos:bpos+2]
      v = (x1 << 8) + x2
      if v == 0xffff :
        return None
      return v/(2.**16-1)
    assert False
      
  def set(self, bpos, pr) :
    """ Set the win probability associated with position ``bpos`` to ``pr``. """
    
    if self.wsize == 4:
      v = int(pr * 2**31)
      self.b[bpos:bpos+4] = v >> 24, (v >> 16) & 0xff, (v >> 8) & 0xff, v & 0xff
    elif self.wsize == 2 :
      v = int(pr * (2**16-1))
      self.b[bpos:bpos+2] = v >> 8, v & 0xff
    else :
      assert False
    if self.tkeys:
      self.tkeys.add(bpos)

  def keys(self) :
    """ Return the set of valid board positions (will be very slow the first time). """
    
    if self.tkeys is None:
      self.tkeys = set()
      for i in range(0, 4 * totalPositions, 4) :
        if self.b[i] != 255:
          self.tkeys.add(i)
    return self.tkeys
    
  ## convenience
  
  def aget(self, board) :
    """ Get the win probability associated with board."""
    
    #if gameOver(getBoard(board)) :
    #  return 0
    return self.get(self.board2key(board))
    
  def aset(self, board, pr) :
    """ Set the win probability associated with board to ``pr``."""
    
    self.set(self.board2key(board), pr)
      
