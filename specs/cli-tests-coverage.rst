::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

======================================
Tests coverage of CLI tests in Tempest
======================================

https://blueprints.launchpad.net/tempest/+spec/cli-tests-coverage

Increase CLI test coverage in Tempest


Problem description
===================

There are many read only CLI missing their test coverage in Tempest.
Some existing CLI tests donot verify the output.

Proposed change
===============

This is spec to increase the read only CLI tests coverage in Tempest,
which includes:

* new CLI tests which are read only and not present in tempest
* improve the existing CLI tests to have more output verification.
* For new CLI tests, minimum python client version needs to be checked
  as per https://review.openstack.org/#/c/99984/

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Mh Raies <mh.raies@nectechnologies.in>

Other contributors:

* Ajay <ayayyadavmdu@gmail.com>
* Vishal kumar mahajan <mahajan.vishal.mca@gmail.com>

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

* new CLI tests needs to be added
* improvement in existing cli tests

Tasks will be managed using etherpad :
(https://etherpad.openstack.org/p/missing-cli-tests-in-tempest)
