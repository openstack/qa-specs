..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Tempest Post-run Cleanup
========================

https://blueprints.launchpad.net/tempest/+spec/post-run-cleanup

Problem description
====================
The existing script, /tempest/stress/cleanup.py, can be used to do some
basic cleanup after a Tempest run, but a more robust tool is needed
to report as much information as possible about dangling objects (leaks)
left behind after a tempest run in an attempt to help find out why the
object(s) was left behind and report a bug against the root cause. Also
the tool should completely reset the environment to the pre-run state
should tempest leave behind any dangling objects.

The idea is that the user should be able look at the report generated
and find the root cause as to why an object was not deleted. Also the
tool will return the system back into a state where tempest can be
re-run with the expectation that the same test results will be returned.

Currently there can be a good deal of manual work needed, depending
on what tests fail, to return to this pre-run state. This blueprint
is designed to alleviate this issue.

Proposed changes
================
- Keep /tempest/stress/cleanup.py as a starting point and extend it.
  It should be moved to from /tempest/stress to tempest/cmd/ and
  an entry point should be added for it as well. This way it is installed
  as a binary when setup.py is run, which also allows it to be unit
  tested.  Currently the tools uses the tempest OpenStack clients and
  this will remain unchanged.
- Fix cleanup.py to delete objects by looping through each tenant/user,
  over the way it currently works, which is to use the admin user and
  "all_tenants" argument, as some object types don't support this
  argument, Floating IPs for example.
- Currently cleanup.py deletes all objects across all users/tenants.
  Add two runtime arguments: --init-saved-state, that creates a JSON
  file containg the pre-tempest run state and --preserve-state, that
  will preserve the deployment's pre-tempest run state, including tenants
  and users defined in tempest.conf. This will enforce that the
  deployment is in the same state it was prior to running tempest and
  allow tempest to be run again without having to reconfigure tempest
  and recreate the tempest test users etc. For example, if
  --preserve-state is true cleanup will load the JSON file (created by
  running cleanup with --init-saved-state flag prior to tempest run)
  containing the preserved state of the environment and marshal the data
  to some defined instance variables. Then, when cleanup is looping
  through floating ips we would have something like:

        for f in floating_ips:
            if not preserve or (preserve and f['id'] not in self.floating_ips):
                try:
                    admin_manager.floating_ips_client.delete_floating_ip(f['id'])
                except Exception:
                    ...

- cleanup.py currently deletes servers (instances), keypairs,
  security groups, floating ips, users, tenants, snapshots and volumes.
  It should also delete any stacks, availability zones and any other objects
  created by Tempest, full list TBD.
- As mentioned in the overview section above some test failures leave the
  system in a strange state. For example, an instance cannot be deleted
  because it is in Error state.  Even after using CLI to reset the instance
  to Active state, future delete calls just result in Error state once
  again. Such a case indicates a bug in OpenStack.  This tool should
  should provide as much detail as possible as to what went wrong so
  a defect can be opened against the problem(s).
- Add argument, --dry-run, that runs cleanup in reporting mode only, showing
  what would be deleted without doing the actual deletes

Scenario 1: run cleanup.py
--------------------------
This is the current behavior, which deletes all objects in the system,
with the exception of the missing ones, stacks and availability zones
for example.

Scenario 2: run cleanup.py --preserve-state
-------------------------------------------
Same as Scenario 1 except that objects defined in tempest.conf, that
are used in a Tempest run are preserved.

For example (exceptions are variables defined in tempest.conf):

- delete all users except: username, alt_username, admin_username
- delete all tenants except: tenant_name, alt_tenant_name, admin_tenant_name
- delete all images except: image_ref, image_ref_alt

Additional Implications
-----------------------
There are cases where cruft will be left in the database do to openstack defects
that don't allow objects to be removed during the cleanup process.
In such cases resetting the system to the pre-existing state requires direct
interaction with the database.  It may be useful to design the cleanup script
so that it has a pluggable interface,  where downstream functionality can be
added to automate required database interactions for example. Although
the API delete failure indicates an upstream bug that needs to be fixed, until
that bug is fixed testing the environment further is blocked until the records
are deleted.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  David Paterson <davpat2112@yahoo.com>

Can optionally can list additional ids if they intend on doing
substantial implementation work on this blueprint.

Milestones
----------
Target Milestone for completion:

- Juno release cycle, approximately the week of July 24th, 2014.

Work Items
----------
- refactor location of cleanup.py
- register new runtime arguments in cleanup.py
- enable filtering deletions based on --preserve-state argument
  and values defined in tempest.conf
- write code for detailed reporting on dangling resources and
  possible root cause for cleanup failure.
- implement code for --dry-run argument, report only mode.

Dependencies
============
Only those listed above

