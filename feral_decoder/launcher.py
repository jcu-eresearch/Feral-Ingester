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

from feral_decoder.commandline import init
import sys

_as = "args"
_kw = "kwargs"

logger = logging.getLogger("Launcher")

def upload():
    sys.argv[0] = "feral_decoder_upload"
    args = init("feral_decoder_upload uploads any cache entries and then archives the cache entry.",
         args=[
             {
                 _as:["--no_decache"],
                 _kw:{"action":"store_true", "default": False, "dest": "no_decache", "help":"This will process the cache"+
                      "file normally, but will not remove it from the cache. Normally used for testing."}
             },
             {
                 _as:["--ignore_ts"],
                 _kw:{"action":"store_true", "default":False, "dest":"ignore_ts", "help":"Ignore the nodes timestamp file."}
             }
         ])
    from feral_decoder.upload import Uploader
    logger.log(logging.TRACE, "Args: %s"%args)
    Uploader(args).run()

def unpack():
    init("feral_json_unpack reads in a newline-delimited JSON file and unpacks it into the cache directory.")


def streams():
    sys.argv[0] = "feral_decoder_create_streams"
    from feral_decoder.create_streams import main
    main()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Nothing to see..."
    else:
        cmd = [sys.argv[0]]
        fn = sys.argv[1]
        opts = sys.argv[2:]
        sys.argv = cmd + opts

        globals()[fn]()