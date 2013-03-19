==================================
Build application forms with Plone
==================================

`osha.applicationform` is a minimalistic Plone add-on that builds on top of the
`PloneFormGen` product to enable you to build forms on the EU-OSHA site,
under the ‘vacancies’ section, so that the applicant can send the CV and the
motivation letter via Web.

* `Source code @ GitHub <http://github.com/syslabcom/osha.applicationform>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/osha.applicationform>`_
* `Continuous Integration @ Travis-CI
  <http://travis-ci.org/syslabcom/osha.applicationform>`_

Installation
============

To install ``osha.applicationform`` you simply add ``osha.applicationform`` to
the list of eggs in your buildout, run buildout and restart Plone. Then,
install `osha.applicationform` using the Add-ons control panel.

Importing HR Application Form
-----------------------------

Theoretically it should be possible to import the form and its fields
automatically with the 'content' GS profile using the structure folder. But
there are some errors when running the profile, so currently the form must be
imported manually.

File hr-application-form.tar.gz in profiles/content contains the exported
form with all the fields.

Steps for importing the form:

1. Create a new Form Folder
2. Change the form view by clicking on "Display -> HR Application Form"
3. Click on "Actions -> Import"
4. Select file "hr-application-form.tar.gz"
5. Check "Remove Existing Form Items?"
6. Click "import"
7. There are some manual steps needed to make the languages field work
properly:
* click on 'Contents' tab on the form folder, then on 'Languages' field
* click 'Edit', then check options 'Allow Row Deletion', 'Allow Row
Insertion' and 'Allow Row Reordering'.
* click 'Save'


Requirements
============

    * `Plone <http://plone.org/>`_ 4.1 or newer
    * `PloneFormGen <http://plone.org/products/ploneformgen>`_ 1.7 or newer

Usage
=====

TODO

