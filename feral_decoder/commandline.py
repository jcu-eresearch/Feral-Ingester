# FeralDecoder decodes data from the Environmental Sensor Nodes and Uploads it to the Sensor Cloud.
# Copyright (C) 2017  NigelB
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import logging
from argparse import ArgumentParser

import os

import sys

from feral_decoder.utils import ensure_paths


def init(description, args=None):
    argParse = ArgumentParser(description=description)
    argParse.add_argument("--config-dir", metavar="<config_dir>", dest="config_dir", default="config", action="store", help="The location of the config directory, default: config")
    argParse.add_argument("-v", "--verbosity", default=0, action="count", help="increase output verbosity")
    if args is not None:
        for arg in args:
            if "args" in arg and "kwargs" in arg:
                argParse.add_argument(*arg["args"], **arg["kwargs"])
            elif "args" in arg and "kwargs" not in arg:
                argParse.add_argument(*arg["args"])
            elif "args" not in arg and "kwargs" in arg:
                argParse.add_argument(**arg["kwargs"])


    args = argParse.parse_args()

    args.config_dir = os.path.abspath(args.config_dir)
    sys.path.append(args.config_dir)

    import FeralDecoder_Paths as Paths
    import FeralDecoder_SensorCloudConfig as SensorCloudConfig
    import FeralDecoder_Config as FeralConfig

    logging.TRACE = 5

    levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        4: logging.TRACE,
        5: logging.NOTSET
    }
    if args.verbosity > 5:
        args.verbosity = 5
    logging.basicConfig(format=FeralConfig.LOGGING_FORMAT,level=levels[args.verbosity])
    logging.addLevelName(logging.TRACE, "TRACE")
    ensure_paths()
    return args