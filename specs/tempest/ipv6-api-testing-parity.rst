..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

============================================
 Improve IPv6 API testing parity in tempest
============================================

https://blueprints.launchpad.net/tempest/+spec/ipv6-api-testing-parity

Current tempest API tests do not validate IPv6 to the same extent
as IPv4.

Problem description
===================

IPv6 is evolving in Neutron and the community is working hard to add the
neccessary support. However, the current API tests in tempest do not
validate IPv6 to the same extent as IPv4.

Also, Neutron now supports two extended attributes for IPv6 subnets
(ipv6-ra-mode and ipv6-address-mode) in the Juno timeframe.

This BP would add the necessary IPv6 tests in tempest.

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

Along with test cases related to subnet attributes, this BP would implement
new test cases in tempest to bring in parity between IPv4 and IPv6 tests.
To start with, new tests would be required in Neutron for
Ports/Security-Groups/Subnets/FWaaS api tests.

The following etherpad link would be used to track all the test cases.

https://etherpad.openstack.org/p/ipv6-api-testing-parity

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
  Juno release

Work Items
----------
The work items include IPv6 API test cases like
 - Subnet test cases.
 - Port operations including Bulk operations.
 - Security Groups and Rules - https://review.openstack.org/#/c/94130
 - FWaaS test cases.
 - Validating if Neutron calculates and assigns IPv6 addresses properly
   (i.e., based on EUI-64 where applicable).

Any new test cases related to the same topic would be tracked using the following
external etherpad link.
https://etherpad.openstack.org/p/ipv6-api-testing-parity

Dependencies
============

- Neutron IPv6 Subnet attributes (ipv6-ra-mode and ipv6-address-mode) are added
  in the Juno+ timeframe for selecting the type of IPv6 network.
  Hence, a config flag needs to be added to tempest to skip the tests while
  running on icehouse jobs.  The required changes in tempest would be addressed
  as part of BP ipv6-subnet-attributes.rst.
  https://blueprints.launchpad.net/tempest/+spec/ipv6-subnet-attributes

  Similarly, devstack needs to populate the flag during the setup. The required
  changes in devstack would be addressed as part of the following BP.
  https://blueprints.launchpad.net/devstack/+spec/tempest-ipv6-attributes-support

- Neutron: Support Router Advertisement Daemon (radvd) for IPv6
  https://review.openstack.org/#/c/101306/

- Neutron: Support for IPv6 dhcpv6-stateless and dhcpv6-statefull modes in Neutron.
  https://review.openstack.org/#/c/102411/
