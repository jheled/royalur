==============
Skill and Luck
==============

Luck is a tricky concept. So, for your sake and mine, let us hope this page is not utter
nonsense. Never assume I know more than you on the subject.

First, games are all about skill. The better player will win a fair game. Not necessarily in each
game, but he will come ahead in the long run. The expected number of points per game for a player is
called *equity*. In a game of skill the supreme master expects to win all his games his equity of 1,
one full point a game. If the game is totally random game anyone will win half and lose half, with
an equity of 0. If your chance of winning a single game is 75% your equity is 0.5: in four games you
expect to win three and lose one, for a total of two points in four games, which is on average half
a point per game.

But no one wins all the time in a real life game. I will surely lose to Stephan Curry in a three
point shooting match, but even **he** misses a few shots every hundred, and I can make a few, so in
a single shot match I might win one time in a thousand. Quite high, actually, when you think about
that lottery ticket you bought yesterday.

Those random factors we call luck limit the earning power of skill. It can buy you only that much
per time unit. In real life those random factors are physical, biological and psychological, but in
board games they are artificial, typically introduced by a random event generator (the *Dice*). The
dice is fair and oblivious to skill, and so limits the equity of better players. Even the greatest
Putzer can sometimes win against the world champion. The dice might provide him enough equity this
one time to overcome the difference in skill.

But luck, surprisingly enough, has a second source. I can beat Magnus Carlsen in a game of chess by
selecting the best moves just by chance. Obviously the effect of such luck is vanishingly small in
chess because of the number of moves per position is large, and most moves are bad or even
catastrophic. In ROGOUR, on the other hand, with only a handful moves per position, this kind of
luck might have a noticeable effect.

Here is how luck and skill interact in a game. You have a some win probability ``p`` before you
throw the dice. This probability is composed of all possible futures: it is the sum of the
probability of throwing a 1 times your probability of winning after you made the best move with 1,
plus the probability of throwing a 2 times your probability of winning after you made the best move
with 2, etc.

.. math::
   p = \sum_{\text{dice d}} Pr(d) Pr(\text{Winning after the best move with d})

Now you throw the dice and get some specific dice value. Since ``p`` is a weighted average of those
possible futures, some will be higher than ``p`` and some smaller. If ``d`` leads to a position with
larger win probability you were lucky, and is smaller unlucky. Skill comes in after you have your
dice. There are usually several possible moves with the same dice, and if you pick any move but the
best, the difference in win probability between that move and the best result in a lose of equity.

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
chance (pun intended). Lose from imperfect play accumulates too. And you win when the sum of you luck
minus your lose by skill is greater than your opponent luck minus skill. This is how Clueless, our
random player, beats Ishtar the goddess of Ur:

::

  Skill: Ishtar 0.00  Clueless -85.58
  ELO:   Ishtar  2000   Clueless  Dreadful beyond words.

  Luck: Ishtar -110.52  Clueless 26.61

Ishtar sat with a single piece on the homestretch for 50 moves of so and so clueless bears off 4
pieces. The luck difference was 1.36 points, not enough to overcome Clueless shedding 0.85 points on
the way.

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
the 1000 ELO points of ROGOUR I think one can claim it is similar to Backgammon (without the
doubling cube.)

.. Local Variables:
.. eval: (auto-fill-mode 1)
.. fill-column: 100
.. End:

..  LocalWords:  Magnus Carlsen vanishingly ROGOUR Putzer unluck Finkel ELO completly
