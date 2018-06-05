#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.analysis.b2g.ttbarres.TTbarResAnaHadronic import *


from Analysis.QJetMass.helpers.eos_get_rootfiles import *

mcsets = [
    'DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X'
    ]

datasets = [
    'DijetSkim_Nrp_JetHT_Run2016B-07Aug17_ver2',
    'DijetSkim_Nrp_JetHT_Run2016C-07Aug17',
    'DijetSkim_Nrp_JetHT_Run2016D-07Aug17',
    'DijetSkim_Nrp_JetHT_Run2016E-07Aug17',
    'DijetSkim_Nrp_JetHT_Run2016F-07Aug17',
    'DijetSkim_Nrp_JetHT_Run2016G-07Aug17',
    'DijetSkim_Nrp_JetHT_Run2016H-07Aug17',
    #'DijetSkim_Nrp_JetHT_Run2017B-17Nov2017',
    #'DijetSkim_Nrp_JetHT_Run2017C-17Nov2017',
    #'DijetSkim_Nrp_JetHT_Run2017D-17Nov2017',
    #'DijetSkim_Nrp_JetHT_Run2017E-17Nov2017',
    #'DijetSkim_Nrp_JetHT_Run2017F-17Nov2017',
]



import random
random.seed(12345)

for dataset in datasets:
    inff = eos_get_rootfiles( '/store/user/rappocc/CRAB_UserFiles/' + dataset )
    p1=PostProcessor(".",inff,'FatJet_pt > 400.','',[ttbarreshad_preddistwriter()],provenance=False, noOut=True, histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')




#p0=PostProcessor(".",files,'FatJet_pt > 400.',"keep_and_drop.txt",[],outputbranchsel="output_keep_and_drop.txt",histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')

#p0=PostProcessor(".",files,'FatJet_pt > 400.',"keep_and_drop.txt",[jetmetUncertaintiesAK4Puppi(), jetmetUncertaintiesAK8Puppi(), ak8JetID(),ak8SubjetVariables(),ttbarreshad_preddistwriter()],outputbranchsel="output_keep_and_drop.txt", histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')


#p2=PostProcessor(".",['test94X_NANO_addPU.root'],'',"keep_and_drop.txt",[TTbarResAnaHadronic()],provenance=False, noOut=True,histFileName='hists.root', histDirName='ttbarres', postfix='predread')

p1.run()
#p2.run()
