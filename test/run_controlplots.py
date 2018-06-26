#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Analysis.TTbarAllHad.TTbarResControlPlotsHadronic import *
from Analysis.TTbarAllHad.eos_get_rootfiles import *


## mcsets = [
##     'DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X'
##     ]

datasets = [
    'CRAB_UserFiles/DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016B-07Aug17_ver2',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016C-07Aug17',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016D-07Aug17',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016E-07Aug17',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016F-07Aug17',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016G-07Aug17',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2016H-07Aug17',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2017B-17Nov2017',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2017C-17Nov2017',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2017D-17Nov2017',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2017E-17Nov2017',
    'CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2017F-17Nov2017',
    'JetHT/JetHT_Run2018A-22May2018-v1',
    'JetHT/JetHT_Run2018A-PromptReco-v1',
    'JetHT/JetHT_Run2018A-PromptReco-v2',
    'JetHT/JetHT_Run2018A-PromptReco-v3',
    'JetHT/JetHT_Run2018B-PromptReco-v1'
]

import random
random.seed(12345)

#inff = inputFiles()
#print 'Input files are :'

#print inff

for dataset in datasets:
    inff = eos_get_rootfiles( '/store/user/rappocc/' + dataset )
    idata = True
    if 'QCD_Pt' in dataset :
        idata=False
    iyear = ''
    if 'Run2018' in dataset :
        iyear = '2018'
    elif 'Run2017' in dataset:
        iyear = '2017'
    else:
        iyear = '2016'
    p1=PostProcessor(".",inff,'nFatJet >= 2 && FatJet_pt[0] > 400. && FatJet_pt[1] > 400.','',
                         [TTbarResControlPlotsHadronic(isData=idata,year=iyear)],
                         provenance=True, histFileName='ttbarreshad_controlplots_' + dataset.split('/')[1] + '.root', histDirName='ttbarres', noOut=True)
    p1.run()
