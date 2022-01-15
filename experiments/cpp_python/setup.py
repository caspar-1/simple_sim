
from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension
extra_compile_args=[]
#extra_compile_args = ['-O0', '-g3']

module1 = Pybind11Extension('simpleSimCore',
                            sources=sorted(glob("src/*.cpp")),
                            include_dirs=['src'],
                            extra_compile_args=extra_compile_args,
                            #language='c++17',
                            )


setup(name='simpleSimCore',
      version='0.0.0',
      description='Simple Simulator Core',
      ext_modules=[module1]
      )
