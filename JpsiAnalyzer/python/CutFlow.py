#!/usr/bin/env python
from ROOT import *
class CutFlow :
  def __init__(self, lep1, lep2 ) :
    self.lep1 = lep1
    self.lep2 = lep2
    self.zBoson = lep1+lep2
  def Print(self) :
    print self.lep1.M(),"  ",self.lep2.M(),"  ",self.zBoson.M()
  def Step1( self ) :
    if ( self.lep1.valid() and self.lep2.valid() and self.zBoson.M() >20 and int(self.lep1.q*self.lep2.q) == -1 ) :
      return True
    else :
      return False
  def Step2( self ) :
    if ( self.lep1.type == self.lep2.type ) :
      if ( self.zBoson.M() < 76 or self.zBoson.M() > 106 ) :
        return True
      else :
        return False
    else :
      return True
  def Step3( self, nJets ) :
    if ( nJets >=1 ) :
      return True
    else :
      return False
  def Step4( self, jpsi_list) :
    nJpsi = len(jpsi_list) 
    if nJpsi ==0 :
      return False
    else :
      flag = False
      for jpsi in jpsi_list :
        if( jpsi.M()>3.0 and jpsi.M()<3.2 and jpsi.minDR<0.5) :
          flag = True
      return flag
    
  def Step5( self, jpsi_list ) :
    flag = False
    for jpsi in jpsi_list :
      if ( jpsi.vProb>0.001 and jpsi.l3D < 2 and jpsi.l3D>0.02 ) :
      #if ( jpsi.vProb>0.001 and jpsi.l3D < 2 ) :
        flag = True 
    return flag
