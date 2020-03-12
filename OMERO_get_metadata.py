import omero
from omero.gateway import BlitzGateway
import os
import getpass
import threading
import time
import pandas as pd
from PIL import Image
import xml.etree.ElementTree as ET
#root = ET.fromstring(imageDesc)

# initialise OMERO
USER = getpass.getuser()
print 'username: ', USER
PASS = getpass.getpass('Enter password:')
HOST='omero1.bioch.ox.ac.uk'

conn = BlitzGateway(USER, PASS, host=HOST, port=4064)
conn.connect()
conn.SERVICE_OPTS.setOmeroGroup(-1)

print 'login successful'

# keep connection to OMERO alive
def keep_connection_alive():
    while True:
        conn.keepAlive()
        time.sleep(60)

th_ka = threading.Thread(target = keep_connection_alive)
th_ka.daemon = True
th_ka.start()

# Get directory with .ome.tiffs
indir = '/usr/people/bioc1301/src/OMERO_scripts/OMERO_Figure_screen_dataset/CNS_figures/mRNAlocalisation'
files = os.listdir(indir)
#files = ['382793.ome.tiff', '382794.ome.tiff']

# instantiate lists for storing metadata
imageID = []
filename = []
xy_pix = []
z_pix = []
ch_size = []
channels = []

def get_metadata():
#for file in files:
    if file.endswith('ome.tiff'):
        print 'getting metadata from:', file
        image = conn.getObject("Image", file[:-9])
        imageID.append(file)
        filename.append(image.getName())
        xy_pix.append(image.getPixelSizeX())
        z_pix.append(image.getPixelSizeZ())
        ch_size.append(image.getSizeC())
        channel_list = []
        for channel in image.getChannels():
            channel_list.append(channel.getLabel())
            print channel.getExcitationWavelength()
        channels.append(channel_list)        

#image = conn.getObject("Image", 382793)
#image.getDescription().getValue();

def get_excitationWave():        
    im = Image.open('382793.ome.tiff')
    imageDesc = im.tag[270]
    imageDesc


#df = pd.DataFrame({'filename':filename, 'imageID':imageID, 'xy_pix':xy_pix, 'z_pix':z_pix, 'ch_size':ch_size, 'channels':channels})
#df = df[['filename', 'imageID', 'xy_pix', 'z_pix', 'ch_size', 'channels']]
#df.to_csv(os.path.join(indir,'metadata.csv'), index=True)

