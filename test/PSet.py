import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
)
process.source.fileNames = [
    '/store/data/Run2018B/JetHT/NANOAOD/Nano14Dec2018-v1/80000/0E8F10F1-30CA-4D4F-80EA-C9851CABC967.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet()
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('ttbarreshad.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
