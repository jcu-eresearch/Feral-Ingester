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

import sensor_cloud

from feral_decoder.constants import FeralConstants as fc
from feral_decoder.constants import SensorCloudConstants as sc

sensor_cloud.configuration.username = 'username'
sensor_cloud.configuration.password = 'password'

organisation = "organisation"
reporting_period = "PT15M"
sample_period = "P3Y"

streams = {
    fc.Temperature: {
        sc.UnitOfMeasure: "http://registry.it.csiro.au/def/qudt/1.1/qudt-unit/DegreeCelsius",
        sc.ObservedProperty: "http://registry.it.csiro.au/def/environment/property/air_temperature",
        sc.InterpolationType: "http://www.opengis.net/def/waterml/2.0/interpolationType/Continuous",
        sc.SamplePeriod: sample_period,
        sc.ReportingPeriod: reporting_period,
        sc.Organisation: organisation,
    },
    fc.Humidity: {
        sc.UnitOfMeasure: "http://registry.it.csiro.au/def/qudt/1.1/qudt-unit/Percent",
        sc.ObservedProperty: "http://data.sense-t.org.au/registry/def/sop/RelativeHumidity",
        sc.InterpolationType: "http://www.opengis.net/def/waterml/2.0/interpolationType/Continuous",
        sc.SamplePeriod: sample_period,
        sc.ReportingPeriod: reporting_period,
        sc.Organisation: organisation,
    },
    fc.Pressure: {
        sc.UnitOfMeasure: "http://data.sense-t.org.au/registry/def/su/HectoPascal",
        sc.ObservedProperty: "http://registry.it.csiro.au/def/environment/property/air_pressure",
        sc.InterpolationType: "http://www.opengis.net/def/waterml/2.0/interpolationType/Continuous",
        sc.SamplePeriod: sample_period,
        sc.ReportingPeriod: reporting_period,
        sc.Organisation: organisation,
    },
    fc.Lux: {
        sc.UnitOfMeasure: "http://registry.it.csiro.au/def/qudt/1.1/qudt-unit/Lux",
        sc.ObservedProperty: "http://registry.it.csiro.au/def/environment/property/air_pressure",
        sc.InterpolationType: "http://www.opengis.net/def/waterml/2.0/interpolationType/Continuous",
        sc.SamplePeriod: sample_period,
        sc.ReportingPeriod: reporting_period,
        sc.Organisation: organisation,
    },
    fc.BatteryVoltage: {
        sc.UnitOfMeasure: "http://registry.it.csiro.au/def/qudt/1.1/qudt-unit/Volt",
        sc.ObservedProperty: "http://data.sense-t.org.au/registry/def/sop/battery_voltage",
        sc.InterpolationType: "http://www.opengis.net/def/waterml/2.0/interpolationType/Continuous",
        sc.SamplePeriod: sample_period,
        sc.ReportingPeriod: reporting_period,
        sc.Organisation: organisation,
    }
}