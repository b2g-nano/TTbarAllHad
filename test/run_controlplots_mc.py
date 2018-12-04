#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Analysis.TTbarAllHad.TTbarResControlPlotsHadronic import *


import random
random.seed(12345)

inff = inputFiles()
print 'Input files are :'

print inff

idata = False
iyear = '2018'


p1=PostProcessor(".",inff,'nFatJet >= 2 && FatJet_pt[0] > 400. && FatJet_pt[1] > 400.','',
                     [TTbarResControlPlotsHadronic(isData=idata,year=iyear)],
                     provenance=True, histFileName='ttbarreshad.root', histDirName='ttbarres', noOut=True)
p1.run()
