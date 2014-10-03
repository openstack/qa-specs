..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Tempest Client for Scenario Tests
=================================

https://blueprints.launchpad.net/tempest/+spec/tempest-client-scenarios

Tempest currently has tests using 2 different OpenStack clients. The
first is a client written in Tempest for testability and
debugability. The second is the various native clients. This adds debt
to the Tempest code that we should remove.

Problem description
===================

As Tempest grew up we grew tests that included poking directly at the
raw API with our own client, as well as through the various native
clients for the projects. As the volume of tests have grown, and some
of the complexities in Tempest (like tenant isolation) have shown up,
the 2 client strategy has become problematic.

1. It means that various abstractions need to be built above the
   clients to do things like waiting for resources to be created,
   handling tenant isolation, and doing safe cleanup.
2. The debugging output is radically different depending on the client
   that has failed. We can fix and react to a debuability issue in the
   Tempest client in tree. Addressing something as simple as reduction
   of extraneous token messages needs to be landed in 10 trees before
   it's fixed in a tempest run.
3. It's demotivating to work on the code.


Proposed change
===============

We do a wholesale cut over of the openstack clients to the Tempest
client in all the scenario tests.

We remove the abstractions that were built just for these
clients.


Alternatives
------------

Keep things as they are. This however has begun to be a top issue
impacting gate debugability.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
   * Masayuki Igawa <igawa@mxs.nes.nec.co.jp>

Other contributors:
   * Andrea Frittoli <andrea.frittoli@hp.com>
   * Daisuke Morita <morita.daisuke@lab.ntt.co.jp>

Work Items
----------

- replace official clients in tempest/scenario with tempest clients
- add hacking rule to provide use of official clients
- remove tenant isolation abstraction

Will be tracked in:
  https://etherpad.openstack.org/p/tempest-client-scenarios



Dependencies
============
None


Referenences
============
Mailing list discussion - http://lists.openstack.org/pipermail/openstack-dev/2014-July/039879.html
