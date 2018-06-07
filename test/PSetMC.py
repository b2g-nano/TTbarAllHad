import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
)
process.source.fileNames = [
    '/store/user/rappocc/CRAB_UserFiles/DijetSkim_Nrp_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_94X/180518_183607/0000/dijets_nanoskim_83.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet()
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('ttbarreshad_nanoskim.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
