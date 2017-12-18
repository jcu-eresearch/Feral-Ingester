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

from feral_decoder.constants import KeyConstants as kc

coen_prefix = "coen"



sensors = {
    "0080000004004c2f": {kc.prefix: coen_prefix},
    "0080000004004c30": {kc.prefix: coen_prefix},
    "0080000004004c36": {kc.prefix: coen_prefix},
    "0080000004004c2e": {kc.prefix: coen_prefix},
    "0080000004004c38": {kc.prefix: coen_prefix},
    "0080000004004c3a": {kc.prefix: coen_prefix},
    "0080000004004c39": {kc.prefix: coen_prefix},


    "0080000004004c1c": {kc.prefix: coen_prefix},
}
