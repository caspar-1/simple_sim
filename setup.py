
from setuptools import setup

setup(
    name = "simple_sim",
    version = "1.0.0",
    description = "a simple fixed step simulation engine",
    author = "Caspar Lucas",
    python_requires='>=3.6',
    install_requires=[
        'pynput',
        'numpy'
        ],
        
    package_dir={'simple_sim':'src/simple_sim'},
    packages=['simple_sim'],

)