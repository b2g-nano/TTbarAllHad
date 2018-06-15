#!/usr/bin/env python

import ROOT
import itertools

if __name__ == "__main__":
    s_2017 = 'mistag_DijetSkim_Nrp_JetHT_Run2017%s-17Nov2017_AntiTag.root'
    runs_2017 = ['B', 'C', 'D', 'E', 'F']
    s_2016 = 'mistag_DijetSkim_Nrp_JetHT_Run2016%s-17Nov2017_AntiTag.root'
    runs_2016 = ['B', 'C', 'D', 'E', 'F', 'G', 'H']

    
    btagcats = ["0 b-tag", "1 b-tag", "2 b-tag"]   # 0, 1, >=2 btags
    ycats = [',Central', ',Forward']          # Central and forward
    # Combine categories like "0bcen", "0bfwd", etc:
    anacats = [ b+y for b,y in itertools.product( btagcats, ycats) ]
    ncats = 6
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 3, ROOT.kMagenta + 3]
    markers = [20,21,22,23,29]
    canvs = []
    effs = []
    legs = []
    hists = []

    files = []
    for irun,run in enumerate(runs_2017):
        s = s_2017 % ( run )
        f = ROOT.TFile(s)
        files.append(f)
            
    for icat in xrange(ncats) :
        c1 = ROOT.TCanvas("c" + str(icat), "c" + str(icat))
        leg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        dens = []
        nums = []
        for irun,run in enumerate(runs_2017):
            s = s_2017 % ( run )
            f = files[irun]
            num = f.Get("ttbarres/preddist%s_num" % (icat) ).Clone('num' + str(icat) + str(run))
            den = f.Get("ttbarres/preddist%s_den" % (icat) ).Clone('den' + str(icat) + str(run))
            num.Rebin(100)
            den.Rebin(100)
            eff = ROOT.TEfficiency(num,den)
            eff.SetName("eff%d_%s" % (icat, run ) )
            eff.SetTitle( anacats[icat] + ';Jet Momentum (GeV);Mistag Rate')
            eff.SetMarkerStyle(markers[irun])
            eff.SetMarkerColor(colors[irun])
            if irun == 0 :
                eff.Draw()
                ROOT.gPad.Update()
                eff.GetPaintedGraph().GetXaxis().SetRangeUser(0,2500)
                eff.GetPaintedGraph().SetMaximum(0.12)
            else :
                eff.Draw("same")
            leg.AddEntry( eff, 'Run2017%s' % (run), 'p')
            nums.append(num)
            dens.append(den)
            effs.append(eff)
            hists.append(num)
            hists.append(den)
        numtot = nums[0].Clone("numtot" + str(icat))
        dentot = dens[0].Clone("dentot" + str(icat))
        for hist in nums[1:]:
            numtot.Add( hist )
        for hist in dens[1:]:
            dentot.Add(hist)
        efftot = ROOT.TEfficiency(numtot,dentot)
        efftot.SetName('efftot' + str(icat))
        efftot.SetFillStyle(3001)
        efftot.SetFillColor(1)
        leg.AddEntry( efftot, 'Total', 'lf')
        efftot.Draw('L30 same')
        effs.append(efftot)
        c1.Update()
        canvs.append(c1)
        leg.Draw()
        legs.append(leg)
        c1.Print('mistags_%d.png' % (icat), 'png')
        c1.Print('mistags_%d.pdf' % (icat), 'pdf')
        
        
        
