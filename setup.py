from setuptools import setup
import pystrafe

setup(
    name='pystrafe',
    packages=['pystrafe', 'pystrafe.tests'],
    version=pystrafe.__version__,
    description='Python routines for Half-Life physics computations',
    install_requires=['scipy'],
    python_requires='>=3.2.*',
    license='MIT',
    author='Chong Jiang Wei',
    author_email='me@jwchong.com',
    url='https://github.com/Matherunner/pystrafe',
    keywords='math game physics',
    classifiers=[],
)
