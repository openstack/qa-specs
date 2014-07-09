::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

============================
Implement Barbican API tests
============================

https://blueprints.launchpad.net/tempest/+spec/add-basic-tests-for-barbican

Add test coverage in Tempest for Barbican APIs


Problem description
===================
Barbican is a ReST API designed for the secure storage, provisioning and management of secrets.
Barbican is an incubated openstack project and it is important that we have tempest tests to validate the
functionality of Barbican API. The goal is to create a set of tests that exercises the documented
positive paths and options of the APIs. The Barbican API specification is located at
https://github.com/cloudkeep/barbican/wiki/Application-Programming-Interface

Proposed change
===============

This blueprint proposes to add functional test coverage for Barbican APIs tests.
Following Implementation is needed in Tempest:

1. Implement service client in /tempest/services/key_management/
2. Implement test cases in /tempest/api/key_management/

1. Implement service client
---------------------------
Seperate service clients is implemented for each type of resource
For example:
secrets_client.py handles API calls to the secrets resource
orders_client.py handles API calls to the orders resource
container_client.py handles API calls to the containers resource


2. Implement test cases
-----------------------
Seperate folder of each type of API needs to be maintained

For example:
tempest/api/key_management/secrets
tempest/api/key_management/orders
tempest/api/key_management/containers

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Meera Belur

Other contributors:
  Apal Song

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------
- Add service clients
- Add new test cases for each APIs using service client

To manage these work items an etherpad has been created
https://etherpad.openstack.org/p/test-barbican-api
