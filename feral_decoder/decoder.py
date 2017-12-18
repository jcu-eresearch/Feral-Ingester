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

import datetime
from bitstring import BitArray, BitStream
import base64


def unpack_record(stream):
    result = {
        "ts": stream.read(32).intle,
        "pressure": float(stream.read(32).intle)/10000,
        "temperature": float(stream.read(32).intle)/100,
        "humidity": float(stream.read(32).intle)/1000,
        "lux": stream.read(32).intle/1000,
        "battery": float(stream.read(32).intle)/1000,
        "flags":{
            "padding": stream.read(6).int,
            "bme_ok": stream.read(1).bool,
            "lux_found": stream.read(1).bool,
        }
    }

    result["time"] = datetime.datetime.fromtimestamp(result["ts"])

    return result

def unpack_data(data):
    bin_data = base64.b64decode(data)
    data = BitStream(bytes=bin_data)

    record_size = data.read(8).intle
    record_count = data.read(8).intle
    result = []
    for i in range(record_count):
        result.append(unpack_record(data.read(record_size * 8)))
    return {"record_size":record_size, "record_count": record_count, "results": result}
