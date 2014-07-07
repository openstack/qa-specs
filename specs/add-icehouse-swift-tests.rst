::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

================================
Add Swift API Tests for Icehouse
================================

https://blueprints.launchpad.net/tempest/+spec/add-icehouse-swift-tests

Add Swift API tests which are added in Icehouse release (version 1.13.1)

Problem description
===================

Between Havana and Icehouse releases, some new features are added in Swift.
However, Tempest currently has only subset of API tests of those features.

Proposed change
===============

Add API tests for following new functions.

- New-style container synchronization
- Getting contents inline by TempURL
- POST request to delete multiple containers and objects in bulk
- PUT object with 'If-None-Match: ``*``' header

New file test_container_sync_middleware.py will be created to include tests
of new container synchronization. Test cases for other two features are added in
existing appropriate files.

In new container sync feature, 'realm' and 'cluster' names are used in
"X-Container-Sync-To" header like
//<realm_name>/<cluster_name>/<account>/<container> to specify where to
synchronize objects as substitute for URL which is
used in old-style container sync. Realm and cluster names are defined
in Swift's container-sync-realms.conf, therefore it is also necessary to
specify realm and cluster names in tempest.conf. Following two config values
must be added::

    [object-storage]
    realm_name=<realm name>
    cluster_name=<cluster name>

Implementation
==============

Assignee(s)
-----------

Daisuke Morita <morita.daisuke@lab.ntt.co.jp>

Milestones
----------

Target Milestone for completion:
  Juno-3

Work Items
----------

- Write test cases for Swift's new functions
- Add config values to run tests of new-style container sync

Working progress will be tracked in http://goo.gl/qRLgZe (Google Doc).

