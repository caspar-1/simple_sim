
from setuptools import setup


exec(open("./src/simple_sim/version.py").read())


setup(
    name = "simple_sim",
    version =__version__,
    description = "a simple fixed step simulation engine",
    author = "Caspar Lucas",
    python_requires='>=3.6',
    install_requires=[
        'pynput',
        'numpy'
        ],
        
    package_dir={'simple_sim':'src/simple_sim'},
    packages=['simple_sim','simple_sim.blocks'],

)