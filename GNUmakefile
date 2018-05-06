all: sphinx

sphinx:
	PYTHONPATH=$$PYTHONPATH:~/lib/`python --version 2>&1 | sed -s "s/Python /version-/"`/lib/python sphinx-build -b html doc docs

# Install in $HOME/lib; add  $HOME/lib/version-XXX/lib/python to PYTHONPATH.
install:
# fake irogaur for clueless install
	echo "" > irogaur.py
	python setup.py install --home=~/lib/`python --version 2>&1 | sed -s "s/Python /version-/"`
	rm -f irogaur.py irogaur.pyc

clean:
	python setup.py	clean --all
