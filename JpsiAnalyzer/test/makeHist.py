#!/usr/bin/env python
from ROOT import *
import os
from NtupleAnalyzer import *
import multiprocessing

def process( sample, mode,files, weightVar ='puWeight') :
  print "Making histogram %s"%sample
  ana = NtupleAnalyzer( mode, files,'hist/%s__%s.root'%(sample,mode) )
  ana.setWeightVar(weightVar)

  #cut_s0="1"
  cut_s1="1"
  cut_s2="1"
  #cut_s3 = "jets_pt[0] >=30"
  #cut_s4="@jpsiMuMu_pt.size()>=1 && jpsiMuMu_m>3.0 && jpsiMuMu_m<3.2"
  #cut_s5="jpsiMuMu_l3D<2.0 && jpsiMuMu_jetDR<0.5 && jpsiMuMu_vProb>0.001"
  if ( mode == "MuMu" ) :
    cut_s1 = "muons_pt[0]>20. && muons_pt[1]>20. && muons_relIso[0]<0.15 && muons_relIso[1]<0.15"
    cut_s2 = "1"
  elif ( mode == "ElEl") :
    cut_s1 = "electrons_pt[0]>20. && electrons_pt[1]>20. && electrons_relIso[0]<0.15 && electrons_relIso[1]<0.15"
    cut_s2 = "1"
  elif ( mode == "MuEl" ) :
    cut_s1 = "muons_pt[0]>20. && muons_relIso[0]<0.15 && electrons_pt[0]>20. && electrons_relIso[0]<0.15"
    cut_s2 = "1"
      
  #cut_s1 = "muons_pt[0]>20 && muons_relIso[0]<0.15 && muons_pt[1]>20 && muons_relIso[1]<0.15"    
  #cut_s1 = "1"    
  ana.addH1("f_electron_pt","electrons_pt[0]","Leading Electron pT",100,0. ,200. )
  ana.addH1("s_electron_pt","electrons_pt[1]","Next Leading Electron pT",100,0. ,200. )
  ana.addH1("electrons_pt","electrons_pt","Electron pT",100,0. ,200. )

  ana.addH1("f_muon_pt","muons_pt[0]","Leading Muon pT",100,0. ,200. )
  ana.addH1("s_muon_pt","muons_pt[1]","Next Leading Muon pT",100,0. ,200. )
  ana.addH1("muons_pt","muons_pt","Muon pT",100,0. ,200. )

  

  ana.addH1("jpsiMuMu_pt","jpsiMuMu_pt","Jpsi pT from MuMu ",100,0. ,200. )
  ana.addH1("nJpsi","@jpsiMuMu_pt.size()","#  f Jpsi from MuMu ",10,0,10 )
  ana.addH1("jpsi_mass","jpsis_m","J/#psi mass (GeV/c^{2})",20,3.0,3.2);

  ana.addH1("nVertex", "nVertex", "nVertex;Vertex multiplicity;Events", 60, 0, 60)

  histlist = "f_electron_pt, s_electron_pt, f_muon_pt, s_muon_pt, electrons_pt,muons_pt,nVertex,jpsiMuMu_pt,nJpsi"

  #ana.addCutStep("S0", cut_s0, histlist)
  ana.addCutStep("S1", cut_s1, histlist)
  ana.addCutStep("S2", cut_s2, histlist)
  #ana.addCutStep("S3", cut_s3, histlist)
  #ana.addCutStep("S4", cut_s4, histlist)
  #ana.addCutStep("S5", cut_s5, histlist)
  ana.process()

if __name__ == '__main__' :
  samples = {}
  modes = ["MuMu","MuEl","ElEl"]
  for mode in modes  :
    for f in os.listdir("ntuple"):
      if len(f) <12 : continue
      if f[-11:] != ("__%s.root"%mode) : continue
      s = f.replace("__%s.root"%mode,"")
      sampleName = (s, mode)
      if sampleName not in samples: samples[sampleName] = []
      samples[sampleName].append("ntuple/%s" % f)
  
  #print samples

  p = multiprocessing.Pool(multiprocessing.cpu_count())
  for key in samples.keys() :
    sample = key
    files = samples[key]
    for mode in modes :
      p.apply_async(process, [sample[0], mode, files])
      #print  sample[0], mode, files
      pass
  p.close()
  p.join() 
  """
  for sample, mode in samples.keys():
    if 'Run20' in sample: continue
    os.system("hadd -f hist/%s__All.root hist/%s__MuMu.root hist/%s__ElEl.root hist/%s__MuEl.root" % (sample, sample, sample, sample))
  os.system("hadd -f hist/Run2012__ElEl.root hist/DoubleElectron_Run2012*-22Jan2013__ElEl.root")
  os.system("hadd -f hist/Run2012__MuMu.root hist/DoubleMu_Run2012*-22Jan2013__MuMu.root")
  os.system("hadd -f hist/Run2012__MuEl.root hist/MuEG_Run2012*-22Jan2013__MuEl.root")
  os.system("hadd -f hist/Run2012__All.root hist/Run2012__MuMu.root hist/Run2012__ElEl.root hist/Run2012__MuEl.root")
  print "END"
  """
