import ROOT
import math 
import time
from plot_dict import *


ROOT.gROOT.SetBatch(ROOT.kTRUE)

version = '_DoublePF'

#for version in ['','_Quad','_DoublePF','_DoublePFMuon']:
#for version in ['_Quad']:
for version in ['_DoublePhoton']:
    if 'DoublePhoton' in version:
        rebin = 6
    else:
        rebin = 1

    #file = ROOT.TFile("histos_BTagTrigNanoAOD_RunD_Quad.root")
    file = ROOT.TFile("histos_RunD%s.root"%version)
    workdir =file.GetDirectory("BTagNanoAOD")


    Numerator = workdir.Get("h_sub_passtrig")
    Denominator = workdir.Get("h_sub_all")
    if 'DoublePhoton' in version:
        Numerator.Rebin(rebin)
        Denominator.Rebin(rebin)


    Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'BTAG')
    Efficiency.SetLineColor(linecolor[1])
    Efficiency.SetMarkerStyle(markerstylesolid[1])
    Efficiency.SetMarkerColor(markercolor[1])
    Efficiency.SetMarkerSize(1.5)
    Efficiency.SetTitle("Trigger Efficiency")
    Efficiency.GetXaxis().SetTitle(Numerator.GetXaxis().GetTitle())
    Efficiency.GetYaxis().SetTitle("Trigger Efficiency")
    Efficiency.GetYaxis().SetRange(0,2) 

    legend = ROOT.TLegend(0.5,0.1,0.9,0.4)
    legend.SetFillStyle(1001)
    legend.SetBorderSize(0)
    legend.AddEntry(Efficiency,"DeepJet","ep")

    canvas=ROOT.TCanvas("Trigger Efficicency", "Trigger Efficiency")
    canvas.SetGrid()
    Efficiency.Draw("ap")
    legend.Draw("same")

    canvas.SaveAs("Efficiency.pdf")

    #file = ROOT.TFile("histos_BTagTrigNanoAOD_RunC_Quad.root")
    file = ROOT.TFile("histos_RunC%s.root"%version)
    workdir =file.GetDirectory("BTagNanoAOD")


    Numerator = workdir.Get("h_sub_passtrig")
    Denominator = workdir.Get("h_sub_all")
    if 'DoublePhoton' in version:
        Numerator.Rebin(rebin)
        Denominator.Rebin(rebin)



    Efficiency2 = ROOT.TGraphAsymmErrors(Numerator,Denominator,'BTAG')
    Efficiency2.SetLineColor(linecolor[1])
    Efficiency2.SetMarkerStyle(markerstylesolid[1])
    Efficiency2.SetMarkerColor(markercolor[1])
    Efficiency2.SetMarkerSize(1.5)
    Efficiency2.SetTitle("Trigger Efficiency2")
    Efficiency2.GetXaxis().SetTitle(Numerator.GetXaxis().GetTitle())
    Efficiency2.GetYaxis().SetTitle("Trigger Efficiency2")
    Efficiency2.GetYaxis().SetRange(0,2) 

    legend2 = ROOT.TLegend(0.5,0.1,0.9,0.4)
    legend2.SetFillStyle(1001)
    legend2.SetBorderSize(0)
    legend2.AddEntry(Efficiency2,"DeepJet","ep")

    canvas2=ROOT.TCanvas("Trigger Efficicency2", "Trigger Efficiency2")
    canvas2.SetGrid()
    Efficiency2.Draw("ap")
    legend2.Draw("same")

    canvas2.SaveAs("Efficiency2.pdf")

    #file = ROOT.TFile("histos_BTagTrigNanoAOD_RunE_Quad.root")
    file = ROOT.TFile("histos_RunE%s.root"%version)
    workdir =file.GetDirectory("BTagNanoAOD")


    Numerator = workdir.Get("h_sub_passtrig")
    Denominator = workdir.Get("h_sub_all")
    if 'DoublePhoton' in version:
        Numerator.Rebin(rebin)
        Denominator.Rebin(rebin)



    Efficiency3 = ROOT.TGraphAsymmErrors(Numerator,Denominator,'BTAG')
    Efficiency3.SetLineColor(linecolor[1])
    Efficiency3.SetMarkerStyle(markerstylesolid[1])
    Efficiency3.SetMarkerColor(markercolor[1])
    Efficiency3.SetMarkerSize(1.5)
    Efficiency3.SetTitle("Trigger Efficiency3")
    Efficiency3.GetXaxis().SetTitle(Numerator.GetXaxis().GetTitle())
    Efficiency3.GetYaxis().SetTitle("Trigger Efficiency3")
    Efficiency3.GetYaxis().SetRange(0,2) 

    legend3 = ROOT.TLegend(0.5,0.1,0.9,0.4)
    legend3.SetFillStyle(1001)
    legend3.SetBorderSize(0)
    legend3.AddEntry(Efficiency3,"DeepJet","ep")

    canvas3=ROOT.TCanvas("Trigger Efficicency3", "Trigger Efficiency3")
    canvas3.SetGrid()
    Efficiency3.Draw("ap")
    legend3.Draw("same")

    canvas3.SaveAs("Efficiency3.pdf")


    file = ROOT.TFile("histos_RunF%s.root"%version)
    workdir =file.GetDirectory("BTagNanoAOD")


    Numerator = workdir.Get("h_sub_passtrig")
    Denominator = workdir.Get("h_sub_all")
    if 'DoublePhoton' in version:
        Numerator.Rebin(rebin)
        Denominator.Rebin(rebin)



    Efficiency4 = ROOT.TGraphAsymmErrors(Numerator,Denominator,'BTAG')
    Efficiency4.SetLineColor(linecolor[1])
    Efficiency4.SetMarkerStyle(markerstylesolid[1])
    Efficiency4.SetMarkerColor(markercolor[1])
    Efficiency4.SetMarkerSize(1.5)
    Efficiency4.SetTitle("Trigger Efficiency4")
    Efficiency4.GetXaxis().SetTitle(Numerator.GetXaxis().GetTitle())
    Efficiency4.GetYaxis().SetTitle("Trigger Efficiency4")
    Efficiency4.GetYaxis().SetRange(0,2) 

    legendRunF = ROOT.TLegend(0.5,0.1,0.9,0.4)
    legendRunF.SetFillStyle(1001)
    legendRunF.SetBorderSize(0)
    legendRunF.AddEntry(Efficiency4,"DeepJet","ep")

    canvasRunF=ROOT.TCanvas("Trigger Efficicency4", "Trigger Efficiency4")
    canvasRunF.SetGrid()
    Efficiency4.Draw("ap")
    legendRunF.Draw("same")

    canvasRunF.SaveAs("Efficiency4.pdf")

    maxi = 1.0
    if 'Quad' in version:
        maxi = 0.16
    elif 'DoublePFMuon' in version:
        maxi = 0.03
    elif 'DoublePF' in version:
        maxi = 0.2
    elif 'DoublePhoton' in version:
        maxi = 1.2
    else:
        maxi = 1.0

    Efficiency.SetMaximum(maxi)
    Efficiency.SetMinimum(0.0)


    Efficiency2.SetLineColor(ROOT.kRed + 2)
    Efficiency2.SetMarkerColor(ROOT.kRed + 2)

    Efficiency3.SetLineColor(ROOT.kBlue + 2)
    Efficiency3.SetMarkerColor(ROOT.kBlue + 2)

    Efficiency4.SetLineColor(ROOT.kGreen + 2)
    Efficiency4.SetMarkerColor(ROOT.kGreen + 2)

    legend4 = ROOT.TLegend(0.1,0.6,0.4,0.9)
    legend4.SetBorderSize(0)
    legend4.SetFillStyle(1001)
    legend4.AddEntry(Efficiency2,'Run2022C')
    legend4.AddEntry(Efficiency,'Run2022D')
    legend4.AddEntry(Efficiency3,'Run2022E')
    legend4.AddEntry(Efficiency4,'Run2022F')
    canvas3 = ROOT.TCanvas("Comparison","Comparison")
    canvas3.SetGrid()
    Efficiency.Draw("ap")
    Efficiency2.Draw("p same")
    Efficiency3.Draw("p same")
    Efficiency4.Draw("p same")
    legend4.Draw("same")

    #canvas3.SaveAs("Comparison_RunCDE_Quad.pdf")
    canvas3.SaveAs("Comparison_RunCDEF%s.pdf"%version)



