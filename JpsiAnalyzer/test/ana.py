#!/usr/bin/env python

from ROOT import *
import os
from JpsiAna import *
import multiprocessing

def process( sample, mode, files, weightVar ='puWeight') :
  print "Making histogram %s"%sample
  print files, 'hist/%s__%s.root'%(sample,mode)
  ana = JpsiAna( files,mode, 'hist/%s__%s.root'%(sample,mode) )
  ana.process()

if __name__ == '__main__' :
  ntuple_dir= "/cms/data/xrd/store/user/geonmo/ntuple_RD_new/"
  samples = {}
  modes = ["MuMu","MuEl","ElEl"]
  for mode in modes :
    for dir in os.listdir(ntuple_dir) :
      sampleName = (dir, mode)
      if sampleName not in samples :
        samples[sampleName] = []
      for x in os.listdir( ntuple_dir+dir) :
        samples[sampleName].append(ntuple_dir+dir+'/'+x)
  print "loop"
  print samples

  p = multiprocessing.Pool(multiprocessing.cpu_count())
  for key in samples.keys() :
    sample = key
    files = samples[key]
    p.apply_async(process, [sample[0], sample[1], files])
  p.close()
  p.join()
   
  for sample, mode in samples.keys():
    if 'Run20' in sample: continue
    os.system("hadd -f hist/%s__All.root hist/%s__MuMu.root hist/%s__ElEl.root hist/%s__MuEl.root" % (sample, sample, sample, sample))
  os.system("hadd -f hist/Run2012__ElEl.root hist/DoubleElectron_Run2012*-22Jan2013__ElEl.root")
  os.system("hadd -f hist/Run2012__MuMu.root hist/DoubleMu_Run2012*-22Jan2013__MuMu.root")
  os.system("hadd -f hist/Run2012__MuEl.root hist/MuEG_Run2012*-22Jan2013__MuEl.root")
  os.system("hadd -f hist/Run2012__All.root hist/Run2012__MuMu.root hist/Run2012__ElEl.root hist/Run2012__MuEl.root")
