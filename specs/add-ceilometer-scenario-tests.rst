::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

=============================
Add Ceilometer scenario tests
=============================

https://blueprints.launchpad.net/tempest/+spec/add-ceilometer-scenario-tests

Implement complex scenario tests for the Ceilometer project.
Related Etherpad: https://etherpad.openstack.org/p/ceilometer-tempest-testing

Problem description
===================

Telemetry project uses complex interactions inside the OpenStack cloud, so it's
needed to test not only basic Ceilometer capabilities via API testing, but also
more complex scenarios that might happen in the cloud. In this case scenarios
integration tests need to be implemented.

Proposed change
===============

This blueprint contains the following steps to be implemented:

1. Initial Tempest and Ceilometer integration for the scenario tests
2. Scenario tests themselves (we need to start with the alarms and events
   testing)

   Simple alarms test, for example, will follow next scenario:
   - create alarm which triggered to 'alarm' state and send callback by
   alarm_actions if in last period more then one server had been created,
   - create one server,
   - check that alarm triggered to state 'ok',
   - create two servers,
   - check that alarm triggered to state 'alarm',
   - check that alarms callback received.

   Simple events test will look like the following:
   - choose some action for every OpenStack service (like keypair
   creation in Nova) that should lead to notification sent and then event
   created, each action is followed by specific order of
   notifications and special order of events as well,
   - check events come and their order.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * Artur Svechnikov <asvechnikov@mirantis.com>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

* [asvechnikov] Add Ceilometer client for scenarios tests: DONE
* [asvechnikov] Add Ceilometer events scenarios tests: INPROGRESS
* [asvechnikov] Add Ceilometer alarms scenarios tests: INPROGRESS