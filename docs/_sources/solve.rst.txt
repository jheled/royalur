==========
King of Ur
==========

To be the king of Ur you must be the best player in the kingdom. To be the best player in the
kingdom you need to know the winning probability of each and every one of the 137,913,936 possible
positions. How is that possible? As usual, lets start with the simplest case. What is Green winning
probability in position (a)?

::
   
     [0] ....  O. (6)
 (a)     ........
     [0] ....  X. (6)

With a roll of 1 (probability :math:`^1/_4`) Green wins immediately. If not, the turn passes to Red
and due to symmetry he has exactly the same win probability as Green did before rolling. So, if
:math:`p_x` is the win probability,

.. math::

   p_x = \frac{1}{4} + (1 - \frac{1}{4}) (1 - p_x),

giving :math:`p_x = {^4/_7}` [#]_. How about position (b)?

::
  
      [0] ....  O. (6)
  (b)     ........
      [0] ....  .X (6)

Again, with a 2 (:math:`p = {^3/_8}`) Green wins immediately. With a 1 (:math:`p = {^1/_4}`) he gets
another turn and to position (a), which we already analyzed. In all other cases (0, 3 and 4), the
turn passes to Red. So,

.. math::

   p_x = \frac{3}{8} + \frac{1}{4} \frac{4}{7} + \frac{3}{8} (1 - p_o).

Here there is no symmetry, but the logic for Red is the same as before:

.. math::

   p_o = \frac{1}{4} + (1 - \frac{1}{4}) (1 - p_x).

Solving this system of two equations with two unknowns gives :math:`p_x = {^{116}/_{161}}`
and :math:`p_o = {^{74}/_{161}}` (.72 and .46 approximately).

Those two examples teach us that (a) probabilities are best computed in pairs, position coupled with
its inverse. This is because rolling a 0 (or any roll without legal moves) leaves the board
untouched, only reversed, and (b) to compute a the winning probability of ``Z`` we need the
probabilities of positions arising from making a move in ``Z``. Unfortunately, putting positions in
a sequence where for every ``Z`` the "descendants" of ``Z`` all appear before ``Z`` is possible only
for a small set known as race (or no-contact) positions. In a race position hits are no longer
possible, and in ROGOUR this happens when one side has at most two pieces remaining in play, on his
last two squares. In race positions any actual move is "forward" in position space, and so race
positions can be ordered such that (b) always holds. In general such ordering is not possible and
the dependency is circular: eventually the win probability of the position depends on itself.

This is not a problem in itself. As we just saw, every position "depends" upon itself, and yet it
has a well defined probability. The problem is in figuring out the millions of equations involved:
it is insanely difficult, and even if you do, solving them is doubly insane. Luckily there is an
alternative. Take for example the two equations for position (b). They define :math:`p_x,p_o` in
terms of functions of itself, i.e. :math:`p_x,p_o = f(p_x,p_o)`. Assume we have no idea and
arbitrarily start with :math:`p_x,p_o = ({^1/_2},{^1/_2})`, then apply :math:`f` to get a new
"estimate",

.. math::

   p_x = \frac{3}{8} + \frac{1}{4} \frac{4}{7} + \frac{3}{8} (1 - \frac{1}{2})
   
   p_o = \frac{1}{4} + (1 - \frac{1}{4}) (1 - \frac{1}{2})

and get :math:`(\frac{79}{112} \approx 0.70, \frac{5}{8})`. Just one application and :math:`p_x` is
much closer to its true value. Repeating the procedure, plugging those new "estimates" again to f
gets approximately (0.66, 0.47), and after just five iterations the probabilities are accurate to two
decimal places. This is a well known technique called `Fixed-point iteration
<https://en.wikipedia.org/wiki/Fixed-point_iteration>`_, and if the system is "well behaved" it can
work with millions of dimensions, and it better fucking will because it's our only hope here.

So we need to write the win probability of every position as an expression involving the probability
of "descendant" positions, but it is rarely as simple as for (a) and (b), which had just a single
piece for Red and Green. Consider for example position (c).

::
   
      [0] ....  O. (6)
  (c)     X...X...
      [0] ....  .. (5)

To compute the probability we need to cover all possible dice. Let :math:`p_{o,1}` be the win
probability after Green rolled a 1 and made his move, :math:`p_{o,2}` the probability after a move
with 2 and so on. The overall win probability is:

.. math::

   p_x = \frac{1}{16} (1 - p_{o,0}) + \frac{1}{4} (1 - p_{o,1}) + \frac{3}{8} (1 - p_{o,2}) +
   \frac{1}{4} (1 - p_{o,3}) +   \frac{1}{16} (1 - p_{o,4}).

:math:`p_{o,0}` is simply 1 minus the probability of the reversed position, and :math:`p_{o,4}` is
the complement of,

::
   
      [0] ....  O. (6)
  (c)     X.......
      [0] ....  .X (5)

this being the only move. But what about :math:`p_{o,2}`? It is the complement of one of those two,
but which?

::
   
      [0] ....  O. (6)             [0] ....  O. (6)
 4a       ..X.X...            4b       X.....X.
      [0] ....  .. (5)             [0] ....  .. (5)

They look similar to us mortals, but one might be better for Red than the other, and we need to pick
the lesser one for him.

.. math::

   p_{o,2} = \min(p_{4a}, p_{4b})

Similarly for 1 and 3. The appearance of minimums and maximums in our expressions is one of the main
reasons I called it "insane" to think about solving the system directly. The difference between 4a
and 4b, if you want to know, is 1%. Not a lot, but those are the small advantages that accumulate
from the skilled player which makes kings.

This is basically all the "theoretical basis" [#]_ required to compute the win probability of all
ROGOUR positions. Evaluating in pairs, writing the probabilities as functions of other positions'
and solving with fixed point iterations. The rest is engineering. Not necessarily easy engineering,
but stuff requiring time, dedication, willingness to do boring stuff and attention to
details, and not real thought.

.. [#] If you can't solve this simple equation you better skip the rest of this page.
.. [#] If you wish to give it a fancy name.

.. Local Variables:
.. eval: (auto-fill-mode 1)
.. fill-column: 100
.. End:

..  LocalWords:  ROGOUR

..   
