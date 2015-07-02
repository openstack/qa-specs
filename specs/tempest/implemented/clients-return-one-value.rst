..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Clients Return One Value
========================

https://blueprints.launchpad.net/tempest/+spec/clients-return-one-value

Currently tempest clients return a response code and body. Since we moved
response checking to clients, almost all callers of the clients ignore the
response code: :doc:`client-checks-success`. It would be
much cleaner if clients returned a single response
object that was the body, with a property to get the response status and
headers if needed.


Proposed change
===============

Introduce a new ResponseBody class in rest_client::

    class ResponseBody(dict):
        """
        Class that wraps an http response and body into a single value.
        Callers that receive this object will normally use it as a dict but
        can extract the response if needed.
        """
        def __init__(self, response, body=None):
            body_data = body or {}
            self.update(body_data)
            self.response = response

        def __str__(self):
            body = super.__str__(self)
            return "request: %s\nBody: %s" % (self.response, body)

Change all the tempest clients to return this object and change all the calls
to the clients, getting rid of the current '_' for the response.


Alternatives
------------

In theory this could be done in the rest client itself, rather than in each
service client, but that would imply much more regularity of the service
clients than we have. Also, it would then be necessary to change everything
at once because all the tests currently expect two values.

The primary consideration is to not return unused values almost all the time.
Another alternative would be to have an argument to the rest client methods
that says whether a response should also be returned. I think the current
proposal is cleaner.

Implementation
==============

Unfortunately each client class must be changed lockstep with all calls to
that client.

Assignee(s)
-----------
Primary assignees:
  David Kranz <dkranz@redhat.com>

Other contributors:
  Yair Fried <yfried@redhat.com>

Milestones
----------
Target Milestone for completion:

- kilo-1

Work Items (for each service client)
------------------------------------
- Change all methods in the tempest clients to return ResponseBody.
- Change all calls to clients to receive just the response body and check
  the response code if necessary.

