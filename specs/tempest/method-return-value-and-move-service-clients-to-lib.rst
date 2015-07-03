..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

=====================================================================
No truncation in service clients return value and move to tempest-lib
=====================================================================

https://blueprints.launchpad.net/tempest/+spec/method-return-value-and-move-service-clients-to-lib

Make service clients not to truncate response and move those to tempest-lib

Problem description
===================

Service clients are Tempest own REST clients for operating each OpenStack
project's APIs. And  we have a plan to migrate service clients' methods to
tempest-lib.

1.
Currently these method cut out the top key from response like:

::

  def show_host_detail(self, hostname):
      """Show detail information for the host."""

       resp, body = self.get("os-hosts/%s" % str(hostname))
       body = json.loads(body)
       self.validate_response(schema.show_host_detail, resp, body)
       return service_client.ResponseBodyList(resp, body['host'])

However this cutting is wrong as library function, because the caller
cannot know the complete response returned from corresponding APIs.

One example is resource links which are currently truncated by service
clients. So if caller needs to use those resource links, they can not get
from current service clients.

2.
Currently JSON schemas which are used to validate the response in service
clients are present in Tempest. When service clients will be migrated to
Tempest-lib, those schemas should be accessible for service clients in
Tempest-lib.

Proposed change
===============

* Stop cutting out the top key of a response
  we need to remove this kind of cutting from service client methods like:

::

  def show_host_detail(self, hostname):
      """Show detail information for the host."""

      resp, body = self.get("os-hosts/%s" % str(hostname))
      body = json.loads(body)
      self.validate_response(schema.show_host_detail, resp, body)
  -   return service_client.ResponseBodyList(resp, body['host'])
  +   return service_client.ResponseBodyList(resp, body)

* Move JSON Response Schema to Tempest-lib
  Currently Tempest have JSON response schema in 'tempest/api_schema'
  which are used in service clients to validate API response.
  During Vancouver summit, it was decided that for short term solution
  we can move those schema in Tempest-lib along with service clients.

  In long term, each project should provide some way to get those schema
  through API or something else.

* Copy the service client code to tempest-lib repository

* Switch Tempest to use the service client code of tempest-lib

Migration of service clients can be done gradually with one client
class at a time.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Ken'ichi Ohmichi <oomichi@mxs.nes.nec.co.jp>

Other contributors:

* Ghanshyam Mann <ghanshyam.mann@nectechnologies.in>

Milestones
----------

Target Milestone for completion:
  Liberty

Work Items
----------

* Modify service clients' methods return value based on this proposal.
* Move JSON schema to Tempest-lib
* Move Service Clients to Tempest-lib

Dependencies
============

https://blueprints.launchpad.net/tempest/+spec/consistent-service-method-names

References
==========

* We have discussed this working items at Vancouver Summit.
  The log is https://etherpad.openstack.org/p/YVR-QA-Tempest-service-clients
