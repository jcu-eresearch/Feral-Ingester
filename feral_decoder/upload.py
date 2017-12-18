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

import glob
import gzip
import json
import logging

import os
import traceback
from pprint import pprint

import sys

import datetime
import iso8601
import time

import sensor_cloud
import shutil
from sensor_cloud import UnivariateResult

from feral_decoder.decoder import unpack_data
from feral_decoder.constants import KeyConstants as kc, FeralCacheRollType

from feral_decoder.constants import FeralConstants as fc

try:
    from FeralDecoder_Paths import cache_dir, archive_dir, node_dir
    from FeralDecoder_Sensors import sensors
    import FeralDecoder_SensorCloudConfig
    from FeralDecoder_Sensors import sensors
    import FeralDecoder_Config as FeralConfig
except:
    traceback.print_exc(file=sys.stderr)
    sys.exit(2)



class Uploader:
    logger = logging.getLogger("Uploader")

    def __init__(self):
        self.archive_fn = None

    def adjust_time(self, unpacked, offset):
        for result in unpacked['results']:
            result['ts'] += offset
            s = datetime.datetime.fromtimestamp(result['ts'])
            t = s.timetuple()
            d = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, 0, iso8601.UTC)
            result['time'] = d
            result['time_'] = d.strftime('%Y-%m-%dT%H:%M:%S.000000Z')


    def post_observation(self, api_instance, id, value, sample_time):

        result = [UnivariateResult(t=sample_time, v={"v": str(value)})]
        body = sensor_cloud.ObservationsPost(results=result)  # ObservationsPost |
        api_response = api_instance.observations_post(id, body)
        self.logger.log(logging.TRACE, "Result: %s" % api_response)


    def upload(self, entry, unpacked, count):

        node_id = entry["devEUI"]
        sensor_prefix = "%s.%s" % (sensors[node_id][kc.prefix], node_id)

        api_instance = sensor_cloud.DefaultApi()
        results = unpacked['results'][:count]

        for result in results:
            self.post_observation(api_instance, "%s.%s" % (sensor_prefix, fc.Temperature), result['temperature'], result['time_'])
            self.post_observation(api_instance, "%s.%s" % (sensor_prefix, fc.Humidity), result['humidity'], result['time_'])
            self.post_observation(api_instance, "%s.%s" % (sensor_prefix, fc.Pressure), result['pressure'], result['time_'])
            self.post_observation(api_instance, "%s.%s" % (sensor_prefix, fc.Lux), result['lux'], result['time_'])
            self.post_observation(api_instance, "%s.%s" % (sensor_prefix, fc.BatteryVoltage), result['battery'], result['time_'])

    def calculate_archive_file(self, type_name):
        current = datetime.datetime.now()

        if self.archive_fn is None:
            if FeralConfig.cache_period_type == FeralCacheRollType.Monthly:
                self.archive_fn = "%s-%s.json" % (type_name, current.strftime("%Y-%m"))
            elif FeralConfig.cache_period_type == FeralCacheRollType.Period:
                time.mktime(current.timetuple())

            self.archive_fn = os.path.join(archive_dir, self.archive_fn)

    def cache(self, entry, type_name):
        try:
            self.calculate_archive_file(type_name)
            with open(self.archive_fn, "a") as do:
                do.write(json.dumps(entry))
                do.write(os.linesep)
            return True
        except:
            pass

        return False

    def cleanup(self):
        self.cleanup_type(kc.uplink)
        self.cleanup_type(kc.unknown)

    def cleanup_type(self, type):
        self.calculate_archive_file(type)

        for archive_file in glob.glob1(archive_dir, "*.json"):
            fn = os.path.abspath(os.path.join(archive_dir, archive_file))
            if fn != os.path.abspath(self.archive_fn):
                self.logger.info("Compressing old archive: %s"%fn)
                with open(fn, 'rb') as f_in, gzip.open(fn+'.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

    def run(self):

        cache_entries = glob.glob1(cache_dir, "uplink-*")
        cache_entries.sort()

        for cache_entry in cache_entries:
            cache_entry_fn = os.path.join(cache_dir, cache_entry)
            entry = None
            with open(cache_entry_fn, "r") as din:
                entry = json.load(din)
                node_time_file = os.path.join(node_dir, entry["devEUI"])

            # Ignore the entry if the node id is not in the configured list
            if entry["devEUI"] not in sensors:
                self.logger.error("Node: %s not in FeralDecoder_Sensors.sensors, ignoring." % entry["devEUI"])
                if self.cache(entry, kc.unknown):
                    try:
                        os.remove(cache_entry_fn)
                        self.logger.log(logging.TRACE, "Removed cache entry: %s", cache_entry_fn)
                    except:
                        self.logger.exception("Error removing cache entry: %s"%cache_entry_fn)
                continue

            self.logger.debug("Entry found for node: %s." % entry["devEUI"])


            # Retrieve the time of this nodes last transmission
            last_time = None
            if os.path.exists(node_time_file):
                with open(node_time_file, "r") as time_in:
                    last_time = json.load(time_in)
                    last_time = iso8601.parse_date(last_time)
                    last_time = time.mktime(last_time.timetuple())

            rx_time = time.mktime(iso8601.parse_date(entry['rxInfo'][0]['time']).timetuple())

            # Ignore the entry if it is older than the last transmission
            if last_time is not None and rx_time - last_time <= 0:
                self.logger.error(
                    "Reading for sensor (%s) found that is older than or equal to the time of the last entry." % entry[
                        "devEUI"])
                continue

            unpacked = unpack_data(entry['data'])
            first_record = unpacked['results'][0]
            offset = rx_time - first_record['ts']

            logging.log(logging.TRACE, "Offset: %s" % offset)

            # If the previously scheduled transmission was received only insert 4 entries, otherwise insert 8
            count = 4
            if last_time is None:
                count = 8
                self.logger.info("Previous TS not found.")
            else:
                self.logger.info(rx_time - last_time)
                if rx_time - last_time > 5000:
                    count = 8
                    self.logger.info("More than two hours have elapsed(%s), sending all entries." % entry["devEUI"])

            self.adjust_time(unpacked, offset)
            self.upload(entry, unpacked, count)

            if self.cache(entry, kc.uplink):
                try:
                    os.remove(cache_entry_fn)
                    self.logger.log(logging.TRACE, "Removed cache entry: %s", cache_entry_fn)
                except:
                    self.logger.exception("Error removing cache entry: %s"%cache_entry_fn)

            # Store the RX time of this entry
            with open(node_time_file, "w") as time_out:
                json.dump(entry['rxInfo'][0]['time'], time_out)

        self.cleanup()