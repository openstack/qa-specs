..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

=============================================
Tempest support for API microversions testing
=============================================

https://blueprints.launchpad.net/tempest/+spec/api-microversions-testing-support

Since Kilo, nova has implemented API microversions and the other components (Ironic, etc)
also implemented it now. However, currently Tempest does not have any support for microversions
and doesn't test it at all.
This proposal is to add microversions testing support in Tempest.

Problem description
===================

On microversions mechanism, each microversion change is very small.
For example, version 2.2's change is::

 Add 'type' to os-keypairs response
 Change status code for os-keypairs create method from 200 to 201
 Change status code for os-keypairs delete method from 202 to 204

In long term, a lot of microversions will be implemented because all API
changes should be done with microversions. Now Ironic also implements this
microversions and the other projects have a plan to implement it.
So we need to implement consistent basic test way for these projects.

Proposed change
===============

Test classes for each microversion
----------------------------------

* Implement test classes for each microversion
  When adding a new microversion which changes an API, basically we need
  to implement a test class for the API. In addition, each test class
  contains its microversion range with class values like min_microversion
  and max_microversion. For example, we have added a new attribute 'type'
  to os-keypairs response on nova's microversion 2.2, and the corresponding
  test class will be::

    class KeyPairsV22Test(base.BaseKeypairTest):
        min_microversion = '2.2'

        [..]

  as os-keypairs test class. In the above case, max_microversion is not
  contained. That means unlimited as max_microversion. If we change the API
  again with microversion '2.100' as an example, the test class will be::

    class KeyPairsV22Test(base.BaseKeypairTest):
        min_microversion = '2.2'
        max_microversion = '2.99'

        [..]

  and we need to add a test like::

    class KeyPairsV100Test(base.BaseKeypairTest):
        min_microversion = '2.100'

        [..]

* Add configuration options for specifying test target microversions
  We need to specify test target microversions because the supported
  microversions are different between OpenStack clouds. For operating
  multiple microversion tests in a single Tempest operation, configration
  options should represent the range of test target microversions.
  New configration options also are min_microversion and max_microversion,
  and the test classes will be selected like the following::

    TestClass A: min_microversion = None,  max_microversion = 'latest'
    TestClass B: min_microversion = None,  max_microversion = '2.2'
    TestClass C: min_microversion = '2.3', max_microversion = 'latest'
    TestClass D: min_microversion = '2.5', max_microversion = '2.10'

  +--------------------+-----------------------------------------------------+
  | Configration       | Test classes                                        |
  | (min,    max)      | (Passed microversion)                               |
  +====================+=====================================================+
  | None,     None     | A(Not passed), B(Not passed), C & D - Skipped       |
  +--------------------+-----------------------------------------------------+
  | None,     '2.3'    | A(Not passed), B(Not passed), C('2.3'), D - Skipped |
  +--------------------+-----------------------------------------------------+
  | '2.2',    'latest' | A('2.2'), B('2.2'), C('2.3'), D('2.5')              |
  +--------------------+-----------------------------------------------------+
  | '2.2',    '2.3'    | A('2.2'), B('2.2'), C('2.3'), D - Skipped           |
  +--------------------+-----------------------------------------------------+
  | '2.10',   '2.10'   | A('2.10'), B - Skipped, C('2.10'), D('2.10')        |
  +--------------------+-----------------------------------------------------+
  | None,     'latest' | A(Not passed), B(Not passed), C('2.3'), D('2.5')    |
  +--------------------+-----------------------------------------------------+
  | 'latest', 'latest' | A('latest'), B - Skipped, C('latest'), D - Skipped  |
  +--------------------+-----------------------------------------------------+

  So basically the configration min_microversion value is passed on the
  microversion header. However if the selected class' min_microversion
  is bigger, the class' min_microversion is passed instead.
  If you'd like to always pass the maximum micoversion then, you need to
  set the max_microversion and the min_microversion to be the same value,
  like the 5th example above.

  The default configuration values should be (None, None) like 1st example
  for running on the existing clouds which don't support microversions.
  So we need to change the configuration values with openstack-dev/devstack
  and openstack-infra/project-config for operating microversion tests on the
  gate.

  The microversion 'latest' is a magic keyword as final example. When passing
  'latest' as the microversion to each component(Nova, etc.), the component
  takes the latest microversion action on the server side. Some microversions
  will be backwards incompatible and the 'latest' action can break the gate
  test if Tempest doesn't support the microversion at the time. To avoid such
  situation, we should not specify 'latest' on regular gate jobs. It is nice
  to specify it as experimental job to know we need to update Tempest for
  supporting the latest microversion.

  These configration options should be added for each project(Nova, Ironic,
  etc.) because the microversion numbers are different between projects.

JSON-Schema for each microversion (Nova specific)
-------------------------------------------------

* Define responses for each microversion
  Backwards compatible changes also need new microversions on Nova's
  microversions and Tempest is verifying it by checking Nova API responses
  don't contain any extra attributes with JSON-Schema additionalProperties
  feature. So we need to define the responses for each microversions and
  Tempest needs to switch the response definition of JSON-Schema by the
  microversion.
  Now the responses are defined under tempest_lib/api_schema/response/compute/
  of tempest-lib and the one of the base microversion v2.1 is defined under
  ./v2_1 . Each microversion is a little different from the previous one and
  it is necessary to define the difference under ./v2_2, ./v2_3, etc.

* Make service clients switch response definition for each microversion
  Service clients of Nova will switch the definition based on the microversion.

Tempest-lib migration plan
--------------------------

* Steps:

  #. Implement the microversion testing framework in Tempest.
     The framework includes skipping methods etc for microversion tests based
     on the provided configuration.

  #. Implement base framework for service clients to pass microversion to a
     request header in Tempest.

  #. Implement tests case for Nova microversion v2.2 as sample in Tempest.
     This includes schema and service client change also.
     We can test the microversion testing framework at this time, and it will
     be ready to migrate the framework to tempest-lib.

  #. Migrate the microversion testing framework to tempest-lib

External consumption
--------------------

Once all frameworks are migrated to Tempest-lib, other projects can
use the same for their microversion testing.
Document needs to be updated how to consume the microversion testing
framework with some example.

Projects
========

* openstack/tempest
* openstack/tempest-lib
* openstack-dev/devstack
* openstack-infra/project-config

Implementation
==============

Assignee(s)
-----------

* Ken'ichi Ohmichi <ken-oomichi@wx.jp.nec.com>
* Ghanshyam Mann <ghanshyam.mann@nectechnologies.in>
* Yuiko Takada <yui-takada@tg.jp.nec.com>

Milestones
----------

Target Milestone for completion:
  Mitaka-1

Work Items
----------

* Implement base test classe for microversions
* Pass a test target microversion to service clients
* Add a test class for a single microversion(as sample)
* Migrate tested microversion testing framework to Tempest-lib
* Consume those interface from Tempest-lib and remove from Tempest
* Change the configrations on openstack-infra/project-config for master

Dependencies
============

None

References
==========
* https://review.openstack.org/#/c/242296/
