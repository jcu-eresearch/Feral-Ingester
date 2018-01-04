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

import sensor_cloud

from feral_decoder.commandline import init
from feral_decoder.constants import KeyConstants as kc


def run():
    import FeralDecoder_SensorCloudConfig as SensorCloudConfig
    import FeralDecoder_Sensors as SensorConfig

    logger = logging.getLogger("Locations")


    for sensor_id in SensorConfig.sensors:

        sensor_prefix = SensorConfig.sensors[sensor_id][kc.prefix]
        group = sensor_prefix

        sensor_id_prefix = "%s.%s"%(sensor_prefix, sensor_id)
        location = sensor_id_prefix

        api_instance = sensor_cloud.DefaultApi()

        data = api_instance.locations_get(id=location)

        if data.embedded is None:

            body = sensor_cloud.LocationPost(
                id=location,
                organisationid=SensorCloudConfig.organisation,
                description=location,
                groupids=[group],
                geo_json=
                {
                    "type": "Point",
                    "coordinates": [0,0,0]
                }
            )


            api_instance.locations_id_put(location, body)
            logger.info("Created location: %s"%location)
        else:
            logger.info("Location: %s already exists, skipping."%location)

def main():
    init("feral_decoder_create_locations creates the sensor-cloud.io locations to attach the data streams to.")
    run()

if __name__ == "__main__":
    main()