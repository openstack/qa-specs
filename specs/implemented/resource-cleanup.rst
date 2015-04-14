::

 This work is licensed under a Creative Commons Attribution 3.0 Unported License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

================
Resource Cleanup
================

https://blueprints.launchpad.net/tempest/+spec/resource-cleanup

Tempest test resource cleanup

Problem description
===================

The cleanup/release of test resources created/allocated in the class level
test fixtures is invoked in the class level tearDown fixture.
However tearDownClass is invoked by the unittest framework only in case
setUpClass is successful. This is causing resources being leaked when:

- a skip exception is raised after resources (typically test accounts)
  have already been allocated
- there is a temporary failure in the system under test which causes the
  setUpClass to fail

The test-accounts bp introduces the possibility to run parallel tests
using a configured list of pre-provisioned test accounts. Test accounts
are allocated and released by each test class, and a failure to release
leads to exhaustion of test accounts.

Proposed change
===============

Disallow overriding ``setUpClass`` defined in ``BaseTestCase`` with a hacking
rule. Define ``setUpClass`` so that it calls one (or more) other methods to be
overridden by descendants. Decorate it with the ``@safe_setup`` decorator.
This way tearDownClass will always be invoked.

::

    @classmethod
    @safe_setup
    def setUpClass(cls):
        cls.setUpClassCalled = True
        cls.resource_setup()

..

While doing this change, an extra benefit can  be gained by structuring
the setup in a series of methods, to enforce the least possible resource
allocation before failure and thus quick cleanup as well.

PoC for this is available here: https://review.openstack.org/#/c/115353.

::

    @classmethod
    @safe_setup
    def setUpClass(cls):
        cls.setUpClassCalled = True
        # All checks that may generate a skip
        cls.setup_skip_checks()
        # Any setup code that does not require / generate test resources
        cls.setup_pre_resources()
        # Allocation of all required credentials
        cls.setup_allocate_credentials()
        # Shortcuts to clients
        cls.setup_clients()
        # Allocation of shared test resources
        cls.setup_create_resources()
        # Any setup code to be run after resource allocation
        cls.setup_post_resources()

..

The tearDownClass fixture requires fixing in several places, because
several tearDownClass implementation would become unsafe, as they expect
attributes defined during setUpClass, which may not be there anymore.

Disallow overriding ``tearDownClass`` defined in ``BaseTestCase`` with
an hacking rule. Define ``tearDownClass`` so that it invokes a descendant
specifc cleanup code, and finally cleans-up credentials.

::

    @classmethod
    def tearDownClass(cls):
        at_exit_set.discard(cls)
        try:
            cls.resource_cleanup()
        finally:
            cls._cleanup_credentials() # Defined in BaseTestCase

..

Alternatives
------------
Two alternatives have been identified.

Massive fixture decoration
--------------------------
Decorate all ``setUpClass`` implementation with ``@safe_setup`` and all
``tearDownClass`` implementation with ``@safe_teardown``.
This approach requires a mass change to tempest, which as the benefit of
being almost scriptable (PoC: https://review.openstack.org/#/c/115123/).
It has the downfall of requiring every new test class to add those two
decorators.

Migrate to TestResources
------------------------
This may still be an option on the long term, but at the moment the
effort of the migration would be more than the benefit from it.
Additional work to ensure cleanup of resources would still be required
anyways.


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

- Define base fixtures
- Migrate base classes and tests to use the new framework (multiple patches)
  Work tracked in https://etherpad.openstack.org/p/tempest-resource-cleanup
- Hacking rule to prevent overriding of setUpClass and tearDownClass

Dependencies
============

None
