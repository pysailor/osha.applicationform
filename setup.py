# -*- coding: utf-8 -*-
"""Installer for this package."""

from setuptools import find_packages
from setuptools import setup

import os


# shamlessly stolen from Hexagon IT guys
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'HISTORY.rst') + \
    read('docs', 'LICENSE.rst')

setup(
    name='osha.applicationform',
    version='0.1',
    description="Plone add-on for usign PloneFormGen to create a form on the "
                "EU-OSHA site, under the ‘vacancies’ section, so that the "
                "applicant can send the CV and the motivation letter via Web.",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone Python',
    author='Syslab.com GmbH',
    url='https://github.com/syslabcom/osha.applicationform',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['osha'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'archetypes.schemaextender',
        'five.grok',
        'Pillow',
        'Plone',
        'plone.api',
        'plone.app.contentlisting',
        'Products.PloneFormGen',
        'Products.PFGDataGrid',
        'Products.PublicJobVacancy',
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'jarn.mkrelease',
            'pep8',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'setuptools-flakes',
            'zest.releaser',
            'zptlint',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
