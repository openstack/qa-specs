..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Data driven testing for Tempest
===============================

https://blueprints.launchpad.net/tempest/+spec/tempest-ddt


Add support for data driven testing within Tempest.

Problem Description
===================

Currently we see tests with for-loop that iterate through different
data set. This can be problematic for debugging and in general
for test separation (See [1] for some samples).


Proposed Change
===============

Using the ddt framework [2] to extract the data out of the tests.
DDT will dynamically create tests out of the given data set.
The DDT framework is already heavily used by unit tests within
the projects.

Example
-------
The test before ddt::

   icmp_type_codes = [(3, 2), (3, 0), (8, 0), (0, 0), (11, None)]
        for icmp_type, icmp_code in icmp_type_codes:
            self._create_verify_security_group_rule(sg_id, direction,
                                                    self.ethertype, protocol,
                                                    icmp_type, icmp_code)

Instead of iterating through a set of data the corresponding ddt code would
look like::

    @ddt.data((3, 2), (3, 0), (8, 0), (0, 0), (11, None))
    def test_create_security_group_rule_with_icmp_type_code(self, type_codes):
        self._create_verify_security_group_rule(sg_id, direction,
                                                self.ethertype, protocol,
                                                type_codes[0], type_codes[1])

Performance
-----------

Any generated test will rerun setUp() and tearDown(). Code on class level
should work without any change (and no rerun at all). In Tempest the resource
setup is usually done within class methods which won't effect the performance.


Idempotent_id and refstack
--------------------------

Since refstack should handle generated tests under the same id, it should
be fine to use the idempotent decorator to uniquely identify the test group.

Implementation
==============

Assignee(s)
-----------

Primary assignees:
  Marc Koderer

Milestones
----------

Target Milestone for completion:
  mitaka-3

Work Items
----------

* Implement idempotent_id functionality
* Port tests

Dependencies
============

None.

References
==========

1. https://review.openstack.org/#/c/223953/
2. https://pypi.python.org/pypi/ddt

.. _config_tempest.py: https://github.com/redhat-openstack/tempest/blob/master/tools/config_tempest.py
