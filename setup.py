#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Custom build hooks for CGRtools — keep this file tiny!
#
from importlib.util import find_spec
from pathlib import Path
from distutils.command.sdist import sdist
from distutils.util import get_platform
from setuptools import setup
from setuptools.command.build_ext import build_ext

class _sdist(sdist):
    """Ship *both* INCHI binaries inside the source distribution."""
    def finalize_options(self):
        super().finalize_options()
        self.distribution.data_files = self.distribution.data_files or []
        self.distribution.data_files.append(
            ('lib', ['INCHI/libinchi.so', 'INCHI/libinchi.dll'])
        )


if find_spec("wheel"):
    from wheel.bdist_wheel import bdist_wheel

    class _bdist_wheel(bdist_wheel):
        """Strip the irrelevant INCHI binary from the wheel."""
        def finalize_options(self):
            super().finalize_options()
            self.root_is_pure = False         # wheel contains native files
            platform = get_platform()
            self.distribution.data_files = [
                ('lib', ['INCHI/libinchi.dll' if platform.startswith('win') else
                         'INCHI/libinchi.so'])
            ]


if find_spec("Cython"):
    from Cython.Build import cythonize

    class _build_ext(build_ext):
        def finalize_options(self):
            super().finalize_options()
            self.distribution.ext_modules = cythonize(
                self.distribution.ext_modules, language_level=3
            )

cmdclass = {'sdist': _sdist}
if find_spec("wheel"):
    cmdclass['bdist_wheel'] = _bdist_wheel
if find_spec("Cython"):
    cmdclass['build_ext'] = _build_ext

setup(cmdclass=cmdclass)
