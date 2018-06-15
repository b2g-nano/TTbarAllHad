"""@TTbarResTrigsHadronic Package to check triggers for ttbar hadronic analysis. 
"""

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

"""@TTbarResTrigsHadronic Package to check triggers for ttbar hadronic analysis. 


This is a simple trigger-level analysis that will compute the offline jet HT (either precomputed,
or on the fly if not available) as a function of different trigger acceptances. 
It will compute histograms to calculate the trigger turnon thresholds. 


"""
class TTbarResTrigsHadronic(Module):
    def __init__(self ):
        """ Initialization for the module 
        """
        self.writeHistFile = True
        self.trigTurnonList = {
            'HLT_AK8PFHT850_TrimMass50':'HLT_AK8PFHT900_TrimMass50',
            'HLT_PFHT890':'HLT_PFHT1050',
            }
        
    def beginJob(self, histFile, histDirName):
        """Book control histograms and the predictions for the background.

        The background is data-driven and estimated by weighting the 1-tag region
        by the mistag rate to extrapolate to the 2-tag region. 
        """
        Module.beginJob(self, histFile, histDirName)
        for itrig,jtrig in self.trigTurnonList.iteritems():
            self.addObject (ROOT.TH1F('h_ak4ht_' + itrig,   'h_ak4ht_' + itrig,   25, 0, 5000) )
            self.addObject (ROOT.TH1F('h_ak4ht_' + jtrig,   'h_ak4ht_' + jtrig,   25, 0, 5000) )
            
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
        # Select the jets that satisfy jet ID and mass requirements. 
        ak8_pts = [ event.FatJet_pt[i] for i in xrange(event.nFatJet) if event.FatJet_jetId[i] > 0 and abs(event.FatJet_eta[i]) < 2.5 and abs(event.FatJet_msoftdrop[i]) > 50.]
        if len(ak8_pts) < 2 :
            return False

        # Calculate HT. Get it from the event if it is there, otherwise calculate on the fly. 
        ht = 0.0
        if hasattr( event, "HT_pt"):
            ht = event.HT_pt
        else :
            for i in xrange( event.nJet ) :
                ht += event.Jet_pt[i]

        # Calculate the trigger turnons. 
        for itrig,jtrig in self.trigTurnonList.iteritems():
            if getattr( event, itrig ) == 1: 
                getattr(self, 'h_ak4ht_'+itrig).Fill( ht, weight )
                if getattr( event, jtrig ) == 1: 
                    getattr(self, 'h_ak4ht_'+jtrig).Fill( ht, weight )


        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbartrighad = lambda : TTbarResTrigsHadronic() 
