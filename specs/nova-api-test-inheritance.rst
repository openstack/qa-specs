::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

====================================
Improve Nova API test serviceability
====================================

https://blueprints.launchpad.net/tempest/+spec/nova-api-test-inheritance

Improve Nova API test serviceability by sharing Nova v2/v3 API test code.


Problem description
===================

Now there is a lot of copy&paste test code for Nova v2/v3 API tests.
In addition, we need to add many checks for API test coverage.
As the result, we should apply the same changes to v2 and v3 tests and
that becomes much maintenance burden now.


Proposed change
===============

To improve the maintenancebility, this blueprint proposes the changes to share
v2 and v3 API test code. The proposed way is the following three steps.

1. Create common base test class
2. Make each v2 test class inherit the v3 test class
3. Change the Nova API test directory structure

1. Create common base test class
--------------------------------

Now each Nova API test class inherits like:

* [v2 test class] -> [BaseV2ComputeTest] -> [BaseComputeTest]
* [v3 test class] -> [BaseV3ComputeTest] -> [BaseComputeTest]

To share API test classes, we need to create common base test class instead
of BaseV2ComputeTest/BaseV3ComputeTest. The class instance can switch its
behavior based on some variable which represents an API version.
After applying this common class to every API test classes, the existing
BaseV2ComputeTest and BaseV3ComputeTest can be removed.

2. Make each v2 test class inherit the v3 test class
----------------------------------------------------

We need to change v3 test classes' inheritances to the common base test class
and change v2 test classes' inheritances to v3 test class:

* [v2 test class] -> [v3 test class] -> [CommonComputeTest]

In v2 test class, the variable which represents an API version should be "2",
and the variable should be "3" in v3 test class::

  class SomeApiV3Test(CommonComputeTest):
    _api_version = 3
    [..]

  class SomeApiV2Test(SomeApiV3Test):
    _api_version = 2
    [..]

3. Change the Nova API test directory structure
-----------------------------------------------

Current test directory structure is

* tempest/api/compute/    : v2 API test files
* tempest/api/compute/v3/ : v3 API test files

This structure is not understandable, and it is better to move v2 API test
files to some directory which shows v2's one clearly.

This blueprint proposes to change the structure to

* tempest/api/compute/    : common test files
* tempest/api/compute/v2/ : v2 API specific test files
* tempest/api/compute/v3/ : v3 API specific test files

If there is no shared code between the v2 and v3 APIs the inheritance model
from (2) won't work. So in these cases the hierarchy will be:

* [v2 test class] -> [CommonComputeTest]
* [v3 test class] -> [CommonComputeTest]

and these test files will be stored directly in:

* tempest/api/compute/v2/
* tempest/api/compute/v3/


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Ken'ichi Ohmichi <oomichi@mxs.nes.nec.co.jp>

Other contributors:
  Ghanshyam Mann <ghanshyam.mann@nectechnologies.in>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

- Add a common class for Nova v2/v3 API tests
- Add a common admin class for Nova v2/v3 API tests
- Share API test clases
  This work needs a lot of patchset.
  To manage the task progress, I prepare the etherpad:
  https://etherpad.openstack.org/p/nova-api-test-inheritance

