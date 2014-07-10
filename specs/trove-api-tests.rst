::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

============================
Implement Trove API tests
============================

https://blueprints.launchpad.net/tempest/+spec/tempest-guest-tests

Increase integration test coverage in Tempest


Problem description
===================

Currently only below Trove APIs test cases are present in Tempest-
    -flavor
    -version

Tempest should have more Trove APIs test coverage.


Proposed change
===============

This blueprint proposes to add more Trove APIs tests.
Following Implementation is needed in Tempest:

1. Implement service client in /tempest/services/database/
2. Implement test cases in /tempest/api/database/

1. Implement service client
--------------------------------
Seperate service client should be implemented for each type of APIs

For example-

* All instance APIs client should be implemented in
  /tempest/api/database/json/instances_client.py
* All backup APIs client should be implemented in
  /tempest/api/database/json/backups_client.py

2. Implement test cases
--------------------------------
Seperate folder of each type of API needs to be maintained

For example-

* All instance APIs tests should go under /tempest/api/database/instances
* All backup APIs tests should go under /tempest/api/database/backups.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Nikhil Manchanda <SlickNik@gmail.com>

Other contributors:

* Ghanshyam Mann <ghanshyam.mann@nectechnologies.in>
* Peter Stachowski <peter@tesora.com>
* Ravikumar Venkatesan <ravikumar.venkatesan@hp.com>
* Ashish Nigam <ashish.nigam1@globallogic.com>

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

- Add service client for each type of APIs
- Add new test cases for each APIs using service client

  Tasks will be managed using etherpad :
  (https://etherpad.openstack.org/p/trove-tempest-items)
