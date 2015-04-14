::

 This work is licensed under a Creative Commons Attribution 3.0 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

===================================================
 Tempest support for multiple keystone API versions
===================================================

https://blueprints.launchpad.net/tempest/+spec/multi-keystone-api-version-tests

Decouple tempest from keystone version specifics and run tests with keystone v3

Problem description
===================

Tempest code is tightly coupled with keystone V2 specific implementations.
Common classes (such as rest client and tenant isolation), test base classes
and test themselves all assume the identity service is provided by a keystone
v2 endpoint.
Tempest shall be able to run with a keystone V3 identity service, and newer versions
as they become available.

Proposed change
===============

A new configuration flag is introduced to specify the auth version to be used.
The flag is defined as follows:

::

    cfg.StrOpt('auth_version',
               default='v2',
               help="Identity API version to be used for authentication "
                    "for API tests."),

..

And it's used to select the matching version of Credentials and Auth Provider:

::

    if CONF.identity.auth_version == 'v2':
        credential_class = KeystoneV2Credentials
        auth_provider_class = KeystoneV2AuthProvider
    elif CONF.identity.auth_version == 'v3':
        credential_class = KeystoneV3Credentials
        auth_provider_class = KeystoneV3AuthProvider
    else:
        raise exceptions.InvalidConfiguration('Unsupported auth version')

..

A number of refactors are required to achieve this and make sure we don't need
to change test code again when moving to different keystone API versions.

Authentication are factored out in an authentication provider. Credentials are handled
via a dedicated class, provided to tests by a credential manager.
Clients managers receive credentials and are the sole responsible for instantiating
clients and provide them to tests. At the moment client managers instantiate all
available clients when created. This is unnecessary, and it leads to issues when not
all openstack services are available for test. Client managers are thus changed to
lazy instantiation of clients.

Manager __init__ method signature before and after refactor:

::

 Before:

    def __init__(self, username=None, password=None, tenant_name=None,
                 interface='json', service=None):

 After:

    def __init__(self, credentials=None, interface='json', service=None):

..

Authentication in rest client before and after refactor:

::

 Before:

    def request(self, method, url,
                headers=None, body=None):
        if (self.token is None) or (self.base_url is None):
            self._set_auth()

        if headers is None:
            headers = {}
        headers['X-Auth-Token'] = self.token

        resp, resp_body = self._request(method, url,
                                        headers=headers, body=body)

 After:

    def _request(self, method, url, headers=None, body=None):
        # Authenticate the request with the auth provider
        req_url, req_headers, req_body = self.auth_provider.auth_request(
            method, url, headers, body, self.filters)

..

Access to credentials IDs from the tests, before and after refactor:

::

 Before:

        # Retrieve the ResellerAdmin tenant id
        _, users = cls.os_admin.identity_client.get_users()
        reseller_user_id = next(usr['id'] for usr in users if usr['name']
                                == cls.data.test_user)

        # Retrieve the ResellerAdmin tenant id
        _, tenants = cls.os_admin.identity_client.list_tenants()
        reseller_tenant_id = next(tnt['id'] for tnt in tenants if tnt['name']
                                  == cls.data.test_tenant)

 After:

        # Retrieve the ResellerAdmin user id
        reseller_user_id = cls.data.test_credentials.user_id

        # Retrieve the ResellerAdmin tenant id
        reseller_tenant_id = cls.data.test_credentials.tenant_id

..

Areas affected by refactor:

- Rest client (tempest/common/rest_client.py): move auth code to an external auth provider
- Client managers (tempest/manager.py, tempest/clients.py, tempest/scenario/manager.py): work with a Credentials class. Lazy load of clients.
- Tests base classes (tempest/api/\*\*/base.py): adapt where needed to modified rest client, client manager and credentials
- Tests: adapt where needed to modified rest client, client manager and credentials

Alternatives
------------

We could change all the code in place - without refactoring - adding checks for the
configured auth version. This would still require touching a considerable chunk
of tempest code, without the benefit for future keystone versions.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  Andrea Frittoli <andrea.frittoli@hp.com>

Milestones
----------
Target Milestone for completion:
  Juno-1

Work Items
----------
- Move auth from rest_client to auth provider
- Provide unit tests for the new auth and credential classes
- Refactor Manager, Credentials class everywhere
- Client Manager provide client lazy load
- Tenant isolation support for V3
- Provide multi auth-version for API tests
- Provide multi auth-version for scenario tests
- Provide multi auth-version for CLI tests
- Provide multi auth-version for 3rd part tests
- Provide multi auth-version for stress framework
- Add experimental job with auth_version = v3

Dependencies
============
- Python bindings and CLI are not yet all V3 ready. Some of the work in this blueprint
  will have to be postponed until this is fixed
