::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===========================
More Selectable Swift Tests
===========================

https://blueprints.launchpad.net/tempest/+spec/more-selectable-swift-tests

Enable to run API tests more flexibly for various Swift installation

Problem description
===================

Currently, Tempest can select API test cases by referring discoverable_apis
config setting in tempest.conf. However, this feature supports only selecting
removable functions using WSGI middlewares although Swift has many
functional selectabilities other than using middlewares.

Proposed change
===============

Add config parameters in tempest.conf for selecting tests for following Swift
body's functionalities.

- (Old-style) Container Sync: mirroring objects in the container to another
  container
- Object Versioning: versioning all objects in the container
- Discoverability: providing details about the Swift installation

Above features are independent of middleware settings. Whether to use some
middlewares or not is defined in Swift's proxy server, on the other hand,
container sync and object versioning require settings in storage server and
running background daemons. Discoverability function is enabled/disabled at
proxy servers, but this function is to expose Swift's installed middlewares
and other features, so the setting is independent of middleware settings.

Config values are added in tempest.conf as follows::

    [object-storage-feature-enabled]
    container_sync=True/False
    object_versioning=True/False
    discoverability=True/False

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

- Add config values to select tests
- Insert skip annotations into appropriate test cases