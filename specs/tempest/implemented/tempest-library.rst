..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

===========================================
 Create Separate Functional Testing Library
===========================================

https://blueprints.launchpad.net/tempest/+spec/tempest-library


With a recent desire to create a number of functional tests for individual
OpenStack projects a common toolkit for building functional tests is needed.
Using Tempest's core functionality start a new functional testing library to
reuse this code in spinning up new project specific test suites.

Problem description
===================

For several years Tempest has been the integrated test suite for OpenStack.
However, recently as the scope and complexity of Tempest have continued to grow
we've found that there is a need for project specific functional testing. With
the ease of spinning up devstack slaves for testing this is a simple thing to
add to the ci infrastructure. However writing the functional test suite is not
as straightforward and would require a great deal of duplicated effort between
the projects.

Proposed change
===============

Take what common test infrastructure we have currently in tempest and split it
out into a separate library. This library will live in a separate repository,
published on pypi, have a separate bug tracker, and enforce a stable api for
use. (which will be enforced with unit testing) The intent is for this library
to be usable to build a functional test suite using the same building blocks as
Tempest.

As functionality is moved from Tempest into the library it may need to be
refactored slightly to be portable. For example, the RestClient and the service
clients will need to be refactored to not depend on the tempest config file.
These changes should occur at the same time the functionality is added to the
library.

Once a set of functionality is ported to the library it can be removed from
tempest tree and the library used instead. We should do this as soon as the
functionality lands in the library. This will ensure that we aren't maintaining
2 sets of the same code. It will also help ensure the functionality of the code
by actually using the library interface inside of tempest. For example consider
this workflow with python-novaclient CLI tests:

 #. Add CLI base test classes with core functionality to the new library
 #. Switch the tempest CLI tests to use the library instead
 #. Remove code in tempest which has been switched to the library
 #. Add a functional test suite to the novaclient repository and copy the
    appropriate CLI tests from tempest
 #. Remove the copied novaclient CLI tests from tempest

The first 3 steps from this example will be applied to anything that moves into
the library. Steps 4 and 5 only apply when we've decided a certain class of
testing no longer belongs in tempest.

The first working example of this should be the CLI tests because they were only
added to Tempest before having non-Tempest devstack jobs was a simple matter. By
there very nature they should be a project specific functional test so adding
CLI framework to the library should make it quite simple to move those tests out
of Tempest.

The other aspect to consider is that the library will be consumed by the
projects functional tests, not mandating functionality. All the pieces should
be optional, so that projects can use what they need to. For example, while the
tempest clients will be available in the library there should be no requirement
to use it. Also, until decisions are made around removing a certain class of
testing from tempest we shouldn't be removing tests from tempest.

Alternatives
------------

One alternative is that we modify code inside of Tempest to do the same basic
functionality. The issue with this is that tempest will become overloaded with
having too many jobs. Additionally, the new library could conceivably contain
features and code that would have no place inside of Tempest, but would belong
in the project specific functional testing. Additionally, splitting it out into
separate library will make the publishing and release a simpler matter, since
we wouldn't necessarily want to be publishing all of tempest on pypi as a
test-requirement for the projects.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Matthew Treinish <mtreinish@kortar.org>

Other contributors:
  Ken'ichi Ohmichi <oomichi@mxs.nes.nec.co.jp>

Milestones
----------

Target Milestone for completion:
  Kilo Release

Work Items
----------

 * Start new repository for the library

   * Create launchpad page for the project
   * Create PyPI entry for the project

 * Copy base test class and other core functionality to run tests
 * Copy and remove config and tempest specific code from CLI test framework
 * Add devstack support for installing the library from git
 * Setup the infra jobs to make it co-gating along with all the projects that
   consume it
 * Migrate other commmon features and utilities related to testing, for example:

   * Exceptions
   * Common decorators
   * Matchers
   * SSH validation code

 * Copy and convert the Tempest REST Client

   * Clean up the REST Client code
   * Separate the base REST Client code from Tempest specific code
   * Move the REST Client specific exception to base REST Client code
   * Copy the base REST Client code to tempest-lib repository
   * Switch Tempest to use the base REST Client code of tempest-lib

 * Cleanup in Tempest service clients

   * Use ResponseBody/List on all service clients for consistent interface
   * Remove CONF values from service clients

     Current service clients contain CONF values from tempest.conf but they
     should be independent from tempest.conf as library functions.

 * Add documentation and examples for using the libraries interfaces

Dependencies
============

This shouldn't be dependent on any other effors, however it may cause conflicts
with other BPs in progress, so care should be made when porting things to ensure
all the in progress efforts don't end up being lost in the aftermath of a
library conversion.

References
==========

- http://lists.openstack.org/pipermail/openstack-dev/2014-March/028920.html
