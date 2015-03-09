from setuptools import setup, find_packages
import os

version = '1.0.0.dev0'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'plone.app.testing',
    ]

setup(name='ftw.pdfify',
      version=version,
      description='Create PDF from documents.',
      long_description=open('README.md').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.pdfify',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'pdfify_celery',
      ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
