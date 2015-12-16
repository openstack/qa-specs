..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

==================================
 Tempest External Plugin Interface
==================================


https://blueprints.launchpad.net/tempest/+spec/external-plugin-interface

Create an external plugin interface to enable loading additional tempest-like
tests from out of tree to enable projects to maintain their own testing out
of tree.


Problem description
===================

As part of the recent governance change to rework OpenStack under a big tent
the QA program needs to be able to handle an influx of "OpenStack" projects.
As part of this pivot most QA projects are shifting from directly supporting
every project in-tree to moving towards providing projects to self service.
A missing piece of this was the tempest external plugin model, all the other
QA projects contain support for extending functionality with out of tree
plugins but tempest was putting the burden on the user for constructing this.
Moving forward having a unified supported model for enabling this is necessary.

Proposed change
===============

The first step for the plugin interface is to handle the loading of the
additional tests in the plugin. The additional paths of the external tests will
need to be passed into the unittest discovery mechanism. To do this registering
an entry point that tempest will be able to load as part of it's run command
will be used. This will enable any installed python package which contains a
tempest entry point to be seamlessly discovered and used as part of a wider
"Tempest" test suite.

You would register the entrypoint when using pbr by adding an entry to
your setup.cfg like::

    [entry_points]
    tempest.test_plugins =
        plugin_name = plugin_dir.config:load_plugin

This will register a new plugin to tempest to use the additional testing.
Stevedore will probably be leveraged on the tempest side in the new cli
run command to load the plugins when run to add the additional pieces. The
hook referred to in the setup.cfg will return the test path to use for unittest
discovery. The stevedore manager in tempest will then use this returned path to
construct a set of test paths to use for discovery including tempest in-tree
tests and all installed plugins, this will give the appearance when running
tempest of a unified test suite.

As for the plugins themselves they will contain a few key pieces, mainly the
tests, additional configuration.

An example of the base directory structure for a plugin to start with would
look something like::

    plugin_dir/
      config.py
      tests/
        api/
        scenario/
      services/

However, this is just suggested bare minimum, it is not going to cover every
potential plugins use case so have additional files or directories in plugins
will be expected.

The various pieces here:
 * config.py will contain 2 things first is the registration method which
   will provide all the necessary information to tempest to execute the plugin
   remotely and second the additional configuration options. There will be a
   unified method on the plugin class, likely called register_opts(), (and
   also list opts so that we have a call for sample config generation) which
   will register all the new groups and new options. This puts the burden on
   the plugin to either create new groups for options or to extend existing
   groups where appropriate.
 * The tests dir will contain the actual tests. The example above used 2
   subdirs for api tests and scenario tests, but that isn't a hard requirement.
   Any desired organization of tests can be used in a plugin. However a single
   parent dir for all tests is used to make the test discovery logic in tempest
   a bit easier to deal with.
 * Services will contain the additional api clients based on the RestClient
   from tempest-lib if needed.

It is also worth noting that we should strive to make these plugins be able to
fully self execute on their own with a traditional test runner without any need
to use tempest. The use of the plugin is only to enable easier integration with
the wider test suite for other projects. A cookiecutter repo (either as part of
the existing devstack-plugin-cookiecutter or a separate repo) will be leveraged
to enable a fast path template for projects to use when initially setting up a
new tempest plugin.

There are several things from tempest-lib which are missing which are really
needed to leverage out-of-tree plugins, mainly the base test class fixtures
and the credential providers. These are not requirements for starting work
on the plugins as the plugins can temporarily depend on tempest code for that
however, in the medium term we should migrate these to tempest-lib to lock down
the interface for using them.

Another thing which we'll be changing is our contract around the tempest config
file. Traditionally we have said not to rely on config options from directly
from tempest but this will change with plugins since code out of tree will have
to rely on existing options as a base set to build off of. This means in the
future we'll have to provide better guarantees on the stability of tempest's
config file.


Alternatives
------------

An alternative approach would be to not use loadable entrypoint and instead
place the burden on the tempest end user to load the plugins. So when calling
tempest run you would specify a list of plugins to load at the same time.
The disadvantage of this approach is that it requires the user to know where
the plugins are located on the system. While using an entrypoint only requires
the additional code to be installed and then tempest will use external location
automatically.

Additionally, if a plugin interface was not added there would be nothing
stopping anyone from using tempest-lib and the same mechanism as what is
expected in a plugin to create an isolated tempest-like test suite. (in fact
several projects have already done this) This was also the previously
recommended approach for out of tree tempest tests. The disadvantage with only
doing this is that everything is treated in isolation so each test suite would
have to be dealt with in isolation. However, with the scope of what's allowed
in tempest clearly defined now we expect many more of these external suites to
be added in the future. Being able to deal with them in a single manner and
using a single workflow to deal with all of them at once is much more desirable,
and a far lower burden on the end user.


Projects
========

* openstack/tempest
* openstack/tempest-lib

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  mtreinish

Milestones
----------

Target Milestone for completion:
  Liberty-2

Work Items
----------

- Add support to tempest run to load installed entry-points
- Modify the tempest documentation to outline project scope and changes to
  in-tree tempest policy (including things like config file changes)
- Create documentation for using plugins
- Add missing interfaces to tempest-lib
- Create cookie-cutter repo for tempest-plugins

Dependencies
============

- A tempest unified cli which adds a new run interface is required before we
  have a place to add the extension loading support to
- Adding an additional interface to unittest to handle a list of discovery
  points might be needed.
