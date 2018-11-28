========================
More on the world of  Ur
========================

A typical game of ROGOUR lasts between 177 and 243 turns (A turn is one roll of
the dice followed by a legal move, if any). There is no longest game. With
enough zeros you can get to any length. The shortest possible "cooperative" game
is 42 turns: Green hops from home to `d` to `4` to `7`, Red makes some meaningless
move, Green bears off with a 3, another meaningless move by Red, a total of 6
turns, and the cycle repeats six more times for the remaining pieces.

This is kind of obvious when you think about it. Slightly more surprising is the
fact that the shortest *perfect* is 42 turns as well. I wish Douglas Adams was
alive and I could write and tell him about it. A perfect game is one played
between two perfect players (two Ishtars), where each move is the best
available. It looks slightly different than the "cooperative" game above since
Red's dice has to be carefully crafted so she has no opportunity to disrupt
Green. Needless to say, it is a feast of fours for Green and threes and zeros
for Red. You can find the game record in the games directory
(``shortestPerfectGame.ur``).

The expected number of turns in a game is 209.810273. This is exact, and
computed in a similar way as position probabilities, that is, by solving an
enormous system of equations with 137,913,936 unknowns, using the same shortcuts
and techniques we used before. This is for Ishtar vs. Ishtar games. The numbers
are different when other players get involved. It falls to around 195 when
Ishtar plays Santa (1820 ELO), and to 190 when she plays against Sam (1650
ELO). But it is 210 again for Santa vs. Sam, so it seems to depend on the
difference in skill. The larger the difference, the shorter the game. Hardly
surprising.

Due to the simple nature of the rules every board position is reachable from the
starting position. You can always "go backwards", that is find a piece to move
backwards. What might be slightly more surprising is that every position is
reachable in at most 56 turns. Those *max* positions are all of the
"two-sided-bearoff" variety:

::
  
   [0] ....  OO (5)     [0] ....  O. (6)     [0] ....  O. (6)
       ........             ........             ........
   [0] ....  XX (5)     [0] ....  XX (5)     [0] ....  .X (6)

And so on.

Still, even though all positions are reachable, some might never appear with
good play. That is, never reached in a game of two perfect players. Actually I
expected this set to be quite large, but I was wrong. Only 5,941,240 positions
(4.3%) never appear under perfect play. That means that a ROGOUR expert needs to
be familiar with almost any type of position.

..  LocalWords:  ROGOUR Ishtars

.. Local Variables:
.. eval: (auto-fill-mode 1)
.. fill-column: 80
.. End:
