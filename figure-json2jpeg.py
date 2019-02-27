#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright (C) 2018 David Pinto <david.pinto@bioch.ox.ac.uk>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os.path
import sys

import omero_tools
from Figure_To_Pdf import TiffExport


def main(dir_path, metadata_fpath):
    conn = omero_tools.get_connection()
    conn.SERVICE_OPTS.setOmeroGroup(-1)

    metadata = [line.split(',') for line in open(metadata_fpath, 'r')]
    for fig_metadata in metadata:
        fig_id = int(fig_metadata[0])

        json_path = os.path.join(dir_path, '%d.json' % fig_id)
        jpg_path = os.path.join(dir_path, '%d.jpg' % fig_id)
        with open(json_path, 'r') as fh:
            if os.path.exists(jpg_path):
                print (jpg_path,"already exists")
                fig_text = fh.read()
                pass
            else:
                print ("building",json_path)
                fig_text = fh.read()

        fig_json = json.loads(fig_text)
        if int(fig_json['page_count']) > 1:
            raise RuntimeError("more than one page for figure id '%d'" % fig_id)

        export_params = {
            'Figure_JSON' : fig_text,
            'Webclient_URI': 'https://omero1.bioch.ox.ac.uk',
            'Export_Option' : 'TIFF', # change to jpeg
        }
        fig_export = TiffExport(conn, export_params,
                                export_images=False)
        def get_figure_file_name(page=None):
            return os.path.join(dir_path, '%d.jpg' % fig_id)
        fig_export.get_figure_file_name = get_figure_file_name
        # fig_export.build_figure()
	try:
	    fig_export.build_figure()
	except:
	    print("failed to build figure '%d'" % fig_id)

	# Convert .pdf to .png
	#print ("Converting .pdfs to .pngs ...")
	#os.system('mogrify -density 400 -background white -alpha remove -format png ./*.pdf[0]')


if __name__ == '__main__':
    main(*sys.argv[1:])
    #Arguments
    #dir_path = path to json files
    #metadata_fpath = path to metadata file
