"""@TTbarResAnaHadronic Package to perform the data-driven mistag-rate-based ttbar hadronic analysis. 
"""

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetSysColl import JetSysColl, JetSysObj

import random
import itertools

"""@TTbarResControlPlotsHadronic Package to make simple control plots of the preselection
for the ttbar all hadronic analysis. 
"""
class TTbarResControlPlotsHadronic(Module):
    def __init__(self, htCut=1100., minMSD=110., maxMSD=240., tau32Cut=0.6, ak8PtMin=400., bdisc=0.7, isData=False, year='2016'):
        """ Initialization for the module 
        """
        self.htCut = htCut
        self.minMSD = minMSD
        self.maxMSD = maxMSD
        self.tau32Cut = tau32Cut
        self.ak8PtMin = ak8PtMin
        self.bdisc = bdisc
        self.writeHistFile = True
        self.isData = isData
        self.year=year
        
    def beginJob(self, histFile, histDirName):
        """Book control histograms and the predictions for the background.

        The background is data-driven and estimated by weighting the 1-tag region
        by the mistag rate to extrapolate to the 2-tag region. 
        """
        Module.beginJob(self, histFile, histDirName)
        self.addObject ( ROOT.TH1F('h_ak4ht',   'h_ak4ht',   25, 0, 5000) )
        self.addObject ( ROOT.TH1F('h_ak8pt',   'h_ak8pt',   25, 0, 2500) )
        self.addObject ( ROOT.TH1F('h_ak8msd',  'h_ak8msd',  25, 0, 500) )
        self.addObject ( ROOT.TH1F('h_ak8tau32','h_ak8tau32',25, 0, 1.0) )
        self.addObject ( ROOT.TH1F('h_ak8n3b1', 'h_ak8n3b1', 25, 0, 5.0) )
        self.addObject ( ROOT.TH1F('h_mttbar',  'h_mttbar',  25, 0, 5000) )

            
    def endJob(self):
        Module.endJob(self)
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
        
    def analyze(self, event):
        """Perform either the anti-tag and probe (mistag estimate) or double tag (signal region) selection.
        """
        weight = 1.0

        if hasattr( event, "Generator_weight") and abs( event.Generator_weight - 1.0) > 1e-3 :
            weight *= event.Generator_weight
            
        # Get the collections of AK4 and AK8 jets
        self.ak8JetsColl = Collection(event, "FatJet")

        # Select the jets that satisfy jet ID. 
        ak8Jets = [ x for x in self.ak8JetsColl if x.jetId > 0 ]
        if len(ak8Jets) < 2 :
            return False


        # Apply HT cut to ensure we are on the trigger plateau
        ht = 0.0
        if hasattr( event, "HT_pt"):
            ht = event.HT_pt
        else :
            for i in xrange( event.nJet ) :
                ht += event.Jet_pt[i]

        self.h_ak4ht.Fill( ht, weight )
        if ht < self.htCut :
            return False
        ##print 'passed HT cut'

        for jet in ak8Jets[0:1] : 
            self.h_ak8pt.Fill( jet.p4().Perp(), weight )
            if jet.p4().Perp() > 400. :
                
                self.h_ak8msd.Fill( jet.msoftdrop, weight )
                if jet.msoftdrop > 100. and jet.msoftdrop < 250. : 
                    self.h_ak8tau32.Fill( jet.tau3 / jet.tau2 if jet.tau2 > 0.0 else 0.0, weight )
                    self.h_ak8n3b1.Fill( jet.n3b1, weight )

        ttbarP4 =  ak8Jets[0].p4() + ak8Jets[1].p4()
        self.h_mttbar.Fill( ttbarP4.M(), weight )

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbarreshad = lambda : TTbarResControlPlotsHadronic() 
ttbarreshad_data = lambda : TTbarResControlPlotsHadronic(isData=True) 
