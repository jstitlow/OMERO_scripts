20180820
Notes on using questionaire.py, goal is to quickly assess NMJ expression patterns

-modified list_figures.py script to only print 'zegami2' files
-questionaire.py script has sys arguments, path/to/questions, path/to/outputdir, and path/to/images/*.jpg
-modified question file in data/figures/question to have 3 questions

-so I get it to run, the GUI opens with the correct questions, but none of the buttons seem to work

Notes on OMERO_Figure scoring script
-environment is setup on ssh bioc1301@bioch2125

20181013
Using questionaire.py to quickly analyse glia expression
2111855/Lasp CPTI002905 appears to be not expressed in NMJ
Write MK's code to find disease associations in the collection

20181015
Cleaning up the code for generating Zegami databases
-list-figures.py find all of the figures in Omero labelled Zegami and parse the filenames into a .csv file
 just as the figure2zegami.py script does

TO DO:
-write code to merge other datasets to the zegami text file
    -Davis lab sequencing data
    -Other sources
    -flymine output
    -smFISH screen annotations

KNOWN ISSUES:
-zegami.csv has to be cleaned up as follows
    -remove Maria's data and others that are mis-labelled
    -remove template data
    -remove hyphens from CPTI ID numbers
    -several typos in figure_name (CPTI numbers) that make it difficult to correlate

SUMMARY OF WORKFLOW TO BUILD ZEGAMI COLLECTION
-begin OMERO session
    -make login from ../DavidGUI/ directory
-generate zegami.csv file from OMERO.Figure names that include Zegami
    -list-figures.py
-download figures as json files
    -download-figures.py
    -requires arguments for outdir path and metadata(zegami.csv) path
    -will have to delete first row because the code is looking integer values
-convert json files to jpg for the scoring app and png for Zegami
    -figure-json2jpeg.py
    -requires arguments for outdir path and metadata(zegami.csv) path
-convert jpg files to png

-expand zegami.csv file with other datasets
    -run runFlymineQueries_zegami.py #needs Py2 because of some dictionary nonsense
      -export PATH="/usr/people/bioc1301/miniconda3/bin:$PATH"
      -source activate py27

SUMMARY OF WORKFLOW TO USE SCORING APP
-Generate image files (.jpgs) and ID table using the Zegami workflow above
-Run questionnaire.py script
    -arguments
        -questions path
        -answers dir
        -image path
