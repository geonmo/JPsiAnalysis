#!/usr/bin/env python
from ROOT import *
from JPsiAnalysis.JpsiAnalyzer.Lepton import Lepton
from JPsiAnalysis.JpsiAnalyzer.Jet import Jet
from JPsiAnalysis.JpsiAnalyzer.CutFlow import *
from JPsiAnalysis.JpsiAnalyzer.Jpsi import Jpsi
#from JPsiAnalysis.JpsiAnalyzer.EventContent import EventContent

class EventContent :
  def __init__(self, ev) :
    self.lep_list = []
    self.muon_list =[]
    self.elec_list =[]
    self.jet_list = []
    self.jpsi_list =[]
    self.jpsimm_list =[]
    self.jpsiee_list =[]
    self.cleanedJet_list=[]
    for i in range( len( ev.muons_pt) ) :
      temp_muon = Lepton( ev.muons_pt[i], ev.muons_eta[i], ev.muons_phi[i], ev.muons_m[i], ev.muons_q[i], ev.muons_relIso[i], 'm',ev.muons_isLoose[i], 1)
      self.muon_list.append( temp_muon )
      self.lep_list.append( temp_muon ) 
    
    for i in range( len( ev.electrons_pt) ) :
      temp_elec =  Lepton( ev.electrons_pt[i], ev.electrons_eta[i], ev.electrons_phi[i], ev.electrons_m[i], ev.electrons_q[i], ev.electrons_relIso[i], 'm',1, ev.electrons_mva[i])
      self.elec_list.append( temp_elec)
      self.lep_list.append( temp_elec)
    for i in range( len ( ev.jets_pt) ) :
      self.jet_list.append( Jet(ev.jets_pt[i], ev.jets_eta[i], ev.jets_phi[i], ev.jets_m[i], ev.jets_bTagCSV[i]))
   
    for i in range( len( ev.jpsiMuMu_pt) ) :
      temp_jpsi = Jpsi( ev.jpsiMuMu_pt[i], ev.jpsiMuMu_eta[i], ev.jpsiMuMu_phi[i], ev.jpsiMuMu_m[i], ev.jpsiMuMu_vProb[i], ev.jpsiMuMu_l3D[i])
      self.jpsi_list.append(temp_jpsi)
      self.jpsimm_list.append(temp_jpsi)

    for i in range( len( ev.jpsiElEl_pt) ) :
      temp_jpsi =  Jpsi( ev.jpsiElEl_pt[i], ev.jpsiElEl_eta[i], ev.jpsiElEl_phi[i], ev.jpsiElEl_m[i], ev.jpsiElEl_vProb[i], ev.jpsiElEl_l3D[i])
      self.jpsi_list.append( temp_jpsi)
      self.jpsiee_list.append( temp_jpsi)

    self.JetCleaning()
    self.jpsi_list = self.jpsimm_list+ self.jpsiee_list
    self.lep_list = self.muon_list + self.elec_list

  def JetCleaning( self ) :
    cleaned_jets =[]
    for jet in self.jet_list :
      jet_keep_flag = True
      for lep in self.lep_list : 
        if ( jet.DeltaR( lep ) < 0.5 ) :
          jet_keep_flag = False
      if( jet_keep_flag ) :
          cleaned_jets.append( jet )
    self.cleanedJet_list = cleaned_jets 
    
