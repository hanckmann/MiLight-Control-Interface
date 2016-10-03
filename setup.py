from setuptools import setup, find_packages
import sys, os

version = '1.0.1'

setup(name='mci',
      version=version,
      description='MiLight-Control-Interface',
      long_description='''The MiLight Control Interface is a powerful Python API to control MiLight LED bulbs and strips (White and RGBW).''',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Home Automation',
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='milight interface',
      author='Patrick Hanckmann',
      author_email='hanckmann@gmail.com',
      url='https://hanckmann.com',
      license='GNU Lesser General Public License v2 (LGPLv2)',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points='''
      # -*- Entry points: -*-
      ''',
      )
