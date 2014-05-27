..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
 Migrate the negative tests to use auto-gen framework
=====================================================

https://blueprints.launchpad.net/tempest/+spec/autogen-negative-tests

The negative testing framework for api test autogeneration was implemented
during Icehouse. This blueprint is about porting all existing test's to use the
framework.


Problem description
===================

Simple and manual negative tests have usually many code duplication and test
only few aspects. It's also hard to track what is already tested and what is
missing.

Proposed change
===============

- Create porting guide
- Porting all existing negative test (based on JSON) to the framework
- Copy old XML based to negative tests in separate file
- Adapt the framework if something is missing

Alternatives
------------

Let the old test untouched and use the framework only for new tests.

Implementation
==============

Assignee(s)
-----------

Primary assignees:
  David Kranz (dkranz)
  Marc Koderer (mkoderer)


Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

Will be tracked in:
  https://etherpad.openstack.org/p/bp_negative_tests

Dependencies
============

- This blueprint depends on a fixed api schema definition (different blueprint)
