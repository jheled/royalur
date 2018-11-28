==============================
The (Classic) Royal Game of Ur
==============================
.. image:: Royal-Game-of-Ur.jpg
  :align: center
  :scale: 25 %

The Royal Game of Ur (ROGOUR) is a 5000 year old board game. Watch this
entertaining `video <https://youtu.be/WZskjLq040I>`_ for an excellent
introduction by Irving Finkel. Finkel, a curator in the British museum and a fan
of the game since childhood, deciphered the game rules from a 4000 years old
cuneiform tablet which describes a **modern** versions of the game!

I was immediately captivated, which is hardly surprising. The game has been
capturing the hearts of men, women and children for thousands of years. But it
was not just the cool factor, the unusual dice, and the idea that we can play it exactly
like our great ancestors. I was also drawn by the game's compact form: with only
14 pieces on 20 squares it might be small enough to crack on my own small
laptop!!  Even more, I was intrigued when Finkel claimed with great authority
that the balance of luck and skill in ROGOUR is 50%-50%, while Backgammon is
closer to 40-60. I will return to this question of luck vs. skill later, but for
now let me say I suspect Finkel underestimates how much skill can hide in a simple
looking games like ROGOUR. It is an easy mistake to make; the board is
relatively small and there are only a few moves per position. Yet, looks can be
deceiving. Let me give you a taste. You are red and rolled a 3. Assuming you
either watched the video or read :ref:`rules`, what is your move?

.. 42lOb
.. image:: pos01.png
  :align: center
  :scale: 50 %

Most players would not think once and hit the green piece at 7, possibly with a
superior smirk towards green. After all, that piece is about to enter the home
stretch, and hitting it costs green 11 whole pips! And now **WE** have a piece
only 4 pips away from the finish line. But it turns out this is not the best move:
at this stage of the game controlling the *safe* 4 square is more important than
hitting. Entering another piece gives red 57.18%, while hitting green gives only
54.2%!! An equity loss of 0.06!

I suggest you go and play a few games against the machine (the program is called
`tkur`). You have a few opponents to choose from, starting with Joe, an absolute
beginner, to Ishtar, the Ur goddess [#]_. You should record you games (with a
`-r`) and analyze them using `printGame`.
   
This repository contains code relating to ROGUR, the fascinating precursor to
backgammon.

.. At the moment you can play against Ishtar (the perfect player) or
.. some "human-like" opponents (using either a very primitive `curses
.. <https://en.wikipedia.org/wiki/Curses_(programming_library)>`__ interface or a
.. `Tkinter <https://en.wikipedia.org/wiki/Tkinter>`_ GUI), then view and analyze
.. your saved games. See the ``games`` directory for examples.

.. toctree::
   rules
   gamesize
   humanst
   solve
   luck
   world
   play
   
The ROGOUR code
---------------
.. 50% luck 50% skill = 75%-25%, 0.5 equity ?

.. toctree::
   :maxdepth: 5

   scripts
	      
   urlib

.. [#] I am aware the Sumerians called her Inanna, but the Assyrians and
       Babylonians knew her as Ishtar, a name which I think is more
       familiar today.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

..  LocalWords:  Finkel rosetta ROGOUR royalur Rulez gamesize humanst Inanna printGame tkur

.. Local Variables:
.. eval: (auto-fill-mode 1)
.. fill-column: 80
.. End:

