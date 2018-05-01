from distutils.core import setup, Extension
import glob

module1 = Extension('royalur.irogaur',
                    sources = ['royalur/irogaur.cc'],
                    extra_compile_args=['-std=c++0x', '-O3'])

classifiers=[
  "Development Status :: 3 - Alpha",
  "Environment :: Console",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: GNU Affero General Public License v3",
  "Programming Language :: Python",
  "Topic :: Games :: Board Games"
  ]

from royalur import __version__

setup (name = 'royalur',
       version = __version__,
       description = 'Classical Royal Game of Ur',
       long_description = '',
       author = 'Joseph Heled',
       author_email = 'jheled@gmail.com',
       url = 'https://github.com/jheled/royalur',
       license = 'LGPL (V3)',
       classifiers = classifiers,
       platforms = ["Linux", "Mac OS-X"],
       packages = ['royalur'],
       package_dir={'royalur': 'royalur'},
       ext_modules = [module1],
       scripts = glob.glob('scripts/*'),
       data_files=[
         ('data', glob.glob('data/db16.bin')),
         ('doc',glob.glob('html/*.*')),
         ('doc/_images', glob.glob('html/_images/*.*')),
         ('doc/_images/math', glob.glob('html/_images/math/*.*')),
         ('doc/_static', glob.glob('html/_static/*.*'))
       ]
)
