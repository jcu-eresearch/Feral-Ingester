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
from argparse import Namespace

import sensor_cloud

from feral_decoder.commandline import init
from feral_decoder.constants import KeyConstants as kc


def add_streams():
    import FeralDecoder_SensorCloudConfig as SensorCloudConfig
    import FeralDecoder_Sensors as SensorConfig

    logger = logging.getLogger("Streams")

    for sensor_id in SensorConfig.sensors:

        sensor_prefix = SensorConfig.sensors[sensor_id][kc.prefix]

        sensor_id_prefix = "%s.%s"%(sensor_prefix, sensor_id)
        location = sensor_id_prefix
        group = sensor_prefix

        api_instance = sensor_cloud.DefaultApi()

        # If the group does not exist, create it.
        data = api_instance.groups_get(id=sensor_id_prefix)
        if data.embedded is None:
            logger.info("Creating group "+sensor_id_prefix)
            body = sensor_cloud.GroupPost(
                id=sensor_id_prefix,
                name=sensor_id,
                organisationid=SensorCloudConfig.organisation,
                description=sensor_id_prefix,
                groupids=[group]
            )
            api_instance.groups_id_put(sensor_id_prefix, body)
        else:
            logger.info("Group: %s already exists, skipping."%sensor_id_prefix)

        for stream in SensorCloudConfig.streams:
            stream_id = sensor_id_prefix+"."+stream

            stream_data = Namespace(**SensorCloudConfig.streams[stream])

            # If stream does not exist, create it
            data = api_instance.streams_get(id=stream_id)
            if data.embedded is None:
                body = sensor_cloud.StreamPost(stream_id,

                                               locationid=location,
                                               organisationid=stream_data.organisation,
                                               sample_period=stream_data.samplePeriod,
                                               reporting_period=stream_data.reportingPeriod,
                                               groupids=[group, sensor_id_prefix],
                                               stream_metadata=sensor_cloud.StreamMetadata(
                                                   type=".ScalarStreamMetaData",
                                                   observed_property=stream_data.observedProperty,
                                                   unit_of_measure=stream_data.unitOfMeasure,
                                                   interpolation_type=stream_data.interpolationType,
                                                ),
                                               resulttype="scalarvalue"
                                            )
                api_instance.streams_id_put(stream_id, body)
                logger.info("Created stream: %s"%stream_id)

            else:
                logger.info("Stream: %s already exists, skipping."%stream_id)

def remove_streams():
    import FeralDecoder_SensorCloudConfig as SensorCloudConfig
    import FeralDecoder_Sensors as SensorConfig

    logger = logging.getLogger("Streams")

    for sensor_id in SensorConfig.sensors:
        sensor_prefix = SensorConfig.sensors[sensor_id][kc.prefix]

        sensor_id_prefix = "%s.%s"%(sensor_prefix, sensor_id)
        location = sensor_id_prefix
        group = sensor_prefix

        api_instance = sensor_cloud.DefaultApi()

        for stream in SensorCloudConfig.streams:
            stream_id = sensor_id_prefix+"."+stream
            try:
                api_instance.observations_delete(stream_id)
                api_instance.streams_id_delete(stream_id)
                logger.info("Deleted stream: %s"%stream_id)
            except:
                logger.exception("Error removeing stream: %s"%stream_id)
                pass

        api_instance.groups_id_delete(sensor_id_prefix)

def main():
    args = init("feral_decoder_create_streams create all of the sata streams in the sensor cloud.", args=[
        {
            "args":["-r", "--remove"],
            "kwargs":
                {
                    "action":'store_true',
                    "default": False,
                    "help": "Remove the streams instead of creating them."
                }
        },
    ])

    if args.remove:
        remove_streams()
    else:
        add_streams()


if __name__ == "__main__":
    main()