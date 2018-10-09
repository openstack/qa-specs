::
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

==================================================
 Increase the number of scenario tests for Neutron
==================================================

https://blueprints.launchpad.net/tempest/+spec/neutron-advanced-scenarios

Increase the number and coverage of scenario tests in Tempest for Neutron.

Problem description
===================

Currently there is a limited number of scenario tests in Tempest for Neutron.
Attempts have been made in the recent past to increase this number. However,
these efforts have not been very effective due to the following factors:

* A very small number of developers currently contributing code for Neutron
  scenario tests.
* The lack of a structured process to make sure developers achieve progress.

Proposed change
===============

Under this blueprint, a structured process will be followed with the overall
goal of creating a community of engaged and well supported scenario tests
developers. This process consists of the following steps:

#. A "How to develop scenario tests for Neutron" tutorial will be developed as
   an extension to the `Tempest documentation
   <https://docs.openstack.org/tempest/latest/field_guide/scenario.html>`_.
   This tutorial will include clear and strict guidelines for documentation and
   logging. On one hand, each test is unique, and complex operations will most
   likely be included in supporting methods or shared between modules, so
   documentation should provide sufficient information about the test for
   people outside the Tempest or Neutron efforts, hopefully even for "simple"
   users who will use the scenarios to test their deployment. On the other
   hand, tests operation should be logged in detail so it is clear what
   progress and operations took place prior to any failure that might arise.
#. A set of scenario tests will be well specified taking as a starting point
   the result of the design summit in Atlanta and captured at the
   `Juno design summit etherpad
   <https://etherpad.openstack.org/p/TempestAndNeutronJuno>`_. The
   specification of these scenarios will be done in close cooperation with the
   Neutron core team. The specification of each scenario will include a list
   of people with expertise to support the test developer.
#. A message will be sent to the openstack-dev mailing list inviting developers
   to select one of the scenarios specified at the `Juno design summit etherpad
   <https://etherpad.openstack.org/p/TempestAndNeutronJuno>`_. Developers will
   assign themselves to the scenarios they have interest on by signing their
   name next to the corresponding specification in the above mentioned
   etherpad.
#. Progress will be tracked for each scenario on a weekly basis.
    * The main goal of this tracking is to make sure developers are getting
      the support they need.
    * Tracking will insure developers get prompt reviews from Neutron and
      Tempest cores.
    * Progress will be discussed at the Neutron and Tempest weekly IRC
      meetings.
    * The tracking will be kept at the `Juno design summit etherpad
      <https://etherpad.openstack.org/p/TempestAndNeutronJuno>`_.
#. Test owners will be designated. Owners will be in charge of maintaining the
   code, debug future failures, enhancing code documentation and logging, as
   well as providing reasonable support for relevant questions (though adequate
   docs should minimize such questions), thus easing new contributors into the
   community

The tests developed as result of this process will reside in the tempest tree
hierarchy at tempest/scenario

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Miguel Lavalle <miguel@mlavalle.com>

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

* Create tutorial on Tempest scenario tests for Neutron: Juno-1
* Create specification of scenarios to develop: Juno-1
* Send message to openstack-dev inviting developers to review tutorial and
  select scenarios to implement: Juno-1
* Merge new Neutron scenarios to Tempest tree: Juno-3

Dependencies
============

None
