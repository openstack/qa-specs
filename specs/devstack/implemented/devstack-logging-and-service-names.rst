..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..
  This template should be in ReSTructured text. The filename in the git
  repository should match the launchpad URL, for example a URL of
  https://blueprints.launchpad.net/tempest/+spec/awesome-thing should be named
  awesome-thing.rst .  Please do not delete any of the sections in this
  template.  If you have nothing to say for a whole section, just write: None
  For help with syntax, see http://sphinx-doc.org/rest.html
  To test out your formatting, see http://www.tele3.cz/jbar/rest/rest.html

===================================
DevStack Logging and Service Names
===================================

`NOTE: This spec is still a work in progress, it is being posted to get some early
feedback on scope and ordering of steps.`

https://blueprints.launchpad.net/tempest/+spec/devstack-logging-and-service-names

DevStack is in need of updates to its log file handling and service naming, both
of which were appropriate for the originalscreen-based installs with a handful
of services.

This spec contains both the log file reform as well as the service name updates
as they are a bit intertwined so some steps will address them both as necessary.

Problem description
===================

DevStack's logging configuration was initially based on saving ``screen`` logs,
as part of the development of not using ``screen`` the logging was kept compatible
and it became obvious that the original special case was not required.

Historically DevStack has used abbreviated service names for identifying services
to enable, naming log files and as window names in screen.  OpenStack has grown
to the point that the abbreviated names are too confusing and non-obvious,
especially for the not-so-recently renamed Neutron.

These topics were covered at the Paris summit, notes in the `OpenStack Etherpad`_.

.. _`OpenStack Etherpad`: https://etherpad.openstack.org/p/kilo-summit-devstack-grenade


Proposed change
===============

Logging
-------

Update DevStack's logging configuration to set a logging directory rather than parsing
that out of a filename.  Ultimately eliminate the use of ``SCREEN_LOGDIR``.

* Use ``LOGDIR`` as the primary setting in local.conf for log locations, default to
  ``${DEST}/logs`` if ``LOGFILENAME`` is not set.

* Continue to use ``LOGFILENAME`` if set, if ``LOGFILE`` is not set continue to set it to
  $(dirname ``$LOGFILENAME``).

* Deprecate ``SCREEN_LOGDIR`` and use ``LOGDIR`` instead.  For a compatibility period
  leave symlinks in the old screen log locations.

* Remove ``screen-`` from the beginning of the service log filenames

* Service log files will implicitly be renamed as the service names change (see above)

Grenade should work seamlessly as it lets both DevStack runs do their thing and
``devstack-gate`` contains all of the specifics that need updating fro Grenade jobs.

Service Names
-------------

Use fully-formed names for service names (like ceilometer does today): ``nova-compute``,
``glance-registry``, etc.  The names will use the project name, as used in ``devstack/lib/*``
followed by '-' and a descriptive name of the service.

Also allow multiple instances of service names, as in running the fake hypervisor has
a number of ``nova-cpu`` instances.  Append an instance counter to the name similar to
how ``n-cpu-N`` is currently handled.  Optionally use a ':' as the separator between the
service name and instance number.  This will be used in the log file name so it must be
shell-safe.

* There needs to be a mapping of the old abbreviated names to the full names to handle
  backward compatibility.

* This will make ``ENABLED_SERVICES`` very long by default and harder to scan visually.
  Is this a real concern? With the recent forced update to using Bash 4 we could use an
  associative array to do the mapping and the enabled list in a single shot.

  (Note:  We just started doing something in Grenade to handle mapping abbreviated
  service names-> processes (https://review.openstack.org/#/c/113405/5/check-sanity)
  This would help move that logic into DevStack and also help provide other mappings
  (ie, service name -> database name))

* Log filenames will change, but there is more on that front (see below).

* Grenade will need to be updated before the backward compatibility can be removed.


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  dtroyer

Work Items
----------

1. Logging: change the log file names in ``SCREEN_LOGDIR`` so the actual files
   with the timestamp in the names end with the timestamp::

    screen-c-sch.2014-12-10-193405.log becomes  screen-c-sch.log.2014-12-10-193405

2. Logging: change ``devstack-gate`` to look for ``*.log``
   rather than symlinks to select the log files it copies out of ``screen-logs``.

3. Logging: switch from ``SCREEN_LOGDIR`` to ``LOGDIR`` for log tests.  This will
   move the log files out of ``SCREEN_LOGDIR`` so leave backward-compatibility
   symlinks in the old locations.  (This is the reason for #2 as ``devstack-gate``
   selects the files top copy by the symlink attribute.)

4. Logging: follow up in ``devstack-gate`` to use LOGDIR directly and copy log files
   from there.

5. Logging: after a time, remove the symlinks from ``SCREEN_LOGDIR``.

6. Services: change how multiple instances of services are handled, currently in
   ``lib/nova start_nova_compute()`` and ``stop_nova_compute()``.  If the separator
   is changed the config filenames will also change, reconsider if parsing is necessary.

7. Services: build the new service naming structures and compatibility.

8. Services and Logging: switch logging to use the new service names and ensure nothing
   gets lost in ``devstack-gate`` copies.



Dependencies
============

The only dependencies are in the order of changes required in multiple projects.
