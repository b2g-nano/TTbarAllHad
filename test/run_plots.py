#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *

from Analysis.TTbarAllHad.TTbarResAnaHadronic import *


from Analysis.TTbarAllHad.eos_get_rootfiles import *

mcsets = [
    'DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X'
    ]

datasets = [
    #'DijetSkim_Nrp_JetHT_Run2016B-07Aug17_ver2',
    #'DijetSkim_Nrp_JetHT_Run2016C-07Aug17',
    #'DijetSkim_Nrp_JetHT_Run2016D-07Aug17',
    #'DijetSkim_Nrp_JetHT_Run2016E-07Aug17',
    #'DijetSkim_Nrp_JetHT_Run2016F-07Aug17',
    #'DijetSkim_Nrp_JetHT_Run2016G-07Aug17',
    #'DijetSkim_Nrp_JetHT_Run2016H-07Aug17',
    'DijetSkim_Nrp_JetHT_Run2017B-17Nov2017',
    'DijetSkim_Nrp_JetHT_Run2017C-17Nov2017',
    'DijetSkim_Nrp_JetHT_Run2017D-17Nov2017',
    'DijetSkim_Nrp_JetHT_Run2017E-17Nov2017',
    'DijetSkim_Nrp_JetHT_Run2017F-17Nov2017',
]
jecs = [
    #[jetRecalib2016BCD, jetRecalibAK8Puppi2016BCD],
    #[jetRecalib2016BCD, jetRecalibAK8Puppi2016BCD],
    #[jetRecalib2016BCD, jetRecalibAK8Puppi2016BCD],
    #[jetRecalib2016EF,  jetRecalibAK8Puppi2016EF ],
    #[jetRecalib2016EF,  jetRecalibAK8Puppi2016EF ],
    #[jetRecalib2016GH,  jetRecalibAK8Puppi2016GH ],
    #[jetRecalib2016GH,  jetRecalibAK8Puppi2016GH ],
    [jetRecalib2017B, jetRecalibAK8Puppi2017B],
    [jetRecalib2017C, jetRecalibAK8Puppi2017C],
    [jetRecalib2017D, jetRecalibAK8Puppi2017D],
    [jetRecalib2017E, jetRecalibAK8Puppi2017E],
    [jetRecalib2017F, jetRecalibAK8Puppi2017F],
    ]


import random
random.seed(12345)

for i,dataset in enumerate(datasets[0:1]):
    inff = eos_get_rootfiles( '/store/user/rappocc/CRAB_UserFiles/' + dataset )
    #p1=PostProcessor(".",inff,'FatJet_pt > 400.','',[jecs[i][0](),jecs[i][1](),ttbarreshad_preddistwriter(isData=True)], histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')
    p1=PostProcessor(".",inff[0:1],'nFatJet >= 2 && FatJet_pt[0] > 400. && FatJet_pt[1] > 400. && MET_sumEt > 1100.','',[ttbarreshad_preddistwriter_data()], noOut=True, histFileName='ttbarreshad_predfile_' + dataset + '.root', histDirName='ttbarres', postfix='predwrite')
    p1.run()



#p0=PostProcessor(".",files,'FatJet_pt > 400.',"keep_and_drop.txt",[],outputbranchsel="output_keep_and_drop.txt",histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')

#p0=PostProcessor(".",files,'FatJet_pt > 400.',"keep_and_drop.txt",[jetmetUncertaintiesAK4Puppi(), jetmetUncertaintiesAK8Puppi(), ak8JetID(),ak8SubjetVariables(),ttbarreshad_preddistwriter()],outputbranchsel="output_keep_and_drop.txt", histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')


#p2=PostProcessor(".",['test94X_NANO_addPU.root'],'',"keep_and_drop.txt",[TTbarResAnaHadronic()],provenance=False, noOut=True,histFileName='hists.root', histDirName='ttbarres', postfix='predread')


#p2.run()
