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
    self.nJpsi = [ TH1F(), TH1F(), TH1F(), TH1F(), TH1F() ]
    self.nMuon = [ TH1F(), TH1F(), TH1F(), TH1F(), TH1F() ]
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

  def addHist( self, hist) :
    self.hist[name] = hist

  def HistBooking(self) :
    self.outFile.mkdir("S1")
    self.outFile.mkdir("S2")
    self.outFile.mkdir("S3")
    self.outFile.mkdir("S4")
    self.outFile.mkdir("S5")

    hist_nJpsi = TH1F("nJpsi","# of J/#psi meson",10,0,10)
    hist_nMuon = TH1F("nMuon","# of Muon",10,0,10)
    for i in range(5) :
      self.nJpsi[i] = hist_nJpsi.Clone()
      self.nMuon[i] = hist_nMuon.Clone()
      self.outFile.cd()

  def FillHist( self, ev, passed) :
    weight = ev.puWeight
    jpsi_list = self.ev_info.jpsi_list
    for i in range(passed) :
      self.nJpsi[i].Fill( len( self.ev_info.jpsi_list),weight )
      self.nMuon[i].Fill( len( self.ev_info.muon_list),weight )
      self.hNEvent.Fill( i+2.5 )
      self.hWeight.Fill( i+2.5, weight )
      if( passed ==5 ) : 
        print "passed 5!  ",i+2.5 

  """ 
  def InitEvent( self, ev ) :
    lep_list = []
    muon_list =[]
    elec_list =[]
    jet_list = []
    jpsi_list =[]
    jpsimm_list =[]
    jpsiee_list =[]
    for i in range( len( ev.muons_pt) ) :
      temp_muon = Lepton( ev.muons_pt[i], ev.muons_eta[i], ev.muons_phi[i], ev.muons_m[i], ev.muons_q[i], ev.muons_relIso[i], 'm',ev.muons_isLoose[i], 1)
      muon_list.append( temp_muon )
      lep_list.append( temp_muon ) 
    
    for i in range( len( ev.electrons_pt) ) :
      temp_elec =  Lepton( ev.electrons_pt[i], ev.electrons_eta[i], ev.electrons_phi[i], ev.electrons_m[i], ev.electrons_q[i], ev.electrons_relIso[i], 'm',1, ev.electrons_mva[i])
      elec_list.append( temp_elec)
      lep_list.append( temp_elec)
    for i in range( len ( ev.jets_pt) ) :
      jet_list.append( Jet(ev.jets_pt[i], ev.jets_eta[i], ev.jets_phi[i], ev.jets_m[i], ev.jets_bTagCSV[i]))
   
    for i in range( len( ev.jpsiMuMu_pt) ) :
      temp_jpsi = Jpsi( ev.jpsiMuMu_pt[i], ev.jpsiMuMu_eta[i], ev.jpsiMuMu_phi[i], ev.jpsiMuMu_m[i], ev.jpsiMuMu_vProb[i], ev.jpsiMuMu_l3D[i])
      jpsi_list.append(temp_jpsi)
      jpsimm_list.append(temp_jpsi)

    for i in range( len( ev.jpsiElEl_pt) ) :
      temp_jpsi =  Jpsi( ev.jpsiElEl_pt[i], ev.jpsiElEl_eta[i], ev.jpsiElEl_phi[i], ev.jpsiElEl_m[i], ev.jpsiElEl_vProb[i], ev.jpsiElEl_l3D[i])
      jpsi_list.append( temp_jpsi)
      jpsiee_list.append( temp_jpsi)

    return muon_list, elec_list , jet_list, jpsimm_list, jpsiee_list

  """

  def process( self) :
    for ev in self.chain :
      self.ev_info = EventContent(ev) 
      #muon_list, elec_list, jet_list, jpsimm_list, jpsiee_list = self.InitEvent( ev )
      lep_list  = self.ev_info.lep_list
      jpsi_list = self.ev_info.jpsi_list
      cleanedJet = self.ev_info.cleanedJet_list
      if ( len( lep_list ) <2 ) : continue
      lep1 = lep_list[0]
      #ev_flag = Flag()
      max_passed = 0
      for lep2 in lep_list[1:] :
        cf = CutFlow( lep1, lep2 )
        passed = 0
        if ( cf.Step1() ) : passed = 1
        if ( cf.Step1() and cf.Step2() ) : passed = 2
        if ( cf.Step1() and cf.Step2() and cf.Step3(len(cleanedJet )) ) : passed = 3
        if ( cf.Step1() and cf.Step2() and cf.Step3(len(cleanedJet )) and cf.Step4( jpsi_list ) )  : passed = 4
        if ( cf.Step1() and cf.Step2() and cf.Step3(len(cleanedJet )) and cf.Step4( jpsi_list ) and cf.Step5( jpsi_list ) ) : passed = 5
        
        if ( passed > max_passed) : max_passed = passed
  
      if ( max_passed ==5 ) : print "event : ",ev.event,"  is passed to step 5"
 
      self.hNEvent.Fill( 1 )
      self.hWeight.Fill( 1, ev.puWeight )
      self.FillHist( ev, max_passed) 

    self.Write()

  def Write(self) :
    self.hNEvent.Write()
    self.hWeight.Write()
    for i in range(5) :
      self.outFile.cd("S%d"%(i+1))
      self.nMuon[i].Write()
      self.nJpsi[i].Write()

  def Print(self) :
    print self.inputFiles
    print self.mode
    print self.scale
    print self.outFile



if __name__ == "__main__" :
  #ntuples = ["ntuple/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola__MuMu.root"]
  ntuples = ["ntuple/WW_TuneZ2star_8TeV_pythia6_tauola__MuMu.root"]
  ana = JpsiAna(ntuples,"MuMu","hist.root")

  #ana.Print()
  ana.process()
  #ana.Write()


