=====================
Human-like Strategies
=====================

Even a board games novice likely to notice some useful principles (or
strategies) after playing a few games of ROGOUR. For example:

- Back you go, little fella. AKA *hit*.
    Hit an opponent piece if you can.

- Hit them hard, AKA *Chuck* Norris.
    Specifically, hit the most advanced opponent piece.

- Let's do that again, AKA *Donkey* in Duloc.
    Pick moves with give you an extra turn.

- Play it *safe*.
    Prefer positions with a piece on square 4, which is protected from hits.

- Play like a *Bear*
    Bear off a piece if you can.

- The *Homestretch*
    Play pieces into the homestretch (y or z), where they can never be hit again.

- Catch me if you can, AKA *Frank* Abagnale.
    Minimize the probability of getting hit on the opponent next turn. This is
    slightly less straightforward as the others, but takes only a little
    practice to master.

- *Extra* hitter.
    Play the move which gives an extra move **and** has the highest probability of
    hitting an opponent piece in that second move.

Simple-minded Humans
--------------------

Lets start with the most simple minded humans, so simple they can manage only
one of those principles. They look at all the possible moves, discard the
non-compatible ones, and choose a move at random from those remaining. How well
do they fare against the most simple player possible, Mister Random himself?

It is only fitting to let the computer evaluate those human-like strategies. For
each principle, the computer plays 10,000 games against Mr Random (5000 as
green, 5000 as red), and counts wins and losses. Below is a table listing the
win percentages of each strategy, from highest to lowest:

.. csv-table:: Principle win rate (%) against random player
   :header: "Frank", "Chuck", "Hit", "Donkey", "Extra", "H-stretch", "bear", "safe"
   :widths: 9, 9, 9, 9, 9, 9, 9, 9

   93.4-94.3, 85.9-87.2, 85.4-86.8, 69.2-71.0, 68.6-70.4, 62.4-64.3, 58.4-60.4, 58.4-60.3

Note that the win rate is given as a 95% `credible interval
<https://en.wikipedia.org/wiki/Credible_interval>`_ [1]_, mainly to demonstrate
that 10,000 trial are sufficient to separate between the principles.

This simple table is already quite interesting. Even the weakest principle,
safe, wins on average 0.2 points per game, a rating difference of about 65 `ELO
<https://en.wikipedia.org/wiki/Elo_rating_system>`_ points. The strongest,
Frank, is 470 ELO points stronger. Also, Frank is faring considerably better
than Chuck: not getting hit seems more important than hitting, at least against
a random opponent. Or maybe it is the fact that the Frank principle applies to
all positions, while Chuck only to positions with possible hits. That said,
those numbers do not necessarily reflect the relative strength of the various
principle when pitted one against the other. When we let everyone play everyone
else (28 matches, again 10,000 games each) and convert the pairwise wins/loses
into ELO we get the ratings below:

.. csv-table:: Principle ELO rating from pairwise matches 
   :header: "Frank", "Chuck", "Hit", "Donkey", "Extra", "H-stretch", "Safe", "Bear"
   :widths: 9, 9, 9, 9, 9, 9, 9, 9

   1759, 1590, 1585, 1444, 1444, 1406, 1405, 1367

In fact, the agreement between the two lists is very good. The order is almost
identical, only in this pool *safe* is doing better than *bear*, whereas against
random they were equal.

Advanced Humans
---------------

But surly this is taking a very dim view of humanity? Real humans can easily
deal with multiple criteria, so why not our computer masquerading as a human? It
is quite easy to combine principles: each one is a filter, and we can create a
*compound-filter* by stringing together several principles and applying them in
succession. For example **"hit;Frank"** plays by removing all non-hitting moves
and selecting the safest among the rest, and **"Frank;hit"** keeps the safer
ones and picks a move that hit from the rest. However, there are `109600
<https://oeis.org/A007526>`_ possible compound-filters, so it is not feasible to
find the best by trying out all pairs.

But even if finding the best is hard, we can certainly evolve good ones. If we
view those principles as "*genes*" and the compound-filter as a "*genome*" we
can start with a pool of random genomes and evolve it over time. This extremely
simplified evolutionary process proceeds generation by generation. In each
generation we take an existing genome and create a new one by adding, removing
or changing a gene. If the new genome outperforms the weakest in the pool it
replaces it, otherwise it is discarded. If we keep track of the genomes coming
out from the pool we get a list of progressively stronger players. This
competitive process, like most evolutionary ones, is very effective. After 300
generations the pool already contains very similar players of roughly the same
strength. A sample of progressively stronger players from this process, together
with *random* and the strongest looks like this:

- Random
- Frank
- safe;homestretch;hit;Extra                         (1)
- homestretch;Frank;bear;safe;Donkey;hit;Chuck;Extra (2)
- safe;homestretch;hit;Extra;Chuck;Frank;bear;Donkey (3)
- Extra;Chuck;hit;bear;homestretch;Frank;Donkey;safe (4)
- hit;Donkey;safe;homestretch;Extra;bear;Frank       (5)
- hit;Donkey;safe;homestretch;Extra;bear;Frank;Chuck (6)
- hit;safe;Extra;bear;Frank;Donkey;homestretch;Chuck (7)
- hit;safe;Extra;bear;Frank;Donkey                   (8)
- hit;safe;Donkey;bear;Frank;Extra;homestretch;Chuck (9)

Like the products of most evolutionary systems, it is almost impossible to
understand why each outperforms the previous ones, but when we play all pairwise
matches and assign ELO's we get the following picture:

.. csv-table:: ELO rating from pairwise matches 
   :header: "Random", "Frank", 1, 2, 3, 4, 5, 6, 7, 9, 8
   :widths: 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9

   760 , 1323 , 1363 , 1413 , 1565 , 1638 , 1683 , 1686 , 1687 , 1690 , 1693

This relatively simple process generates quite strong players, yet ones which
make human like mistakes. Just play (8) and you will see what I mean. Having
human-like opponents of various strengths is actually quite nice, because
usually it is hard to "degrade" a strong computer players in natural ways.


.. [1] The exact details of how to compute those credible intervals are in the source.

..  LocalWords:  ROGOUR Abagnale Duloc
