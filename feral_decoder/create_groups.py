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

    logger = logging.getLogger("Groups")

    parents = {}

    for sensor_id in SensorConfig.sensors:

        sensor_prefix = SensorConfig.sensors[sensor_id][kc.prefix]
        parent_group = sensor_prefix



        sensor_id_prefix = "%s.%s"%(sensor_prefix, sensor_id)
        group = sensor_id_prefix

        api_instance = sensor_cloud.DefaultApi()



        if parent_group not in parents:
            data = api_instance.groups_get(id=parent_group)
            if data.embedded is None:
                body = sensor_cloud.GroupPost(id=parent_group, name=parent_group.capitalize(), organisationid=SensorCloudConfig.organisation)
                api_instance.groups_id_put(parent_group, body)
                logger.info("Created Parent Group: %s"%parent_group.capitalize())

            parents[parent_group] = True

        data = api_instance.groups_get(id=group)


        if data.embedded is None:
            body = sensor_cloud.GroupPost(id=group, name=sensor_id, organisationid=SensorCloudConfig.organisation, groupids=[
                parent_group
            ])
            api_instance.groups_id_put(group, body)
            logger.info("Created Group: %s"%group)
        else:
            logger.info("Location: %s already exists, skipping."%group)

def main():
    init("feral_decoder_create_groups creates the sensor-cloud.io groups to attach the data streams and locations to.")
    run()

if __name__ == "__main__":
    main()