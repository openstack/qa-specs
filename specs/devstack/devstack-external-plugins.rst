..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=========================
Devstack external plugins
=========================

https://blueprints.launchpad.net/tempest/+spec/devstack-external-plugins

Support external plugins for devstack.

Problem description
===================

Devstack has a pretty strong plugin support, you just have to drop
your extra feature in the extras.d/ directory and it will
automatically parse the file and install the feature as long you have
enabled it in your local.conf.

This all works very well but that's not very flexible for projects
that are not able to be integrated directly in devstack
core. Currently an external OpenStack project who wants to tell its
users how to test a feature has to explain how to download a file to
put in the `extras.d` directory and enabling it.

As for integrated projects they may wants to take care of how they do
devstack directly in their own repo and get devstack to use that
instead of having to request for a change in devstack repository.

Proposed change
===============

Devstack would provide a new enable_plugin function call that would be
of the following format::

  enable_plugin <name> <http://git.openstack.org/foo/external_feature>
  [refname]

`name` is an arbitrary name picked for enablement, `repo` is the
full url to a git repo, and `refname` is the optional ref
description (defaulting to `master` if none is provided).

Devstack would then checkout that repository in `${DEST}/name` and
look for a `/devstack/` directory in there from the root of the repo.

Files in there would have :

* `/devstack/settings` - a file that gets sourced to override global settings,
  those variables become instantly available in the global namespace.
* `/devstack/plugin.sh` - dispatcher for the various phases

Devstack when executed will then:

* Get the configuration of the `extras.d` repos.
* Clone the extras repository to `${DEST}`
* Run all the `extras.d` scripts at a particular phase
* Run all the plugins `plugin.sh` at a particular phase

This would let the out of tree projects that needs to communicate about their
config to export data via settings that would let the other configure based on
their setup.

Alternatives
------------

The alternative would be to stay as the status quo like we have now and have
them to curl the extras file from the external repository and place it in the
`extras.d` directory.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * Chmouel Boudjnah <chmouel@chmouel.com>

Other contributors:
  * Sean Dague <sean@dague.net>


Milestones
----------

Target Milestone for completion:
  Kilo-2

Work Items
----------

* Add support in devstack.
* Get an example repository setup.
* Get a project like nova-docker to use it.
  * (glusterfs is a good current candidate)
