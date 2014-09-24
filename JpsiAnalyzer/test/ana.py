#!/usr/bin/env python
import xml.etree.ElementTree as ET
# set ntuple lists.
from JPsiAnalysis.JpsiAnalyzer.Lepton import Lepton
tree = ET.parse("../data/sample.xml")

root = tree.getroot()

#root = ET.fromstring("signal")

for child in root :
  print child.tag, child.attrib
  for subchild in child :
    print subchild.tag, subchild.attrib,subchild.text

