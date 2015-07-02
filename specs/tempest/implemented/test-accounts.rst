::

 This work is licensed under a Creative Commons Attribution 3.0 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

=============
Test accounts
=============

https://blueprints.launchpad.net/tempest/+spec/test-accounts

Tempest test accounts management

Problem description
===================

Tempest relies on tenant isolation for parallel test executions. Test accounts
are provisioned on the fly for each test class to ensure isolation.
This approach requires an identity admin account being available for the
provisioning.
The aim of this blueprint is to provide an alternative solution,
specifically pre-provisioned accounts, and to solve the problems related to
this approach: how test accounts are allocated to different test processes
spawned by testr, including alt user and other test accounts, and how we can
support both tenant isolation and this new implementation in tempest, and
easily switch between the two.

Proposed change
===============

Abstract the existing tenant isolation mechanism to a credentials provider
meta-class with two different implementations:

- A configured credentials provider, which uses credentials statically
  configured in tempest.conf. This can be used to avoid including admin
  credentials in the configuration at test run-time
- A dynamic credentials provider, which uses the existing tenant isolation
  logic to generate credentials on the fly using identity admin credentials

Move the logic that selects test accounts out of test and test base classes
into a separate ``credentials_factory`` class, which provides the correct
implementation of tenant isolation to tests based on configuration.
The ``credentials_factory`` is the sole responsible for reading configuration
related to test accounts, and the existing ``get_credentials`` methods from
auth.py should be dropped, and the corresponding logic implemented in the
configured credentials provider.

Change from something like this repeated in various slightly different flavours:

::

        if CONF.compute.allow_tenant_isolation:
            cls.os = clients.Manager(cls.isolated_creds.get_primary_creds())
        else:
            cls.os = clients.Manager()

        if CONF.compute.allow_tenant_isolation:
            cls.os = clients.Manager(cls.isolated_creds.get_alt_creds())
        else:
            cls.os_alt = clients.AltManager()

..

To a code where tenant isolation is hidden to tests:

::

        # Provides the right implementation based on the configuration
        cls.isolated_creds = credentials_factory.get_isolated_credentials()

        # This may raise an AccountNotAvailable
        cls.os = clients.Manager(cls.isolated_creds.get_primary_creds())
        cls.os_alt = clients.Manager(cls.isolated_creds.get_alt_creds())

..

Preserve the tenant_isolation flag, but move it out of compute to a
``common`` configuration group. Remove the current user account
settings from the identity section, and create lists of settings in the
``common`` configuration group instead, for users, tenants, passwords and
domains.

As an indication users expects a list of values = CONCURRENCY x 2.
Tenant, password and domain will expect a list of values either the same
length as users, or with just 1 element, which represents the default value
for all users.

Once a test is completed it releases the accounts it requested, and
they are available for the next test to use.
This should highlight issues with resource cleanup in tests, such as
resource leaks and non-blocking deletes.

The configured credentials provider implements the logic to provide accounts
to tests from the pre-configured ones, ensuring that one account is only used
by one test only at any time. We use a file based reservation mechanism,
which addresses the following issues:

- avoid the initial race where parallel test processes all want to allocate a
  test account at once
- ensure that file(s) used for reservation are cleanup up when testing is done,
  even though each process alone does not have the knowledge about when test
  overall is completed

How many accounts will tests require may vary depending on which tests
are executed. At the moment two per process is typically enough, if we
exclude identity tests, which we can do because they mostly require admin
credentials anyways, so they would not run without admin credentials
configured. Still it may happen that no account is available when test request
it. In this case we the test will fail with AccountNotAvailable.

Assumptions
-----------
All non-admin test accounts have the same roles associated.
All resources associated to an account that require admin credentials
for creation are pre-created.


Alternatives
------------
Implement static allocation of accounts to test processes to avoid the
reservation system. That requires either naming conventions for test accounts,
or each test process to be aware of it's own ID, so that a selection can be
made based on hashing.

Implementation
==============

Assignee(s)
-----------
  Andrea Frittoli <andrea.frittoli@hp.com>

Milestones
----------
Target Milestone for completion:
  Juno-final

Work Items
----------

- Expose the tenant isolation interface into a metaclass
- Move the existing tenant isolation to the dynamic accounts provider
- Implement the static accounts provider and reservation mechanism, including
  the modified configuration options
- Implement a credentials_factory
- Adapt tests and test base classes (in multiple steps)

Dependencies
============

None
