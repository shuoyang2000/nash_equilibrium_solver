from setuptools import setup

setup(name='nash_equilibrium_solver',
      version='0.0.0',
      author='Shuo Yang',
      author_email='yangs1@seas.upenn.edu',
      package_dir={'': 'NE_solver'},
      install_requires=['gurobipy~=11.0.0',
                        'numpy~=1.26.4',
                        'pyyaml~=6.0.1']
      )