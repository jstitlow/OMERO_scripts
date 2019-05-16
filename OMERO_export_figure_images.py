####################################################
# OMERO export figure images
#
# Download images from a list of figure IDs
#
# WORKFLOW
#
# 1. Specify a list of figure IDs
# 2. Get image IDs from figure .json file
# 3. Download them from OMERO
#####################################################

import omero
from omero.gateway import BlitzGateway
import os
import getpass
import threading
import time
import pandas as pd
import json

PASS = getpass.getpass("Enter Password:")
conn = BlitzGateway('bioc1301', PASS, host='omero1.bioch.ox.ac.uk', port=4064, group='davisgroup')
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)

# Get images
#fig_IDs = pd.read_csv('fig_IDs.csv')
#project_ID = 5868

# get json files
#indir = '/usr/people/bioc1301/src/OMERO_scripts/test/'
#json_files = [indir+file for file in os.listdir(indir) if file.endswith('.json')]

#json_files = [indir+file for file in os.listdir(indir) if file.endswith('.json')]
figure_IDs = pd.read_csv('/usr/people/bioc1301/src/Zegami_scripts/Zegami_collection_27_Feb_2019/figures/NMJ_imageID_json.csv')
figure_IDs = figure_IDs['old_imageIds']
#figure_IDs = open(figure_IDs).read().splitlines()

def export_original_file():
    for ID in figure_IDs:
        image = conn.getObject('Image', ID)
        print image
        for orig_file in image.getImportedImageFiles():
            file_name = orig_file.getName()
            print "Downloading...", file_name
            with open(file_name, "wb") as f:
                for chunk in orig_file.getFileInChunks(buf=2621440):
                    f.write(chunk)

                    
import omero
import subprocess

filename = ('/usr/people/bioc1301/src/OMERO_scripts/test.oir')
hostname = ('omero1.bioch.ox.ac.uk:4064')
username = ('bioc1301')
key = ('0c5a03f6-06e7-4da4-9842-502a17d36ab9')

def export_ometiff(figureIDs,hostname,username,key):
    for ID in figure_IDs:
        export_command = "/opt/OMERO.py-5.4.8-ice36-b99/bin/omero import --file "+filename+" -s "+hostname+" -u "+username+" -k "+ key
        popen = subprocess.Popen(import_command, shell=True, stdout=subprocess.PIPE)
        out, err = popen.communicate()

        omeroID = out.split(':')[1]
        print omeroID

#export_ometiff(figureIDs,hostname,username,key)

conn.close()

# bin/omero export --file image.tif Image:<id>