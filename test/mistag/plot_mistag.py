#!/usr/bin/env python

import ROOT
import itertools

from tdrstyle import setTDRStyle

setTDRStyle()


## ROOT.gROOT.Macro("rootlogon.C")

## ROOT.gStyle.SetOptStat(000000)
## ROOT.gStyle.SetTitleOffset(1.0, "Y");
## ROOT.gStyle.SetPadRightMargin(0.15)
## ROOT.gStyle.SetTitleFont(43,"XYZ")
## ROOT.gStyle.SetTitleSize(30,"XYZ")
## ROOT.gStyle.SetTitleOffset(1.0, "X")
## ROOT.gStyle.SetTitleOffset(0.8, "Y")
## ROOT.gStyle.SetLabelFont(43,"XYZ")
## ROOT.gStyle.SetLabelSize(22,"XYZ")


s_2018 = 'mistag_DijetSkim_Nrp_JetHT_Run2018%s-PromptReco_AntiTag.root'
runs_2018 = ['A', 'B']
hists_2018 = []
s_2017 = 'mistag_DijetSkim_Nrp_JetHT_Run2017%s-17Nov2017_AntiTag.root'
runs_2017 = ['B', 'C', 'D', 'E', 'F']
hists_2017 = []
s_2016 = 'mistag_DijetSkim_Nrp_JetHT_Run2016%s-17Nov2017_AntiTag.root'
runs_2016 = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
hists_2016 = []
styles = [20,21,22]
colors = [1,2,4]

runs_list = [ runs_2016, runs_2017, runs_2018]
basestrs = [ s_2016, s_2017, s_2018 ]

btagcats = ["0 b-tag", "1 b-tag", "2 b-tag"]   # 0, 1, >=2 btags
ycats = [',Central', ',Forward']          # Central and forward
# Combine categories like "0bcen", "0bfwd", etc:
anacats = [ b+y for b,y in itertools.product( btagcats, ycats) ]
ncats = 6
files = []
effs = []
canvs = []
legs = []

for icat in xrange(ncats) :
    c1 = ROOT.TCanvas("c" + str(icat), "c" + str(icat))
    leg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    for iyear,year in enumerate( ['2016', '2017', '2018'] ):
        dens = []
        nums = []
        for irun,run in enumerate(runs_list[iyear]):
            s = basestrs[iyear] % ( run )
            f = ROOT.TFile( s )
            num = f.Get("ttbarres/preddist%s_num" % (icat) ).Clone('num' + str(icat) + str(run))
            den = f.Get("ttbarres/preddist%s_den" % (icat) ).Clone('den' + str(icat) + str(run))
            num.Rebin(100)
            den.Rebin(100)
            nums.append(num)
            dens.append(den)
            files.append(f)
        numtot = nums[0].Clone("numtot" + str(icat))
        dentot = dens[0].Clone("dentot" + str(icat))
        for hist in nums[1:]:
            numtot.Add( hist )
        for hist in dens[1:]:
            dentot.Add(hist)
        efftot = ROOT.TEfficiency(numtot,dentot)
        efftot.SetName('efftot' + str(icat) + str(iyear))            
        efftot.SetTitle( anacats[icat] + ';Jet Momentum (GeV);Mistag Rate')            
        efftot.SetMarkerStyle( styles[iyear] )
        efftot.SetMarkerColor( colors[iyear] )
        leg.AddEntry( efftot, year, 'p')
        if iyear == 0 : 
            efftot.Draw('AL')
            ROOT.gPad.Update()
            efftot.GetPaintedGraph().GetXaxis().SetRangeUser(0,2500)
            efftot.GetPaintedGraph().SetMaximum(0.12)
        else :
            efftot.Draw("L same")
        effs.append(efftot)


    canvs.append(c1)
    leg.Draw()
    legs.append(leg)
    c1.Update()
    c1.Print('mistags_%d.png' % (icat), 'png')
    c1.Print('mistags_%d.pdf' % (icat), 'pdf')



