::

 This work is licensed under a Creative Commons Attribution 3.0 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

=======================
Test accounts Continued
=======================

https://blueprints.launchpad.net/tempest/+spec/test-accounts-continued

Tempest test accounts management

Problem description
===================

The "Test accounts" spec provided support for preprovisioned accounts,
as well as for those accounts to be configured in YAML format.
There are a few limitations to the existing limitations:

- all accounts must belong to the same network
- all accounts must be of the same type, so we have a combination of
  accounts configured in tempest.conf and in accounts.yaml

Proposed change
===============

Extend the format of the accounts YAML file to support specifying the
name and type of resources pre-provisioned for an account. Such resources
are intended to be reused by tests, and shall not be cleaned-up.

::

        - credentials:
              username: 'user_1'
              tenant_name: 'test_tenant_1'
              password: 'test_password'
          resources:
              network: 'my_network'
              subnet: 'my_subnet'

        - credentials:
              username: 'user_2'
              (...)

..

Extend the format of the accounts YAML file to support specifying the
account type of an account. We may have an account type identifier,
or alternatively a list of roles.

::

        - credentials:
              username: 'admin'
              tenant_name: 'admin_tenant'
              password: 'admin_password'
          type: 'admin'

        - credentials:
              username: 'swift_admin'
              tenant_name: 'admin_tenant'
              password: 'admin_password'
          roles:
              - reseller

..

Adapt the credentials providers to be able to handle credentials
requests based on specific roles as well as account type (available
today via dedicated methods).

The abstract implementation would be something like:

::

    @abc.abstractmethod
    def get_creds_by_roles(self, roles=None):
        return

    def get_creds_by_type(self, type=None):
        if type == "primary":
            return get_primary_creds()
            (...)

..

Adapt the non pre-provisioned account scenario to also read accounts
from the accounts YAML file, and deprecate any account information
in tempest.conf beyond the name of account file.

Provide a tool to be consumed by devstack to generate the
pre-provisioned accounts and the corresponding YAML file. Work on
this is already started here https://review.openstack.org/#/c/107758/.

Integrate with the post-run clean-up tool, to avoid deleting
pre-provisioned resources specified in the YAML file.


Alternatives
------------
The current implementation is functional but incomplete, so the only
alternative is not to use it, or suffer its limitation.

Implementation
==============

Assignee(s)
-----------
  Andrea Frittoli <andrea.frittoli@hp.com>

Milestones
----------
Target Milestone for completion:
  Kilo-final

Work Items
----------

- Extend the YAML file parser
- Implement the non-cleanup of configure resources
- Deprecate account configuration options
- Read account info from YAML, with fallback to deprecated
  configuration options
- Implement provisioning tool
- Switch devstack and job definition to use the accounts YAML file in
  case of tenant isolation as well as pre-provisioned accounts
- Configure check/gate to run a combination of tenant isolation and
  pre-provisioned accounts

Dependencies
============

None
