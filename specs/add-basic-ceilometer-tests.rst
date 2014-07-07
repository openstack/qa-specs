::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

==============================
Add basic tests for Ceilometer
==============================

https://blueprints.launchpad.net/tempest/+spec/add-basic-ceilometer-tests

Implement basic integration tests for the Ceilometer project.
Related Etherpad: https://etherpad.openstack.org/p/ceilometer-tempest-testing

Problem description
===================

Now Ceilometer is the important metering/monitoring projects of OpenStack.
So it's necessary to include the basic tests into Tempest to make sure it works
fine, as currently there are no these tests presented.

Proposed change
===============

This blueprint contains the following steps to be implemented:

1. Initial Ceilometer Tempest integration
2. Basic REST API based tests

1. Initial Ceilometer Tempest integration
-----------------------------------------

This point includes initial Telemetry client testing code, base classes and
configuration for the Telemetry tests. This step includes Telemetry client
to be implemented as well.

2. Basic REST API based tests
-----------------------------

This step should cover the API functionality for the Ceilometer project. This
requires the following changes:

  * alarm-history API tests and alarming API itself
  * notifications tests for the different types of the notifications (from
    Nova, Cinder, Neutron, Swift, etc.)
  * pollsters tests (with different services polling)
  * other non-scenarios changes (if needed)


Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * Yassine Lamgarchal <yassine.lamgarchal@enovance.com>

Other contributors:
  * Vadim Rovachev <vrovachev@mirantis.com>
  * ravikumar-venkatesan <ravikumar.venkatesan@hp.com>
  * Mehdi Abaakouk <mehdi.abaakouk@enovance.com>
  * nayna-patel <nayna.patel@hp.com>

Ongoing maintainer:
  * Vadim Rovachev <vrovachev@mirantis.com>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* [sileht] Add initial ceilometerclient testing code: DONE
* [yassine] Add base class for Telemetry tests: DONE
* [yassine] Add config for Telemetry: DONE
* [vrovachev] Create telemetry client for tempest: INPROGRESS
* [vrovachev] Create cinder notifications tests: INPROGRESS
* [vrovachev] Create neutron notifications tests: INPROGRESS
* [vrovachev] Create object storage notifications tests: INPROGRESS
* [vrovachev] Create compute notifications tests: INPROGRESS
* [ravikumar] Create all alarms tests: INPROGRESS
* [vrovachev] Create all pollsters tests: TODO

