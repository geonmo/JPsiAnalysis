import FWCore.ParameterSet.Config as cms

process = cms.Process("Ntuple")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:out_ttbar.root',
    ),
)

process.load("KrAFT.GenericNtuple.flatNtuple_cfi")
process.load("KrAFT.GenericNtuple.flatCands_cfi")
process.passFEDM = cms.EDFilter("HLTHighLevel",
    eventSetupPathsKey = cms.string(''),
    TriggerResultsTag = cms.InputTag("TriggerResults","","KrAFT"),
    HLTPaths = cms.vstring(
        "CANDSEL",
    ),
    throw = cms.bool(False),
    andOr = cms.bool(True)
)

process.p = cms.Path( process.passFEDM
                      +process.fEvent
)

process.options = cms.untracked.PSet( 
                    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("ntuple_ttbar.root"),
)


HLTMuMu = cms.PSet( src = cms.InputTag("flatEventInfo","HLTDoubleMu"))
HLTElEl = cms.PSet( src = cms.InputTag("flatEventInfo","HLTDoubleElectron"))
HLTMuEG = cms.PSet( src = cms.InputTag("flatEventInfo","HLTMuEG"))

setattr( process.fEvent.int,"HLTMuMu",HLTMuMu)
setattr( process.fEvent.int,"HLTElEl",HLTElEl)
setattr( process.fEvent.int,"HLTMuEG",HLTMuEG)

