..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
 API schema unification
=======================

https://blueprints.launchpad.net/tempest/+spec/api-schema-unification

API schema's are used for different purposes in Tempest. This blueprint tries
to unify all existing ways.


Problem description
===================

Tempest currently has two sources of schema definitions:

 - The response validation framework (``tempest/api_schema``)
 - The negative test framework, which automatically creates requests
   (``etc/schema``)

Differences in a nutshell:

 - File type
   - ``etc/schema`` files are json based
   - ``tempest/api_schema`` files are python modules
 - Data type
   - ``etc/schema`` contains Tempest related data (result code check base on
   generators)
   - ``tempest/api_schema`` contains data that can be imported from projects
 - Content
   - ``etc/schema`` is used for request generation
   - ``tempest/api_schema`` is used for response validation


Proposed change
===============

Move all schema's to tempest/api_schema and use .py files instead of .json
files. This gives the possibility to use inheritance (or any other python
magic) to reduce code duplication. Inside of the py files the data format
will be dicts instead of json. This is due to the fact that all existing
definitions are already defined as dicts.

The proposed folder structure::

  tempest
  |-> api_schema
  |  |-> request # old content of ``etc/schema``
  |  |  |-> compute
  |  |  |  |-> v2
  |  |  |  |-> v3
  |  |-> response # old content of ``tempest/api_schema``
  |  |  |-> compute
  |  |  |  |-> v2
  |  |  |  |-> v3


Next steps
----------
Out of scope of this blueprint but next steps:

 - Replace dicts with json definitons
 - Having same/similar json style
 - Using same load mechanism

Alternatives
------------
To be discussed.


Implementation
==============

Assignee(s)
-----------

Primary assignees:
  Marc Koderer (mkoderer)


Milestones
----------

Target Milestone for completion:
  Juno-final

Work Items
----------

 1. Move all files to one location
 2. Rewrite all .json files to .py files and adapt negative testing framework
 3. Unify filenames to have consistence between /response and /request

Dependencies
============

None.
