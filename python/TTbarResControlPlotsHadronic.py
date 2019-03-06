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
    def __init__(self, htCut=1100., minMSD=110., maxMSD=240., tau32Cut=0.6, ak8PtMin=400., bdisc=0.7):
        """ Initialization for the module 
        """
        self.htCut = htCut
        self.minMSD = minMSD
        self.maxMSD = maxMSD
        self.tau32Cut = tau32Cut
        self.ak8PtMin = ak8PtMin
        self.bdisc = bdisc
        self.writeHistFile = True
        
    def beginJob(self, histFile, histDirName):
        """Book control histograms and the predictions for the background.

        The background is data-driven and estimated by weighting the 1-tag region
        by the mistag rate to extrapolate to the 2-tag region. 
        """
        Module.beginJob(self, histFile, histDirName)
        self.addObject ( ROOT.TH1F('h_ak4ht',    'h_ak4ht',    100, 0, 5000) )
        self.addObject ( ROOT.TH1F('h_ak8pt',    'h_ak8pt',    100, 0, 2500) )
        self.addObject ( ROOT.TH1F('h_ak8m',     'h_ak8m',     100, 0, 1000) )
        self.addObject ( ROOT.TH1F('h_ak8msd',   'h_ak8msd',   100, 0, 1000) )
        self.addObject ( ROOT.TH1F('h_ak8m_mod', 'h_ak8m_mod', 100, 0, 1000) )
        self.addObject ( ROOT.TH1F('h_ak8m_modb','h_ak8m_modb',100, 0, 1000) )
        self.addObject ( ROOT.TH1F('h_ak8tau32', 'h_ak8tau32', 100, 0, 1.0) )
        self.addObject ( ROOT.TH1F('h_ak8n3b1',  'h_ak8n3b1',  100, 0, 5.0) )
        self.addObject ( ROOT.TH1F('h_mttbar',   'h_mttbar',   100, 0, 5000) )

            
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
        ak8Jets = [ x for x in self.ak8JetsColl if x.jetId > 0 and x.pt > self.ak8PtMin ]
        if len(ak8Jets) < 2 :
            return False


        # Apply HT cut to ensure we are on the trigger plateau
        ht = 0.0
        if hasattr( event, "HT_pt"):
            ht = event.HT_pt
        else :
            ht = sum([ event.Jet_pt[i] for i in range(event.nJet) ])

        self.h_ak4ht.Fill( ht, weight )
        if ht < self.htCut :
            return False
        ##print 'passed HT cut'

        
        for jet in ak8Jets[0:1] :
            tau32 = jet.tau3 / jet.tau2 if jet.tau2 > 0.0 else 0.0
            self.h_ak8pt.Fill( jet.p4().Perp(), weight )
            if jet.p4().Perp() > self.ak8PtMin :
                
                self.h_ak8msd.Fill( jet.msoftdrop, weight )
                if jet.msoftdrop > self.minMSD and jet.msoftdrop < self.maxMSD : 
                    self.h_ak8tau32.Fill( tau32, weight )
                    self.h_ak8n3b1.Fill( jet.n3b1, weight )

        ttbarP4 =  ak8Jets[0].p4() + ak8Jets[1].p4()
        self.h_mttbar.Fill( ttbarP4.M(), weight )

        indices = [0,1]
        random.shuffle( indices )
        itagJet = indices[0]
        iprobeJet = indices[1]
        tau32 = ak8Jets[itagJet].tau3 / ak8Jets[itagJet].tau2 if ak8Jets[itagJet].tau2 > 0.0 else 0.0
        if self.minMSD < ak8Jets[itagJet].msoftdrop < self.maxMSD and tau32 < self.tau32Cut :
            self.h_ak8m_mod.Fill( ak8Jets[iprobeJet].mass )
            if ak8Jets[itagJet].btagCSVV2 < self.bdisc:
                self.h_ak8m_modb.Fill( ak8Jets[iprobeJet].mass )
        

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbarreshad = lambda : TTbarResControlPlotsHadronic() 
