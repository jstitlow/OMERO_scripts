################################################################################################# 
# OMEROfigure_json2jpg.py
#
# - downloads json files from OMERO.figures 
# - builds jpg files for each image
#
# --DEPENDENCIES--
#   
#   omero_tools.py
#   Figure_To_Pdf.py
#
#################################################################################################

import omero
from omero.gateway import BlitzGateway
import os
import getpass
import threading
import time
import pandas as pd
import json
import omero_tools
from Figure_To_Pdf import TiffExport

# setup OMERO connection
PASS = getpass.getpass("Enter Password:")
conn = BlitzGateway('bioc1301', PASS, host='omero1.bioch.ox.ac.uk', port=4064, group='davisgroup')
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)

# specify a list of figureIDs and outdir
figure_IDs = '/usr/people/bioc1301/src/OMERO_scripts/OMERO_Figure_screen_dataset/NMJ_figureIDs.csv'
figure_IDs = open(figure_IDs).read().splitlines()
outdir = '/usr/people/bioc1301/src/OMERO_scripts/OMERO_Figure_screen_dataset/json/'

# download OMEROfigure json files
for fig_ID in figure_IDs:
    try: 
        fig = conn.getObject('FileAnnotation', fig_ID)
        if fig is None:
            print fig_ID, 'is broken'
        try:
            fig_json = json.loads("".join(fig.getFileInChunks()))
        except:
            pass
        else:
            with open(os.path.join(outdir, fig_ID+'.json'), 'w') as fh:
                json.dump(fig_json, fh)
                print 'downloaded figure:', fig_ID
    except: 
        print fig_ID, 'does not exist'
        pass

    json_path = os.path.join(outdir, fig_ID+'.json')
    with open(json_path, 'r') as fh:
        fig_text = fh.read()
    
    # build jpg file
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
        return os.path.join(outdir, fig_ID+'.jpg')
    fig_export.get_figure_file_name = get_figure_file_name
    # fig_export.build_figure()
	
    try:
        fig_export.build_figure()
        print ('building:', fig_ID+'.jpg')
        
    except:
        print("failed to build figure",fig_ID+'.jpg')
            
conn.close
