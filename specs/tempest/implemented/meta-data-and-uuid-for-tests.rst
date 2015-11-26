..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

=============================
 meta data and uuid for tests
=============================

https://blueprints.launchpad.net/tempest/+spec/meta

The purpose of this spec is to define a standard for attaching meta data such
as Universally Unique Identifiers (UUIDs) to tests that are to be used by
tempest. This specification should be enforced both for tests that are to live
in the tempest repository as well as tests that will eventually reside within
their own repositories.

Problem description
===================

While there are many reasons to want meta data attached to tests. One of
the complaints that led to this specification is the lack of a unique
identifier for tests. If you cannot track a specific test over time, long term
data carries less meaning and progress is more complicated to track.

Proposed change
===============

Each test will have a decorator that will accept a required arguments
containing a uuid and meta as kwargs. This open ended approach for meta data
should insure flexibility for the future. Such as allow Defcore to directly
tag tests with capability data moving forward.

This change will also require the development of a tool for inserting the
decorators with uuid content for all the existing tests. This tool can also be
used as a uniqueness validation and missing uuid checker in the gate.

Alternatives
------------

It was also suggest that meta data can be written into parseable doc strings.

Implementation
==============

This change will require the following components be developed.

- uniqueness tester / detect missing meta / insert meta

This tool will check for unique UUID decorators for all test_* methods in
test_*py files. This is done in a single pass to build a list of undecorated
tests, which can the be used as a gate check in the qa pipeline. From
this list another tool will generate unique UUID metadata and insert it
into all undecorated tests.

Example::

    meta_decorator_check.py /path/to/test(s)

- scans the directory/files in path, parses for methods missing the
  decorator or finds tests with duplicate UUIDs.

With the same tool you can add the --insert-missing arg. This will generate
and insert the missing decorators.

Example::

    meta_decorator_check.py --insert-missing /path/to/test(s)

- decorator

The UUID and meta decorator format will be as follows::

  '@test.meta(uuid='12345678-1234-5678-1234-567812345678',
              otherdata='another value')

For sphinx autodoc generation it will append the following to the doc string::

    uuid: '12345678-1234-5678-1234-567812345678'
    otherdata :'another value'

To insure the data is passed to subunit output we add the testtools attr::

    uuid='12345678-1234-5678-1234-567812345678'
    otherdata='another value'

- hacking

New hacking will need to be added to insure that a decorator is set for all
tests. First a new rule to be added to tempest/hacking/checks.py.

    all_tests_need_uuid_metadata

    """Check that a test has unique UUID metadata

        All tests should have a unique UUID identifier in the metadata
        of the form:
        '@test.meta(uuid='12345678-1234-5678-1234-567812345678')
        to give a stable point of reference.

         T108"""

The Tempest coding guide will be updated to reflect the new hacking
rule.

Assignee(s)
-----------

Primary assignee:
    David Lenwell (davidlenwell, dlenwell@gmail.com)
    Chris Hoge (hogepodge, chris@openstack.org)
    Sergey Slipushenko (automated test tagging)

Milestones
----------

Target Milestone for completion:
  K-3

Work Items
----------

- creation of decorator
- creation of the generate_meta / uniqueness testing tool
- use the generate_meta tool to generate default meta data for all existing
  tests.
- implementation of gate tests
- update tempest coding guide with new hacking rule

Dependencies
============

- No known external dependencies.
