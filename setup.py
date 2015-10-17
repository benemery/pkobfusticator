import os
from setuptools import setup, find_packages
import sys

BASE_DIR = os.path.dirname(__file__)

sys.path.append(os.path.join(BASE_DIR, 'src'))

install_require = [
]

test_require = [
    # Testing
    'pytest==2.8.2',
    'pytest-cache==1.0',
    'pytest-coverage',

    # Code quality
    'flake8==2.4.1',
    'radon==1.2.2',
]

setup(
    name="pkobfusticator",
    version="0.0.1",
    author="Ben Emery",
    author_email="willcodefortea@gmail.com",
    description="",
    url="",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_require,
    extras_require={
        'tests': test_require
    }
)
