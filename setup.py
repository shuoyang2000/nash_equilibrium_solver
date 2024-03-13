from setuptools import setup

setup(name='nash_equilibrium_solver',
      version='0.0.0',
      package_dir={'': 'NE_solver'},
      install_requires=['gurobipy~=11.0.0',
                        'numpy~=1.26.4']
      )