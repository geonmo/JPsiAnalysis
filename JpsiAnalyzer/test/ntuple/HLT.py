#!/usr/bin/env python

from ROOT import *
import os
#file = TFile("/pnfs/user/kraft_data/MC/DYJetsToLL_M-10To50filter_8TeV-madgraph/ntuple_20140827.root")
datasets=[]
dir_mc = "/pnfs/user/kraft_data/MC"
for x in os.listdir(dir_mc) :
  datasets.append(dir_mc+"/"+x+"/ntuple.root")
dataset_dict={}
for dataset in datasets :
  name = dataset.split('/')[-2]
  dataset_dict[name] = dataset

for key in dataset_dict.keys()[:1] :
  file = TFile(dataset_dict[key])
  tree = file.Get("fEvent/event")
  #print key,dataset_dict[key]

  filename = key+"__MuMu"+".root"
  outfile = TFile( filename,"RECREATE")
  ntuple1 = tree.CopyTree("HLTMuMu==1&& @muons_pt.size()>=2")
  ntuple1.Write()
  outfile.Close()

  filename = key+"__ElEl"+".root"
  outfile = TFile("DYElEl.root","RECREATE")
  ntuple2 = tree.CopyTree("HLTElEl==1 && @electrons_pt.size() >=2")
  ntuple2.Write()
  outfile.Close()

  filename = key+"__MuEl"+".root"
  outfile = TFile(filename,"RECREATE")
  ntuple3 = tree.CopyTree("HLTMuEG==1 && @electrons_pt.size() >=1&&@muons_pt.size()>=1")
  ntuple3.Write()
  outfile.Close()

