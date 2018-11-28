==============
Skill and Luck
==============

Luck is a tricky concept. So, for your sake and mine, let us hope this page is not utter
nonsense. Never assume I know more that you on anuthing.

First, games are all about skill. The better player will win a fair game. Not each and every time,
but he will come ahead in the long run. The expected number of points a player wins per game is
called *equity*. In a game of pure skill the supreme master expects to win all his games, and his
equity is 1, or one full point per game. If the game is totally random any player will win half the
time and lose the other half, with an equity of zero. If your chance of winning a single game is 75%
your equity is 0.5: you expect to win three out of four games, and lose one, for a total of two
points per four games, which is on average half a point per game.

But in real life no one wins all the time. I will surely lose to Stephan Curry in a three point
shooting match, but even **he** misses a few shots every hundred, and I can make a few, so if the
"math" consists of just one shot match I should win one time in a thousand. Quite high, actually,
when you think about that lottery ticket you bought yesterday.

Those random factors we call luck limit the earning power of skill. Skill can buy you only that much
per time unit. In real life those random factors are physical, biological and psychological. In
board games they are artificial, typically introduced by a random event generator (the *Dice*). The
dice is fair and oblivious to skill, and limits the equity of better players. Even the greatest
Putzer can sometimes win against the world champion. The dice might provide him enough equity just
this one time to overcome the skill gap.

But luck, surprisingly enough, has a second source. I can beat Magnus Carlsen in a game of chess by
selecting the best moves just by chance. Obviously the effect of such luck is vanishingly small in
chess because there are many moves per position, and most of them are bad or even catastrophic. In
ROGOUR, on the other hand, there are only a handful of moves in each position, and this kind of luck
may have a noticeable effect.

Here is how luck and skill interact in a game. Say the win probability before you roll the dice is
``p``. This probability is composed of all possible futures: it is the sum of the probability of
throwing a 1 times your probability of winning after you made the best move with a 1, plus the
probability of throwing a 2 times your probability of winning after you made the best move with 2,
etc.

.. math::
   p = \sum_{\text{dice d}} Pr(d) Pr(\text{Winning after the best move with d})

Now you roll the dice and get some specific value. Since ``p`` is a weighted average of those
possible futures, some will be higher than ``p`` and others smaller. If ``d`` leads to a position
whose win probability is higher you were lucky, and if it is smaller, unlucky. Skill comes in after
you got your dice. There are several possible moves with the same dice, and if you pick any move but
the best, the difference in win probability between that move and the best one is what you lose in
equity.

If that is not explicit enough, here is an example from real play. It is late in the game and both
sides has only two pieces left in play. Before the throw X winning probability was 47.1%. He got a
2, which is lucky since it brings his winning chances to 51.31%, more than 4%, which is the
threshold I use for lucky. You get this kind of lucky about one time out of twenty in ROGOUR. But X
was greedy and hit O, which is usually good but here it is not as good as playing his other piece
from b to d, advancing his backward piece and getting an extra chance to hit O with a 2 or a 3. And
4 would be quite good as well.

::
    
    X: 2! 4
    [0] ....  .. (5)
        ..oX.o..         
    [0] ..x.  .. (5)
    
        b 51.31          
     ** 4 50.13  (-1.18) 

So luck and unluck accumulate throw by throw. The expected value of the total luck is zero: this is
what fair means. But in a particular game one side might be luckier than the other, just by
chance (pun intended). Loss from imperfect play also accumulates. And you win when your total luck
minus your losses by skill is bigger than your opponent luck minus skill. This is how Clueless, our
random player, beats Ishtar the goddess of Ur:

::

  Skill: Ishtar 0.00  Clueless -85.58
  ELO:   Ishtar  2000   Clueless  Dreadful beyond words.

  Luck: Ishtar -110.52  Clueless 26.61

Ishtar sat with a single piece on the home stretch for 50 moves or so while Clueless raced off 4
pieces. The luck difference was 1.36 points, big enough to compensate for Clueless throwing away
0.85 points during the game.

Now that we hopefully understand a little better the interplay between luck and skill we can go back
to Finkel statement about the fifty-fifty contribution. And I honestly not sure what it means. An
equity difference of 0.5 is equivalent to an ELO difference of 190, which is clearly much smaller
than the range of ROGOUR which is larger than a 1000 points. Another interpretation can be the
"relative" size of luck and skill. By size I mean the standard deviation of your typical luck
difference on a single throw. For ROGOUR this turns out to be about 3.5%. But what is the size of
skill? The size of errors by Clueless, our completly random player, is around 4%. Which is about
equal to luck, only it is ridiculous to speak about skill for someone completly devoid of it. And if
you look at even very weak players luck size drops to 1, 1.5%. Obviously, when you have skill your
errors are smaller, and luck becomes more prominent. With two perfect players it is pure luck that
decides the outcome. This sounds paradoxical until you think about it. What matters is not absolute
skill but the difference in skill. So the important measure is the range of skill possible. And with
the 1000 ELO points of ROGOUR I think one can claim it is similar to plain Backgammon (without the
doubling cube.)

.. Local Variables:
.. eval: (auto-fill-mode 1)
.. fill-column: 100
.. End:

..  LocalWords:  Magnus Carlsen vanishingly ROGOUR Putzer unluck Finkel ELO completly
