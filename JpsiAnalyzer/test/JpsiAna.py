#!/usr/bin/env python
from ROOT import *
from JPsiAnalysis.JpsiAnalyzer.Lepton import Lepton
from JPsiAnalysis.JpsiAnalyzer.Jet import Jet
from JPsiAnalysis.JpsiAnalyzer.CutFlow import *
from JPsiAnalysis.JpsiAnalyzer.Jpsi import Jpsi
from JPsiAnalysis.JpsiAnalyzer.EventContent import EventContent

class JpsiAna :
  def __init__(self, inFileNames, mode, outFileName) :
    self.hist={}
    self.inputFiles=[]
    self.chain = TChain("fEvent/event")
    #self.mode = inFileNames[0].split(".")[0].split("__")[-1]
    self.mode = mode
    self.nEventTotal = 0
    self.nPreCut = 0
    self.ev_info = 0
    for inFileName in inFileNames:
      f = TFile(inFileName)
      if f == None: continue
      tree = f.Get("fEvent/event")
      for entry in tree :
        count = len(entry.pseudoTopJet_m)
        if ( count ==0) : self.isMC = False
        else : self.isMC = True
        break
      hNEvent = f.Get("fEvent/hNEvent")
      if hNEvent == None: continue
      self.nEventTotal += hNEvent.GetBinContent(1)
      self.chain.Add(inFileName)
      if self.isMC: self.scale = max(1, self.nEventTotal)
    self.outFile = TFile(outFileName, "RECREATE")
    self.outDir = self.outFile
    self.outDir.cd()
    self.HistBooking()
    self.hNEvent = TH1F("step","step",7,0,7)
    self.hNEvent.GetXaxis().SetBinLabel(1,"Total")
    self.hNEvent.GetXaxis().SetBinLabel(2,"PreCut")

    self.hWeight = TH1F("weight_step","Weighted nPassed",7,0,7)
    self.hWeight.GetXaxis().SetBinLabel(1,"Total")
    self.hWeight.GetXaxis().SetBinLabel(2,"PreCut")
    
    for x in range(5) :
      self.hNEvent.GetXaxis().SetBinLabel(x+3,"S%d"%(x+1))
      self.hWeight.GetXaxis().SetBinLabel(x+3,"S%d"%(x+1))

    self.hNEvent.Fill(0,self.nEventTotal)
    self.hWeight.Fill(0,self.nEventTotal)

  def addH1( self, name, title, binx, xmin, xmax) :
    hist = TH1F(name, title, binx, xmin, xmax)
    self.hist[name] = [hist.Clone(),hist.Clone(),hist.Clone(),hist.Clone(),hist.Clone()]

  def HistBooking(self) :
    self.outFile.mkdir("S1")
    self.outFile.mkdir("S2")
    self.outFile.mkdir("S3")
    self.outFile.mkdir("S4")
    self.outFile.mkdir("S5")

    self.addH1("nMuon","Number of Muons",10,0,10)
    self.addH1("nJpsi","Number of J/#psi meson",10,0,10)

    self.addH1("JPsiMass","JPsi Mass;J/#psi mass [GeV];Events",20,3.0,3.2)
    self.addH1("JPsiPt","JPsi Pt;J/#psi Pt [GeV];Events",28,0,140.)
    self.addH1("JPsiEta", "JPsi #eta;J/#psi #eta ;Events", 25, -2.5, 2.5)
    self.addH1("JPsiPhi", "JPsi #phi;J/#psi #phi ;Events", 100, -TMath.Pi(), TMath.Pi())
    self.addH1("JPsil3D", "JPsidlPV;3D distance PV-J/#psi vertex [cm];Events", 22,0,2.2)
    self.addH1("JPsiMinDR", "JPsiJetMinDR;#Delta R(J/#psi-jet) min;Events", 20,0.0,2.0)
    self.addH1("JPsivProb","JPsivProb;J/#psi vertex prob.;Events", 10, 0.0, 1)

    self.addH1("l1JpsiMass","Lepton + J/#psi Mass; l+J/#psi Mass; Gev/c^2",100,0,100)
    self.addH1("l2JpsiMass","Lepton + J/#psi Mass; l+J/#psi Mass; Gev/c^2",100,0,100)

  def FillHist( self, ev, passed) :
    weight = ev.puWeight
    jpsi_list = self.ev_info.jpsi_list
    lep1 = self.ev_info.lep1
    lep2 = self.ev_info.lep2
    for i in range(passed) :
      self.hist["nJpsi"][i].Fill( len( self.ev_info.jpsi_list),weight )
      self.hist["nMuon"][i].Fill( len( self.ev_info.muon_list),weight )
      self.hNEvent.Fill( i+2.5 )
      self.hWeight.Fill( i+2.5, weight )
      if ( len(jpsi_list) > 0) : print "passed : ",passed," jpsi : ",len(jpsi_list)
      for jpsi in jpsi_list :
        self.hist["JPsiMass"][i].Fill( jpsi.M() )
        self.hist["JPsiPt"][i].Fill( jpsi.Pt() )
        self.hist["JPsiEta"][i].Fill( jpsi.Eta() )
        self.hist["JPsiPhi"][i].Fill( jpsi.Phi() )
        self.hist["JPsil3D"][i].Fill( jpsi.l3D )
        self.hist["JPsiMinDR"][i].Fill( jpsi.minDR)
        self.hist["JPsivProb"][i].Fill( jpsi.vProb)
        self.hist["l1JpsiMass"][i].Fill( (jpsi+lep1).M() )
        self.hist["l2JpsiMass"][i].Fill( (jpsi+lep2).M() )

  def process( self) :
    for ev in self.chain :
      self.ev_info = EventContent(ev,self.mode) 
      lep_list  = self.ev_info.lep_list
      cleanedJet = self.ev_info.cleanedJet_list
      jpsi_list = self.ev_info.jpsi_list

      if ( len( lep_list ) <2 ) : continue
      lep1 = lep_list[0]
      max_passed = 0
      for lep2 in lep_list[1:] :
        cf = CutFlow( lep1, lep2 )
        passed = 0
        if ( not cf.Step1() ) : 
          passed = 0
        elif ( not cf.Step2() ) : 
          passed = 1
        elif ( not cf.Step3(len(cleanedJet )) ) : 
          passed = 2
        elif ( not cf.Step4( jpsi_list ) )  : 
          passed = 3
        elif ( not cf.Step5( jpsi_list ) ) : 
          passed = 4
        else :
          passed = 5
        if ( passed > max_passed) : max_passed = passed
  
      self.hNEvent.Fill( 1.5 )
      self.hWeight.Fill( 1.5 , ev.puWeight )
      self.FillHist( ev, max_passed) 

    self.Write()

  def Write(self) :
    self.hNEvent.Write()
    self.hWeight.Write()
    for i in range(5) :
      self.outFile.cd("S%d"%(i+1))
      for name in self.hist.keys() :
        self.hist[name][i].Write()

  def Print(self) :
    print self.inputFiles
    print self.mode
    print self.scale
    print self.outFile



if __name__ == "__main__" :
  #ntuples = ["ntuple/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola__MuMu.root"]
  ntuples = ["ntuple/WW_TuneZ2star_8TeV_pythia6_tauola__MuMu.root"]
  ana = JpsiAna(ntuples,"MuMu","hist.root")

  ana.process()


