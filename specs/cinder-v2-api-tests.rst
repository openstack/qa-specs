::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

============================
Implement Cinder V2 API test
============================

https://blueprints.launchpad.net/tempest/+spec/cinder-v2-api-tests

Implement Cinder v2 API test by sharing service client and test code with v1.


Problem description
===================

Tempest doesn't have enough Cinder v2 api tests. We need to add more tests
for it. Cinder v2 api only has some small updates, so v1 and v2 tests could
share service client and test code. In this way, we don't need to maintain
many duplictate test codes.


Proposed change
===============

This blueprint proposes that Cinder v1 and v2 tests share service client and
test code. It includes the the following changes:

1. Create common service clients
2. Create common base test class
3. Make each v1 test class inherit the v2 test class
4. Change the Cinder API test directory structure

1. Create common service clients
--------------------------------

v1 and v2 service client only have very little difference. Most codes should
be same. So we could create a common service client and inherit it by v1 and
v2.

* [v1 service client] -> [CommonServiceClient]
* [v2 service client] -> [CommonServiceClient]

2. Create common base test class
--------------------------------

Now each Cinder API test class inherits like:

* [v1 test class] -> [BaseVolumeV1Test] -> [BaseVolumeTest]
* [v2 test class] -> [BaseVolumeV2Test] -> [BaseVolumeTest]

To share API test classes, we need to create common base test class instead
of BaseVolumeV1Test/BaseVolumeV2Test. The class instance can switch its
behavior based on some variable which represents an API version.
After applying this common class to every API test classes, the existing
BaseVolumeV1Test and BaseVolumeV2Test can be removed.

3. Make each v1 test class inherit the v2 test class
----------------------------------------------------

We need to change v2 test classes' inheritances to the common base test class
and change v1 test classes' inheritances to v2 test class:

* [v1 test class] -> [v2 test class] -> [CommonVolumeTest]

In v1 test class, the variable which represents an API version should be "1",
and the variable should be "2" in v2 test class::

  class SomeApiV2Test(CommonVolumeTest):
    _api_version = 2
    [..]

  class SomeApiV1Test(SomeApiV2Test):
    _api_version = 1
    [..]

4. Change the Cinder API test directory structure
-------------------------------------------------

Current test directory structure is

* tempest/api/volume/    : v1 API test files
* tempest/api/volume/v2/ : v2 API test files

This structure is not understandable, and it is better to move v1 API test
files to some directory which shows v1's one clearly.

This blueprint proposes to change the structure to

* tempest/api/volume/    : common test files
* tempest/api/volume/v1/ : v1 API specific test files
* tempest/api/volume/v2/ : v2 API specific test files

The test cases which can share the code between v1 and v2 will be stored in
"tempest/api/volume/".
For specific test cases which don't have shared code, the inheritance model
from (3) won't work. The hierarchy would be:

* [v1 test class] -> [CommonVolumeTest]
* [v2 test class] -> [CommonVolumeTest]

and these test files would be stored in:

* tempest/api/volume/v1/
* tempest/api/volume/v2/


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Zhi Kun Liu <liuzhikun@gmail.com>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

- Add common service client for v1 and v2
- Add a common class for Cinder v1/v2 API tests
- Add a common admin class for Cinder v1/v2 API tests
- Add new test cases using the new shared test classes
  Using a google docs spreadsheet to manage the task progress:
  (`cinder_v2_api_tests <https://docs.google.com/spreadsheets/d/1ztFAn1D677zTVBahZB0sLjQkcU2_oIthZ-eRNRHI4LM>`_)
