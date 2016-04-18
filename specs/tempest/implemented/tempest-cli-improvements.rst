..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.
 http://creativecommons.org/licenses/by/3.0/legalcode

========================
Tempest CLI Improvements
========================

https://blueprints.launchpad.net/tempest/+spec/tempest-cli-improvements


Make the Tempest CLI design more consistent and intuitive by utilizing the
setuptools and cliff python libraries.

Problem Description
===================

There are currently some Tempest CLI endpoints created when tempest is
installed but there is no consistency in the console command names or function.

Proposed Change
===============

Create an intuitive set of CLI endpoints for Tempest.

Add cliff Support to Tempest
----------------------------
Cliff enables creation of console scripts by using a clean class
structure for building applications and commands.

See: https://pypi.python.org/pypi/cliff/

For example setup.cfg would have::

    [entry_points]
    console_scripts =
        tempest = tempest.cmd.main:main
    tempest.cm =
        cleanup = tempest.cmd.main:CleanupCmd
        # ...

and tempest.cmd.main would look something like::

   from cliff.app import App
   from cliff.commandmanager import CommandManager
   from cliff.command import Command
   # ...

   class Main(App):

       log = logging.getLogger(__name__)

       def __init__(self):
           super(Main, self).__init__(
               description='Tempest cli application',
               version='0.1',
               command_manager=CommandManager('tempest.cm'))

       def initialize_app(self, argv):
           self.log.info('tempest initialize_app')

       def prepare_to_run_command(self, cmd):
           self.log.info('prepare_to_run_command %s', cmd.__class__.__name__)

       def clean_up(self, cmd, result, err):
           self.log.info('Tempest app clean_up %s', cmd.__class__.__name__)
           if err:
               self.log.info('Tempest error: %s', err)

   # A sample command implementation would look like:

   class CleanupCmd(Command):
       log = logging.getLogger(__name__)

       def get_description(self):
           description = "Utility for cleaning up ..."
           return description

       def get_parser(self, prog_name):
           parser = super(CleanupCmd, self).get_parser(prog_name)
           parser.add_argument('--init-saved-state', action="store_true",
                               dest='init_saved_state', default=False,
                               help="Init help...")
           # More args ...
           return parser

       def take_action(self, parsed_args):
           cu = cleanup.Cleanup(parsed_args)
           cu.run()
           self.log.info("Cleanup Done!")

   The end result, after running 'setup.py install', this command is valid::

       tempest cleanup --init-saved-state


Proposed command structure
--------------------------
::

    tempest cleanup
        arguments:
            --dry-run
            --init-saved-state
            --delete-tempest-conf-objects

    tempest create-config
        arguments:
            TBD

    tempest verify-config
        arguments:
            --update, -u
            --output, -o
            --replace-ext, -r

    tempest javelin
            --mode, -m
            --resources, -r
            --devstack-base, -d
            --config-file, -c
            --os-username
            --os-password
            --os-tenant-name

Implementation
==============

Assignee(s)
-----------

Primary assignees:
  David Paterson

Milestones
----------

Target Milestone for completion:
  Liberty-1

Work Items
----------

* Add support for Cliff.
* Define endpoints and commands in setup.cfg.
* Create stubbed tempest.cmd.main module providing main cliff-based CLI facade.
* Refactor and migrate existing commands. For each command a new class that extends cliff.command.Command will need to be implemented:

  * javelin2
  * run-tempest-stress
  * tempest-cleanup
  * verify-tempest-config

* Migrate config_tempest.py_ from downstream repository and integrate with cliff.


Dependencies
============

* cliff - adds framework for creating CLI applications and commands.

References
==========
* https://etherpad.openstack.org/p/tempest-cli
* https://etherpad.openstack.org/p/YVR-QA-Tempest-CLI
* https://etherpad.openstack.org/p/YVR-QA-Liberty-Priorities
* http://docs.openstack.org/developer/cliff
* https://github.com/redhat-openstack/tempest/blob/master/tools/config_tempest.py

.. _config_tempest.py: https://github.com/redhat-openstack/tempest/blob/master/tools/config_tempest.py
