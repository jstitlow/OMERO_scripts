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

USER = os.environ['USER']
PASS = getpass.getpass("Enter Password:")

HOST="omero1.bioch.ox.ac.uk"
conn = BlitzGateway(USER, PASS, host=HOST, port=4064)
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)

# keep connection to OMERO alive
def keep_connection_alive():
    while True:
        conn.keepAlive()
        time.sleep(60)

th_ka = threading.Thread(target = keep_connection_alive)
th_ka.daemon = True
th_ka.start()


# Get images
#fig_IDs = pd.read_csv('fig_IDs.csv')
#project_ID = 5868

# get json files
indir = '/usr/people/bioc1301/src/OMERO_scripts/test/'
json_files = [indir+file for file in os.listdir(indir) if file.endswith('.json')]


image_list = []
broken_figures = []

for figure in json_files:
    #print 'Retrieving images from figure:', figure
    with open(figure) as datafile:
        data = json.load(datafile)
        try:
            for i in data['panels']:
                image_list.append(i['imageId'])
        except:
            broken_figures.append(figure)
            pass

for ID in set(image_list):

    image = conn.getObject('Image', ID)
    print image
    for f in image.getImportedImageFiles():
        filename = f.getName()
        t = open(f.getName(), 'wb')
        try:
            for chunk in f.getFileInChunks():
                t.write(chunk)
        finally:
            t.close()
    #print image

    #with open(image, "wb") as f:
    #    for chunk in image.getFileInChunks(buf=2621440):
    #        f.write(chunk)


filename = None


#for ID in fig_IDs['fig_ID']:
#    image = conn.getObject("Image", ID)
#    print image

#for image in conn.getObject("Project", project_ID).listChildren():

#    for orig_file in image.getImportedImageFiles():

#        for ID in fig_IDs['fig_ID']:
#            file_name = orig_file.getName()
#            print "Downloading...", file_name

            #with open(file_name, "wb") as f:
            #  for chunk in orig_file.getFileInChunks(buf=2621440):
            #    f.write(chunk)

conn.close()
