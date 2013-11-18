from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='collective.solr_collection',
      version=version,
      description="A Plone collection that looks inside Solr",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        ],
      keywords='plone solr collection',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://github.com/PloneGov-IT/collective.solr_collection',
      license='GPL',
      namespace_packages=['collective'],
      include_package_data=True,
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.solr',
          'plone.app.collection',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
