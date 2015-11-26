..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
 Branchless Tempest - Service Extensions
=========================================

https://blueprints.launchpad.net/tempest/+spec/branchless-tempest-extensions

This is the follow on work for branchless tempest for new service
extensions that are added over the course of a release.

Problem description
===================
In moving to branchless Tempest we're now running Tempest across
multiple OpenStack code branches. Today that's icehouse and juno,
however it will be icehouse, juno, kepler in the future.

What happens when a new extension is added to Nova in Juno, and tests
in tempest are wanted for that part of the API? Today that test would
fail because it could not pass icehouse.

Proposed change
===============
The proposed change is to add another layer to the devstack-gate
feature grid which specifies which extensions are supported at each
release.

Today in the nova definition we've got ::

    nova:
      base:
         services: [n-api, n-cond, n-cpu, n-crt, n-net, n-obj, n-sch]

This would imagine a world where the definition would look as follows
::

    nova:
      base:
         services: [n-api, n-cond, n-cpu, n-crt, n-net, n-obj, n-sch]
      icehouse:
         compute-ext: [floating-ips, aggregates, ... ]

The non existence of an extensions list means assume 'all'. It is also
expected that you'd be able to specify 'rm-compute-ext' much like
rm-services, so that you could do something as follows.
::

      nova-cells:
        base:
          services: [n-cell]
          rm-compute-ext: [aggregates, hosts]

That would disable those nova extensions any time it was configured.

For this to function there needs to be changes in

- devstack-gate

  - to parse these additional stanzas and pass them down to devstack

- devstack

  - to take extension lists for projects and set the correct
    extensions up based on it
  - to compute the 'all' case correctly for master (especially if we
    support the rm-compute-ext stanza)
  - to set the correct tempest fields for enabled features when these
    map to feature flags.


Alternatives
------------
Nova API microversions might obviate the need here in the branch case,
as we'd be able to specify a specific test has a specific required
version. However that wouldn't solve the cells case.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  None yet


Milestones
----------
Not Known


Work Items
----------
The work items span projects

- see above

Dependencies
============
Only those listed above
