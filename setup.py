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
    name='pyoa',
    packages=['pyoa'],
    description='OA Python Client',
    long_description=long_description,
    keywords='pyoa, oa',
    packages=find_packages(exclude=['docs']),
    install_requires=requirements,
    version='1.0',
    author='Isaac Elbaz',
    author_email='isaac.elbaz@advantisolutions.com',
    url='https://www.advantisolutions.com/'
)
