=====================
 QA Specs Repository
=====================

This is a git repository for doing design review on QA enhancements as
part of the OpenStack program. This provides an ability to ensure that
everyone has signed off on the approach to solving a problem early
on.

Repository Structure
====================
The expected structure of the repository is as follows::

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

Specs for new tests
===================
If you're writing a new spec to improve the testing coverage in Tempest the
requirements for what is included in the specification are slightly less
stringent and different from other proposals. This is because blueprints for
more tests are more about tracking the effort in a single place and assigning
a unified topic in gerrit for ease of review, it's less about the
implementation details. Blueprints/specifications for new tests should only
ever be opened for overarching development efforts. For example there should
only ever only need to be a single blueprint for adding tests for a project.

Most of these efforts require a method to track the work items outside of
launchpad. Both etherpad and google docs have been used very successfully for
this. The goal is to list out all the tests that need to be written and allow
people to mark that they intend to work on a specific test. This prevents
duplication of effort as well as provide overall status tracking. An external
tool like etherpad or google docs is better at this because it allows
concurrent use and more dynamic editing than launchpad.

The only details required in the proposed change section for a spec about new
tests are:

* What is being tested and the scope of what will be covered by the blueprint
* What external tool is being used to track the development.

  * If no external tracking is being used just explain why.
