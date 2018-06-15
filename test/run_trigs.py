#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Analysis.TTbarAllHad.TTbarResTrigsHadronic import *
from Analysis.TTbarAllHad.eos_get_rootfiles import *


## mcsets = [
##     'DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X'
##     ]

datasets = [
    'JetHT_Run2018A-22May2018-v1',
    'JetHT_Run2018A-PromptReco-v1',
    'JetHT_Run2018A-PromptReco-v2',
    'JetHT_Run2018A-PromptReco-v3',
    'JetHT_Run2018B-PromptReco-v1'
]

import random
random.seed(12345)

#inff = inputFiles()
#print 'Input files are :'

#print inff

for dataset in datasets:
    s = '/store/user/rappocc/JetHT/' + dataset
    print ' getting ', s
    inff = eos_get_rootfiles( s )
    p1=PostProcessor(".",inff[0:1],'nFatJet >= 2 && FatJet_pt[0] > 350. && FatJet_pt[1] > 350.','',[ttbartrighad()], provenance=True, histFileName='ttbarreshad_trigfile_' + dataset + '.root', histDirName='ttbarres', noOut=True)
    p1.run()
