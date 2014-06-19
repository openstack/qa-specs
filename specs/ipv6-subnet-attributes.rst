..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

=================================
IPv6 Subnet Attribute API tests
=================================

https://blueprints.launchpad.net/tempest/+spec/ipv6-subnet-attributes

Add IPv6 API tests for validating Neutron Subnet Extended attributes.

Problem description
===================

Support for IPv6 is evolving in OpenStack. Neutron now supports two
extended attributes for IPv6 subnets (ipv6-ra-mode and ipv6-address-mode)
in the Juno timeframe.

This BP would add the necessary IPv6 API tests in tempest.

Proposed change
===============

Neutron BP: IPv6 Subnet attributes are implemented as part of the following BP
- https://blueprints.launchpad.net/neutron/+spec/ipv6-two-attributes

The possible values for the subnet attributes are as follows.
 - ipv6-ra-mode {dhcpv6-stateful, dhcpv6-stateless, slaac}
 - ipv6-address-mode {dhcpv6-stateful, dhcpv6-stateless, slaac}

The two IPv6 attributes provide flexibility to choose the type of IPv6 network.
However, not all combinations of the two attributes are valid. Valid and
invalid combinations are captured in the Neutron ipv6-provider-nets-slaac.rst
blueprint and also at the following link.
- https://www.dropbox.com/s/9bojvv9vywsz8sd/IPv6%20Two%20Modes%20v3.0.pdf

This BP would add new API tests in tempest to validate both positive and
negative tests.

Neutron IPv6 Subnet attributes are supported in Juno+ releases.
Hence, a config flag would be added to tempest to skip the tests while
running against icehouse jobs like check-tempest-dsvm-neutron-icehouse.

Alternatives
------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
 - Sridhar Gaddam <sridhargaddam@enovance.com>
 - Sean M. Collins <sean_collins2@cable.comcast.com>


Milestones
----------

Target Milestone for completion:
  Juno-2

Work Items
----------
The work items include adding IPv6 API tests for

- Positive test cases.
- Negative tests.
- Adding a config flag support to tempest to skip the tests while running on icehouse jobs (https://review.openstack.org/#/c/93502)

Dependencies
============

- Devstack needs to populate the config flag during the setup, so that
  tempest could decide whether to run the tests or skip them.
  The required changes in Devstack would be done as part of the following BP.
  https://blueprints.launchpad.net/devstack/+spec/tempest-ipv6-attributes-support
