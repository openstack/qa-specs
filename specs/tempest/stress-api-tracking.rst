::

 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

..

==================================
Implement API Tracking
==================================

Previous BP URL: https://blueprints.launchpad.net/tempest/+spec/stress-api-tracking

Problem description
===================

API Call success/failure statistics provide valuable information in test
scenarios. However, manually tracking these in test cases is tedious and
reduces the readability of tests.

Proposed change
===============

Create a decorator that can be applied to select clients that will
automatically monitor the number of calls, successes, and failures of its public methods.

Create a new class called "Trace" with a single public method called "decorate" that will
wrap any desired class's public methods with the following functionality:

#. When such methods return normally the call is successful
#. When the method raises an exception

    * If a method in the stack trace is white-listed, the call is successful.
    * If no methods in the stack trace are white-listed, the call is a failure.

Example expected (and configurable) whitelisted methods could include:

* is_resource_deleted
* wait_for_server_termination

For each decorated method, maintain a dictionary that tracks:

#. The number of successfull calls
#. The number of failed calls
#. The list of observed stacktraces for the failed calls


Client APIs can then be decorated by e.g.::

    def setUpTracking(self, trace):
        """add stats tracking decorator to services."""
        if self.manager:
            if self.manager.servers_client:
                trace.decorate(self.manager.servers_client)
            if self.manager.network_client:
                trace.decorate(self.manager.network_client)
            if self.manager.limits_client:
                trace.decorate(self.manager.limits_client)
            if self.manager.keypairs_client:
                trace.decorate(self.manager.keypairs_client)
            if self.manager.quotas_client:
                trace.decorate(self.manager.quotas_client)
            if self.manager.flavors_client:
                trace.decorate(self.manager.flavors_client)
            if self.manager.floating_ips_client:
                trace.decorate(self.manager.floating_ips_client)
            if self.manager.snapshots_client:
                trace.decorate(self.manager.snapshots_client)
            if self.manager.volumes_client:
                trace.decorate(self.manager.volumes_client)
            if self.manager.volume_types_client:
                trace.decorate(self.manager.volume_types_client)

Run the test as usual.

Finally, the Stats class provides a basic implementation to log collected statistics as well as return the
statistics object for custom logging and other use cases.

At the end of a stress test run, print out the statistics gathered e.g. using LOG.info() logging::

    2014-03-13 15:23:40.729 12273 INFO tempest.stress.driver [-] [VolumesClientJSON:get_volume] 6225 pass, 0 fail
    2014-03-13 15:23:40.729 12273 INFO tempest.stress.driver [-] [VolumesClientJSON:create_volume] 151 pass, 0 fail
    2014-03-13 15:23:40.730 12273 INFO tempest.stress.driver [-] [SnapshotsClientJSON:create_snapshot] 278 pass, 0 fail
    2014-03-13 15:23:40.730 12273 INFO tempest.stress.driver [-] [SnapshotsClientJSON:delete_snapshot] 260 pass, 0 fail
    2014-03-13 15:23:40.730 12273 INFO tempest.stress.driver [-] [VolumesClientJSON:delete_volume] 133 pass, 0 fail
    2014-03-13 15:23:40.731 12273 INFO tempest.stress.driver [-] [ServersClientJSON:detach_volume] 583 pass, 0 fail
    2014-03-13 15:23:40.731 12273 INFO tempest.stress.driver [-] [VolumesClientJSON:list_volumes] 2833 pass, 0 fail
    2014-03-13 15:23:40.731 12273 INFO tempest.stress.driver [-] [ServersClientJSON:attach_volume] 595 pass, 0 fail
    2014-03-13 15:23:40.732 12273 INFO tempest.stress.driver [-] [ServersClientJSON:get_server] 11 pass, 0 fail
    2014-03-13 15:23:40.732 12273 INFO tempest.stress.driver [-] [SnapshotsClientJSON:wait_for_snapshot_status] 278 pass, 0 fail
    2014-03-13 15:23:40.732 12273 INFO tempest.stress.driver [-] [VolumesClientJSON:wait_for_volume_status] 1607 pass, 0 fail
    2014-03-13 15:23:40.732 12273 INFO tempest.stress.driver [-] [ServersClientJSON:wait_for_server_status] 2 pass, 0 fail
    2014-03-13 15:23:40.732 12273 INFO tempest.stress.driver [-] [ServersClientJSON:create_server] 2 pass, 0 fail
    2014-03-13 15:23:40.732 12273 INFO tempest.stress.driver [-] [SnapshotsClientJSON:list_snapshots] 2833 pass, 0 fail
    2014-03-13 15:23:40.733 12273 INFO tempest.stress.driver [-] [SnapshotsClientJSON:get_snapshot] 550 pass, 0 fail


New classes could be located in module:
common/tracking.py



Implementation
==============

Assignee(s)
-----------

Ramy Asselin <ramy.asselin@hp.com>

Walter A. Boring IV <walter.boring@hp.com>

Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------

[walter-boring] API Statistics Wrapper: DONE

[ramy-asselin] Stabilize API Statistics Wrapper: DONE

[walter-boring] Cinder Stress Test: DONE

[ramy-asselin] Stabilize Cinder Stress Tests: DONE

[ramy-asselin] Cinder CHO Test: DONE

[ramy-asselin] Cinder CHO Stabilize: DONE

[ramy-asselin] DOCUMENTATION: TODO

[ramy-asselin] Test Cases: TODO

[ramy-asselin] Code Cleanup: TODO

Current Solution
----------------
API Tracking: https://review.openstack.org/#/c/90449/

