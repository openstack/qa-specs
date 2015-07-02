::

 This work is licensed under a Creative Commons Attribution 3.0 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

=========================================
Multiple strategies for ssh access to VMs
=========================================

https://blueprints.launchpad.net/tempest/+spec/ssh-auth-strategy

Different strategies for ssh access to VMs in tests.

Problem description
===================

Ssh access to created servers is in several cases key to properly validate the
result of an API call or a scenario (use case) test. This is true for compute
but not limited to it. Network and volume verification must often rely on test
servers, and ssh access to the VM helps significantly for the verification.

Support for ssh access to VMs in tempest tests is both heterogeneous as well
as incomplete. Not all tests honour the same config options. The existing
``run_ssh`` option is only taken into account by some of the tests, the compute
API ones. Not all tests use the same strategy for ssh access, and several tests
do not perform any ssh verification at all. The reason often is that ssh
verification is a common source of "flakiness" and timeouts in tests, and
allocation of the resources required for ssh verification can be expensive.


Proposed change
===============

Consolidate the available configuration options and make sure they are
honoured everywhere. Configuration shall be declaritive, i.e. tempest users
shall configure how they expect ssh to work, and if that's not compatible
with the deployed cloud tempest shall raise an ``InvalidConfiguration``.
Improve the configuration help text to guide configuration for instance
validation.

Current configuration options relevant to instance validation are:

- ``CONF.auth.allow_tenant_isolation``: affects the fixed network name
- ``CONF.compute.[image|image_alt]_ssh_user``
- ``CONF.compute.image_ssh_password``: not image specific, and it's used
  by only two tests, without checking against the ssh_auth_method
- ``CONF.compute.image_alt_ssh_password``: unused
- ``CONF.compute.run_ssh``
- ``CONF.compute.ssh_auth_method``: used for resource setup by API compute
  tests, but not honoured by the tests. The image[_alt]_ssh_[user|password]
  settings are  meant to be used when this is set to "configured".
  At the moment it is not enforced nor documented
- ``CONF.compute.ssh_connect_method``: used for resource setup by API
  compute tests, not honoured by the tests. When set to floating, it
  should be verified that a floating IP range is configured
- ``CONF.compute.ssh_user``: currently used for ssh verification by most
  API and scenario tests, which is a problem because configuration supports
  different images, each with an own ssh user
- ``CONF.compute.ping_timeout``: used by scenario test only
- ``CONF.compute.ssh_timeout``: used by RemoteClient
- ``CONF.compute.ssh_channel_timeout``: used by RemoteClient
- ``CONF.compute.fixed_network_name``: used by API and scenario tests.
  It's the name of the network for the primary IP with nova networking;
  or with neutron networking when tenant isolation is disabled.
  The logic, as implemented by test_list_server_filters shall be moved
  to an helper and reused everywhere. It may be used for ssh validation
  only if floating IPs are disabled
- ``CONF.compute.network_for_ssh``: used by RemoteClient and some scenario
  tests to discover an IP for ssh validation. It can be used if floating
  IP for ssh is disabled, in which case the fixed_network_name could be
  used as well; except for the case of multi-nic testing, which would
  require more logic anyways to enable the 2nd nic
- ``CONF.compute.ip_version_for_ssh``: used by ``RemoteClient``.
  It should be overridable via parameter instead of one config for all
  tests.
- ``CONF.compute.use_floatingip_for_ssh``: used by some scenario tests,
  duplicate of ssh_connect_method, which is not used at the moment
- ``CONF.compute.path_to_private_key``: unused
- ``CONF.network.tenant_network_reachable``: used by scenario tests. In
  some cases it's used for tests that want to verify both tenant and
  public network connectivity. In other cases it's used to find out which
  IP to be used for instance validation, which overlaps with the
  ssh_connect_method
- ``CONF.network.public_network_id``: used for allocation of floating
  IPs when neutron is enabled.

Target configuration shall include a new group "validation" used for all
option related to validation of API call results, and the following options:

- ``CONF.validation.connect_method``: default ssh method. Tests may
  still use different method if they want to do so (fixed or floating)
- ``CONF.validation.auth_method``: default auth method. Tests may
  still use a different method if they want to do so (only ssh key
  supported for now). Additional methods will be handled in a
  separate spec
- ``CONF.validation.ip_version_for_ssh``: default IP version for ssh
- ``CONF.validation.*timeout`` (for ping, connect and ssh)
- ``CONF.*.*ssh_user`` (for the various images available)
- ``CONF.network.fixed_network_name``: default fixed network name; this
  parameter is only valid in case of nova network (with flat networking),
  and for now with pre-provisioned accounts. Once the bp
  test-accounts-continued is implemented this may still be used as
  default fixed network name if not specified in accounts.yaml.
- ``CONF.network.floating_network_name``: default floating network name,
  used to allocate floating IPs when neutron is enabled. Deprecates
  ``CONF.network.public_network_id``
- ``CONF.network.tenant_network_reachable``: used when the configured
  ssh_connect_method is "fixed". If this is set to false raise an
  ``InvalidConfiguration`` exception

Configuration options that are renamed or that planned for removal
should go through the deprecation process.

A few options are image specific: image name, ssh user / password,
typical time to boot / ssh.
Such options would be better handled in a dedicated images.yaml file
rather than in tempest.conf. This will be handled in a separate spec.

Define an helper functions that read, validate and process the
configuration, which in future will help decoupling
``create_test_server`` from CONF, for migration to tempest-lib.

Extend the existing ``RemoteClient`` to provide tools for:

- ping: attempts a single ping to a target to server
- connect: attempts a single TCP connect on a generic port to a target server
- ssh: attempts a single ssh connection to a target server
- validaton: validates a server by using a configurable sequence of the above;
  cares about retries and timeouts

Bits of implementation for that are already available in scenario
tests. They should be consolidated in ``RemoteClient``.

Define a ``validation_resources`` function, similar to the existing
``network_resources``, to be used in the class level ``resource_setup``,
which allocates required reusable resources, such as: a key pair, a
security group with rules in it, and a floating ip. It returns all the
resources in form of a dict, ready to be used in ``create_test_server``.
Tests which use more than one server will allocated additional floating
IPs on demand. Once bp test-accounts-continued is implemented as well
we may consider consolidating ``validation_resources`` and
``network_resources``.

Centralize ``create_test_server``, and make sure all tests use
this central implementation. Add the following features:

- it includes an ``sshable`` boolean parameter in the ``create_test_server``
  helper function, defaults to ``False``. If set to ``True`` it ensures the
  server is created with all the required resources associated, e.g. that it
  has a public key injected, and IP address on a public network, a security
  group that allows for ICMP and ssh communication. The default to false
  ensures that resources are used only when required.

- it accepts a resources dict with reusable items, which can be: a key_name,
  a security_group with rules for ssh and icmp in, a floating_ip. These are
  passed in as parameters in preparation for the migration to tempest-lib.

- it extends the valid value for ``wait_until`` with new types of wait
  abilities: ``PINGABLE`` and ``SSHABLE``. For instance if an ``SSHABLE``
  server is requested the create method takes care of performing basic ssh
  validation as well.

- it returns a tuple ``(created_server, remote_client)``, where the remote
  client is already initialized with access resources such as public key,
  admin password, IP address, ssh account name.

::

    def create_test_server(self, client, wait_until=None, sshable=False,
                           resources=None, **kwargs):
        if sshable == True and run_ssh == True:
            read config via helpers
            process result, extend kwargs, but do not override
                public_key: if key_name not defined use from resources or create
                sg rules: use from resources, or create sg with rules and append
                network name: append to network dict
                floating ip: use from resources or allocate one
            validation == True
        (...)
        server = servers_client.create_server(**kwargs)
        wait for status
        if ip_type == 'floating':
            attach an IP
        if validation:
             build params based on helpers above
             remote = RemoteClient(**params)
             wait for status (extended: ping / connect / ssh)
             return remote

    def test_foo(self):
        myvm = servers.create_test_server(
            sshable=True, wait_until='SSHABLE')
        myvm['remote_client'].write_to_console("I could do something more useful")

..

A server can still be made ssh-able "by-hand" for more complex scenarios, such
as hot-plug tests, where the server may only be connected at a later stage to
a public network.

In case a test class contains tests which make use of ssh-able servers, network
resources must be prepared for the tenant (if not yet available), so that it
is possible to have network access to the VM.

Alternatives
------------

As run_ssh is currently disabled, an alternative could be to completely
drop ssh verification from API tests. However a number of cases cannot really
be verified unless ssh verification is on (e.g. reboot, rebuild, config drive).


Implementation
==============

Assignee(s)
-----------
Primary assignee:
  Andrea Frittoli <andrea.frittoli@hp.com>

Other assignees:
  Nithya Ganesan <nithya.ganesan@hp.com>,
  Joseph Lanoux <joseph.lanoux@hp.com>


Milestones
----------
Target Milestone for completion:
  Kilo-2

Work Items
----------

- Introduce new configuration options, and helpers to read them
- Create a validation_resources function
- Create shared create_test_server function
- Create shared ssh verification function / extend RemoteClient
- Migrate tests to the new format (multiple patches)
- Deprecate un-used / removed configuration options
- Setup experimental / periodic jobs that run with validation
  enabled - the aim is to promote both run_ssh and sshable to
  be ``True`` by default, as well maintain the code path healthy
  until that happens

Dependencies
============

None
