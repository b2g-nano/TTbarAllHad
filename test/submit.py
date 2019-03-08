#!/usr/bin/env python                                                                                                                                                                                 
"""                                                                                                                                                                                                   
This is a small script that submits a config over many datasets                                                                                                                                       
"""
import os
from optparse import OptionParser

from Analysis.TTbarAllHad.eos_get_rootfiles import *

def make_list(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def getOptions() :
    """                                                                                                                                                                                               
    Parse and return the arguments provided by the user.                                                                                                                                              
    """
    usage = ('usage: python submit_all.py -c CONFIG -d DIR -f DATASETS_FILE')

    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="cfg", default="PSet.py",
        help=("The crab script you want to submit "),
        metavar="CONFIG")

    parser.add_option("--shscript", dest="shscript", default="crab_script.sh",
        help=("The bash script you want to submit "),
        metavar="SH")

    parser.add_option("--nanoscript", dest="nanoscript", default="run_plots.py",
        help=("The nanoaod script you want to submit "),
        metavar="NANOPY")
    
    parser.add_option("-o", "--outfile", dest="outfile", default="ttbarreshad.root",
        help=("The output file name "),
        metavar="OUT")
    
    parser.add_option("-d", "--dir", dest="dir", default="NANO",
        help=("The crab directory you want to use "),
        metavar="DIR")
    parser.add_option("-f", "--datasets", dest="datasets",
        help=("File listing datasets to run over"),
        metavar="FILE")
    parser.add_option("-t", "--tag", dest="tag", default='',
        help=("Dataset tag"),
        metavar="TAG")
    parser.add_option("-s", "--storageSite", dest="storageSite", default="T3_US_FNALLPC",
        help=("Site"),
        metavar="SITE")

    parser.add_option("-l", "--lumiMask", dest="lumiMask",
        help=("Lumi Mask JSON file"),
        metavar="LUMIMASK")

    (options, args) = parser.parse_args()

    if options.cfg == None or options.dir == None or options.datasets == None or options.storageSite == None:
        parser.error(usage)

    return options


def main():

    options = getOptions()

    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException
                           
    config.section_("General")
    config.General.workArea = options.dir
    config.General.transferLogs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = options.cfg

    config.section_("Data")
    config.Data.inputDataset = None
    config.Data.publication = False

    config.section_("Site")
    config.Site.storageSite = options.storageSite

    print 'Using config ' + options.cfg
    print 'Writing to directory ' + options.dir

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print 'Cannot execute command'
            print hte.headers

    #############################################################################################                                                                                                     
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##                                                                                                     
    #############################################################################################                                                                                                     

    datasetsFile = open( options.datasets )
    jobsLines = datasetsFile.readlines()
    adataset = None
    for ijob, job in enumerate(jobsLines) :

        adataset = job.rstrip()

        config.JobType.scriptExe = options.shscript
        config.JobType.inputFiles = [options.cfg ,options.shscript, options.nanoscript ,'./haddnano.py', 'keep_and_drop.txt', 'FrameworkJobReport.xml', 'mistag_rates.root', 'modmass.root']
        config.JobType.sendPythonFolder  = True
        
        #lfnList = eos_get_rootfiles( adataset )

        #print ("dataset %s has %d files" % (adataset, len(lfnList)))
        
        #config.Data.userInputFiles = lfnList
        config.Data.splitting = 'FileBased'
        config.Data.unitsPerJob = 50
      
        config.Data.inputDataset = adataset
        config.Data.inputDBS = 'global'
        config.JobType.outputFiles = [ options.outfile ]
        if options.lumiMask:
            config.Data.lumiMask = options.lumiMask

        requestname = '_'.join( adataset.split('/')[0:3] )[0:100]
        print 'requestname = ', requestname
        config.General.requestName = requestname
        config.Data.outputDatasetTag = requestname + '_' + options.tag
        print 'Submitting ' + config.General.requestName + ', dataset = ' + job
        print 'Configuration :'
        print config
        try :
            from multiprocessing import Process
            print 'submitting...'
            
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()
            #submit(config)                                                                                                                                                                           
        except :
            print 'Not submitted.'



if __name__ == '__main__':
    main()



