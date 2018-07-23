#!/bin/bash

# Creates a new OMERO dataset and imports all files within a specified directory.
# The OMERO environment is already setup on mprocessor1.
# Pass directory path as 1st argument (e.g.,"~/path/*.tiff" including quotes)
# Pass dataset name as 2nd argument
# Should prompt login to give OMERO credentials.
# Make sure python installation is usr/bin not conda (which python)
# If conda then change in ~/.bashrc
# Also use screen -S omero to avoid logout issues
# --group AdultBrain smFISH
# Create loop to select each .tiff file in a directory

for i in $1; do

# OMERO CLI command for importing files to a named dataset
        # Creates new dataset if one doesn't already exist
        /opt/OMERO.server-5.4.5-ice35-b83/bin/omero import ${i} -T Dataset:+name:$2\
        --group 'AdultBrain smFISH'
done
