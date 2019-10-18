## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

"""
.. automodule:: royalur.urcore
  :members:

.. automodule:: royalur.play
  :members:

.. automodule:: royalur.humanStrategies
  :members:

.. automodule:: royalur.probsdb
  :members:

"""

from urcore import *
from probsdb import *
from play import *
from humanStrategies import bestHumanStrategySoFar

import os.path
royalURdataDir = os.path.realpath(os.path.dirname(__file__) + '/../../../data')

__version__ = "0.2.1.dev1"
"""The version of royalUr"""

