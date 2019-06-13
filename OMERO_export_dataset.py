import omero
from omero.gateway import BlitzGateway
import os
import getpass
import threading
import time

# specify a dataset
dataset_id = 16822

# initialise OMERO
USER = os.environ['USER']
PASS = getpass.getpass("Enter Password:")
HOST = os.environ['HOST']

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

for image in conn.getObject("Dataset", dataset_id).listChildren():

    for orig_file in image.getImportedImageFiles():

        file_name = orig_file.getName()
        print ("Downloading...", file_name)

#    with open(file_name, "wb") as f:
#        for chunk in orig_file.getFileInChunks(buf=2621440):
#            f.write(chunk)

conn.close()
