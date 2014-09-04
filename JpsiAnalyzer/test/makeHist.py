#!/usr/bin/env python
from ROOT import *
import os
from NtupleAnalyzer import *
import multiprocessing

def process( sample, hltPath,files, weightVar ='puWeight') :
  print "Making histogram %s"%sample
  ana = NtupleAnalyzer( hltPath,files,'hist/%s__%s.root'%(sample,hltPath) )
  #print ana
  ana.setWeightVar(weightVar)
  ana.setPrecut(hltPath)

  #cut_s0="1"
  cut_s1="1"
  cut_s2="1"
  cut_s3 = "jets_pt[0] >=30"
  cut_s4="@jpsiMuMu_pt.size()>=1 && jpsiMuMu_m>3.0 && jpsiMuMu_m<3.2"
  cut_s5="jpsiMuMu_l3D<2.0 && jpsiMuMu_jetDR<0.5 && jpsiMuMu_vProb>0.001"
  if ( hltPath == "HLTMuMu" ) :
    cut_s1 = "muons_pt[0]>20. && muons_pt[1]>20. && muons_relIso[0]<0.15 && muons_relIso[1]<0.15"
    cut_s2 = "1"
  elif ( hltPath == "HLTElEl") :
    cut_s1 = "electrons_pt[0]>20. && electrons_pt[1]>20. && electrons_relIso[0]<0.15 && electrons_relIso[1]<0.15"
    cut_s2 = "1"
  elif ( hltPath == "HLTMuEG" ) :
    cut_s1 = "muons_pt[0]>20. && muons_relIso[0]<0.15 && electrons_pt[0]>20. && electrons_relIso[0]<0.15"
    cut_s2 = "1"
      
  #cut_s1 = "muons_pt[0]>20 && muons_relIso[0]<0.15 && muons_pt[1]>20 && muons_relIso[1]<0.15"    
  cut_s1 = "1"    
  ana.addH1("f_electron_pt","electrons_pt[0]","Leading Electron pT",100,0. ,200. )
  ana.addH1("s_electron_pt","electrons_pt[1]","Next Leading Electron pT",100,0. ,200. )
  ana.addH1("electrons_pt","electrons_pt","Electron pT",100,0. ,200. )

  ana.addH1("f_muon_pt","muons_pt[0]","Leading Muon pT",100,0. ,200. )
  ana.addH1("s_muon_pt","muons_pt[1]","Next Leading Muon pT",100,0. ,200. )
  ana.addH1("muons_pt","muons_pt","Muon pT",100,0. ,200. )

  

  ana.addH1("jpsiMuMu_pt","jpsiMuMu_pt","Jpsi pT from MuMu ",100,0. ,200. )
  ana.addH1("nJpsi","@jpsiMuMu_pt.size()","# of Jpsi from MuMu ",10,0,10 )
  ana.addH1("jpsi_mass","jpsis_m","J/#psi mass (GeV/c^{2})",20,3.0,3.2);

  ana.addH1("nVertex", "nVertex", "nVertex;Vertex multiplicity;Events", 60, 0, 60)

  histlist = "f_electron_pt, s_electron_pt, f_muon_pt, s_muon_pt, electrons_pt,muons_pt,nVertex,jpsiMuMu_pt,nJpsi"

  #ana.addCutStep("S0", cut_s0, histlist)
  ana.addCutStep("S1", cut_s1, histlist)
  ana.addCutStep("S2", cut_s2, histlist)
  ana.addCutStep("S3", cut_s3, histlist)
  ana.addCutStep("S4", cut_s4, histlist)
  ana.addCutStep("S5", cut_s5, histlist)
  ana.process()

if __name__ == '__main__' :
  ntuple_dir = '/pnfs/user/kraft_data/'
  mc_dir = ntuple_dir+'/MC/'
  rd_dir = ntuple_dir+'/RD/'

  samples ={}
  dirs = os.listdir(mc_dir)
  for dir in dirs :
    filename = mc_dir+'/'+dir+'/ntuple.root'
    if ( os.path.exists( filename ) ) :
      samples[dir] =  [filename]

  dirs = os.listdir(rd_dir)
  for dir in dirs :
    filename = rd_dir+'/'+dir+'/ntuple.root'
    if ( os.path.exists( filename ) ) :
      samples[dir] =  [filename]

  #print samples

  ## for test,
  #samples ={'default':['/pnfs/user/kraft_data/sample/ntuple_mc.root']}
  modes = ["HLTMuMu","HLTElEl","HLTMuEG"]




  #for mode in modes :
  p = multiprocessing.Pool(multiprocessing.cpu_count())
  for key in samples.keys():
    sample = key
    files = samples[key]
    for mode in modes :
      p.apply_async(process, [sample, mode, files])
      pass
  p.close()
  p.join() 

  for sample in samples :
    if 'Run20' in sample : continue
    cmd = ("hadd -f hist/%s__All.root hist/%s__HLTMuMu.root hist/%s__HLTElEl.root hist/%s__HLTMuEG.root" % (sample, sample, sample, sample))
    os.system(cmd)
    break
  for sample in samples :
    if('Run20' in sample ):  
      cmd1 =("hadd -f hist/Run2012__HLTElEl.root hist/DoubleElectron_Run2012*-22Jan2013__HLTElEl.root")
      cmd2 =("hadd -f hist/Run2012__HLTMuMu.root hist/DoubleMu_Run2012*-22Jan2013__HLTMuMu.root")
      cmd3 =("hadd -f hist/Run2012__HLTMuEG.root hist/MuEG_Run2012*-22Jan2013__HLTMuEG.root")
      cmd4 =("hadd -f hist/Run2012__All.root hist/Run2012__HLTMuMu.root hist/Run2012__HLTElEl.root hist/Run2012__HLTMuEG.root")
      
      os.system( cmd1 ) 
      os.system( cmd2 ) 
      os.system( cmd3 ) 
      os.system( cmd4 )
      break 



