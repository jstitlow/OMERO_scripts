##########################################################################
# Upload images to OMERO and get imageId
#
# ---login with omero login---
#
# TODO:
#
# -iterate over a folder
# -store IDs in a dictionary or spreadsheet and link them to old imageIds
#   and json file
###########################################################################

import omero
import subprocess
import os
import pandas as pd


hostname = ('omero1.bioch.ox.ac.uk:4064')
username = ('bioc1301')
key = subprocess.Popen(['/opt/OMERO.py-5.4.8-ice36-b99/bin/omero', 'sessions', 'key'], stdout=subprocess.PIPE)
key = key.stdout.read()
#key = ('0c5a03f6-06e7-4da4-9842-502a17d36ab9')
dataset = '17859'

def import_to_omero(filename,hostname,username,key):

    import_command = "/opt/OMERO.py-5.4.8-ice36-b99/bin/omero import "+filename+" -s "+hostname+" -u "+username+" -k "+key+" -d "+dataset
    popen = subprocess.Popen(import_command, shell=True, stdout=subprocess.PIPE)
    out, err = popen.communicate()

    omeroID = out.split(':')[1].rstrip()
    print omeroID
    new_ID.append(omeroID)
    
indir = ('/usr/people/bioc1301/src/OMERO_scripts/OMERO_Figure_screen_dataset/test')
infiles = os.listdir(indir)

old_ID = []
new_ID = []

for file in infiles:
    if file.endswith('.r3d'):
            old_ID.append(file)
            file = os.path.join(indir, file)
            import_to_omero(file,hostname,username,key)

df = pd.DataFrame({'old_imageIds':old_ID, 'new_imageIds':new_ID})
df = df[['old_imageIds', 'new_imageIds']]
df.to_csv(os.path.join(indir,'new_NMJ_imageIDs.csv'), index=True)
print df


