=====================
 QA Specs Repository
=====================

This is a git repository for doing design review on QA enhancements as
part of the OpenStack program. This provides an ability to ensure that
everyone has signed off on the approach to solving a problem early
on.

Repository Structure
====================
The expected structure of the respository is as follows::

  specs/
      implemented/


Expected Work Flow
==================

1. Create a blueprint stub in ``tempest`` blueprint repository
2. Propose review to qa-specs repository (ensure bp:blueprint_name is
   in the commit message
3. Link ``Read the full specification`` to the gerrit address of the spec
4. Bring forward the proposed item to the openstack-qa meeting for summary
5. Review happens on proposal by qa-core members, and others
6. Iterate until review is Approved or Rejected

Once a Review is Approved...

1. Update blueprint, Copy summary text of blueprint to there
2. Link ``Read the full specification`` to the git address of the spec
3. Profit!


Revisiting Specs
================
We don't always get everything right the first time. If we realize we
need to revisit a specification because something changed, either we
now know more, or a new idea came in which we should embrace, we'll
manage this by proposing an update to the spec in question.

Learn as we go
==============
This is a new way of attempting things, so we're going to be low in
process to begin with to figure out where we go from here. Expect some
early flexibility in evolving this effort over time.
