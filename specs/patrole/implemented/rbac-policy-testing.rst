..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode
..

===================
RBAC Policy Testing
===================

https://blueprints.launchpad.net/tempest/+spec/rbac-policy-testing

OpenStack deployments have standard RBAC (Role-Based Access Control)
policies that are customized in different ways by users of OpenStack.
These policies need to be enforced and verified to ensure secure
operation of an Openstack Deployment.

Problem Description
===================
Currently there is no unified way to test that RBAC
policies are correctly enforced. This is important because these policies
define how potentially sensitive information and functionality are accessed.

Proposed Change
===============
The proposed solution involves creating a plugin that enables RBAC tests to be
written in such a way that they can verify that an individual policy was
correctly enforced on the specified rbac_role. Tests should primarily be written
as an extension of an existing Tempest test that is wrapped in the plugin's
functionality. The plugin determines what roles should have access to a given
API based on the policy.json file for that service.

For example, a test can be written that only tests the policies for
"compute_extension:services" as follows:

.. code-block:: python

    @test.requires_ext(extension='os-services', service='compute')
    @rbac_rule_validation.action(
        component="Compute",
        rule="compute_extension:services")
    @test.idempotent_id('ec55d455-bab2-4c36-b282-ae3af0efe287')
    def test_services_ext(self):
        try:
            rbac_utils.switch_role(self, switchToRbacRole=True)
            self.client.list_services()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

A key aspect of these tests is that they are testing only a single policy, even
though a normal flow might require the usage of actions covered by multiple policies.
To enable this, the role used for the tests will alternate between "admin" and
the "rbac_role" specified in the config options. This is done so that there is no
chance of other policies besides the one being tested changing the outcome of the test.
To switch roles, the switch_role method of rbac_utils is called. Calling the method with
switchToRbacRole=True tells Keystone to set the current role to the "rbac_role" while
switchToRbacRole=False tells Keystone to set the current role to "admin".

This effort involves creating the plugin for new tests that verify correct
RBAC policy enforcement. This effort will include sample tests but is
not intended to provide full testing coverage of all policies and APIs.
The core code will exist in an external repository containing a plugin, while
individual tests will be written within the plugin. There is not currently
any functionality that needs to be added to tempest/lib, but that may change as more
tests are written.

Alternatives
------------
An alternative is to utilize the cinnamon-role plugin that was being
considered.

Advantages: Utilizing the cinnamon-role plugin enables RBAC functionality
to be wrapped around existing tests with minimal extra effort.

Disadvantages: Cinnamon-role doesn't allow for testing
of individual API endpoints by switching role mid-test.

Another alternative is to add the RBAC test framework into Tempest's core functionality.

Advantages: Easier deployment, don't need extra addons.

Disadvantages: Rbac testing is not something that is considered part of Tempest's
core functionality.


Projects
========
List the qa projects that this spec effects. For example:
* openstack/tempest

Implementation
==============
Assignee(s)
-----------
Primary assignees:
  david-purcell [david.purcell@att.com]
  jallirs [randeep.jalli@att.com]
  syjulian [julian.sy@att.com]
  fm577c [felipe.monteiro@att.com]
  sblanco1 [samantha.blanco@att.com]

Milestones
----------
Target Milestone for completion:
  ocata-2

Work Items
----------
* create plugin for role testing
* add supporting code to tempest/lib/rbac if needed
* add initial group of tests

Dependencies
============
None

