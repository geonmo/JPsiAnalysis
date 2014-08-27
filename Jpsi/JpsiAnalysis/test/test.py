#!/usr/bin/env python
from ROOT import *
file = TFile("/pnfs/user/kraft_data/sample/ntuple_mc.root")
tree = file.Get("fEvent/event")
for entry in tree :
  c =  len(entry.pseudoTopJet_eta)
  if ( c == 0 ) :
    print "DATA"
    break
  else :
    print "MC"
    break
