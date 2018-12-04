import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
)
process.source.fileNames = [
    '/store/data/Run2018A/JetHT/NANOAOD/14Sep2018_ver1-v1/60000/CF60DD31-A427-254C-B571-36FEED03C8E1.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet()
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('ttbarreshad.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
