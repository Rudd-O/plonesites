#!/usr/bin/env python

import os
import sys

def main(adjustedzope2cmd, extra_cmdline_args):
    embedded = os.path.join(os.path.dirname(__file__), "upgrader_embedded.py")
    adjustedzope2cmd.options.program += ["upgrader"]
    adjustedzope2cmd.options.args = ['-c', embedded] + adjustedzope2cmd.options.args[1:]
    ret = adjustedzope2cmd.do_run('')
    sys.exit(ret)
