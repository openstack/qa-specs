..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

========================
 Reintegrate Tempest-Lib
========================

https://blueprints.launchpad.net/tempest/+spec/tempest-lib-reintegration


Problem description
===================

For several releases we've had tempest-lib which is a separate python repo
and python package that contains a stable library interface suitable for
external consumption. The idea behind the project is to migrate common pieces
from tempest into the new repo. However, this migration process and having
code which once lived in tempest be somewhere else adds a lot of friction to
the process. For example, after a service client migration if we need to update
or add a test which requires a client change it requires landing a change in
tempest-lib, pushing a tempest-lib release with that change included, landing
a global-requirements and upper-constraints bump, and then finally we can use
the change in tempest. This has proven to be very expensive process and caused
a lot of headaches as we've moved more code into tempest-lib.

Proposed change
===============

The proposed change is to copy all the library code that currently exists in
the tempest-lib repo and migrate it to tempest/lib in the tempest repo. We then
will declare all public interface under that directory as stable interfaces,
just like we did in tempest-lib. Any public interface that lands in tempest.lib
will be assumed to be a stable interface once it lives in the namespace.

The tempest-lib repository will stay around, however, instead of continuing to
push migrated pieces into it or maintaining a passthrough layer with
semver versioning in the tempest-lib repo we'll just push a final 1.0.0 release
and mark the it as deprecated. We'll add a python deprecation warning which will
be emitted when tempest-lib is used to recommend users directly use
tempest.lib. This will mean users will continue to have tempest-lib work the way
it does today, but will have to migrate to it's new home in the tempest repo
if they want any bug fixes or features. By doing this we avoid the maintanence
overhead with having to add and keep the passthrough layer. It also means we're
less likely to slip up by trying to implement a passthrough layer which could
potentially break tempest-lib consumers. There isn't anything that would break
users if they stay on tempest-lib since we will never remove the repo, we just
won't have any active development there. **We will never remove the tempest-lib
repo or the pypi releases for it.** We just likely will never push another
release or any patches to it post deprecation and re-integration.

This reintegration of tempest-lib should change our release cadence for tempest
a bit. Previously we've pushed tempest releases on every start of a new
OpenStack release, a major new feature change lands in tempest, and when we EOL
a stable branch. However, since we'll likely be more frequently adding things
to the library interface bumping the version will likely happen more frequently.
The release versioning scheme for tempest will change slightly. We'll still keep
the monotonically increasing integer, but we'll also have a minor versions to
indicate tempest-lib versions in a semver-like manner inside that. For example,
tempest-10.0.0 will indicate the first release in the series with mitaka
support. Then 10.1.0 will be the first tempest.lib release in that series with
feature adds, and 10.0.1 would be a tempest.lib bugfix release after the mitaka
release (but before the feature release). The minor versions will be reset
to 0 at the start of every major version. Continuing from the previous example,
at the Kilo EOL the version will be 11.0 regardless of how many tempest.lib
version bumps we pushed.

Tempest-lib "migrations" which are really efforts to stabilize the interfaces
are still valuable. But, instead of going through the process of migrating all
the code to an external repo we just have to move the code to tempest.lib in
the tempest repo. Then we can add the tempest-lib shim if desired.

Alternatives
============

Maintain the status quo
-----------------------
We can keep the status quo. This works for the most part, but it adds a lot of
friction to the development workflow. Especially as we try to mature or add on
to existing interfaces. The perfect example of this is with anything involving
the service clients. The OpenStack APIs evolve over time (hopefully using
microversions) and we need to update the clients to use the new features in
tests this becomes a lengthy and drawn out process.

Create a passthrough tempest-lib wrapper
----------------------------------------
We could keep tempest-lib around, but instead of holding code directly it could
be just be a passthrough to tempest.lib. This would be done for 2 reasons,
backwards compatibility for current tempest-lib users and to enable using semver
versioning of the library interface.Tempest-lib could become a library with a
shim passthrough to tempest.lib for all the modules exposed via the library
interface. We'd then start the 1.x.x release series for tempest-lib after the
lib code has been moved back to tempest. Tempest-lib would depend on tempest in
requirements.txt and we could control the tempest versions used by the
passthrough in tempest-lib's requirements. For example, the rest_client module
in tempest-lib would end up looking something like::

    from tempest.lib.common import rest_client

    __all__ = ['RestClient', 'ResponseBody', 'ResponseBodyData',
               'ResponseBodyList']

    class RestClient(rest_client.RestClient):
        pass

    class ResponseBody(rest_client.ResponseBody):
        pass

    class ResponseBodyData(rest_client.ResponseBodyData):
        pass

    class ResponseBodyList(rest_client.ResponseBodyList):
        pass

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Matthew Treinish <mtreinish@kortar.org>


Milestones
----------

Target Milestone for completion:
  Mitaka Release

Work Items
----------

 * Take ownership of tempest on pypi [1]_
 * Enable publishing tempest to pypi [2]_
 * Add reno release notes to both tempest and tempest-lib
 * Iterate through reintegration:
   * Move all the code from tempest-lib to tempest.lib in the tempest repo
 * Add tempest docs about the lib interface and the new release versioning
 * Push new tempest release to mark reintegration of lib
 * Add python warning for tempest-lib deprecation
 * Push tempest-lib release 1.0
 * Modify the existing migration tooling to work with the new lib location

Dependencies
============

This shouldn't be dependent on any other effors, however it may cause conflicts
with other BPs in progress, especially with in-progress efforts to do lib
migrations.

References
==========

.. [1] http://sourceforge.net/p/pypi/support-requests/590/
.. [2] https://review.openstack.org/#/c/275958/
