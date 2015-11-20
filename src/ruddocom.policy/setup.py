from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='ruddocom.policy',
      version=version,
      description="Rudd-O.com policy package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Manuel Amador (Rudd-O)',
      author_email='rudd-o@rudd-o.com',
      url='http://rudd-o.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ruddocom'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'Products.PloneKeywordManager',
          'plone.app.caching',
          'collective.ckeditor',
          'collective.plonefinder',
          'plone.app.dexterity',
          'plone.app.multilingual == 2.0.1',
          'archetypes.multilingual == 2.0.1dev0',
          'plone.app.theming',
          'Products.RedirectionTool',
          'wildcard.fixpersistentutilities == 1.1b7',
      ],
      # -*- Extra requirements: -*-
      extras_require={
          'test': ['plone.app.testing']
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone

      [plone.recipe.zope2instance.ctl]
      upgrade = ruddocom.policy.upgrader:main
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
