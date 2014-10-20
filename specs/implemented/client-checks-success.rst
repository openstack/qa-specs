..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================
Move success response checking to tempest clients
=================================================

https://blueprints.launchpad.net/tempest/+spec/client-checks-success

To ensure API stability, api calls from tempest should check that the response
code in the success case is the expected value. Right now these checks are done
by the callers of the apis and in an inconsistent way. There is no policy or
guideline for when to check. It would be better if the response code was
always checked and api callers did not have to worry about this.

Problem description
===================

It has been the policy that tests of an api should validate the response code.
Failure is handled by clients raising exceptions but the caller was supposed
to check the response on success. But many api tests also call other apis as
part of preparing for the actual test calls. In some cases we check the
response for those and in other cases we don't, but really all calls should
be checked. Expecting code that calls apis to handle this is unnecessary and
error prone.

The new code added to validate nova apis with schemas does the checking in
the client. We should move all checking to the client except where multiple
success return codes are possible.

There are two methods on RestClient that handle this:

validate_response(cls, schema, resp, body)
  This is used with the new schema validation.

expected_success(self, expected_code, read_code)
  This was an earlier attempt to rationalize response checking but is only used
  by the image clients.


Proposed change
===============

Move all response checking to the clients. Use validate_response to check the
success code, adding schemas for apis that do not have them yet.
Then we can remove all checks from the test code
itself except where there are multiple possible 2xx responses. In that case
the caller should also check for a specific value.


Alternatives
------------

Continue to clutter the test code with an inconsistent set of checks that will
be required after every api call.

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  David Kranz <dkranz@redhat.com>

Milestones
----------
Target Milestone for completion:

- Juno

Work Items
----------
- Change all api calls in the tempest clients to check response code, adding
  new schemas as necessary.
- Remove all checking for 2xx from tests unless a specific value is expected
  out of several that could be returned by the api.

