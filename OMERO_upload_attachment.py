# Import files to OMERO dataset
#
# *****NOTE*****
#
# -change username to your username
# -may require specific group, e.g., if None Type error
# -requires command line arguments for -dataset and -indir


from omero.gateway import BlitzGateway
import getpass
import argparse
import sys
import os


PASS = getpass.getpass("Enter Password:")
conn = BlitzGateway('bioc1301', PASS, host='omero1.bioch.ox.ac.uk', port=4064, group='davisgroup')
conn.connect()

group = conn.getGroupFromContext()

def main(argList):

    parser= argparse.ArgumentParser()

    # specify infile and where to put it
    parser.add_argument('-dataset', help='dataset where file should be attached')
    parser.add_argument('-indir', help='directory of files to be attached')

    args= parser.parse_args(args=argList)

    # find dataset in OMERO
    dataset_id = args.dataset
    dataset = conn.getObject("Dataset", dataset_id)

    # get a local file e.g. result of some analysis
    infiles = os.listdir(args.indir)

    # loop through files
    for i in infiles:
        #can specificy namespace
        #namespace = "imperial.training.demo"
            # also include ns=namespace, in file_ann below
        i = os.path.join(args.indir, i)
        print "\nCreating FileAnnotation for", i
        file_ann = conn.createFileAnnfromLocalFile(i, mimetype="text/plain", desc=None)
        print "Attaching FileAnnotation to Dataset: ", "File ID:", file_ann.getId(), \
            ",", file_ann.getFile().getName(), "Size:", file_ann.getFile().getSize()
        dataset.linkAnnotation(file_ann)     # link it to dataset.

if __name__=='__main__':
    main(sys.argv[1:])
