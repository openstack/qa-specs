::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===================================
Add a config file verification tool
===================================

https://blueprints.launchpad.net/tempest/+spec/config-verification

Add a new tempest tool that will query the services' APIs to check if config
options are set correctly.

Problem description
===================

The tempest config file has tons of options and the number is just growing.
Additionally some of the options aren't exactly trivial to set completely.
For example, the api extensions options are either all or a list of all the
enabled extensions. Most of the services support discovery of almost all the
options we use in the config file.

Proposed change
===============

To write a tool which will use an existing config file and verify that
everything is set matching what the services report as being enabled. It will
start by reading in the config file and then use the tempest clients to query
the services to check that things like api versions, catalog types, and
extensions match what is reported by the services. It will also have a flag to
overwrite the config file with the values with reported by the services.

This new tool will be added to the tools/ directory in the root of the tempest
tree along with the other helper utilities in tempest.

The usage statement for the new tool will be something like the following::

    usage: verify_tempest_config.py [-h] [-u] [-n]

    optional arguments:
      -h, --help    show this help message and exit
      -u, --update  Update the config file with results from api queries. This
                    assumes whatever is set in the config file is incorrect. In
                    the case of endpoint checks where it could either be the
                    incorrect catalog type or the service available option the
                    service available option is assumed to be incorrect and is
                    thus changed. A copy of the original config file will be
                    created with .orig appended to the filename.
      -n, --nocopy  Don't create a copy of original config file when running
                    with the update option.

To test the functionality of the tool unit tests will be added to verify that
both the verification functionality and the config file updating work as
intended.


Alternatives
------------

The alternative would be having a tool that generated the config file directly
however this has a chicken and egg problem. If you want to autconfigure tempest
using feature discovery you need to have auth to talk to the services, and the
auth is part of the config file. So instead of having some hybrid between a
generator and existing config having a tool which verifies an existing config
file would clean up any confusion. Also having an option to overwrite it with
the autodiscovery results will essentially be a config generator.

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

- Add basic verification script
- Add config file updating feature
- Add unit tests for config verification functionality
- Add unit tests for config file updating functionality
