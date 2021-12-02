
from setuptools import setup
from Cython.Build import cythonize

exec(open("./src/simplesimulator/version.py").read())


setup(
    name = "simplesimulator",
    version =__version__,
    description = "a simple fixed step simulation engine",
    author = "Caspar Lucas",
    python_requires='>=3.6',
    install_requires=[
        'pynput',
        'numpy',
        'scipy',
        'matplotlib'
        ],

    package_dir={'':'src'},
    #packages=['simplesimulator','simplesimulator.blocks'],
    #ext_modules =cythonize(["src/simplesimulator/__init__.py"])
    ext_modules =cythonize(["Examples/example_1.py"])

)