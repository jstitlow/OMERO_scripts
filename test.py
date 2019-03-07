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


def import_to_omero(filename,hostname,username):
    #importing into OMERO
    try:
        with open(filename, "r") as fh:
            logging.debug( 'file opening passed' )
    except:
        raise(Exception,'File opening failed')

    logging.debug('importing '+filename+' into OMERO')
    import_command = "/opt/OMERO.py-5.4.8-ice36-b99/bin/omero import "+filename+" -s "+hostname+" -u "+username+" -k "
    popen = subprocess.Popen(import_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out, err = popen.communicate()

    if popen.returncode is not 0:
        raise RuntimeError('Failed to import'+filename)
    else:
        #we are only interested in the omero ID
        omeroID = out.split(':')[1]

imageId = ('547912')
image = conn.getObject("Image", imageId)
print image
fileset = image.getFileset()
print fileset
fs_id = fileset.getId()
print fs_id
#fs_id = str('20180810_CPTI001308_ventral.oir')

#fileset = conn.getObject("Fileset", fs_id)
#print fileset
