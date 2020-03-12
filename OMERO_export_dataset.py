import omero
from omero.gateway import BlitzGateway
import os
import getpass
import threading
import time


def print_obj(obj, indent=0):
    """
    Helper method to display info about OMERO objects.
    Not all objects will have a "name" or owner field.
    """
    print """%s%s:%s  Name:"%s" (owner=%s)""" % (
        " " * indent,
        obj.OMERO_CLASS,
        obj.getId(),
        obj.getName(),
        obj.getOwnerOmeName())

# initialise OMERO
USER = getpass.getuser()
print ('username: ', USER)
PASS = getpass.getpass('Enter password:')
HOST='omero1.bioch.ox.ac.uk'

conn = BlitzGateway(USER, PASS, host=HOST, port=4064)
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)

print ('login successful')
dataset_id = input ('Enter dataset ID:')

# keep connection to OMERO alive
def keep_connection_alive():
    while True:
        conn.keepAlive()
        time.sleep(60)

th_ka = threading.Thread(target = keep_connection_alive)
th_ka.daemon = True
th_ka.start()

for image in conn.getObject('Dataset', dataset_id).listChildren():

    print_obj(image, 4)
#    for orig_file in image.getImportedImageFiles():

#        file_name = orig_file.getName()
#        print ('Downloading...', file_name)

#    with open(file_name, 'wb') as f:
#        for chunk in orig_file.getFileInChunks(buf=2621440):
#            f.write(chunk)

conn.close()
