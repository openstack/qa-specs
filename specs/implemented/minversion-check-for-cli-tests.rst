..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

===================================
Check minimum version for CLI tests
===================================

https://blueprints.launchpad.net/tempest/+spec/minversion-check-for-cli-tests

There are CLI tests added to Tempest for commands which may not be available
yet in released versions of the clients, so downstream packagers would not
have those commands available for CI and the tests will fail.

Problem description
===================

The use case is testing stable/icehouse server code, i.e. nova, with packaged
versions of the clients that are supported for the stable/icehouse release of
Nova, which is python-novaclient-2.17.0 in the 2014.1 release of the server
code.

With branchless Tempest there is no stable/icehouse branch for Tempest, and so
when new CLI tests are added to Tempest on master which require commands
or other functions in the clients, they can fail for downstream packagers
if the required commands/functions are not in released versions of the clients
on pypi.python.org, where the packager may be getting their source tar.gz from.

One specific example here is the server-group-list CLI test added for the Nova
client which is not in a released version of python-novaclient. Anyone running
Tempest against a released version of the client will fail this new CLI test.

Note that the community gate CI does not have an issue with this since Tempest
is run against trunk level code for the clients rather than released versions.

Proposed change
===============

Add a simple decorator that can be used in the tempest/cli tests for checking
that the installed version of the client is at a minimum version to support the
test, otherwise the test is skipped.

The decorator would be applied to feature tests introduced since Icehouse due
to the branchless Tempest strategy and the lack of a stable/icehouse branch.

Alternatives
------------

There are not really any good alternatives to this issue for downstream
packagers/deployers if they are not running CI against trunk levels of code
for the clients. They can reset HEAD for Tempest to some arbitrary commit
around the time of the server release they are testing, e.g. sometime around
the 2014.1 release for stable/icehouse testing, but then they are frozen to
that commit in Tempest and do not get future bug fixes that would have been
backported when there were stable branches for Tempest. The other alternative
is manually excluding the unsupported CLI tests but this is cumbersome and
only works around the issue after the fact rather than putting the check in
the code when the test runs.

Implementation
==============

Assignee(s)
-----------

Matt Riedemann <mriedem@us.ibm.com>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

#. Write the decorator code. The work in progress patch is here:

   https://review.openstack.org/#/c/100031/

#. Apply the decorator to the CLI tests, with a primary focus on any tests
   added after the 2014.1 Icehouse release, especially for those tests which
   require newer client code than what is in a released version.


Dependencies
============

* This is only an issue introduced by the "Branchless Tempest" blueprint but is
  not technically tied to that blueprint's implementation, but is listed here
  for posterity:

  https://blueprints.launchpad.net/tempest/+spec/branchless-tempest
