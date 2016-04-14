::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

========================
Refactor Client Managers
========================

https://blueprints.launchpad.net/tempest/+spec/client-manager-refactor

The current client managers depends on a relatively large number of
configuration items, that is the combination of all clients parameters.
This makes its migration to tempest-lib troublesome.

Problem description
===================

We have several plans about the client manager:

- make it as stable interface in tempest.lib. This will help in turn the
  migration of credential providers and service clients to the .lib namespace.
  And it will give people writing tempest plug-in a home for their custom
  service clients
- change it so that it is possible for plug-in developer to add their service
  clients dynamically into the client manager, so we can have a consistent
  way of accessing test clients from tests

The current client managers depends on CONF, and it's structure does not
easily allow for runtime registration of extra clients.

For instance, in *Manager* class:

::

        self.network_client = NetworkClient(
            self.auth_provider,
            CONF.network.catalog_type,
            CONF.network.region or CONF.identity.region,
            endpoint_type=CONF.network.endpoint_type,
            build_interval=CONF.network.build_interval,
            build_timeout=CONF.network.build_timeout,

..

Another issue with the current structure is that new API versions lead to
proliferation of client attributes in the client manager classes. With
service clients being split into pieces, the size of the client manager
grows accordingly.

Proposed change
===============

Split the client manager in two parts.

The first part provides lazy loading of clients, and it does not depend on
tempest CONF, as it is planned for migration to tempest.lib.
It covers the six client groups for the six core services covered by tempest in
the big tent. It exposes an interface to register further service clients.

Lazy loading of clients provides protection against clients that try to
make API calls at __init__ time; it also helps in running tempest with the
minimum amount of CONF required for the clients in use by a specific test run.

The second part passes tempest CONF values to the first one. It registers
any non-core client, whether still in tempest tree or coming from a plug-in.

The client registration interface could look like:

::

    def register_clients_group(self, name, service_clients, description=None,
                               group_params=None, **client_params):
        """Register a client group to the client manager

        The client manager in tempest only manages the six core client.
        Any extra client, provided via tempest plugin-in, must be registered
        via this API.

        All clients registered via this API must support all parameters
        defined in common parameters.

        Clients registered via this API must ensure uniqueness of client
        names within the client group.

        :param name: Name of the client group, e.g. 'orchestration'
        :param service_clients: A list with all service clients
        :param description: A description of the group
        :param group_params: A set of extra parameters expected by clients
                             in this group
        :param client_params: each is a set of client specific parameters,
                              where the key matches service_client.__name__
        """

..

The tempest plugin ``TempestPlugin`` interface is extended with a method to
return the service client data specific to a plugin. Each plugin defines
a new service clients group and the relevant data.

Service Clients data is stored in a singleton ``ServiceClientsData``.
``ServiceClientsData`` is instantiated by the ``TempestTestPluginManager``,
which obtains the service client data from each plugin and registers it.

Client managers used by tests consume the service client data singleton,
and dynamically defines a set of attributes which can be used to access the
clients.

Attributes names are statically defined for now. They will be the same names as
now, to minimize the impact on the codebase. For plugins, attributes names
include the group name, to avoid name conflicts across service clients that
belong to different plugins.

In future we may define a standard naming convention for attribute
names and to enforce it by deriving names automatically. Future names may not
contain the '_client' suffix, to save space and allow for always specifying
the client provider in test code, so to make the code more readable.
This naming convention will not be implemented as part of this spec.

Alternatives
------------

Keep the manager on tempest side, and have big tent teams write their own
managers. Carry long list of clients as parameters in cred providers and
other parts of tempest

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Andrea Frittoli <andrea.frittoli@hpe.com>


Milestones
----------

Target Milestone for completion:
  Newton-1

Work Items
----------

- Core functionality in manager part1, with unit test coverage and migration
  of one client group
- Migration of other client groups (one per patch)
- Implementation of the registration interface (does not depend on step 2)
- Registration of non-core clients from tempest tree
- Registration of non-core clients from plugins
- Separate manager part1 into it's own module, and include maanger.py along

Work has stared on this: Change-id I3aa094449ed4348dcb9e29f224c7663c1aefeb23

Dependencies
============

None
