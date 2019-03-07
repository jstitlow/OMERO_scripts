import omero
from omero.gateway import BlitzGateway
import os
import getpass
import threading
import time
import subprocess

USER = os.environ['USER']
PASS = getpass.getpass("Enter Password:")
HOST = os.environ['HOST']

dataset_id = 16822
#filename = '/usr/people/bioc1301/src/OMERO_scripts/test/2017nov29_001473(cpx)_control_60x_OL_DAPI_syp_DLG_YFP.oir'
HOST='omero1.bioch.ox.ac.uk'
conn = BlitzGateway(USER, PASS, host=HOST, port=4064)
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)
#key = ('fb1e31ae-00ec-4860-aa8b-2847c17ed916')
#server = ('omero1.bioch.ox.ac.uk:4064')

def import_to_omero():
    #importing into OMERO
    #print filename, hostname, username, key
    #try:
    #    with open(filename, "r") as fh:
    #        print fh
    #except:
    #    print'File opening failed'
    import_command = '/opt/OMERO.py-5.4.8-ice36-b99/bin/omero import /usr/people/bioc1301/src/OMERO_scripts/test.oir -s omero1.bioch.ox.ac.uk:4064 -u bioc1301 -k 8639224d-bedd-4bca-9663-a5dd7b6dd721'
    popen = subprocess.Popen(import_command, shell=True, stdout=subprocess.PIPE)
    out, err = popen.communicate()

    #if popen.returncode is not 0:
    #print('Failed to import'+filename)
    #else:
        #we are only interested in the omero ID
    omeroID = out.split(':')[1]
    print omeroID
    conn.close()

import_to_omero()
