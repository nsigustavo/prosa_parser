from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='prosa_parser',
      version=version,
      description="parser literal text",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='parser',
      author='Gustavo Rezende',
      author_email='nsigustavo@gmail.com',
      url='http://prosa.appspot.com',
      license='mit',
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
