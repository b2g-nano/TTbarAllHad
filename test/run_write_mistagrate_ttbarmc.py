#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Analysis.TTbarAllHad.TTbarResAnaHadronic import *



## mcsets = [
##     'DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X'
##     ]

## datasets = [
##     'DijetSkim_Nrp_JetHT_Run2016B-07Aug17_ver2',
##     'DijetSkim_Nrp_JetHT_Run2016C-07Aug17',
##     'DijetSkim_Nrp_JetHT_Run2016D-07Aug17',
##     'DijetSkim_Nrp_JetHT_Run2016E-07Aug17',
##     'DijetSkim_Nrp_JetHT_Run2016F-07Aug17',
##     'DijetSkim_Nrp_JetHT_Run2016G-07Aug17',
##     'DijetSkim_Nrp_JetHT_Run2016H-07Aug17',
##     'DijetSkim_Nrp_JetHT_Run2017B-17Nov2017',
##     'DijetSkim_Nrp_JetHT_Run2017C-17Nov2017',
##     'DijetSkim_Nrp_JetHT_Run2017D-17Nov2017',
##     'DijetSkim_Nrp_JetHT_Run2017E-17Nov2017',
##     'DijetSkim_Nrp_JetHT_Run2017F-17Nov2017',
## ]

import random
random.seed(12345)

#inff = inputFiles()
#print 'Input files are :'

#print inff
#inff = eos_get_rootfiles( '/store/user/rappocc/CRAB_UserFiles/' + dataset )
inff = [
    'root://cmsxrootd.fnal.gov//store/user/asparker/NanoAODJMARTools-skims/nanoskim-JetsandLepton-94XMC-TTToHadronic_TuneCP5_13TeV-powheg-pythia8-trees.root'
    ]
p1=PostProcessor(".",inff,'nFatJet >= 2 && FatJet_pt[0] > 350. && FatJet_pt[1] > 350.','',[ttbarreshad_preddistwriter_data()], provenance=True, histFileName='mistag_TTToHadronic_TuneCP5_13TeV-powheg-pythia8_AntiTag.root', histDirName='ttbarres', noOut=True)#, haddFileName = 'ttbarreshad_nanoskim.root')
p1.run()
