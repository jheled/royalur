all: sphinx install

sphinx:
	python setup.py build_sphinx

# TODO: change build-from-source instructions; wheels now build
install:
	python setup.py bdist_wheel
	echo "Now run 'python -mpip install <dist\file_you_just_created.whl>[curses,Pillow]'"

clean:
	python setup.py	clean --all
