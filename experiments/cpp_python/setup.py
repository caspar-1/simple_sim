
from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

module1 = Pybind11Extension('simpleSimCore',
                    sources = sorted(glob("src/*.cpp")),
                    include_dirs=['src'])



setup (name = 'simpleSimCore',
       version = '0.0.0',
       description = 'Simple Simulator Core',
       ext_modules = [module1]
       )

