Opening Urrors 
==============

The Royal game of Ur looks simple. Seven identical pieces per side on a small
board with just a few simple rules. Typically only two or three possible moves
in each turn, and the best one is usually obvious. But looks can be
deceiving. For example, getting to start increase your winning chances by 1.5%,
from 50% to 51.5%. Say you roll a 1 and your opponent rolls 1 too, and now you
roll a 2. Your move?

::
   
   X: ==@@
   
   [6] ...o  .. (0)
       ........
   [6] ...x  .. (0)

If you moved from `a` to `c` you squandered your good luck and then some. You
shed almost 2% and stand at 49.6%. The correct move is to enter a second piece
to `b` with a 51.5%.

::
   
   X: ==@@
   
   [6] ...o  .. (0)
       ........
   [6] ...x  .. (0)
   
       e 51.49  
    ** a 49.59  (-1.90)

In fact, entering two pieces with 1 and 2 (or 2 and 1) at the start is always
correct, regardless of Red dice and moves. This is nice because it makes an easy
to remember rule. It would have been even nicer if there was an obvious reason
and you did not need to remember anything, but I can't see anything clear cut.
Sure, I can claim than now 2,3 and 4 will get me to `d` on the next turn for an
extra move, but I am pretty sure I could invent something as reasonable if it
was the other way round. With that in mind, let's review the opening moves.

Ur Openings
-----------

(1,1),(2,2),(3,3) and (4,4) are forced, and we took care of (1,2) and (2,1)
above. What about (1,3)? Typically you move your piece to `d` for the extra turn
(case (a)), but not always. If the `4` if already occupied (your so very lucky
opponent started with a (4,4)) you enter two pieces (case (b)), unless there is
a juicy target to hit (like case (c)). The same rules apply to (3,1).

::

        (a)                   (b)                  (c)
   [6] ..O.  .. (0)     [5] ...O  .. (0)     [5] ....  .. (0)
       ........             ...O....             .O.O....
   [6] X...  .. (0)     [5] .X.X  .. (0)     [6] X...  .. (0)

It seems that after your opponent captured the `4` you move to a defensive
stance and retaliate by hitting pieces on the 1-3 squares. (1,3) is not as
simple as (1,2) but at least there is a relatively simple way to remember what
to do.

(2,3) is next. Like (1,2) you almost always enter two pieces, but there are two
exceptions. If your opponent has a piece on `1` (after (4,1)) you hit it, and
you advance to `1` if he has a piece on `3`, like so.

::
   
  [6] ....  .. (0)
      X.O.....
  [6] ....  .. (0)

But doing so when Green has a piece on `2` is quite an error (-1.5%). I could
invent a story why this is so, but honestly I find it slightly mystifying.

::

  X: =@@@  b               X: =@@@  b
  [6] ....  .. (0)         [6] ....  .. (0)
      ..o.....                 .o......
  [6] ..X.  .. (0)         [6] ..X.  .. (0)
  
   ** b 47.74                  e 48.10  
      e 46.96               ** b 46.62  (-1.48)

The same rules apply to (3,2). With a (4,1) you advance to `1`. With (1,4) you
enter two pieces, unless there is a Red piece to hit at `1`. Not hitting cost
2%!. 

(4,2)/(2,4) are identical to (4,1)/(1,4). You obviously advance to `2` with a
(4,2), and split (2,4) unless there is a hit on `2`. Same for (4,3) and (3,4).

This examination of Green first two turns exemplify the deceptiveness of
ROGOUR. Almost every case is clear and obvious, but the few exceptions can cost
you none trivial amount of equity if you are unaware of them.

.. Local Variables:
.. eval: (auto-fill-mode 1)
.. fill-column: 80
.. End:

..  LocalWords:  ROGOUR
