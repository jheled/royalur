import setuptools
import os.path
import re
import glob

module1 = setuptools.Extension("royalur.irogaur",
                               [os.path.join("royalur", "irogaur.cc")])

metadata = dict(re.findall("__([a-z]+)__ = \"([^\"]+)\"",
                open(os.path.join("royalur", "__init__.py"), "r").read()))

setuptools.setup(
    name="royalur",
    version=metadata["version"],
    description="Classical Royal Game of Ur",
    author="Joseph Heled",
    author_email="jheled@gmail.com",
    url="https://github.com/jheled/royalur",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Board Games"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    ext_modules=[module1],
    entry_points={
        "console_scripts": [
            "printGame=royalur.cli.printGame:main",
            "curses-gui=royalur.cli.cursesGUI:main [curses]"
        ],
        "gui_scripts": [
            "tkur=royalur.gui.tkur:main [Pillow]"
        ]
    },
    extras_require={
        "curses": ["windows-curses;platform_system=='Windows'"],
        "Pillow": ["Pillow"]
    },
    data_files=[
        # Comment out big data file until things stabilize. The distribution
        # will stay small and the data file is not expected to change
        ('scripts', glob.glob(os.path.join("scripts", "*.py"))),
        ('doc',glob.glob(os.path.join("html", "*.*"))),
        ('doc/_images', glob.glob(os.path.join("html", "_images", "*.*"))),
        ('doc/_images/math', glob.glob(os.path.join("html", "_images", "math", "*.*"))),
        ('doc/_static', glob.glob(os.path.join("html", "_static", "*.*")))
    ]
)
