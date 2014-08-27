#!/usr/bin/env python
from ROOT import *
import os
from NtupleAnalyzer import *
import multiprocessing
"""
MC_dir = os.listdir("/pnfs/user/kraft_data/MC")
RD_dir = os.listdir("/pnfs/user/kraft_data/RD")
#RD_dir.remove('loop.py')
#MC_dir.remove('loop.py')

MC_TTbar_signal = []
MC_TTbar_other  = []
MC_Single_top = []
MC_Dibosons = []
MC_WJetToLNu =[]
MC_DY =[]

MC_mass =[]
for dataset in MC_dir :
	if ( dataset.find("mass") != -1 ) :
		MC_mass.append(dataset)


#print MC_dir
#print RD_dir
#print MC_mass
"""

def process( sample, hltPath,files, weightVar ='puWeight') :
  print "Making histogram %s"%sample
  ana = NtupleAnalyzer( hltPath,files,'hist/%s_%s.root'%(sample,hltPath) )
  print ana
  ana.setWeightVar(weightVar)
  #ana.setPrecut(hltPath)

  cut_s0="1"
  cut_s1=""
  if ( hltPath == "HLTMuMu" ) :
    cut_s1 = "muons_pt[0]>20. && muons_pt[1]>20. && muons_relIso[0]<0.15 && muons_relIso[1]<0.15"
  elif ( hltPath == "HLTElEl") :
    cut_s1 = "electrons_pt[0]>20. && electrons_pt[1]>20. && electrons_relIso[0]<0.15 && electrons_relIso[1]<0.15"
      
  #cut_s1 = "muons_pt[0]>20 && muons_relIso[0]<0.15 && muons_pt[1]>20 && muons_relIso[1]<0.15"    
  cut_s1 = "1"    
  ana.addH1("f_electron_pt","electrons_pt[0]","Leading Electron pT",100,0. ,200. )
  ana.addH1("s_electron_pt","electrons_pt[1]","Next Leading Electron pT",100,0. ,200. )
  ana.addH1("electrons_pt","electrons_pt","Electron pT",100,0. ,200. )

  ana.addH1("f_muon_pt","muons_pt[0]","Leading Muon pT",100,0. ,200. )
  ana.addH1("s_muon_pt","muons_pt[1]","Next Leading Muon pT",100,0. ,200. )
  ana.addH1("muons_pt","muons_pt","Muon pT",100,0. ,200. )

  ana.addH1("nVertex", "nVertex", "nVertex;Vertex multiplicity;Events", 60, 0, 60)

  ana.addCutStep("S0", cut_s0, "f_electron_pt, s_electron_pt, f_muon_pt, s_muon_pt, electrons_pt,muons_pt,nVertex")
  ana.addCutStep("S1", cut_s1, "f_electron_pt, s_electron_pt, f_muon_pt, s_muon_pt, electrons_pt,muons_pt,nVertex")
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
  print samples

  dirs = os.listdir(rd_dir)
  for dir in dirs :
    filename = rd_dir+'/'+dir+'/ntuple.root'
    if ( os.path.exists( filename ) ) :
      samples[dir] =  [filename]
  #print samples

  #samples ={'default':['/pnfs/user/kraft_data/sample/ntuple_mc.root']}
  modes = ["HLTMuMu","HLTElEl","HLTMuEG"]


  #for mode in modes :
  p = multiprocessing.Pool(multiprocessing.cpu_count())
  for key in samples.keys():
    sample = key
    files = samples[key]
    for mode in modes :
      print [sample,mode,files]
      p.apply_async(process, [sample, mode, files])
    #if 'QCD' not in sample and 'Run201' not in sample:
    #  p.apply_async(process, [sample+"puHi", mode, files, "puWeightUp"])
    #  p.apply_async(process, [sample+"puLo", mode, files, "puWeightDn"])
  p.close()
  p.join() 
