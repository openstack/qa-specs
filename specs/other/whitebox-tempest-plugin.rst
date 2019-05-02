..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

=======================
Whitebox Tempest Plugin
=======================

https://blueprints.launchpad.net/tempest/+spec/whitebox-tempest-plugin

Problem description
===================

Tempest defines its scope as only what is accessible through the various REST
APIs. Some cloud features cannot be properly tested when using only the REST
API. For example, in the context of Nova using the libvirt driver, certain
features can only be fully tested by examining the XML of the instances.
Specifically, live-migrating an instance with dedicated CPUs can appear to
succeed, while in actuality the live migration has caused the instance to no
longer have dedicated CPUs. Only by looking at the instance's XML can we
validate that the dedicated CPU SLA has been respected.

Proposed change
===============

The whitebox-tempest-plugin is a Tempest plugin whose scope explicitly requires
peeking behind the curtain. In other words, if a feature or behavior can be
fully tested using only a REST API, such a test does not belong in
whitebox-tempest-plugin. On the other hand, if fully testing a feature or
behavior requires accessing the control plane like a human operator or admin
would, such a test belongs in whitebox-tempest plugin.

The plugin provides a framework for tests to look behind the curtain. It
currently contains Tempest-style clients that can examine an instance's XML,
examine the database, read and write INI configuration options, and restart
services. All of these are used by tests that are concentrated around Nova NFV
features like CPU pinning and NUMA-aware live-migration.

While currently heavily centered on Nova and NFV, whitebox-tempest-plugin aims
to be useful for testing any OpenStack project.

Alternatives
------------

While various team-specific or project-specific Tempest plugins exist whose
scope sometimes intersects with whitebox-tempest-plugin, the whitebox testing
use case does not currently have an alternative community solution.

Projects
========

Whitebox-tempest-plugin is self-contained. It includes a devstack plugin to add
whitebox-specific options to tempest.conf.

Implementation
==============

Assignee(s)
-----------

The current whitebox-tempest-plugin team is composed of Joe Hakim Rahme (rahmu),
Sean Mooney (sean-k-mooney) and Artom Lifshitz (notartom).

Milestones
----------

Ussuri.

Work Items
----------

The current roadmap consists of:

- Start using whitebox-tempest-plugin in the Nova NFV Zuul job.

- Whitebox supports undercloud/overcloud TripleO deployments, but there is no
  upstream CI coverage for this. Work is in progress to add a TripleO CI job.
  The new job will use a multinode standalone TripleO deployment, which is also
  in the process of being developed.

Dependencies
============

Whitebox requires the following Python modules:

- sshtunnel (needed to access the overcloud database, will be dropped once the
  TripleO CI job is done, as a standalone TripleO deployment does not have the
  undercloud/overcloud distinction).

- pymysql (needed to intereact with the database)

References
==========

* Nova NFV Zuul job: https://review.opendev.org/#/c/679656/
* TripleO CI job:  https://review.opendev.org/#/c/705113/
