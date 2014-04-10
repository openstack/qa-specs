..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
 Branchless Tempest
=============================

https://blueprints.launchpad.net/tempest/+spec/branchless-tempest

Tempest historically has been treated like a core service, with a
stable/foo release branch cut at every release of OpenStack. However,
Tempest is largely black box testing for the OpenStack API. The API is
represented by major versions, not by release tags, so Tempest should
not need branches. This change would have a number of interesting
cascading impacts, all of which should be positive for the health of
the project.

Problem description
===================
Our current release method for Tempest is to create a stable/foo
branch at every release of the OpenStack core services. This has a
number of side effects.

- tests are only added to master, and rarely backported. Completely
  valid stable/havana testing has been lost.
- behavior changes can happen between stable/havana and master
  because the version of the test run between them is different
- what version of Tempest should a CDing public cloud test against?
  (i.e. releases aren't meaningful to lots of consumers)
- stable/havana ends up being used as a global flag for what features
  are supported in OpenStack. But that's not meaningful because most
  environments run with a specific list of features enabled, not just
  anything we shipped in stable/havana.

Tempest has organically grown up as a tool that works really well in
our upstream gate, and medium well for people testing real
deployments. One of the reasons for this difference is that we use the
stable/foo Tempest branches to make assumptions about the relationship
of services, and devstack, which set up Tempest. Breaking this
convenience relationship will make us be much more dilligent in being
explicit about Tempest as a tool designed to run under any setup
environment.

Proposed change
===============
Under the proposed branchless environment we'd do the following:

- Not set a stable/icehouse Tempest branch
- stable/icehouse integrated services would be tested with Tempest master
- Tempest master would be gated on successful runs against:

  - integrated services on master branches
  - integrated services on stable/icehouse branches
  - (Note: this would double the # of jobs to be run on Tempest
    proposed changes)

- post release, devstack-gate would change to explicitly set not only
  the services that Tempest expects to tests, but also the extensions
  it expects to test on each branch

This has cascading implications, probably best described as scenarios
(I'll use nova as the example service for all scenarios, mostly
because I'm more familiar with the extensions model, not because it's
being picked on):

Scenario 1: New Tests for new features
--------------------------------------
If a new feature is added to Nova in Juno, and a new test is added to
Tempest for this feature, this test will need to be behind a feature
flag (as the feature wasn't available in Icehouse).

- nova stable/icehouse - Test Skipped, feature not available
- nova master - Test run

This has the added benefit of making sure that a new Nova change is
added in such a way that it's somehow discoverable that it's not there
(i.e. behind an unloaded extension), and that Tempest has a knob for
configuring or not configuring it.

Scenario 2: Bug fix on core project needing Tempest change
----------------------------------------------------------
Previously a behavior change in nova master that needed a Tempest
change could be changed via the tempest 2 step:

- propose change to nova, get a nova +2
- propose skip on Tempest, +Aed after nova +2 on change
- land nova change in master and stable/icehouse (if required)
- land changed test in Tempest

In this new model the change *will also* need to be backported to
stable/icehouse simultaneously. Or we decide that this is behavior
that should not be tested for, and drop the test entirely.

Scenario 3: New Tests for existing features
-------------------------------------------
When adding new tests for existing features the new tests will need to
simultaneously pass when tested against nova master and nova
stable/icehouse. If we discover there is a difference of behavior
between the two, we'll need to harmonize that behavior before landing
the test. We end up with 3 options:

- fix nova master to reflect nova stable/icehouse behavior (nova regression)
- fix nova stable/icehouse to reflect nova master behavior (missing
  backport)
- decide to not land the Tempest test as it is attempting to verify
  behavior we don't consider stable

Scenario 4: Obsolete Tests
--------------------------
A feature, like Nova XML v2 is deprecated is icehouse, and
(hypothetically) removed in juno. Howeve the XML v2 tests are in
Tempest, and we still need to test icehouse releases.

This would be handled by a slow deprecation / feature flag:

- Tempest v2 XML feature flag added (default to false)
- Devstack-gate modified to set to true for stable/icehouse
- Tests are skipped in master, run in stable/icehouse
- Once stable/icehouse is no longer supported upstream (Feb 2015),
  tests are removed from Tempest entirely.

This will mean that Tempest will contain more legacy code, however
that's a trade off we take with the benefits this provides.

Additional Implications
-----------------------
This will have some interesting additional fallout:

- stable/* branches won't be broken so often: with the massive number
  of tempest patches that will require a working stable/* gate to
  land, stable/* will get a lot more regular testing, and be in a
  working state more often
- API guaruntees will tighten up. We'll not only be testing that the
  API does what we expect in Tempest, but also that it acts the same
  across multiple versions. The added friction to breaking that kind
  of behavior will slow down any future breaks there. This means a
  practical increase of API compatibility requirements.

Alternatives
------------
The alternative is to continue with the current approach which uses
stable/* branches in Tempest. However that has caused more
unintentional coupling with devstack that we'd like, and I believe
that long term it's the wrong approach for a test suite like Tempest.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  Sean Dague <sean@dague.net>

Can optionally can list additional ids if they intend on doing
substantial implementation work on this blueprint.

Milestones
----------
Target Milestone for completion:

- April 17th for main infrastructure
- Juno release cycle to handle various backports to devstack
  stable/icehouse to support all tempest feature flags

Work Items
----------
The work items span projects

- devstack-gate generic branch override support (DONE)
- infrastructure jobs to gate Tempest on stable/icehouse (when
  available)
- devstack-gate changes to select not only services, but also features
  supported at each release
- devstack support for setting stable/icehouse features
- additional Tempest feature flags for optional features not yet
  addressed

Dependencies
============
Only those listed above
