import FWCore.ParameterSet.Config as cms

runOnMC = True

from KrAFT.Configuration.customise_cff import *
process = initialize(runOnMC)
customisePAT(process, runOnMC=runOnMC, outputModules=[])

process.source.fileNames = [
    #'/store/relval/CMSSW_5_3_12_patch2/RelValProdTTbar/GEN-SIM-RECO/START53_LV2-v1/00000/5E865D62-AA2B-E311-AA04-002618943962.root',
    #'/store/relval/CMSSW_5_3_12_patch2/RelValProdTTbar/GEN-SIM-RECO/START53_LV2-v1/00000/92EB24DF-C72B-E311-8AA2-00261894390E.root',
		#'file:fulllepton.root',
    #'file:0000CAC5-D4DA-E111-8872-00A0D1EEF328.root',
    'file:/pnfs/user/youngjo/topref/ttbar_01.root',
    'file:/pnfs/user/youngjo/topref/ttbar_02.root'
]

process.load("KrAFT.Configuration.flatEDM_MC_cff")
process.load("KrAFT.Configuration.commonFilters_MC_cff")

process.partons = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        "drop *",
        "drop pt <= 0",
        "keep status = 3", # For the pythia
        "+keep pdgId = 443",
        "keep+ pdgId = 443",
        "+keep pdgId = 15",
        "keep+ pdgId = 15",
    ),
)


process.GEN = cms.Path(
    process.pseudoTop
  + process.partons
  * process.flatPseudoTopLepton + process.flatPseudoTopNu + process.flatPseudoTopJet
)


process.CANDSEL = cms.Path(
    process.preFilterSequence
  + process.patPF2PATSequencePFlow
  + process.analysisObjectSequence
)

process.out.SelectEvents.SelectEvents.append("GEN")
process.output = cms.EndPath(process.out)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

#process.GlobalTag.globaltag = cms.string('START53_V27::All')
