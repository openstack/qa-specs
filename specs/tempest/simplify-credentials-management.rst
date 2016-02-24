::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===============================
Simplify credentials management
===============================

https://blueprints.launchpad.net/tempest/+spec/simplify-credentials-management

Refactor the way credentials/client managers are obtained by the test
classes so that it is clear which class attributes reference the client
managers with specific credentials.

Problem description
===================

Credentials are allocated by defining an array that enumerates the needed
credentials for a given test class.  For instance::

    credentials = [['operator', CONF.object_storage.operator_role],
                   ['operator_alt', CONF.object_storage.operator_role]]

When the ``setup_credentials`` class method of the base test class is called,
the client managers associated with credentials are mapped to class attributes
with the prefix ``os_roles``.  Credentials can also be allocated in this
manner::

    credentials = ['primary', 'alt', 'admin']

In this case the client managers are aliased to three class attributes, for
instance ``os``, ``manager``, ``os_primary`` are all set to the client
manager using the ``primary`` credentials. This can be confusing for someone
trying to understand a test case, because it is not intuitive for the setting
of a class variable to result in attributes being set and what the names of
those attributes are.

Proposed change
===============

The proposed change is to explicitly assign the attribute values in the given
class's ``setup_credentials`` class method; for instance::

    cls.os_roles_operator = cls.get_client_manager(
        roles=[CONF.object_storage.operator_role], force_new=True)
    cls.os_roles_operator_alt = cls.get_client_manager(
        roles=[CONF.object_storage.operator_role], force_new=True)

For classes that use the ``primary``, ``alt`` and/or ``admin`` credentials, the
logic would look like this::

    cls.os_primary = cls.get_client_manager(credential_type='primary')

All aliasing would be removed.

In either case the credential de-allocation logic can remain the way it is.

Implementation
==============

Assignee(s)
-----------

John Warren <jswarren@us.ibm.com>

Milestones
----------

Work Items
----------

- tempest/scenario/test_server_multinode.py and subclasses
- tempest/scenario/test_security_groups_basic_ops.py and subclasses
- tempest/scenario/test_aggregates_basic_ops.py and subclasses
- tempest/scenario/manager.py and subclasses
- tempest/api/database/base.py and subclasses
- tempest/api/compute/base.py and subclasses
- tempest/api/compute/test_authorization.py and subclasses
- tempest/api/compute/servers/test_servers_negative.py and subclasses
- tempest/api/telemetry/base.py and subclasses
- tempest/api/baremetal/admin/base.py and subclasses
- tempest/api/object_storage/base.py and subclasses
- tempest/api/object_storage/test_object_services.py and subclasses
- tempest/api/object_storage/test_account_services.py and subclasses
- tempest/api/object_storage/test_account_quotas.py and subclasses
- tempest/api/object_storage/test_container_acl_negative.py and subclasses
- tempest/api/object_storage/test_account_services_negative.py and subclasses
- tempest/api/object_storage/test_container_sync.py and subclasses
- tempest/api/object_storage/test_container_acl.py and subclasses
- tempest/api/object_storage/test_account_quotas_negative.py and subclasses
- tempest/api/data_processing/base.py and subclasses
- tempest/api/network/admin/test_floating_ips_admin_actions.py and subclasses
- tempest/api/network/base.py and subclasses
- tempest/api/volume/base.py and subclasses
- tempest/api/volume/test_volume_transfers.py and subclasses
- tempest/api/identity/base.py and subclasses
- tempest/api/identity/v3/test_projects.py and subclasses
- tempest/api/identity/v2/test_tenants.py and subclasses
- tempest/api/image/base.py and subclasses
- tempest/api/orchestration/base.py and subclasses

