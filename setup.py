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

from setuptools import setup, find_packages

setup(name='FeralDecoder',
      version='0.0.1',
      description='Feral Data Decoder and uploader',
      author='NigelB',
      author_email='nigel.blair@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          # "tzinfo",
          "pytz", ""
          "iso8601"
      ],
      entry_points={
          "console_scripts": [
              "feral_decoder_create_locations = feral_decoder.create_locations:main",
              "feral_decoder_create_streams = feral_decoder.create_streams:main",
              "feral_decoder_upload = feral_decoder.launcher:upload",
              "feral_json_unpack = feral_decoder.unpack:unpack",
          ]
      }
      )