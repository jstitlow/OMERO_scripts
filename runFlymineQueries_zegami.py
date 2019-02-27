# MKT
# purpose: query Flymine database to retrieve data of interest for genes and add to Josh's screen spreadsheet
# notes: Before running this script you will need to install intermine (!), see below
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# TODO
# -write code for the following:
#   -axonseq data
#   -adding FISH annotations (requires MK's code)
#
# -move all Omero.Figures into a common dataset
# -fix Omero.Figure filenames

from intermine.webservice import Service
service = Service("http://www.flymine.org/flymine/service")

import sys
import argparse
import unicodedata
import re
import pandas as pd
import os

#link to location of the file mapping Bangalor or CPTI # to FBg #
flyline_file='Flyline_FBg_whole_genome.csv'

class Query():
    '''Parse parameter file for Flymine query'''
    def __init__(self, paramfile):
        self.constraints={}
        self.filters={}
        f=open(paramfile, 'r')
        for line in f:
            fields=line.strip('\n').split('\t')
            if fields[0]=='QUERY_NAME':
                self.qname=fields[-1]
            elif fields[0]=='QUERY_TYPE':
                self.qtype= fields[-1]
            elif fields[0].startswith('CONSTRAINT'):
                thisconstraint=fields[0].rsplit('CONSTRAINT')[-1]
                if '=' in fields[-1]: #this is a rule, need to separate individual components
                    fs=re.split(r'[<>=]', fields[-1])
                    splitter=fields[-1].strip(fs[0]).strip(fs[-1])
                    self.constraints[fs[0]]=[fs[0], splitter, fs[-1]]

                else:
                    self.constraints[thisconstraint]=[i for i in fields[1:]]
            elif fields[0].startswith('FILTER'): #this is where you can specify which values in a comma-separated list will be output, for example if you only want to report specific phenotypes in a screen
                thisfilter=fields[0].rsplit('FILTER')[-1]
                if '=' in fields[-1]: #this is a rule, need to separate individual components
                    fs= fields[-1].split('=')
                    self.filters[fs[0]]=fs[1].split(',')
                else:
                    self.filters[thisfilter]=[i for i in fields[1:]]
            #I don't remember the distinction between between the filter rule with '=' and the filter rule just with spaces separating
            elif fields[0]=='WRITE':
                self.towrite=fields[-1]
        f.close()

def run_query(query, query_data):
    '''Run Flymine query, based on the Python API examples'''

    thisquery= service.new_query(query.qtype)
    for i in query.constraints:
        thisquery.add_constraint(*query.constraints[i])
    thisquery.add_view(query.towrite) #need to use add_view for those values to be accessible

    if query.filters!={}:
        thesefilters=set(query.filters.values()[0]) #empty set if no filters defined, for now assume only one filter on the towrite column name
    else:
        thesefilters=set()

    #update results dictionary with data from queries
    for row in thisquery.rows():
        if row['primaryIdentifier'] in query_data:#genes included in the screen:
            try:
                #convert all to string data type
                data= row[query.towrite]
                #some types of data need conversion from unicode
                if type(data)!='unicode':
                    valstring= str(data)
                else:
                    valstring=unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
                vals= set(valstring.split(', '))

                #apply filters to query output if needed
                #add query data to any previous query data obtained for gene (each gene can occupy >1 row in query results for any given query)
                if thesefilters!=set([]):
                    query_data[row['primaryIdentifier']]=query_data[row['primaryIdentifier']].union(vals.intersection(thesefilters))

                else:
                    query_data[row['primaryIdentifier']]=query_data[row['primaryIdentifier']].union(vals)

            except KeyError:
                continue

    return query_data

def main(argList):

    parser= argparse.ArgumentParser()
    parser.add_argument('-outname', help='outname for final spreadsheet')
    parser.add_argument('-infile', help='input tsv file to update with new fields, e.g. zegami.tsv')
    parser.add_argument('-query_dir', help='input directory containing query files')
    parser.add_argument('-dataset_dir', help='input directory containing other datasets')

    args= parser.parse_args(args=argList)

    #add OMERO.Figure link and image ID to Zegami.tsv
    zegami_df=pd.read_csv(args.infile)

    zegami_df["OMEROFigurelink"]=str('https://omero1.bioch.ox.ac.uk/figure/file/')+zegami_df["figure_id"].astype(str)
    zegami_df["image"]=zegami_df["figure_id"].astype(str)+str('.png')


    #add whole genome of Flybase_ID to Zegami.tsv
    #left = pd.read_csv(args.infile)
    right = pd.read_csv(flyline_file)
    zegami_df = pd.merge(zegami_df, right, how='outer', on=['Collection'])
    zegami_df= zegami_df.drop(columns=['Gene_x'])
    zegami_df= zegami_df.rename(index=str, columns={"Gene_y": "Gene"})

    #add other datasets to Zegami.tsv
    datasets = [os.path.join(args.dataset_dir, x) for x in os.listdir(args.dataset_dir) if x.endswith('.csv') if not x.startswith('.')]

    for x in datasets:
        print ('adding', x, 'to Zegami.tsv file')
        left = zegami_df
        right = pd.read_csv(x)
        zegami_df=pd.merge(left, right, how='left', on=['Flybase_ID'])

    #run queries
    queries=[os.path.join(args.query_dir, q) for q in os.listdir(args.query_dir) if q.endswith('.txt')]

    for q in queries:
        print ('running Intermine query for', q)
        #parse file to get information to run query
        thisquery= Query(q)
        #store data from queries
        query_data={k:set() for k in zegami_df['Flybase_ID'].tolist()}
        query_data= run_query(thisquery, query_data)
        #convert data to comma-separated list for zegami
        for k in query_data:
            query_data[k]=','.join(query_data[k])

        zegami_df[thisquery.qname]=zegami_df['Flybase_ID'].map(query_data)

    zegami_df.to_csv('%s.tsv' % args.outname, sep='\t', index=False)

if __name__=='__main__':
    main(sys.argv[1:])
