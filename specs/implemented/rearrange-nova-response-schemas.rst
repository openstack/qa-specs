..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Rearrange Nova Response Schemas
===============================

https://blueprints.launchpad.net/tempest/+spec/rearrange-nova-response-schemas

Rearrange Nova Response Schemas

Problem description
===================

Compute response schemas were implemented for v2 and v3 APIs.
At that time common parts were defined in common schemas and
version specific into respective directories (v2 & v3).

Now v3 API is not valid for Nova and v2 and v2.1 API`s response are same.
After removing v3 schemas (https://review.openstack.org/#/c/141274/)
we have only 1 set of schemas for v2 (/v2.1) APIs but those end up in
scattered structure.

It is difficult to read and understand API' complete schema as they are defined
in multiple files.


Proposed change
===============

Rearrange current schemas into better file/directory structure and if needed
then, defined schemas name more clearly as per API methods.

As Nova v2.1 APIs are current API (https://review.openstack.org/#/c/149948/),
we should move all current schema files to directory name v2.1. As nova is going
to release microversion also, schema files for microversion needs to go in their
respective new directories.

Below are the re arrangement details-

* Directory structure-
   api_schema/response/compute/v2.1/  -> will contain all the schema files for v2.1.
   api_schema/response/compute/v2.2/  -> will contain all the schema files for v2.2.
   and so on

* Each resource schema will be defined in single files under v2.1 directory
   For example -hypervisors.py will have all schema of hypervisor resource API.

* Each schema name should be clear enough to easily understand the API for
  which they are defined. For example -

    * list_hypervisors - list hypervisors API schema
    * list_hypervisors_detail - detail list of hypervisors
    * create_get_update_<resource name> - If schema is same for create, get
      & update API of any resource.

   Note- Most of the schema names are defined as per above guidelines but
   if there are some misleading names, those needs to be fixed.
   For example - quota class set and quota set schemas are defined with same
   name (quota_set) in quotas.py and quota_classes.py.


After above re arrangement it will be easy to maintain those schemas.


Alternatives
------------

Keep things as they are which will keep schemas readability and maintenance
difficult.

Implementation
==============

Assignee(s)
-----------
Primary assignees:
   Ghanshyam Mann<ghanshyam.mann@nectechnologies.in>


Milestones
----------
Target Milestone for completion:

* kilo-3

Work Items
------------------------------------
* Change schema as per proposed idea.
* Import the changed schema according to their new path.
* Work will be tracked in: https://etherpad.openstack.org/p/rearrange-compute-response-schemas
