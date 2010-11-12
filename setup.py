from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='modularcache',
      version=version,
      description="cache decorator for python",
      long_description="""\
long long desc""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='memoize cache decorator',
      author='Cyprien Le Pann\xc3\xa9rer',
      author_email='cyplp@free.fr',
      url='',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
