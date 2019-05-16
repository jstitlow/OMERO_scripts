#!/bin/bash

filename=CNS_list.csv;
all_lines=`cat $filename`

for line in $all_lines; do
   /opt/OMERO.py-5.4.10-ice36-b105/bin/omero export \
   --group 'mRNA localisation screen' \
   --file $line.ome.tiff Image:$line 
done

#--skip upgrade
#--group 'mRNA localisation screen'
