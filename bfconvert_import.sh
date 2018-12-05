#!/bin/bash

# shell script to batch convert microscopy files with bfconvert and upload them to OMERO
# Created: 26 August, 2018
# revised: 29 August, 2018
#
# requires two arguments, input files (path/to/files/*) and dataset name for OMERO
#
# input files (any format, currently .oir) are converted to .ome.tiffs and saved in input directory
#
# path/to/bfconvert is hard-coaded, so point it to bfconvert installation
#
# type bfconvert into command line to see additional arguments
#
# %n.tiff creates a separate file for each image series
# .oir files over 1GB are saved as multiple infiles, bfconvert combines them to a single .tiff


# provide username and password for OMERO
read -p "username: " uname
read -s -p "password: " passw

# remove wildcard character from input files argument
outdir=${1::-1}

# use bfconvert to convert all .oir files to .ome.tiff
for i in $1; do
        if [[ $i == *.oir ]]
        then
                ~/src/bioformats/bftools/bfconvert ${i} $outdir%n.ome.tiff
        fi
done

# use CLI to upload all converted .ome.tiffs to OMERO 
for k in $1; do 
        if [[ $k == *.tiff ]]
        then
                /opt/OMERO.server-5.4.5-ice35-b83/bin/omero import -s omero1.bioch.ox.ac.uk -p 4064 -u $uname -g davisgroup -w $passw ${k} -T Dataset:+name:$2
        fi
done
