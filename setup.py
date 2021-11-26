
from setuptools import setup


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
    packages=['simplesimulator','simplesimulator.blocks'],

)