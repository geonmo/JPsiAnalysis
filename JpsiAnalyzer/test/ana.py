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
  samples = {}
  modes = ["MuMu","MuEl","ElEl"]
  print "loop"
  for mode in modes  :
    for f in os.listdir("ntuple"):
      if len(f) <12 : continue
      if f[-11:] != ("__%s.root"%mode) : continue
      s = f.replace("__%s.root"%mode,"")
      sampleName = (s, mode)
      if sampleName not in samples: samples[sampleName] = []
      samples[sampleName].append("ntuple/%s" % f)
  
  p = multiprocessing.Pool(multiprocessing.cpu_count())
  for key in samples.keys() :
    sample = key
    files = samples[key]
    p.apply_async(process, [sample[0], sample[1], files])
  p.close()
  p.join() 
