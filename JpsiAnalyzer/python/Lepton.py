#!/usr/bin/env python
from ROOT import *
class Lepton(TLorentzVector) :
    def __init__( self, pt, eta, phi, m, q, relIso, type , isLoose, mva) :
      TLorentzVector.__init__(self)
      self.SetPtEtaPhiM( pt, eta, phi, m)
      self.q = q
      self.relIso = relIso
      self.type = type
      self.electron_mva = mva
      self.isLoose = isLoose
    def valid( self) :
      if ( self.Pt() >20 and fabs(self.Eta()) < 2.4 and self.relIso<0.15) :
        if( self.type == "m" ) :
            return True
        elif ( self.type == "e" ) :
          if ( self.electron_mva > 0.5 ) :
            return True
          else :
            return False
        else :
            print "??"
            return False
      else : 
        return False
