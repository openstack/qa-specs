..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
 Javelin 2
=============================

https://blueprints.launchpad.net/tempest/+spec/javelin2

During the Juno Summit we discovered that Grenade was not doing the
resource validation that we believed it was. This had always been a
fragile part in grenade because complex validation of resources is
somewhat tough in bash. Instead we should build a tool in Tempest that
provides a way to create, validate, and destroy resources for us in
testing.

Problem description
===================

We need a tool that will create a set of resources, can validate that
that set of resources exists at some later point in time (temporally
disconnected with no shared memory state), and can delete that set of
resources. Having this tool we can very easily test that resources
(users, images, servers, objects, etc) survive an upgrade undisturbed
in grenade testing.

Proposed change
===============

Create a new javelin tool in tempest as part of the cmd directory.

The usage of javelin is as follows::

  usage: javelin.py [-h] -m <create|check|destroy>
                  [--os-username <auth-user-name>]
                  [--os-password <auth-password>]
                  [--os-tenant-name <auth-tenant-name>]
                  [--os-auth-url <auth-url>]

It requires admin keystone credentials to run because it must perform
user/tenant creation and inspection.

Resources are specified in a resources.yaml file::

  tenants:
    - javelin
    - discuss

  users:
    - name: javelin
      pass: gungnir
      tenant: javelin
    - name: javelin2
      pass: gungnir2
      tenant: discuss

  # resources that we want to create
  images:
    - name: javelin_cirros
      owner: javelin
      file: cirros-0.3.2-x86_64-blank.img
      format: ami
      aki: cirros-0.3.2-x86_64-vmlinuz
      ari: cirros-0.3.2-x86_64-initrd

  servers:
    - name: peltast
      owner: javelin
      flavor: m1.small
      image: javelin_cirros
    - name: hoplite
      owner: javelin
      flavor: m1.medium
      image: javelin_cirros

An important piece of the resource definition is the *owner* field,
which is the user (that we've created) that is the owner of that
resource. All operations on that resource will happen as that regular
user to ensure that admin level access does not mask issues.

The check phase will act like a unit test, using well known assert
methods to verify that the correct resources exist.

This whole exercises has, and will continue to, enlighten us on ways
that the Tempest rest_client is difficult to consume outside of
Tempest tests. It should go a long way to making that a cleaner
distinction.

Alternatives
------------

The alternative is to fix the grenade javelin exercises, though
they've been non functional for long enough that this doesn't seem to
be a fruitful direction.

Implementation
==============

Assignee(s)
-----------

Primary::
  sean@dague.net

Additional::
  emilien.macchi@enovance.com


Milestones
----------

Juno-2

Work Items
----------

- initial pass of javelin2 that supports create / check of similar
  resources as were in grenade javelin
- integration of javelin2 into grenade
- addition of destroy phase to clean up javelin2
- expand # of resources beyond what was in grenade to ensure we aren't
  failing once we get beyond singletons
- expansion of resources beyond what was in grenade
  - ceilometer resources
  - neutron resources
- unit tests in tempest


Dependencies
============

None
