from distutils.core import setup, Extension
import os.path
import re
import glob

module1 = Extension('royalur.irogaur',
                    sources = ['royalur/irogaur.cc'],
                    extra_compile_args=['-std=c++0x', '-O3'])

metadata = dict(re.findall("__([a-z]+)__ = \"([^\"]+)\"",
                open(os.path.join("royalur", "__init__.py"), "r").read()))

classifiers=[
  "Development Status :: 3 - Alpha",
  "Environment :: Console",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: GNU Affero General Public License v3",
  "Programming Language :: Python",
  "Topic :: Games :: Board Games"
  ]

## Fails for first ever install
##from royalur import __version__

setup (name = 'royalur',
       version=metadata["version"],
       description = 'Classical Royal Game of Ur',
       long_description = '',
       author = 'Joseph Heled',
       author_email = 'jheled@gmail.com',
       url = 'https://github.com/jheled/royalur',
       classifiers = classifiers,
       platforms = ["Linux", "Mac OS-X"],
       packages = ['royalur'],
       package_dir={'royalur': 'royalur'},
       ext_modules = [module1],
       scripts = filter(lambda x : x not in ["progs/rollout","progs/review-position"],
                        glob.glob('progs/*')),
       data_files=[
         # Comment out big data file until things stabilize. The distribution
         # will stay small and the data file is not expected to change
         ## ('data', glob.glob('data/db16.bin')),
         ('data', []),
         ('scripts', glob.glob('scripts/*.py')),
         ('doc',glob.glob('html/*.*')),
         ('doc/_images', glob.glob('html/_images/*.*')),
         ('doc/_images/math', glob.glob('html/_images/math/*.*')),
         ('doc/_static', glob.glob('html/_static/*.*'))
       ]
)
