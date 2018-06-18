import omero
from omero.gateway import BlitzGateway
import os
import getpass

USER = os.environ['USER']
PASS = getpass.getpass("Enter Password:")
HOST = os.environ['HOST']

dataset_id = 16950

HOST="omero1.bioch.ox.ac.uk"
conn = BlitzGateway(USER, PASS, host=HOST, port=4064)
conn.connect()
# conn.getSession().setTimeToIdle(rlong(60*60*1000))

for image in conn.getObject("Dataset", dataset_id).listChildren():

  for orig_file in image.getImportedImageFiles():

    file_name = orig_file.getName()
    print "Downloading...", file_name

    with open(file_name, "wb") as f:
      for chunk in orig_file.getFileInChunks(buf=2621440):
        f.write(chunk)

conn.close()
