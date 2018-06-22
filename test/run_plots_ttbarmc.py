#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Analysis.TTbarAllHad.TTbarResAnaHadronic import *
from Analysis.TTbarAllHad.eos_get_rootfiles import *


mcsets = [
    'DijetSkim_Nrp_TTToHadronic_TuneCP5_13TeV-powheg-pythia8-94X/'
    ]

import random
random.seed(12345)

#inff = inputFiles()
#print 'Input files are :'

#print inff

for dataset in mcsets:
    inff = eos_get_rootfiles( '/store/user/rappocc/CRAB_UserFiles/' + dataset )
    p1=PostProcessor(".",inff,'nFatJet >= 2 && FatJet_pt[0] > 350. && FatJet_pt[1] > 350.','',[TTbarResAnaHadronic(isData=False,year='2017')], provenance=True, histFileName='plots_TTToHadronic_TuneCP5_13TeV-powheg-pythia8-94X.root', histDirName='ttbarres', noOut=True)#, haddFileName = 'ttbarreshad_nanoskim.root')
p1.run()
