..
  This work is licensed under a Creative Commons Attribution 3.0 Unported
  License.

  http://creativecommons.org/licenses/by/3.0/legalcode

==============================
RBAC Testing Multiple Policies
==============================

`bp rbac-testing-multiple-policies <https://blueprints.launchpad.net/patrole/+spec/rbac-testing-multiple-policies>`_

Problem Description
===================

Patrole currently RBAC tests an API endpoint by checking whether a policy
action is allowed, according to ``oslo.policy`` and then executes
the API endpoint that does policy enforcement with the role specified
under ``CONF.rbac.rbac_test_role``. However, this approach does not account
for API endpoints that enforce multiple policy actions, either directly
(within the implementation of the API endpoint itself) or indirectly (across
different helper functions and API endpoints). The current approach to RBAC
testing in Patrole, therefore, does not always provide complete policy
coverage. Just like multiple calls are made to ``oslo.policy`` by various
endpoints, Patrole should do the same.

For example, take an API that enforces 2 policy actions, A and B, where A is
``admin_api`` and B is ``admin_or_owner``. Calling the API with
``rbac_test_role`` as admin role will necessarily pass, because admin role has
permissions to execute policy actions A and B and will also be able to execute
the API endpoint. However, the test will fail for non-admin role, with the
``rbac_rule_validation`` decorator evaluating *only* policy action B. This is
because a non-admin role (i.e. Member) role *has* permissions to perform policy
action B (which is ``admin_or_owner``) but does *not* have permissions to
execute the API endpoint, since the endpoint enforces an ``admin_api`` policy:
this results in a ``Forbidden`` exception being raised, and the test failing.

Proposed Change
===============

The proposed change is to modify the ``rbac_rule_validation`` decorator to
be able to take a list of policy actions, rather than just one policy action.
For each policy action, a call will be made to ``oslo.policy`` to confirm
whether the test role is allowed to perform the action. Each result from
``oslo.policy`` will be logical-ANDed together. For example, if policy action
A evaluates to ``True`` and policy action B evaluates to ``False``, then the
final outcome is ``False``: therefore, the user should not be able to perform
the API call successfully. As such, Patrole can deduce whether a role is
allowed to call an API that enforces multiple policies.

To provide a concrete example, the following test::

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-lock-server:unlock:unlock_override")
    def test_unlock_server_override(self):
        server = self.create_test_server(wait_until='ACTIVE')
        # In order to trigger the unlock:unlock_override policy instead
        # of the unlock policy, the server must be locked by a different
        # user than the one who is attempting to unlock it.
        self.os_admin.servers_client.lock_server(server['id'])
        self.addCleanup(self.servers_client.unlock_server, server['id'])

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.servers_client.unlock_server(server['id'])

can be changed to::

    @rbac_rule_validation.action(
        service="nova",
        rules=["os_compute_api:os-lock-server:unlock",
               "os_compute_api:os-lock-server:unlock:unlock_override"])
    def test_unlock_server_override(self):
        server = self.create_test_server(wait_until='ACTIVE')
        self.os_admin.servers_client.lock_server(server['id'])
        self.addCleanup(self.servers_client.unlock_server, server['id'])

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.servers_client.unlock_server(server['id'])

According to the Nova documentation for locking a server, the "unlock_override"
policy is "performed only after the check os_compute_api:os-lock-server:unlock
passes". With this change, Patrole will generate its "expected" result based on
whether the test role can perform *all* the policies passed to ``rules``;
otherwise, if the test role cannot perform at least one policy, the expected
result will be ``False``. Afterward, the API action will be called with the test
role and the outcome of which will be compared with the expected result.

If the expected and actual results match, then the test will pass. Otherwise,
Patrole can generate a detailed error message explaining which policies passed
to ``rules`` caused test failure. For example, in the above example, if the
test role has permissions to perform "os_compute_api:os-lock-server:unlock" but
not "os_compute_api:os-lock-server:unlock:unlock_override", then Patrole will
emit an error saying that "os_compute_api:os-lock-server:unlock:unlock_override"
was responsible for test failure. This will help cloud deployers and developers
to determine the source of test failure and to pinpoint inconsistent custom
policy configurations.

Alternatives
------------

Currently, there are no other viable alternatives. It is not feasible or
desirable to repeatedly call each API endpoint against each policy action that
the endpoint enforces, for various fairly obvious reasons:

1. Code redundancy should be minimized, to make code readability and
   maintenance easier.
2. This introduces serious run time concerns in Patrole's gates.

Security Impact
---------------

None.

Notifications Impact
--------------------

``LOG`` statements will have to be updated to convey multiple policy actions
to the user, especially following test failure.

If a Patrole test tests may policies, after test failure, it would be useful
for users for Patrole to log which policies caused the test failure. This can
be determined by iteratively calling ``oslo.policy`` for each policy provided
to the ``rbac_rule_validation`` decorator and storing the list of policies
that are not compatible with the role and the expected test outcome.

Other End User Impact
---------------------

None.

Performance Impact
------------------

The performance impact is negligible. This change will result in barely
slower test run time, because multiple calls will be made to ``oslo.policy``
rather than just one, per Patrole test.

Other Deployer Impact
---------------------

None.

Developer Impact
----------------

The proposed change requires that developers be `prudent` about which policy
actions they include in the proposed ``actions`` parameter. Including an
excessively high number of policy actions is not maintainable and is
cumbersome from a development standpoint. For example, Cinder enforces
``volume_extension:volume_host_attribute`` and
``volume_extension:volume_mig_status_attribute``, along with a number of
different policy actions, for many, many endpoints. Repeating these policy
actions for every Cinder RBAC test would be redundant and bad design.
(If it could be proven that these policy actions are enforced for *every*
Cinder API endpoint, then the policy actions could be auto-injected by the
Patrole framework and logical-ANDed with the policy actions explicitly
specified in ``actions``. However, this approach goes beyond the scope of this
spec).

It is recommended that this enhancement be used *judiciously* by developers.
Only endpoints that enforce multiple relatively *unique* policy actions
should be included in the ``actions`` list. Uniqueness can be inferred, for
example, from
`Keystone's <https://specs.openstack.org/openstack/keystone-specs/specs/keystone/pike/policy-in-code.html>`_
and
`Nova's <https://specs.openstack.org/openstack/nova-specs/specs/newton/implemented/policy-in-code.html>`_
self-documenting in-code policy definitions.

Implementation
==============

Assignee(s)
-----------

Primary assignees:
  * Felipe Monteiro <felipe.monteiro@att.com>
  * Samantha Blanco <samantha.blanco@att.com>

Other contributors:
  * Rick Bartra <rb560u@att.com>

Work Items
----------

* Enhance the ``rbac_rule_validation`` decorator with the ``actions`` parameter
  and deprecate the ``rule`` parameter.
* Write a helper function in ``rbac_rule_validation`` to iteratively call
  ``rbac_policy_parser.RbacPolicyParser.allowed`` for each policy action
  specified in ``actions``, logically ANDing them together, and returning
  the result to ``rbac_rule_validation`` decorator.
* Refactoring tests to use ``actions`` instead of ``rule``.
* Writing new unit tests to test the proposed enhancement.
* Selectively adding multiple policy actions to some tests.
* Confirming that all API tests work with the proposed enhancement.
* Updating documentation.

Dependencies
============

None.

Documentation Impact
====================

Patrole documentation should be updated to convey the new parameter along with
intended use, as described in this spec.

References
==========

* `Policy terminology <https://docs.openstack.org/kilo/config-reference/content/policy-json-file.html>`_
* `Keystone policy in code <https://specs.openstack.org/openstack/keystone-specs/specs/keystone/pike/policy-in-code.html>`_
* `Nova policy in code <https://specs.openstack.org/openstack/nova-specs/specs/newton/implemented/policy-in-code.html>`_
