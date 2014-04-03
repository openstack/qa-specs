::

# This work is licensed under a Creative Commons Attribution 3.0 Unported
# License.
#
# http://creativecommons.org/licenses/by/3.0/legalcode

..

=========================
Add service tags to tests
=========================

https://blueprints.launchpad.net/tempest/+spec/add-service-tags

Add new tags to all tests that specify which services get exercised by the
test.

Problem description
===================

When running tempest there is no clear way to specify only run tests that hit
a subset of services. For example, if you wanted to only run tests that used
cinder for the purposes of verifying a new driver there isn't a method to
easily filter the tests run so that only cinder tests are run. The only option
is to manually construct a regex filter that executes the tests which you think
hit cinder's api.


Proposed change
===============

To add a new decorator which will set a service attr for the test specified.
The decorator will have a single parameter which will be a list of the services
that the test exercises. The decorator will only except valid service
functional names in the list, for example compute, volumes, etc. If an invalid
service is passed into the decorator it will error out. The end result will be
that if you run tempest with the functional name of a service as a regex filter
you will only run the tests that touch the service directly or indirectly (ie
through a proxy api, like nova's images api) So for the example in the problem
statement you would run::

    testr run --parallel volumes

Or some variation of the command and only tests that uses cinder would be run.

The service decorator is only required if the service name is not in the path
for the test. If a test exercises a service that contains the name in the path
then it's redundant to use the service decorator because the regex filter will
already match. For the scenario tests since the is normally not a service name
in the path service tags are required for each test. This will be enforced with
a hacking rule.

A test that is properly decorated will look something like this::

    @test.services('compute', 'volume', 'image', 'network')
    def test_minimum_basic_scenario(self):

which indicates that test_minimum_basic_scenario uses the compute, volume,
image, and networking APIs.

An additional feature of adding service tags is that by tagging the tests we
know that the service is required to run the test. This means we can skip the
test if the required service is set as not available in the config file. This
means that an additional skip decorator or skip exception won't be needed if
for tests where service tagging is applicable. However, for cases where service
tags shouldn't be used, such as places where the patch already contains the
name, the other skip methods will be required. (which they should already have)

The decorator will be put in tempest/test.py while all the test methods in
any of the tempest test categories are subject to having the decorator applied
to them. Of course that's assuming the previously mentioned usage conditions
are met by the test in question.

Implementation
==============

Assignee(s)
-----------

Matthew Treinish <mtreinish@kortar.org>

Milestones
----------

Target Milestone for completion:
  Juno-1

Work Items
----------

- Add service decorator
- Add service tags to scenario tests
- Create Hacking Extension to force service tags in scenario tests
- Add service tags to applicable volume api tests
- Add service tags to applicable compute api tests
- Add service tags to applicable image api tests
- Add service tags to applicable identity api tests
- Add service tags to applicable network api tests
- Add service tags to applicable orchestration api tests
- Add service tags to applicable object api tests
