..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=====================
 Fuzzy test framework
=====================

https://blueprints.launchpad.net/tempest/+spec/fuzzy-test

The negative testing framework tests single aspects of an API server in an
automatic manner based on json schema's. Using this functionality fuzzy tests
can be created with the same process but with a different focus.


Problem description
===================

Tempest does not have any coverage of security aspects. Using such a framework
to detect security vulnerabilities will be an important new testing area for
Tempest.

Proposed change
===============

Focus of this framework is vulnerabilities identification and denial of
service (DoS) attacks. It can use the api schema definitions as input to
produce flawed requests.

Denial of service
-----------------

DoS patterns are easy to validate and are considered as first step.
A certain service produces a portion of flawed requests together with valid
requests like authentication. To validate if a DoS attack was successful a set
of usual Tempest API test can be used for this purpose. To produce the needed
load the stress test framework of Tempest can be used to produce a higher load
rate.

Vulnerabilities identification
------------------------------

Identification of security issues can be very complex and automatic detection
can be only done very limited. To identify issues that may are vulnerabilities
the following data needs to be analyzed:

 - Result of a request:
   Success codes or internal server errors are potential threats that need be
   analyzed and logged by the framework.

 - System availability:
   A check if all the OpenStack components are available be used as validation.

 - Request logging:
   Tempest rest client loges all requests. This is needed to identify request
   or scenarios that causes a threat.

Data generation
---------------

The data generation should support different sources and this could be a
possible interface to 3PP fuzzy testing products. With the multibackend
functionality of the negative testing framework (see
https://review.openstack.org/#/c/73982/) different test generators can be used.
These generator must stick to the interface define in the base class
(tempest.common.negative.base).



Alternatives
------------

Use third party product for fuzzy test generation and don't integrate it in
Tempest.


Implementation
==============

Assignee(s)
-----------

Primary assignees:
  Marc Koderer (mkoderer)


Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

Will be tracked in:
  https://etherpad.openstack.org/p/bp_fuzzy_test

Dependencies
============

None.
