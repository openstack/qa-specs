..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

==================================
 Tempest List Plugins Command
==================================

https://blueprints.launchpad.net/tempest/+spec/list-plugins

Provides a means to list to currently installed Tempest plugins.


Problem description
===================

The Tempest project recently implemented a plugin system to allow external
test repositories to be included in Tempest test runs in a seamless fashion.
Tempest plugins are essentially Python packages that implement a specific
interface and are installed via standard Python tools. However, there is
not a straightforward means for knowing which plugins are currently installed.

Proposed change
===============

Providing a means via the ``tempest`` command line tooling to list the
installed plugins provides a consistent experience to the user. The command
``tempest plugins list`` would provide the user with basic information about
the installed plugins::

  > tempest plugins list
  +------------+---------------------------------------------+
  | Plugin     | EntryPoint                                  |
  +------------+---------------------------------------------+
  | HelloWorld | hello_world_tempest_plugin.plugin:MyPlugin  |
  | Example2   | example_tempest_plugin.plugin:ExamplePlugin |
  +------------+---------------------------------------------+


Projects
========

* openstack/tempest

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  slowrie
  dwalleck

Milestones
----------
Target Milestone for completion:
  Mitaka-2

Work Items
----------
- Create means to query the stevedore.ExtensionManager for registered entrypoints
- Create a function that turns the list of plugins into user readable output
- Add an entry point for the ``plugins list`` command in the tempest.cmd package

Dependencies
============

- prettytable

References
==========

- https://etherpad.openstack.org/p/mitaka-qa-tempest-run-cli
- https://github.com/openstack/tempest/blob/005ff334d485c4ca231d7ee8396d3eb979a9ce59/tempest/test_discover/plugins.py#L74
- https://github.com/openstack/tempest/tree/master/tempest/cmd
