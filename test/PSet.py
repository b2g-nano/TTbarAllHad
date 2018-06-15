import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
)
process.source.fileNames = [
    '/store/user/rappocc/JetHT/JetHT_Run2018A-22May2018-v1/180608_131000/0000/test101X_NANO_1.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet()
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('ttbarreshad_predfile.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
