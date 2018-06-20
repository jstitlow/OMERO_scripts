# -------------figure2zegami-------------
#
# Created by: Steve Taylor
# with input from Will Moore, David Pinto, Mary Thompson, Darragh Ennis, and Ilan Davis
# Revised by : Josh Titlow, 18 May 2018
# 
# Generates .png files from a collection of OMERO.Figures
# 
# Requires setup commands
# >source setup.sh
#
# Requires modified omero/Figure_To_Pdf script to avoid processing on OMERO server
# -included as Figure_To_Pdf.py
#
# Known issues
# -Warning message: No handlers could be found for logger "figure_to_pdf"
# -no idea what this means
#
# ToDo
# -create a command line argument for the search term (e.g., "zegami1")

from omero.rtypes import wrap
from omero.gateway import BlitzGateway
import getpass
import omero
import os
import csv
import sys
import threading
import time
import re
from Figure_To_Pdf import FigureExport

# Connect to OMERO
PASS = getpass.getpass("Enter Password:") 

conn = BlitzGateway('bioc1301', PASS, host='omero1.bioch.ox.ac.uk', port=4064)
conn.connect()

# Keep connection to OMERO alive
def keep_connection_alive():
    while True:
        conn.keepAlive()
        time.sleep(60)

th_ka = threading.Thread(target = keep_connection_alive)
th_ka.daemon = True
th_ka.start()

# Cross-group query to find file
conn.SERVICE_OPTS.setOmeroGroup(-1)

# Create tab-separated file for Zegami collection
format = 'PDF'
zegami_tsv = "zegami.tsv"
y = open(zegami_tsv,'w')
z = csv.writer(y, delimiter="\t")
z.writerow(["Gene","Collection","Compartment", "probe","image","figure_name", "figure_id"])


# Get OMERO.Figure ID from files with "Zegami3" in the filename
num = 1
for f in conn.getObjects("FileAnnotation", attributes={"ns": "omero.web.figure.json"}):
    figure_name = f.getFile().getName().upper()
    id = f.getId()
    if "ZEGAMI3" in figure_name and "TEMPLATE" not in figure_name:
        ann = conn.getObject("FileAnnotation", id)
        
	if ann is None:
            raise Exception('ups! No file annotation with id %d' % id)
        
	print('generating image for figure %d' % id)
        
	# Build .pdf of the Figure from the json file
	json = "".join(ann.getFileInChunks())
        script_params = {
            'Figure_JSON' : json,
            'Webclient_URI': 'https://omero1.bioch.ox.ac.uk/webclient/',
            ## redundant, see https://github.com/ome/omero-figure/issues/290
            'Export_Option' : 'PDF',
        }
    
    	fig_export = FigureExport(conn, script_params, export_images=False)
    	fig_export.build_figure()
    
    # Pass filename parameters to .tsv file
    file_name = figure_name + "." + format
    image_name = figure_name + ".png"
    meta_data = figure_name.split("_")
    meta_data.append(file_name)
    meta_data.append(id)
     
    # check t:whe name has at least 6 fields (including the added figure id) which is a crude way of enforcing the naming scheme
    if len(meta_data) >= 5:
        if "ZEGAMI3" in file_name and "TEMPLATE" not in file_name:
            
	# write out zegami tsv file	   
	    min_info = meta_data[:4]
	    min_info.append(image_name);
	    min_info.append(figure_name);
	    min_info.append(id);
            z.writerow(min_info) 
            
	    if os.path.isfile(image_name):
                print "Got "+image_name+" already. Skipping..."
                continue
	    

	    print "Number of files processed = "+ str(num) + "; id=" + str(id) + "; Figure name = " + figure_name  
 
            num = num + 1

# Convert .pdf to .png
print ("Converting .pdfs to .pngs ...")
os.system('mogrify -density 400 -background white -alpha remove -format png ./*.pdf[0]')

# Remove extra files
os.system('rm *.tiff')
os.system('rm *.jpg')
os.system('rm *.pdf')
