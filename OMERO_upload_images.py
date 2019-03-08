##########################################################################
# Upload images to OMERO and get imageId
#
# ---login with omero login---
# ---get session key with omero sessions list---
#
# TODO:
#
# -iterate over a folder
# -get session automatically
# -store IDs in a dictionary or spreadsheet and link them to old imageIds
#   and json file
###########################################################################

import omero
import subprocess

filename = ('/usr/people/bioc1301/src/OMERO_scripts/test.oir')
hostname = ('omero1.bioch.ox.ac.uk:4064')
username = ('bioc1301')
key = ('0c5a03f6-06e7-4da4-9842-502a17d36ab9')

def import_to_omero(filename,hostname,username,key):

    import_command = "/opt/OMERO.py-5.4.8-ice36-b99/bin/omero import "+filename+" -s "+hostname+" -u "+username+" -k "+ key
    popen = subprocess.Popen(import_command, shell=True, stdout=subprocess.PIPE)
    out, err = popen.communicate()

    omeroID = out.split(':')[1]
    print omeroID

import_to_omero(filename,hostname,username,key)
