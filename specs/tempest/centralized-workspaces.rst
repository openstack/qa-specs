..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

=========================================
 Centralized Tempest Workspace Management
=========================================

https://blueprints.launchpad.net/tempest/+spec/centralized-workspaces

Create a consistent means for creation and management of Tempest workspaces.


Problem description
===================

Currently there is no way to track workspaces in a consistent manner. This
becomes problematic as the number of workspaces increases.


Proposed change
===============

Create a ``.tempest`` file in the user's home directory to be used as a source
of truth for Tempest workspaces. Users can register new workspaces via the
``tempest workspace register`` command. New workspaces are automatically
registered via ``tempest init``. The workspace manager automatically unregisters
any workspaces that no longer exist.

+-----------------------+--------------------------------------------------------------------------+
|        Action         |                                   Command                                |
+=======================+==========================================================================+
| Register a workspace: | tempest workspace register --name <name> --path <path>                   |
+-----------------------+--------------------------------------------------------------------------+
| Rename a workspace:   | tempest workspace update --key <key> --old-value <old> --new-value <new> |
+-----------------------+--------------------------------------------------------------------------+
| List workspaces:      | tempest workspace list                                                   |
+-----------------------+--------------------------------------------------------------------------+

Example Usage
-------------
::

  > cd ~/devstack
  > tempest init --name devstack

  > tempest workspace register --name staging --path /etc/staging

  > tempest workspace list
  +----------+----------------+
  | Name     |    Location    |
  +----------+--------------- +
  | devstack | /root/devstack |
  | staging  | /etc/staging   |
  +----------+----------------+


Projects
========

* openstack/tempest


Implementation
==============

Assignee(s)
-----------

* slowrie
* dwalleck

Milestones
----------

Target Milestone for completion:

- Mitaka-2

Work Items
----------

- Create argparse to handle new ``workspace`` command and subcommands
- Create tracking file and class to represent it
- Add code to list that unregisters workspaces when locations no longer exist


References
==========

- https://etherpad.openstack.org/p/tempest-cli-improvements
