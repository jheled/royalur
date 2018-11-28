.. _rules:

The Rulez:
==========

The Royal Game of Ur (ROGOUR) is a racing board game. Here are the rules of as given by Finkel:

1. Each player races seven pieces from start (*Home*) to finish (off the board,
   where the Blue/Red pieces are), as shown below. That is, red first moves
   right to the left edge of the board, left to right on the middle to the right
   side, and right to left on the last two squares.
   
..  image:: urboarddir-r.png

..

   For convenience, each square is associated with a letter or digit:
   
::
   
    D C B A     Z Y
    1 2 3 4 5 6 7 8         
    d c b a     z y

2. Each square may contain exactly one piece.
3. A move consists of throwing the dice and moving exactly one piece to either
   an empty square, off the board, or to a square containing an opponent piece,
   which is *hit* and promptly returns *home*. The piece may jump over pieces of
   either color. A piece can be borne-off only with the **exact** number of
   pips, no wastage allowed. A piece on ``z`` has to wait for a throw of 1 to go
   off the board.
4. The dice consists of four tetrahedrons (`D4 dice
   <https://en.wikipedia.org/wiki/Four-sided_die>`_) with two vertices marked
   white and two black. The dice value (*pips*) is the sum of the white points
   showing on top. So, each D4 contributes, with equal probability, either a 0
   or a 1 to the total. The dice value range from 0 to 4, with 2 being the most
   likely (:math:`p= {^3/_8}`) and 0 or 4 the least likely (:math:`p=
   {^1/_{16}}`).
5. A player rolling a 0 or without a legal move loses her turn.
6. If the piece lands on a square marked with a rosetta (d,4,z), the player gets
   an additional turn.
7. The middle rosetta (4) is special: a piece on this square is protected and
   can't be hit.

..  LocalWords:  rosetta
