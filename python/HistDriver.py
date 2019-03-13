#! /usr/bin/env python

import ROOT
import array
import math

class StyleDriver :
    def __init__(self, name,
                lineColor=None, fillColor=None, markerColor=None, 
                lineStyle=None, fillStyle=None, markerStyle=None, 
                lineWidth=None):
        self.name        = name
        self.lineColor   = lineColor   
        self.fillColor   = fillColor   
        self.markerColor = markerColor 
        self.lineStyle   = lineStyle   
        self.fillStyle   = fillStyle   
        self.markerStyle = markerStyle 
        self.lineWidth   = lineWidth

        
class HistDriver :
    def __init__( self, lumi=None, dlumi=None ):
        self.lumi_=lumi
        self.hists_ = []  # Keep stuff around until we want them to go out of scope
        self.canvs_ = []
        self.pads_ = []
        self.stacks_ = []
        self.legs_ = []
        self.stampCMSVal = ROOT.TLatex()
        self.stampCMSVal.SetNDC()
        self.stampCMSVal.SetTextFont(43)
        self.stampCMSVal.SetTextSize(25)
        self.styles = {
            #'nom':StyleDriver(name="nom",markerStyle=20,lineStyle=1,lineColor=ROOT.kBlack,fillStyle=1001,fillColor=ROOT.kGray),
            'pythia8':StyleDriver(name="pythia8",markerStyle=0,lineStyle=1,lineColor=ROOT.kBlack,fillStyle=1001,fillColor=ROOT.kYellow),
            '2016':StyleDriver(name="2016",markerStyle=20,lineStyle=1,lineColor=ROOT.kBlack,markerColor=ROOT.kBlack,fillStyle=None,fillColor=None),
            '2017':StyleDriver(name="2017",markerStyle=21,lineStyle=1,lineColor=ROOT.kBlue,markerColor=ROOT.kBlue,fillStyle=None,fillColor=None),
            '2018':StyleDriver(name="2018",markerStyle=22,lineStyle=1,lineColor=ROOT.kRed,markerColor=ROOT.kRed,fillStyle=None,fillColor=None),
            }

        
        
    def setupPads(self, canv):
        canv.cd()
        pad1 = ROOT.TPad('pad' + canv.GetName() + '1', 'pad' + canv.GetName() + '1', 0., 0.3, 1.0, 1.0)
        pad1.SetBottomMargin(0.05)
        pad2 = ROOT.TPad('pad' + canv.GetName() + '2', 'pad' + canv.GetName() + '2', 0., 0.0, 1.0, 0.3)
        pad1.SetTopMargin(0.10)
        pad2.SetTopMargin(0.05)
        pad1.SetLeftMargin(0.15)
        pad2.SetLeftMargin(0.15)
        pad1.SetRightMargin(0.15)
        pad2.SetRightMargin(0.15)
        pad2.SetBottomMargin(0.5)
        pad1.Draw()
        pad2.Draw()
        self.pads_.append([pad1,pad2])
        
        
        self.canvs_.append(canv)
        self.pads_.append( [pad1,pad2] )
        return [pad1, pad2]

    def plotHistAndRatio(self, pad1, pad2, hist, nominal, rationame="_ratio", option1="", option2="", ratiotitle=None, logy=False, logx=False, ratiorange=None, xAxisRange=None ) :

        if xAxisRange != None :
            hist.GetXaxis().SetRangeUser(xAxisRange[0],xAxisRange[2])
        ratio = hist.Clone( hist.GetName() + rationame )            
        pad1.cd()
        hist.GetYaxis().SetTitleOffset(1.2)
        hist.GetXaxis().SetTitleSize(0)
        hist.GetXaxis().SetLabelSize(0)
        hist.Draw(option1)
        pad1.SetLogy(logy)
        pad1.SetLogx(logx)
        pad2.cd()
        pad2.SetLogx(logx)
        if logx:
            hist.GetXaxis().SetMoreLogLabels()

        if logx :
            ratio.GetXaxis().SetNoExponent()
        if ratiotitle != None :
            ratio.GetYaxis().SetTitle(ratiotitle)            
        ratio.Divide( nominal )
        ratio.GetXaxis().SetTickLength(0.07)
        ratio.GetYaxis().SetNdivisions(2,4,0,False)
        ratio.GetYaxis().SetTitleSize(0.10)
        ratio.GetYaxis().SetLabelSize(0.10)
        #ratio.GetYaxis().SetTitleSize(0.2)
        ratio.GetYaxis().SetTitleOffset(0.6)
        ratio.GetXaxis().SetTitleOffset(3.5)

        ratio.Draw(option2)
        
        if ratiorange != None :
            ratio.SetMinimum( ratiorange[0] )
            ratio.SetMaximum( ratiorange[1] )
        self.hists_.append(ratio)



    def plotGraphAndRatio(self, pad1, pad2, hist, nominal, rationame="_ratio", option1="", option2="", ratiotitle=None, logy=False, logx=False, ratiorange=None, xAxisRange=None ) :

        if xAxisRange != None :
            hist.GetXaxis().SetRangeUser(xAxisRange[0],xAxisRange[2])
            
        ratio = hist.Clone( hist.GetName() + rationame )
        ratio.Divide( nominal )
        ratio.SetMarkerStyle(0)
        ratio.GetXaxis().SetTickLength(0.07)
        ratio.GetYaxis().SetNdivisions(2,4,0,False)
        ratio.GetYaxis().SetTitleOffset(1.2)
        ratio.GetXaxis().SetTitleOffset(3.5)
            
        graph1 = getGraph( hist, minmassbin=hist.GetXaxis().FindBin(xAxisRange[0]) )
        graph2 = getGraph( ratio, minmassbin=hist.GetXaxis().FindBin(xAxisRange[0]) )
        pad1.cd()
        hist.GetYaxis().SetTitleOffset(1.2)
        graph1.Draw(option1)
        pad1.SetLogy(logy)
        pad1.SetLogx(logx)
        pad2.cd()
        pad2.SetLogx(logx)        
        graph2.Draw(option2)
        self.hists_.append(graph1)
        self.hists_.append(graph2)
        return graph1,graph2


    def stampCMS( self, pad, text, lumi=None ) :
        pad.cd()
        if lumi == None :
            lumi = self.lumi_ 
        self.stampCMSVal.DrawLatex(0.15, 0.926, text)
        self.stampCMSVal.DrawLatex(0.64, 0.926, "%3.1f fb^{-1} (13 TeV)" % (lumi / 1e3) )
    


def setStylesClass( hist, istyle ) :
    setStyles(hist, lineColor=istyle.lineColor, fillColor=istyle.fillColor, markerColor=istyle.markerColor, 
               lineStyle=istyle.lineStyle, fillStyle=istyle.fillStyle, markerStyle=istyle.markerStyle, 
               lineWidth=istyle.lineWidth )


def setStyles( hist,
               lineColor=None, fillColor=None, markerColor=None, 
               lineStyle=None, fillStyle=None, markerStyle=None, 
               lineWidth=None,
               xaxisTitleSize = None, yaxisTitleSize = None,
               xaxisLabelSize = None, yaxisLabelSize = None, ) :
    if lineStyle != None : hist.SetLineStyle(lineStyle)
    if fillStyle != None : hist.SetFillStyle(fillStyle)
    if markerStyle != None : hist.SetMarkerStyle(markerStyle)    
    if lineColor != None : hist.SetLineColor(lineColor)
    if fillColor != None : hist.SetFillColor(fillColor)
    if markerColor != None : hist.SetMarkerColor(markerColor)
    if lineWidth != None : hist.SetLineWidth(lineWidth)
    hist.GetXaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetXaxis().SetLabelFont(43)
    hist.GetYaxis().SetTitleFont(42)
    if xaxisTitleSize != None:
        hist.GetXaxis().SetTitleSize( xaxisTitleSize )
    else:
        hist.GetXaxis().SetTitleSize( 20 )
        
    if yaxisTitleSize != None:
        hist.GetYaxis().SetTitleSize( yaxisTitleSize )
    else:
        hist.GetYaxis().SetTitleSize( 0.05 )
        
    if xaxisLabelSize != None:
        hist.GetXaxis().SetLabelSize( xaxisLabelSize )
    else:
        hist.GetXaxis().SetLabelSize( 22 )
        
    if yaxisLabelSize != None:
        hist.GetYaxis().SetLabelSize( yaxisLabelSize )
    else:
        hist.GetYaxis().SetLabelSize( 0.05 )
    

        
# Turn a histogram into a graph
def getGraph( hist, width=None, minmassbin=None ) :
    x = array.array("d", [] )
    y = array.array("d", [] )
    dx = array.array("d", [] )
    dy = array.array("d", [] )
    if minmassbin == None :
        imin = 1
    else :
        imin = minmassbin
    for ibin in xrange( imin, hist.GetNbinsX() + 1):
        val = hist.GetBinContent(ibin) 
        if val > 0. :
            x.append( hist.GetXaxis().GetBinCenter(ibin) )
            dx.append( hist.GetXaxis().GetBinWidth(ibin) / 2. )
            y.append( val )
            dy.append( hist.GetBinError(ibin) )
    graph =ROOT.TGraphErrors( len(x), x, y, dx, dy )
    graph.SetName( hist.GetName() + "_graph")
    graph.SetLineColor( hist.GetLineColor() )
    graph.SetLineStyle( hist.GetLineStyle() )
    if width == None :
        graph.SetLineWidth( hist.GetLineWidth() )
    else : 
        graph.SetLineWidth( width )
    graph.SetFillColor( hist.GetFillColor() )
    graph.SetFillStyle( hist.GetFillStyle() )
    return graph

