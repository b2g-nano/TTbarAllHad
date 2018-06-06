import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
)
process.source.fileNames = [
    '/store/user/rappocc/CRAB_UserFiles/DijetSkim_Nrp_JetHT_Run2017E-17Nov2017/180518_030157/0000/dijets_nanoskim_85.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet()
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('ttbarreshad_nanoskim.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
