==============================================================
diffmongo -- a command-line diff tool for MongoDb databases/collections
==============================================================


diffmongo -- a command-line diff tool for MongoDb databases/collections
It's goal to update MongoDb collections without drop/restore procedure them.


.. contents::

.. section-numbering::


History
=======
This tool was developed for APICrafter project, to keep sane updated of production MongoDb collection.
APICrafter is a data platform that provided access to high quality datasets via API.


Requirements
=============

This module uses datadifflib - https://github.com/datacoon/datadifflib

Main features
=============

* Generates action list of changes of MongoDb collections
* Generates text file of index of MongoDb collections


Python version
--------------

Python version 3.6 or greater is required.


Quickstart
==========

Find README.md in 'examples' directory.

To use example, please use data in this directory

Run 'mongorestore', it will create two collections - massfounders and mold

Run command to generate action list
.. code-block:: bash
    $ diffmongo compare -fd massfounders -fc massfounders -td massfounders -tc mold -i inn -o difftable.csv

it will produce file difftable.csv with list of actions:

* "a" - to add record

* "d" - to delete record

* "c" - to update changed record


Run command to apply actions from actions file
.. code-block:: bash

    $diffmongo apply -df difftable.csv -fd massfounders -fc massfounders -td massfounders -tc mold

it will read file difftable.csv and apply each action to the collection mold

Usage
=====

Synopsis:

.. code-block:: bash

    $ diffmongo [flags] [command] <parameter1> <parameter2> ... <parameterX>


Commands:

*  apply      Apply diff table to the MongoDb collection

*  compare    Compares to MongoDB collections and generates table of...

*  indexcoll  Index single collection

