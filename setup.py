from os import path

from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

# mark our location
here = path.abspath(path.dirname(__file__))

# obtain the long description
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

raw_requirements = parse_requirements(
    path.join(here, 'requirements.txt'), session=False)
requirements = [str(x.req) for x in raw_requirements]

setup(
    name='pyopenaristos',
    packages=['pyopenaristos'],
    description='OA Python Client',
    long_description=long_description,
    keywords='pyopenaristos, oa',
    install_requires=requirements,
    version='1.3',
    author='Isaac Elbaz',
    scripts=[
        'pyopenaristos/bin/oa'
    ],
    download_url='https://github.com/Advanti/pyopenaristos/archive/1.3.tar.gz',
    author_email='isaac.elbaz@advantisolutions.com',
    url='https://www.advantisolutions.com/'
)
