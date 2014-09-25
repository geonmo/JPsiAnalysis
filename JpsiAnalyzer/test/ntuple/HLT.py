#!/usr/bin/env python

from ROOT import *
import os
import multiprocessing

def process( dataset, ntuple_path, channel ) :
  expr = ""
  if ( channel == "MuMu") :
    expr = "@muons_pt.size()>=2"
  elif ( channel == "ElEl") :
    expr = "@electrons_pt.size() >=2"
  elif ( channel == "MuEG") :
    expr = "@electrons_pt.size() >=1&&@muons_pt.size()>=1" 

  file = TFile(ntuple_path)
  filename = dataset+"__"+channel+".root"
  outfile = TFile( filename,"RECREATE")
  outfile.mkdir("fEvent")
  outfile.cd("fEvent")
  tree = file.Get("fEvent/event")
  hNEvent = file.Get("fEvent/hNEvent")
  ntuple = tree.CopyTree(expr)
  ntuple.Write()
  hNEvent.Write()
  outfile.Close()

#file = TFile("/pnfs/user/kraft_data/MC/DYJetsToLL_M-10To50filter_8TeV-madgraph/ntuple_20140827.root")

if __name__ == '__main__' : 

  datasets=[]

  dir_mc = "/pnfs/user/kraft_data/MC"
  for x in os.listdir(dir_mc) :
    datasets.append(dir_mc+"/"+x+"/ntuple.root")

  dir_rd = "/pnfs/user/kraft_data/RD"
  for x in os.listdir(dir_rd) :
    datasets.append(dir_rd+"/"+x+"/ntuple.root")

  dataset_dict={}
  channels = ["MuMu","ElEl","MuEl"]
  for dataset in datasets :
    name = dataset.split('/')[-2]
    dataset_dict[name] = dataset

  p = multiprocessing.Pool(multiprocessing.cpu_count())
  count =0 
  for key in dataset_dict.keys() :
    sample = key
    ntuple_path = dataset_dict[key]
    #print count
    #count=count+1
    for channel in channels :
      p.apply_async(process,[sample,ntuple_path,channel])
      print sample,ntuple_path,channel
      pass
  p.close()
  p.join()
