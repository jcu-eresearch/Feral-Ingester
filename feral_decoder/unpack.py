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

import json
import logging
from pprint import pprint

import os

from feral_decoder.commandline import init


def unpack():

    args = init("feral_json_unpack reads in a newline-delimited JSON file and unpacks it into the cache directory.",
         args=[
                 {
                    "args":["file"],
                    "kwargs":
                    {
                      "help": "The newline terminated JSON file to unpack"
                    }
                  },
                {
                    "args":["prefix"],
                    "kwargs":
                    {
                      "help": "the prefix to add to the cache entries"
                    }
                  },
         ]
        )
    from FeralDecoder_Paths import cache_dir
    logger = logging.getLogger("Unpacker")
    with open(args.file, "r") as din:
        while True:
            data = din.readline().strip()
            if len(data) > 0:
                dat = json.loads(data)
                fn = "%s%s.json"%(args.prefix, dat["rxInfo"][0]["time"].replace(":", "_"))
                cache_fn = os.path.join(cache_dir, fn)
                if not os.path.exists(cache_fn):
                    with open(cache_fn, "w") as dout:
                        json.dump(dat, dout)
                        logger.log(logging.TRACE, "Created cache file: %s"%cache_fn)
                else:
                    logger.log(logging.TRACE, "Skipped file: %s"%cache_fn)
            else:
                break



if __name__ == "__main__":
    unpack()