..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

==================================
 Tempest Run Command
==================================

https://blueprints.launchpad.net/tempest/+spec/tempest-run-cmd

Describes a domain-specific ``tempest run`` command to be used as the primary
entry point for running Tempest tests.


Problem Description
===================

There are a wide range of Tempest use cases ranging from OpenStack gate
testing to the testing of existing public and private clouds across multiple
environments and configurations. Each of these user scenarios has its own
requirements and challenges.

Currently, tempest doesn't actually control it's own execution. It instead
relies on an external test runner, it does not provide a consistent experience
for consumers of Tempest. Users also often have impression that tempest
controls it's own execution. In addition, because these test runners are in no
way specific to Tempest any, items that are domain specific (such as
configuration) must be performed out-of-band using shell scripts or other means.

Proposed Change
===============

Since an effort is already underway to create a set of Tempest-specific
command line tooling, this spec further defines a ``tempest run`` command.
This spec addresses the following problems:

- Providing a flexible runner that enables multiple approaches to the test
  discovery and execution processes
- Facilitating ease of configuration and execution of Tempest across multiple
  environments and configurations
- Builds on testrepository directly in order to leverage current and future
  testrepository capabilities

This spec outlines the beginning steps and basic functionality of the initial
implementation of the run command. It is expected that the functionality of run
will grow over time to suit the needs of tempest in the future.

The command implementation can be broken down into three components:

- Converting the selection regex logic from ostestr into a reusable module
- A command line interface that users will interact with
- A client that drives the execution of tests by interfacing directly with
  testrepository

The logical flow of the proposed test runner is as follows:

- Parse any command line arguments.
- Set necessary environment variables for Tempest based on inputs.
- Determine the set of tests to run using ostestr regex builder
- Call into testrepository with the testr-specific arguments
- Receive the results from test execution
- Perform any post-processing on the test results, if applicable.

Command Line Interface
----------------------

The list of proposed command line arguments are as follows:

Test Execution::

  --parallel
  --serial
  --workers <workers>
  --list

Test Selection and Discovery::

  --tags <list of tag name>
  --services <list of services>

  --include <regex>
  --whitelist-file <file name>
  --exclude <regex>
  --blacklist-file <file name>
    Sample regex file:

        (^tempest\.api) # Comments about this regex
        tempest.scenario.test_server_basic_ops # Matches this test explicitly

Aliases for most commonly used regexes::

    --smoke
    --all

By default the regex will run the equivalent of the full jobs in tox. (running
everything but tests tagged as slow)

Output::

  --subunit
  --html <file name>

By default the console output will be output from subunit-trace

Tempest Configuration::

  --config <config file>

Part of having tempest run having domain specific knowledge is that it's aware
of tempest workspaces and when running in it. However, workspaces aren't a
requirement for actually running tempest, and there is are existing workflows
where you have a separate tempest config file. (which previously could only
be specified by environment variables) This option is providing an easier to
use place on the CLI for doing this. This is a key advantage of having tempest
own it's runner is that it provides another place for passing this type of
information into tempest which we previously could only do via env vars or the
config file.

Testrepository Integration
--------------------------

One of the goals of this spec is to develop an entry point from Tempest
that integrates directly with testrepository rather than calling out to
testr via subprocess. This integration is a more robust design that
allows new features in testrepository to propagate more easily to the Tempest
runner. Inversely, as the Tempest runner evolves, features that would be
useful to any test runner can be pushed down the stack into testrepository.

The planned integration point of the tempest run command with testrepository
is the `CLI UI for testr`_. However, this only one possible approach. The
final solution is likely to evolve during development.

.. _CLI UI for testr: https://github.com/testing-cabal/testrepository/blob/master/testrepository/commands/__init__.py#L165

Projects
========

* openstack/tempest

Implementation
==============

- Extract the regex building logic from ostestr into an externally consumable
  module
- Create a ``tempest run`` entry point in Tempest using cliff
- Handle setup of Tempest specific options such as Tempest configuration
- Implement test selection logic using the ostestr bits and based on the
  provided filtering options (regexes, tags, etc.)

Assignee(s)
-----------

Primary assignee:
- mtreinish
- slowrie

Milestones
----------

Target Milestone for completion:
  Newton-2

References
==========

- `Newton Design Summit CLI Session`_

.. _Newton Design Summit CLI Session: https://etherpad.openstack.org/p/newton-qa-tempest-cli

- `Mitaka Design Summit CLI Session`_

.. _Mitaka Design Summit CLI Session: https://etherpad.openstack.org/p/mitaka-qa-tempest-run-cli

Previous Implementations and Specs

- `os-testr runner`_
- `Prototype by mtreinish`_
- `Previous Tempest CLI spec`_

.. _os-testr runner: https://github.com/openstack/os-testr/blob/master/os_testr/os_testr.py
.. _Prototype by mtreinish: https://review.openstack.org/#/c/197378/8/tempest/cmd/run.py
.. _Previous Tempest CLI spec: https://github.com/openstack/qa-specs/blob/master/specs/tempest/tempest-cli-improvements.rst
