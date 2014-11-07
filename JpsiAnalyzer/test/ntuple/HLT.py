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
  elif ( channel == "MuEl") :
    expr = "@electrons_pt.size() >=1&&@muons_pt.size()>=1" 
  else : 
    return

  chain = TChain("fEvent/event")
  hist = None
  for i, x in enumerate(ntuple_path) :
    print "file : ",x
    f = TFile(x)
    if f == None : continue
    hNEvent =  f.Get("fEvent/hNEvent")
    if hNEvent == None : continue
    if hist == None  :
      hist = hNEvent.Clone() 
    else :
      hist.Add(hNEvent)
    chain.AddFile( x )
  f= TFile(ntuple_path[0])
  #hNEvent = f.Get("fEvent/hNEvent") 
  #hNEvent = chain.Get("fEvent/hNEvent")
  filename = dataset+"__"+channel+".root"
  outfile = TFile( filename,"RECREATE")
  outfile.mkdir("fEvent")
  outfile.cd("fEvent")
  ntuple = chain.CopyTree(expr)
  ntuple.Write()
  hist.Write()
  outfile.Close()

#file = TFile("/pnfs/user/kraft_data/MC/DYJetsToLL_M-10To50filter_8TeV-madgraph/ntuple_20140827.root")

if __name__ == '__main__' : 

  datasets=[]

  """
  dir_mc = "/cms/data/xrd/store/user/geonmo/ntuple_MC_new/"
  for x in os.listdir(dir_mc) :
    datasets.append(dir_mc+"/"+x+"/")
  """

  dir_rd = "/cms/data/xrd/store/user/geonmo/ntuple_RD_new/"
  for x in os.listdir(dir_rd) :
    datasets.append(dir_rd+"/"+x+"/")

  dataset_dict={}
  channels = ["MuMu","ElEl","MuEl"]
  for dataset in datasets :
    name = dataset.split('/')[-2]
    dataset_dict[name] = dataset

  p = multiprocessing.Pool(multiprocessing.cpu_count())
  count =0 
  for key in dataset_dict.keys() :
    sample = key
    path = dir_rd+"/"+sample
    ntuple_path = os.listdir( path)
    full_path =[]
    for ntuple_p in ntuple_path : 
      full_path.append( path+'/'+ntuple_p) 
    #print count
    #count=count+1
    for channel in channels :
      #print sample,ntuple_path,channel
      p.apply_async(process,[sample,full_path,channel])
      pass
  p.close()
  p.join()
