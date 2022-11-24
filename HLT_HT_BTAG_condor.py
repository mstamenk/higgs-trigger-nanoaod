#!/usr/bin/env python
import os, sys, glob
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from importlib import import_module
import argparse

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class TrigBtagAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):

        Module.beginJob(self,histFile,histDirName)

        self.version = str(histFile.GetName()).replace('histos_BTagTrigNanoAOD_RunD_','').replace('.root','')

        if 'DoublePhoton' in self.version:
            self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger" , 2 , 0. , 2. )
            self.h_all      = ROOT.TH1F("h_all" , "; Leading photon pT" , 300, 0., 1500. )
            self.h_passtrig = ROOT.TH1F("h_passtrig" , "; Leading photon pT" , 300, 0., 1500.)

            self.h_sub_all      = ROOT.TH1F("h_sub_all" , "; Sub-leading photon pT" , 300, 0., 1500. )
            self.h_sub_passtrig = ROOT.TH1F("h_sub_passtrig" , "; Sub-leading photon pT" , 300, 0., 1500.)
            self.addObject(self.h_passreftrig )
            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_sub_all )
            self.addObject(self.h_sub_passtrig )

            self.h_csv_all      = ROOT.TH1F("h_csv_all" , "; Leading photon pT" , 300, 0., 1500. )
            self.h_csv_passtrig = ROOT.TH1F("h_csv_passtrig" , "; Leading photon pT" , 300, 0., 1500.)
            self.addObject(self.h_csv_all )
            self.addObject(self.h_csv_passtrig )

        else: # version != 'DoublePhoton'

            self.h_firsthalf_passreftrig  = ROOT.TH1F("h_firsthalf_passreftrig" , "; passed ref trigger" , 2 , 0. , 2. )
            self.h_firsthalf_all      = ROOT.TH1F("h_firsthalf_all" , "; Jet b-tag DeepFlavB" , 10, 0., 1. )
            self.h_firsthalf_passtrig = ROOT.TH1F("h_firsthalf_passtrig" , "; Jet b-tag DeepFlavB" , 10, 0., 1.)
            self.addObject(self.h_firsthalf_passreftrig )
            self.addObject(self.h_firsthalf_all )
            self.addObject(self.h_firsthalf_passtrig )

            self.h_firsthalf_lead_all      = ROOT.TH1F("h_firsthalf_lead_all" , "; Leading jet pT" , 300, 0., 1500. )
            self.h_firsthalf_lead_passtrig = ROOT.TH1F("h_firsthalf_lead_passtrig" , "; Leading jet pT" , 300, 0., 1500.)
            self.addObject(self.h_firsthalf_lead_all )
            self.addObject(self.h_firsthalf_lead_passtrig )

            self.h_firsthalf_csv_all      = ROOT.TH1F("h_firsthalf_csv_all" , "; Jet b-tag DeepFlavB" , 10, 0., 1. )
            self.h_firsthalf_csv_passtrig = ROOT.TH1F("h_firsthalf_csv_passtrig" , "; Jet b-tag DeepFlavB" , 10, 0., 1.)
            self.addObject(self.h_firsthalf_csv_all )
            self.addObject(self.h_firsthalf_csv_passtrig )

            self.h_firsthalf_csv_lead_all      = ROOT.TH1F("h_firsthalf_csv_lead_all" , "; Leading jet pT" , 300, 0., 1500. )
            self.h_firsthalf_csv_lead_passtrig = ROOT.TH1F("h_firsthalf_csv_lead_passtrig" , "; Leading jet pT" , 300, 0., 1500.)
            self.addObject(self.h_firsthalf_csv_lead_all )
            self.addObject(self.h_firsthalf_csv_lead_passtrig )

            # filling second copy for run < 361514
            self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger" , 2 , 0. , 2. )
            self.h_all      = ROOT.TH1F("h_all" , "; Jet b-tag DeepFlavB" , 10, 0., 1. )
            self.h_passtrig = ROOT.TH1F("h_passtrig" , "; Jet b-tag DeepFlavB" , 10, 0., 1.)
            self.addObject(self.h_passreftrig )
            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )

            self.h_lead_all      = ROOT.TH1F("h_lead_all" , "; Leading jet pT" , 300, 0., 1500. )
            self.h_lead_passtrig = ROOT.TH1F("h_lead_passtrig" , "; Leading jet pT" , 300, 0., 1500.)
            self.addObject(self.h_lead_all )
            self.addObject(self.h_lead_passtrig )

            self.h_csv_all      = ROOT.TH1F("h_csv_all" , "; Jet b-tag DeepFlavB" , 10, 0., 1. )
            self.h_csv_passtrig = ROOT.TH1F("h_csv_passtrig" , "; Jet b-tag DeepFlavB" , 10, 0., 1.)
            self.addObject(self.h_csv_all )
            self.addObject(self.h_csv_passtrig )

            self.h_csv_lead_all      = ROOT.TH1F("h_csv_lead_all" , "; Leading jet pT" , 300, 0., 1500. )
            self.h_csv_lead_passtrig = ROOT.TH1F("h_csv_lead_passtrig" , "; Leading jet pT" , 300, 0., 1500.)
            self.addObject(self.h_csv_lead_all )
            self.addObject(self.h_csv_lead_passtrig )





    def analyze(self, event):
        met       = Object(event, "MET")
        hlt       = Object(event, "HLT")
        jets       = Collection(event, "Jet")
        muons = Collection(event,"Muon")
        photons = Collection(event,"Photon")
        trigobj = Collection(event,"TrigObj")
        version = self.version

        # Selection
        pass_selection = False

        if 'PFHT' in version:
            ak4jets = [j for j in jets if j.pt > 40 and abs(j.eta) < 2.4] # PFHT
            if len(ak4jets) > 0 :
                #ak4jets = [j for j in jets if j.pt > 45 and abs(j.eta) < 2.4] # Quad
                #ak4jets = [j for j in jets if j.pt > 45 and abs(j.eta) < 2.4] # DoublePF
                # Selection 
                ht = sum([j.pt for j in jets])
                #if len(ak4jets) < 6 or ht < 500: return False # PFHT
                #if len(ak4jets) < 4 or ht < 500: return False # Quad
                #if len(ak4jets) < 2 or ht < 500: return False # DoublePF
                pass_selection = len(ak4jets) > 5 and ht > 500

        elif 'DoublePFMuon' in version:
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
            ak4jets.sort(key = lambda x : x.pt, reverse = True)
            if len(ak4jets) > 1:
                jet1 = ak4jets[0]
                jet2 = ak4jets[1]
                muons_sorted = [mu for mu in muons if mu.pt > 12]
                if len(muons_sorted) < 1 : return False
                muon = muons_sorted[0]
                pass_selection = (jet1.pt > 40 and jet2.pt > 40 and abs(jet1.eta - jet2.eta) < 1.6 and len(ak4jets) > 1 and muon.pt > 12)

        elif 'DoublePF' in version:
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
            ak4jets.sort(key = lambda x : x.pt, reverse = True)
            if len(ak4jets) > 1:
                jet1 = ak4jets[0]
                jet2 = ak4jets[1]
                pass_selection = (jet1.pt > 116 and jet2.pt > 116 and abs(jet1.eta - jet2.eta) < 1.6 and len(ak4jets) > 1)

        elif 'Quad' in version:
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
            if len(ak4jets) > 3:
                jet1 = ak4jets[0]
                jet2 = ak4jets[1]
                jet3 = ak4jets[2]
                jet4 = ak4jets[3]
                pass_selection =  jet1.pt > 103 and jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and len(ak4jets) > 3

        elif 'DoublePhoton' in version:
            #phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442 and p.hadTowOverEm<0.12 and p.full5x5_sigmaIetaIeta()<0.015 and p.full5x5_r9>.5) or (p.pt > 15 and abs(p.eta)<2.5 and abs(p.eta)>1.5556 and p.hadTowOverEm<0.12 and p.full5x5_sigmaIetaIeta()<0.035 and p.full5x5_r9>.8)]
            trig_phots = [p for p in trigobj if p.id == 22]
            phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442)]
            tag_photons = []
            for photon in phots:
                for trig_phot in trig_phots:
                    if deltaR(photon, trig_phot) < 0.2:
                        tag_photons.append(photon)
            phots = tag_photons
            phots.sort(key = lambda x: x.pt, reverse = True) 
            if len(phots) > 1:
                p1 = phots[0]
                p2 = phots[1]
                pass_selection = p1.pt > 20 and p2.pt > 20
                print(phots)




        if pass_selection == False:
            return False



        #refAccept = hlt.PFHT450_SixPFJet36
        
        #to complete
        triggerAccept = {
            'PFHT'             : 0 if 'UL18' in version else hlt.PFHT450_SixPFJet36_PFBTagDeepJet_1p59,
            'PFHT_csv'         : hlt.PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,

            'DoublePFMuon'     : 0 if 'UL18' in version else hlt.Mu12_DoublePFJets40MaxDeta1p6_DoublePFBTagDeepJet_p71,
            'DoublePFMuon_csv' : hlt.Mu12_DoublePFJets40MaxDeta1p6_DoublePFBTagDeepCSV_p71, #run3
            #'DoublePFMuon_csv' : hlt.Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71, # closest run2 path (?)

            'DoublePF'         : 0 if 'UL18' in version else hlt.DoublePFJets116MaxDeta1p6_DoublePFBTagDeepJet_p71,
            'DoublePF_csv'     : hlt.DoublePFJets116MaxDeta1p6_DoublePFBTagDeepCSV_p71, #run3
            #'DoublePF_csv'     : hlt.DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71, # closest run2 path (?)

            'Quad'             : 0 if 'UL18' in version else hlt.QuadPFJet103_88_75_15_DoublePFBTagDeepJet_1p3_7p7_VBF1,
            'Quad_csv'         : hlt.QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1,
            
}


        refAccept = hlt.IsoMu27
        if 'PFHT' in version:
            sigAccept = triggerAccept['PFHT']
            sigAccept_csv = triggerAccept['PFHT_csv']
        elif 'DoublePFMuon' in version:
            sigAccept = triggerAccept['DoublePFMuon']
            sigAccept_csv = triggerAccept['DoublePFMuon_csv']
        elif 'DoublePF' in version:
            sigAccept = triggerAccept['DoublePF']
            sigAccept_csv = triggerAccept['DoublePF_csv']

        elif 'Quad' in version:
            sigAccept = triggerAccept['Quad']
            sigAccept_csv = triggerAccept['Quad_csv']

        elif 'DoublePhoton' in version:
            sigAccept = hlt.DoublePhoton70
            sigAccept_csv = hlt.DoublePhoton70



        if event.run > 361514:
            self.h_passreftrig.Fill(refAccept)
        else:
            self.h_firsthalf_passreftrig.Fill(refAccept)
            
        if not refAccept == True:
           return False

        if 'DoublePhoton' in version:
            tag_photon = p1
            tag_sub_photon = p2
            self.h_all.Fill(tag_photon.pt)
            self.h_sub_all.Fill(tag_sub_photon.pt)
            if sigAccept == True:
                if event.run > 361514:
                    self.h_passtrig.Fill(tag_photon.pt)
                    self.h_sub_passtrig.Fill(tag_sub_photon.pt)
                else:
                    self.h_firsthalf_passtrig.Fill(tag_photon.pt)
                    self.h_firsthalf_sub_passtrig.Fill(tag_sub_photon.pt)
        else:
            ak4jets.sort(key = lambda x : x.btagDeepFlavB, reverse = True)
            tag_jet = ak4jets[0]
            ak4jets.sort(key = lambda x : x.pt, reverse = True)
            lead_jet = ak4jets[0]
            if event.run > 361514:
                self.h_all.Fill(tag_jet.btagDeepFlavB)
                self.h_lead_all.Fill(lead_jet.pt)

                if sigAccept == True:
                    self.h_passtrig.Fill(tag_jet.btagDeepFlavB)
                    self.h_lead_passtrig.Fill(lead_jet.pt)
            
                #if (sigAccept_csv == True): #and event.run < 357754:
                self.h_csv_all.Fill(tag_jet.btagDeepFlavB)
                self.h_csv_lead_all.Fill(lead_jet.pt)
                if sigAccept_csv == True: 
                    self.h_csv_passtrig.Fill(tag_jet.btagDeepFlavB)
                    self.h_csv_lead_passtrig.Fill(lead_jet.pt)
            else:
                self.h_firsthalf_all.Fill(tag_jet.btagDeepFlavB)
                self.h_firsthalf_lead_all.Fill(lead_jet.pt)

                if sigAccept == True:
                    self.h_firsthalf_passtrig.Fill(tag_jet.btagDeepFlavB)
                    self.h_firsthalf_lead_passtrig.Fill(lead_jet.pt)
            
                #if (sigAccept_csv == True): #and event.run < 357754:
                self.h_firsthalf_csv_all.Fill(tag_jet.btagDeepFlavB)
                self.h_firsthalf_csv_lead_all.Fill(lead_jet.pt)
                if sigAccept_csv == True: 
                    self.h_firsthalf_csv_passtrig.Fill(tag_jet.btagDeepFlavB)
                    self.h_firsthalf_csv_lead_passtrig.Fill(lead_jet.pt)


        return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--version', default='PFHT')
    parser.add_argument('--era', default = 'D')
    parser.add_argument('--input', default = '')
    parser.add_argument('--outdir', default = './')
    parser.add_argument('--id', default = '')
    args = parser.parse_args()

    #path_json = '/isilon/data/users/mstamenk/hig-trigger/CMSSW_10_6_18/src/ShortExerciseTrigger2022/ShortExerciseTrigger/test/golden_json/'
    path_json = './data/golden_json/'
    jsons = {
        '22C':     'Cert_Collisions2022_eraC_355862_357482_Golden.json',
        '22D':     'Cert_Collisions2022_eraD_357538_357900_Golden.json',
        '22E':     'Cert_Collisions2022_eraE_359022_360331_Golden.json',
        '22F':     'Cert_Collisions2022_eraF_360390_361580_Golden.json',
        '18F':  'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt',
    }
    preselection="1"

    samples_file = 'data/dataset_lists/Run{}_Muon.txt'.format(args.era)
    if args.era=='18F':
        samples_file = 'data/dataset_lists/Run18F_SingleMuon.txt'

    with open(samples_file, 'r') as f:
        lines = f.read().splitlines()
#    files = ['root://cmsxrootd.fnal.gov/'+ l for l in lines]
    files = ['root://xrootd-cms.infn.it/' + args.input]
    print(files)

    histFile = "{}/histos_Run{}_{}_{}.root".format(args.outdir,args.era,args.version,args.id)

    p=PostProcessor(
        ".",
        files,
        cut=preselection,
        branchsel=None,
        modules=[TrigBtagAnalysis()],
        noOut=True,
        histFileName=histFile,
        histDirName="BTagNanoAOD",
        jsonInput= path_json + '' + jsons[args.era]
    )
    
    p.run()

    ### to sort 'good files' from files victim of runtime failure
    hist_out = histFile.replace('/histos','/goodfiles/histos')
    os.popen('mv {} {}'.format(histFile, hist_out))
    print('Saving results in {}'.format(hist_out))
