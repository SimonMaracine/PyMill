from setuptools import setup, Extension

module = Extension("minimax", ["minimax.c", "helpers.c"])

setup(
    name='minimax',
    ext_modules=[module]
)
