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
ROOT.gSystem.Load('libAnalysisPredictedDistribution')

"""@TTbarResAnaHadronic Package to perform the data-driven mistag-rate-based ttbar hadronic analysis. 

This module must be run twice: 
1. Make the mistag rate in the "anti-tag and probe" selection 
and the expectation in the signal region from MC,
2. Applies that mistag rate and the mod-mass procedure to the single-tag selection. 

These are all done in bins of
b-tag categories (0, 1, >=2) and rapidity (|y| <= 1.0, |y| > 1.0).
The signal region is two top-tagged jets. 
The background estimate is the single-tag selection weighted by the mistag rate from the
"anti-tag and probe" region, with the mass of the weighted jet set to a random
value from QCD MC in the 1-ttag region. 

The preselection is:
 - AK4-based HT > 1100 GeV (to be on the trigger plateau). 
 - >= 2 AK8 jets with pt > 400 and |eta| < 2.5, loose jet ID applied from matched AK4 jets

The 1-tag selection adds:
 - >=1 AK8 jet with top tagging applied to randomly-assigned tag jet. 

The anti-tag selection is disjoint from the 1-tag selection:
 - >=1 AK8 jet with top tagging VETO applied to randomly-assigned tag jet. 

The 2-tag selection is:
 - >=2 AK8 jets with top tagging applied to both leading jets. 

The ttbar candidate mass assumes the two leading top-tagged jets are the top quarks. 
"""
class TTbarResAnaHadronic(Module):
    def __init__(self, htCut=1100., minMSD=110., maxMSD=240., tau32Cut=0.6, ak8PtMin=400., bdisc=0.7, writePredDist=False, isData=False, year='2016', modMassFileName = None):
        """ Initialization for the module 
        """
        self.htCut = htCut
        self.minMSD = minMSD
        self.maxMSD = maxMSD
        self.tau32Cut = tau32Cut
        self.ak8PtMin = ak8PtMin
        self.bdisc = bdisc
        self.writePredDist = writePredDist
        self.writeHistFile = True
        self.isData = isData
        self.year=year
        
        if not self.isData : 
            self.systs = [
                'nom',
                'pu_up',  'pu_dn',
                'pdf_up', 'pdf_dn',
                'ps_up',  'ps_dn',
                'jec_up', 'jec_dn',
                'jer_up', 'jer_dn',
                'jms_up', 'jms_dn',
                'jmr_up', 'jmr_dn'
                ]
        else :
            self.systs = [ 'nom' ]
        self.btagcats = ["0b", "1b", "2b"]   # 0, 1, >=2 btags
        self.ycats = ['cen', 'fwd']          # Central and forward
        # Combine categories like "0bcen", "0bfwd", etc:
        self.anacats = [ b+y for b,y in itertools.product( self.btagcats, self.ycats) ]
        # Make string-based enumeration into aliases for faster processing speed
        self.systvals = []
        for isys,sys in enumerate(self.systs):
            setattr( self, sys, isys)
            self.systvals.append( getattr(self,sys) )
        self.anacatvals = []        
        for ianacat,anacat in enumerate(self.anacats):
            setattr( self, anacat, ianacat )
            self.anacatvals.append( getattr(self,anacat) )
            
        self.systs_anacats = [ a + '__' + s for s,a in itertools.product( self.systs, self.anacats ) ]

        print self.systs_anacats


        if modMassFileName is None:
            self.modMassFile = ROOT.TFile("modmass.root")
        else :
            self.modMassFile = ROOT.TFile(modMassFileName)
        print [ "ttbarres/h_tagjet_ak8m_%s" % s for s in self.systs_anacats if 'nom' in s ]
        self.modMass = [ self.modMassFile.Get("ttbarres/h_tagjet_ak8m_%s" % s ) for s in self.systs_anacats if 'nom' in s ]

        # Zero out everything except the mass region of the tag to ensure unbiased kinematics.
        # This is the "mass modified" procedure.
        for mm in self.modMass:
            xmin = mm.GetXaxis().FindBin(140.)
            xmax = mm.GetXaxis().FindBin(240.)
            for ibin in range(0,xmin):
                mm.SetBinContent(ibin,0)
                mm.SetBinError(ibin,0)
            for ibin in range(xmax, mm.GetNbinsX()+1):
                mm.SetBinContent(ibin,0)
                mm.SetBinError(ibin,0)


        

    def formcat(self, nbtag, ycat ):
        """Form analysis category based on nbtag and ycat.

        """
        anacat = nbtag * len(self.ycats) + ycat
        return anacat

    def formsyscat( self, syst, nbtag, ycat ):
        return (nbtag * len(self.ycats) + ycat) * len(self.systvals) + syst
        
    def beginJob(self, histFile, histDirName):
        """Book control histograms and the predictions for the background.

        The background is data-driven and estimated by weighting the 1-tag region
        by the mistag rate to extrapolate to the 2-tag region. 
        """
        Module.beginJob(self, histFile, histDirName)


        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak4ht',    'h_ak4ht',    100, 0, 5000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8pt',    'h_ak8pt',    100, 0, 2500) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8msd',   'h_ak8msd',   100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8m',     'h_ak8m',     100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8m_mod', 'h_ak8m_mod', 100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8m_modb','h_ak8m_modb',100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8tau32', 'h_ak8tau32', 100, 0, 1.0) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_ak8n3b1',  'h_ak8n3b1',  100, 0, 5.0) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_mttbar',   'h_mttbar',   100, 0, 5000) )


        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_tagjet_ak8pt',    'h_tagjet_ak8pt',    100, 0, 2500) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_tagjet_ak8msd',   'h_tagjet_ak8msd',   100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_tagjet_ak8m',     'h_tagjet_ak8m',     100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_tagjet_ak8tau32', 'h_tagjet_ak8tau32', 100, 0, 1.0) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_tagjet_ak8n3b1',  'h_tagjet_ak8n3b1',  100, 0, 5.0) )

        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_antitagjet_ak8pt',    'h_antitagjet_ak8pt',    100, 0, 2500) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_antitagjet_ak8msd',   'h_antitagjet_ak8msd',   100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_antitagjet_ak8m',     'h_antitagjet_ak8m',     100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_antitagjet_ak8tau32', 'h_antitagjet_ak8tau32', 100, 0, 1.0) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_antitagjet_ak8n3b1',  'h_antitagjet_ak8n3b1',  100, 0, 5.0) )
        
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_probejet_ak8pt',    'h_probejet_ak8pt',    100, 0, 2500) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_probejet_ak8msd',   'h_probejet_ak8msd',   100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_probejet_ak8m',     'h_probejet_ak8m',     100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_probejet_ak8tau32', 'h_probejet_ak8tau32', 100, 0, 1.0) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_probejet_ak8n3b1',  'h_probejet_ak8n3b1',  100, 0, 5.0) )

        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_signalregion_ak8pt',    'h_signalregion_ak8pt',    100, 0, 2500) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_signalregion_ak8msd',   'h_signalregion_ak8msd',   100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_signalregion_ak8m',     'h_signalregion_ak8m',     100, 0, 1000) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_signalregion_ak8tau32', 'h_signalregion_ak8tau32', 100, 0, 1.0) )
        self.addObjectList (self.systs_anacats, ROOT.TH1F('h_signalregion_ak8n3b1',  'h_signalregion_ak8n3b1',  100, 0, 5.0) )

        
        
        if not self.writePredDist:
            self.predFile = ROOT.TFile( "mistag_rates.root" )
            self.hpred = [ self.predFile.Get( "mistagrate_" + str(iana) + '_' + self.year ) for iana in xrange(len(self.anacatvals))]
            # PredictedDistribution needs to own this to ensure it doesn't go out of scope.
            for iana in xrange(len(self.anacatvals)) :
                ROOT.SetOwnership( self.hpred[iana], False )
                self.addObject( ROOT.PredictedDistribution(self.hpred[iana], "predJetP"+str(iana),        "Jet p_{T} (GeV), cat="+str(iana),   100, 0.0, 3000.) )
                self.addObject( ROOT.PredictedDistribution(self.hpred[iana], "predJetMTTBAR"+str(iana),   "M_{TTBAR} (GeV), cat="+str(iana),   100, 0.0, 5000.))
                self.addObject( ROOT.PredictedDistribution(self.hpred[iana], "predJetMTTBARMod"+str(iana),"M_{TTBAR} (GeV), cat="+str(iana),   100, 0.0, 5000.))
            self.predJetP         = [ getattr( self, "predJetP"         + str (iana)) for iana in xrange(len(self.anacatvals))]
            self.predJetMTTBAR    = [ getattr( self, "predJetMTTBAR"    + str (iana)) for iana in xrange(len(self.anacatvals))]
            self.predJetMTTBARMod = [ getattr( self, "predJetMTTBARMod" + str (iana)) for iana in xrange(len(self.anacatvals))]

            # PredictedDistribution needs to own these also.
            for cat in self.anacatvals : 
                for hist in [self.predJetP[cat], self.predJetMTTBAR[cat],self.predJetMTTBARMod[cat] ] : 
                    ROOT.SetOwnership( hist, False )
        else:
            for iana in xrange(len(self.anacatvals)):
                self.addObject( ROOT.TH1D("preddist"+str(iana) + "_num", "preddist"+str(iana) + "_num", 5000, 0, 5000) )
                self.addObject( ROOT.TH1D("preddist"+str(iana) + "_den", "preddist"+str(iana) + "_den", 5000, 0, 5000) )
                self.addObject( ROOT.TH1D("preddistrho"+str(iana) + "_num", "preddistrho"+str(iana) + "_num", 5000, 0, 1) )
                self.addObject( ROOT.TH1D("preddistrho"+str(iana) + "_den", "preddistrho"+str(iana) + "_den", 5000, 0, 1) )

            self.preddist_num = [ getattr( self, "preddist"+str(iana)+"_num") for iana in xrange(len(self.anacatvals))]
            self.preddist_den = [ getattr( self, "preddist"+str(iana)+"_den") for iana in xrange(len(self.anacatvals))]
            self.preddistrho_num = [ getattr( self, "preddistrho"+str(iana)+"_num") for iana in xrange(len(self.anacatvals))]
            self.preddistrho_den = [ getattr( self, "preddistrho"+str(iana)+"_den") for iana in xrange(len(self.anacatvals))]
            
    def endJob(self):
        """Calculate the correlated and uncorrelated errors.
        """
        if not self.writePredDist:
            for cat in self.anacatvals : 
                for hist in [self.predJetP[cat], self.predJetMTTBAR[cat],self.predJetMTTBARMod[cat] ] : 
                    hist.SetCalculatedErrors()
        Module.endJob(self)
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def passTopTag(self, jet):
        """Selects jets based on tau32 and soft drop mass. 
        """
        tau32 = jet.raw().tau3 / jet.raw().tau2 if jet.raw().tau2 > 0.0 else 0.
        passTau32 = tau32 < self.tau32Cut 
        passMSD = jet.msd() != None and self.minMSD < jet.msd() < self.maxMSD
        return passTau32 and passMSD

    def passTopAntiTag(self, jet):
        """Selects *anti-tagged* jets that satisfy the mass requirement but fail the tau32 cut.
        """
        tau32 = jet.raw().tau3 / jet.raw().tau2 if jet.raw().tau2 > 0.0 else 0.
        passAntiTau32 = tau32 > self.tau32Cut 
        passMSD = jet.msd() != None and self.minMSD < jet.msd() < self.maxMSD
        return passAntiTau32 and passMSD
    
    def deriveWeights(self):
        """Derives all of the weights used that do not adjust the 4-vectors in the event.         
        """
        self.weightsDict = {}
        self.weightsDict[self.nom] = 1.0
        if not self.isData : 
            self.weightsDict[self.pu_up] = 1.0
            self.weightsDict[self.pu_dn] = 1.0
            self.weightsDict[self.pdf_up] = 1.0
            self.weightsDict[self.pdf_dn] = 1.0
            self.weightsDict[self.ps_up] = 1.0
            self.weightsDict[self.ps_dn] = 1.0
        return True

    
    def deriveJetSystsData(self, jetSysCollAK8=None):
        """ Derive all of the jet-based kinematic systematic uncertainties. This includes JEC, JER, JMS, JMR.
        """

        if jetSysCollAK8 != None:
            for ijet, jet in enumerate(jetSysCollAK8.jets_raw()) :
                if ijet not in jetSysCollAK8[self.nom].keys() :
                    continue
                jetSysCollAK8[self.nom   ][ijet].p4().SetPtEtaPhiM( jet.pt          , jet.eta, jet.phi, jet.mass          )
                jetSysCollAK8[self.nom   ][ijet].msd_ = jet.msoftdrop

    
    def deriveJetSystsMC(self, jetSysCollAK8=None):
        """ Derive all of the jet-based kinematic systematic uncertainties. This includes JEC, JER, JMS, JMR.
        """
        if jetSysCollAK8 != None:
            for ijet, jet in enumerate(jetSysCollAK8.jets_raw()) :
                if ijet not in jetSysCollAK8[self.nom].keys() :
                    continue
                jetSysCollAK8[self.nom   ][ijet].p4().SetPtEtaPhiM( jet.pt_nom          , jet.eta, jet.phi, jet.mass_nom          )
                jetSysCollAK8[self.jer_up][ijet].p4().SetPtEtaPhiM( jet.pt_jerUp        , jet.eta, jet.phi, jet.mass_jerUp        )
                jetSysCollAK8[self.jer_dn][ijet].p4().SetPtEtaPhiM( jet.pt_jerDown      , jet.eta, jet.phi, jet.mass_jerDown      )
                jetSysCollAK8[self.jec_up][ijet].p4().SetPtEtaPhiM( jet.pt_jesTotalUp   , jet.eta, jet.phi, jet.mass_jesTotalUp   )
                jetSysCollAK8[self.jec_dn][ijet].p4().SetPtEtaPhiM( jet.pt_jesTotalDown , jet.eta, jet.phi, jet.mass_jesTotalDown )
                jetSysCollAK8[self.jmr_up][ijet].p4().SetPtEtaPhiM( jet.pt_nom          , jet.eta, jet.phi, jet.mass_jmrUp        )
                jetSysCollAK8[self.jmr_dn][ijet].p4().SetPtEtaPhiM( jet.pt_nom          , jet.eta, jet.phi, jet.mass_jmrDown      )
                jetSysCollAK8[self.jms_up][ijet].p4().SetPtEtaPhiM( jet.pt_nom          , jet.eta, jet.phi, jet.mass_jmsUp        )
                jetSysCollAK8[self.jms_dn][ijet].p4().SetPtEtaPhiM( jet.pt_nom          , jet.eta, jet.phi, jet.mass_jmsDown      )
                
                jetSysCollAK8[self.nom   ][ijet].msd_ = jet.msoftdrop_nom
                jetSysCollAK8[self.jer_up][ijet].msd_ = jet.msoftdrop_jerUp                        
                jetSysCollAK8[self.jer_dn][ijet].msd_ = jet.msoftdrop_jerDown      
                jetSysCollAK8[self.jec_up][ijet].msd_ = jet.msoftdrop_jesTotalUp   
                jetSysCollAK8[self.jec_dn][ijet].msd_ = jet.msoftdrop_jesTotalDown 
                jetSysCollAK8[self.jmr_up][ijet].msd_ = jet.msoftdrop_jmrUp                        
                jetSysCollAK8[self.jmr_dn][ijet].msd_ = jet.msoftdrop_jmrDown      
                jetSysCollAK8[self.jms_up][ijet].msd_ = jet.msoftdrop_jmsUp        
                jetSysCollAK8[self.jms_dn][ijet].msd_ = jet.msoftdrop_jmsDown      
                
    def applyWeight(self, isys):
        """ Apply the weights for systematic "isys". If not found, use nominal. 
        """
        if isys not in self.weightsDict.keys():            
            weight = self.weightsDict[self.nom]
        else :
            weight = self.weightsDict[isys]
        return weight
        
    def analyze(self, event):
        """Perform either the anti-tag and probe (mistag estimate) or double tag (signal region) selection.
        """

        # Get the collections of AK4 and AK8 jets
        self.ak8JetsColl = Collection(event, "FatJet")

        
        # Make the systematic variations. Ignore jets that do not pass ID cuts. 
        jetSysCollAK8 = JetSysColl(self.ak8JetsColl, self.systvals, sel = lambda x : x.jetId > 0)
                
        # Derive the kinematic systematic effects. In this case,
        # jet-based systematic 4-vectors (AK4: JEC+JER, AK8:JEC+JER+JMS+JMR)
        if not self.isData : 
            self.deriveJetSystsMC(jetSysCollAK8)
        else :
            self.deriveJetSystsData(jetSysCollAK8)

        # Derive the weights to be used. 
        self.deriveWeights()
        
        # Loop over systematic uncertainties. These may change the kinematics,
        # or the weights. Both need to be adjusted.
        for isys,sys in enumerate(self.systs) :
            #print 'processing systematic : ', sys
            # Apply kinematic selection for this systematic. If no change, just use nominal. 
            ak8JetsSys = jetSysCollAK8[isys]
            
            # Adjust weight. If this systematic has no weight, just use nominal. 
            weight = self.applyWeight(isys)
            # Multiply by any gen weights
            if hasattr( event, "Generator_weight") and abs( event.Generator_weight - 1.0) > 1e-3 :
                weight *= event.Generator_weight
                

            # Now get the AK8 jets that pass the selection.
            # Don't copy the jet (expensive), copy the index (cheap)\
            ak8JetsNdx = [i for i,x in ak8JetsSys.iteritems() if x.p4().Perp() > self.ak8PtMin and abs(x.p4().Eta()) < 2.5]
            
            # Must have two AK8 jets that pass jet ID and kinematic cuts. 
            if len(ak8JetsNdx) < 2 :
                continue

            # Apply HT cut to ensure we are on the trigger plateau
            ht = 0.0
            if hasattr( event, "HT_pt"):
                ht = event.HT_pt
            else :
                ht = sum( [event.Jet_pt[i] for i in range(event.nJet)] )

            if ht < self.htCut :
                return False
            ##print 'passed HT cut'

            # Get a list of the jets that are top-tagged (ttag)
            isTagged = [ self.passTopTag(ak8JetsSys[x]) for x in ak8JetsNdx ]
            isTaggedDict = dict( zip( ak8JetsNdx ,isTagged) )


            #print ' probe : %6.2f %6.2f %6.2f %6.2f ' % ( ak8JetsSys[iprobejet].p4().Perp(), ak8JetsSys[iprobejet].p4().Eta(), ak8JetsSys[iprobejet].p4().Phi(), ak8JetsSys[iprobejet].p4().M() )
            #print '   tag : %6.2f %6.2f %6.2f %6.2f ' % ( ak8JetsSys[itagjet].p4().Perp(), ak8JetsSys[itagjet].p4().Eta(), ak8JetsSys[itagjet].p4().Phi(), ak8JetsSys[itagjet].p4().M() )

            # Get a randomly assigned tag and probe jet from the leading two jets
            random.shuffle( ak8JetsNdx )
            iprobejet, itagjet = ak8JetsNdx[0:2]
            tagjet = ak8JetsSys[itagjet]
            tagraw = jetSysCollAK8.jets_raw()[itagjet]
            probejet = ak8JetsSys[iprobejet]
            proberaw = jetSysCollAK8.jets_raw()[iprobejet]            
                
            # Find the analysis category: (0b,1b,2b) x (y<1,y>1)
            nbtag = min(2, sum( [x.btagCSVV2 > self.bdisc for x in [proberaw, tagraw] ] ))
            yreg = 1 if abs( probejet.p4().Rapidity() ) > 1.0 else 0
            anacat = self.formcat( nbtag, yreg )
            isyscat = self.formsyscat( isys, nbtag, yreg )

            # Require a back-to-back topology
            if abs( tagjet.p4().DeltaPhi( probejet.p4() ) ) < 2.1 :
                continue


            # Make control plots
            for iak8Jet in ak8JetsNdx:
                jet = ak8JetsSys[iak8Jet]
                raw = jetSysCollAK8.jets_raw()[iak8Jet]
                self.h_ak8pt[isyscat].Fill( jet.p4().Perp(), weight )                
                self.h_ak8m[isyscat].Fill( jet.p4().M(), weight )
                self.h_ak8msd[isyscat].Fill( jet.msd(), weight )
                self.h_ak8tau32[isyscat].Fill( raw.tau3 / raw.tau2 if raw.tau2 > 0.0 else 0.0, weight )
                self.h_ak8n3b1[isyscat].Fill( raw.n3b1, weight )




            
            # Check if the event is an anti-tag + probe case. In that case we fill the mistag rate. 
            if isys == self.nom and self.passTopAntiTag(tagjet) :

                # Here are some control plots
                self.h_antitagjet_ak8pt[isyscat].Fill( tagjet.p4().Perp(), weight )                
                self.h_antitagjet_ak8msd[isyscat].Fill( tagjet.msd(), weight )
                self.h_antitagjet_ak8m[isyscat].Fill( tagjet.p4().M(), weight )
                self.h_antitagjet_ak8tau32[isyscat].Fill( tagraw.tau3 / tagraw.tau2 if tagraw.tau2 > 0.0 else 0.0, weight )
                self.h_antitagjet_ak8n3b1[isyscat].Fill( tagraw.n3b1, weight )

                # This is the denominator of the predicted distribution
                if self.writePredDist :
                    self.preddist_den[anacat].Fill( probejet.p4().P(), weight )
                    self.preddistrho_den[anacat].Fill( probejet.msd() / probejet.p4().Perp(), weight )

                # This is the numerator of the predicted distribution, plus control plots
                if self.passTopTag( ak8JetsSys[iprobejet] ):
                    if self.writePredDist:
                        self.preddist_num[anacat].Fill( probejet.p4().P(), weight )
                        self.preddistrho_num[anacat].Fill( probejet.msd() / probejet.p4().Perp(), weight )
                    self.h_probejet_ak8pt[isyscat].Fill( probejet.p4().Perp(), weight )                
                    self.h_probejet_ak8msd[isyscat].Fill( probejet.msd(), weight )
                    self.h_probejet_ak8m[isyscat].Fill( probejet.p4().M(), weight )
                    self.h_probejet_ak8tau32[isyscat].Fill( proberaw.tau3 / proberaw.tau2 if proberaw.tau2 > 0.0 else 0.0, weight )
                    self.h_probejet_ak8n3b1[isyscat].Fill( proberaw.n3b1, weight )                    

                return True
                    
            # Check if we have >=1 ttag
            if self.passTopTag(tagjet) :
                
                if isys == self.nom :
                    ttbarP4 =  probejet.p4() + tagjet.p4()

                    if not self.writePredDist:
                        modMass = self.modMass[isyscat].GetRandom()
                        modMassP4 = ROOT.TLorentzVector()
                        modMassP4.SetPtEtaPhiM( probejet.p4().Perp(), probejet.p4().Eta(), probejet.p4().Phi(), modMass )
                        modMass_ttbarP4 = tagjet.p4() + modMassP4
                        self.predJetP[anacat].Accumulate( probejet.p4().P(), probejet.p4().P(), isTaggedDict[iprobejet], weight )
                        self.predJetMTTBAR[anacat].Accumulate( ttbarP4.M(), probejet.p4().P(), isTaggedDict[iprobejet], weight )
                        self.predJetMTTBARMod[anacat].Accumulate( modMass_ttbarP4.M(), ak8JetsSys[iprobejet].p4().P(), isTaggedDict[iprobejet], weight )
                    self.h_tagjet_ak8pt[isyscat].Fill( tagjet.p4().Perp(), weight )                
                    self.h_tagjet_ak8msd[isyscat].Fill( tagjet.msd(), weight )
                    self.h_tagjet_ak8m[isyscat].Fill( tagjet.p4().M(), weight )
                    self.h_tagjet_ak8tau32[isyscat].Fill( tagraw.tau3 / tagraw.tau2 if tagraw.tau2 > 0.0 else 0.0, weight )
                    self.h_tagjet_ak8n3b1[isyscat].Fill( tagraw.n3b1, weight )
                # Here we have the actual signal region. Fill the double tagged histograms. 
                if isTaggedDict[iprobejet] :
                    # Fill out the kinematics of the probe jet for the background estimate.
                    # The QCD MC will be used from these distributions to estiamte the mod mass procedure
                    self.h_mttbar[isyscat].Fill( ttbarP4.M(), weight )
                    if isys == self.nom:
                        self.h_signalregion_ak8pt[isyscat].Fill( probejet.p4().Perp(), weight )                
                        self.h_signalregion_ak8msd[isyscat].Fill( probejet.msd(), weight )
                        self.h_signalregion_ak8m[isyscat].Fill( probejet.p4().M(), weight )
                        self.h_signalregion_ak8tau32[isyscat].Fill( proberaw.tau3 / proberaw.tau2 if proberaw.tau2 > 0.0 else 0.0, weight )
                        self.h_signalregion_ak8n3b1[isyscat].Fill( proberaw.n3b1, weight )                        


        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbarreshad = lambda : TTbarResAnaHadronic() 
ttbarreshad_preddistwriter = lambda : TTbarResAnaHadronic(writePredDist=True)
ttbarreshad_data = lambda : TTbarResAnaHadronic(isData=True) 
ttbarreshad_preddistwriter_data = lambda : TTbarResAnaHadronic(writePredDist=True,isData=True)
