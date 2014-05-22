::

 This work is licensed under a Creative Commons Attribution 3.0 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

=====================================
Keystone v3 based check and gate jobs
=====================================

https://blueprints.launchpad.net/tempest/+spec/keystone-v3-jobs

Check and gate jobs using keystone V3

Problem description
===================

All check and gate jobs at the moment rely on keystone v2 as identity
service.  Blueprint multi-keystone-api-version-tests introduces in tempest
the ability to run tests relying on keystone V3 API only.
The version of the keystone API to be used is controlled via a configuration
flag. Dedicated jobs are requied to exercise the V3 option, in preparation
for keystone V2 deprecation planned for Juno.


Proposed change
===============

Setup keystone v3 jobs to be run initially as experimental only.
They will be promoted then to check and eventually gate.

Running fully v3 jobs is beyond the scope of tempest and infrastructure
alone, as it requires changes in other OpenStack projects:

- python bindings to either support keystone v3 API or consume Keystone
  Client Session Objects (see http://www.jamielennox.net/blog/2014/02/24/client-session-objects/)
- core services to be integrated with keystone v3 model and API
  Such changes are defined in details in dedicated blueprints.

As dependencies will be implemented in Juno, it won't be possible
to run full v3 jobs against Icehouse. The keystone v3 jobs can still
be used against icehouse, with the limitation that only the authentication
of tempest clients and creation of isolated user and projects will be
based on the v3 API.

Alternatives
------------
It would be possible to run all tests via v2 and v3 in parallel.
However this would significantly increase the gate duration.

Implementation
==============

Assignee(s)
-----------
  Andrea Frittoli <andrea.frittoli@hp.com>

Milestones
----------
Target Milestone for completion:
  Juno-final

Work Items
----------
- Define a localrc variable in devstack for auth_version=v3
- Define an option in devstack-gate to setup the localrc variable
- Define two jobs in the experimental pipeline for tempest:
  dsvm-keystonev3-full and dsvm-neutron-keystonev3-full
- Track the progress of dependencies, and enhance jobs accordingly
- Run the jobs on demand until all issues are fixed and results are stable
- Promote the jobs to check for tempest
- Promote the jobs to check for all projects
- Promote the jobs to gate


Dependencies
============

A fully v3 check job depends on having v3 support in a number of places

- tempest framework and its tests https://blueprints.launchpad.net/tempest/+spec/multi-keystone-api-version-tests
- official python bindings and CLI tools
- openstack services

The current jobs will only be partially v3 until all dependencies are met.
The migration strategy from identity API v2 to v3 will be documented as part of
https://blueprints.launchpad.net/keystone/+spec/document-v2-to-v3-transition
