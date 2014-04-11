#!/usr/bin/python

# Copyright 2014 Samsung Electronics
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import fileinput
import os
import re
import sys

ERRORS = 0


def error(msg):
    global ERRORS
    ERRORS += 1
    print(msg)


def get_options():
    parser = argparse.ArgumentParser(
        description='RST sanity checker')
    parser.add_argument('-d', '--dir', help="Specifications Directory",
                        default="specs")
    return parser.parse_args()


def find_rst_files(dirname):
    files = []
    for root, dirnames, filenames in os.walk(dirname):
        for f in filenames:
            if f != ".keep":
                files.append("%s/%s" % (root, f))
    return files


def ensure_files_end_in_rst(files):
    for fname in files:
        if not re.search("\.rst$", fname):
            error("E001: Filename %s does not end in .rst" % fname)


def ensure_lt80(files):
    for fname in files:
        for line in fileinput.input(fname):
            if len(line) > 80:
                i = fileinput.lineno()
                error("E002: File %s:%s exceeds 80 columns" % (fname, i))


def main():
    opts = get_options()
    files = find_rst_files(opts.dir)
    ensure_files_end_in_rst(files)
    ensure_lt80(files)
    if ERRORS > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
