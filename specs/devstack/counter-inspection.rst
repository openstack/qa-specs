..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

..

========================================================
Inspect counters for data collection and gating purposes
========================================================

Problem description
===================

OpenStack projects vary on their impact to the underlying infrastructure
that they rely on greatly. This is hard to measure without going to a
full scale deployment, but we should be able to measure the impact by
inspecting counters already maintained by the system.

Proposed change
===============

* Create a new "OpenStack QA Tools" repository to house small tools
  written in python for purposes such as this.

  * Create a tool, `os-collect-counters`, which collects relevant counters
    from any backends it can reach using its own configuration and
    outputs a JSON mapping with all counters. Includes ability to delta
    with a previous run to allow showing impact on the counters for a
    given time window.

    * Initial counters will be at a minimum a set of MySQL counters (such
      as Innodb_bytes_written) and published messages from the RabbitMQ
      management interface, summarized by scope that can be inferred
      from each queue name.

* Leverage existing subunit/statsd/graphite infrastructure to record results of
  several tests in the devstack gate.

  * For each run, the JSON from `os-collect-counters` will be added as an
    attachment to the subunit stream.

  * The counters in the attachment will be fed into statsd/graphite to
    allow establishing trends.

    * This will be facilitated by adding attachment storage plugins to
      subunit2sql. The plugin used for OpenStack gate jobs will be
      specific to OpenStack's infrastructure and look for the specifically
      named attachment to push into statsd/graphite.

* Monitor counters for stable indicators and identify the best predictors of
  problems.

  * Once stable counters are identified, create an upper bounds for
    these counters to help prevent new changes in the system from
    accidentally introducing an inordinate amount of cost into the tested
    code paths.

    Since there are daunting social issues around failing gate tests
    on global collisions, warnings and bugs about said warnings are
    likely the only reasonable outcome we can achieve. It will take a
    considerable amount of community agreement to make these limits hard.


Implementation
==============

A new python repo, `os-performance-tools`_, has already been created, and
will be maintained for the purposes of extracting and pushing counters
into statsd/graphite. This will include a subunit2sql attachments plugin
and code to output the counters as a subunit attachment.

.. _`os-performance-tools`: https://review.openstack.org/#/c/244428/

Assignee(s)
-----------

Primary assignee:

* Clint Byrum <clint@fewbar.com>

Milestones
----------

Target Milestone for completion:
  Mitaka-2

Work Items
----------

* Create tools to emit counters from a running installation
* Modify devstack gate job output to include counters
* Add subunit2sql attachment plugin to subunit2sql workers
  to push counters to infra graphite
* Analyze data for stable counters and useful trends
* Add upper bounds check to devstack gate

Dependencies
============

References
==========

