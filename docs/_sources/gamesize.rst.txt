The size of Ur
==============

How big is the kingdom of Ur? To compute the number of ROGOUR positions we start
with a smaller configuration, one whose size is relatively easy to figure
out. Let :math:`C_{g,r,m}` be the number of configurations with :math:`g` green
and :math:`r` red pieces on the board, with :math:`m` green pieces in the common
strip (squares 1-8). The :math:`g-m` pieces on ``abcdyz`` can be placed in
:math:`\binom{6}{g-m}` ways, the :math:`m` pieces on ``1-8`` in
:math:`\binom{8}{m}` ways, and the :math:`r` pieces in :math:`\binom{14-m}{r}`,
since :math:`m` squares are occupied by green pieces.

.. math::
   C_{g,r,m} = \binom{6}{g-m} \binom{8}{m} \binom{14-m}{r}.

Summing over :math:`m` would give us :math:`C_{g,r}`, the number of
configurations with :math:`g` green and :math:`r` red pieces on the board:

.. math::
   C_{g,r} = \sum_{m=0}^g C_{g,r,m}.

The remaining :math:`7-g` green pieces can be distributed between the home
(waiting to start the race) and off (born out of the board) in :math:`1+7-g`
ways, and so the total number of positions with :math:`g`/:math:`r` Green/Red
pieces on the board is

.. math::
   N_{g,r} = (8-g) C_{g,r} (8-r).

And the total number of Ur positions is:

.. math::
   N_{ur} = \sum_{g=0}^7 \sum_{r=0}^7 N_{g,r},

which comes up to, Ta-Dam, **137,913,936** positions.

Not a small number, but tiny in the world of games. Chess has somewhere around
:math:`10^{50}` positions, Backgammon :math:`10^{19}`
(`18,528,584,051,601,162,496 <http://www.bkgm.com/rgb/rgb.cgi?view+371>`_ to be
precise). 138 million is definitely within reach, and one of the reasons I got
excited. Even more exciting is this breakdown by number of green/red pieces
borne off.

.. csv-table:: Ur positions by Green/Red borne-off pieces
   :header: "g/r", "0", "1", "2", "3", "4", "5"
   :widths: 5, 6, 6, 6, 6, 6, 6

   **0**, :math:`10^{7.3}`, -, -, -, -, -
   **1**, :math:`10^{7.5}`, :math:`10^{7.2}`, -, -, -, -
   **2**, :math:`10^{7.3}`, :math:`10^{7.2}`, :math:`10^{6.7}`, -, -, -
   **3**, :math:`10^{7.0}`, :math:`10^{6.9}`, :math:`10^{6.7}`, :math:`10^{6.1}`, -, -
   **4**, :math:`10^{6.6}`, :math:`10^{6.5}`, :math:`10^{6.3}`, :math:`10^{5.9}`, :math:`10^{5.2}`, -
   **5**, :math:`10^{6.1}`, :math:`10^{5.9}`, :math:`10^{5.7}`, :math:`10^{5.4}`, :math:`10^{4.9}`, :math:`10^{4.0}`
      
Since a borne-off piece never returns to the board it is possible to analyze the
game in stages. First all 6/6 positions, i.e. a single green piece vs. a single
red piece, then 6/5 (2 green vs. one red), which always lead either to a 6/6
position or to the game end, then 5/5 and so on. This is quite nice when you
don't have a Google farm at your disposal.

.. LocalWords:  ROGOUR
