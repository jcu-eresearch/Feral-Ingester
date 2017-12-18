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
import os


def ensure_paths():
    from FeralDecoder_Paths import cache_dir, archive_dir, node_dir, unknown_dir

    logger = logging.getLogger("Paths")

    logger.info("Cache Directory: %s"%cache_dir)
    logger.info("Archive Directory: %s"%archive_dir)
    logger.info("Node Directory: %s"%node_dir)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        logger.info("Created: %s"%cache_dir)

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        logger.info("Created: %s"%archive_dir)

    if not os.path.exists(node_dir):
        os.makedirs(node_dir)
        logger.info("Created: %s"%node_dir)

    if not os.path.exists(unknown_dir):
        os.makedirs(unknown_dir)
        logger.info("Created: %s"%unknown_dir)

    return cache_dir, archive_dir