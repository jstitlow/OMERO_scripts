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

figure_IDs = '/usr/people/bioc1301/src/OMERO_scripts/OMERO_Figure_screen_dataset/CNS_missing_jsons.csv'
figure_IDs = open(figure_IDs).read().splitlines()
outdir = '/usr/people/bioc1301/src/OMERO_scripts/OMERO_Figure_screen_dataset/json/'

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

    conn.close
