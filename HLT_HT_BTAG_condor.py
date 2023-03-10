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

# - utility for even bins in log scale
import numpy as np
from array import array
def log_binning(nbin,low_edge,up_edge):
    bins = np.logspace(np.log10(low_edge),np.log10(up_edge),nbin+1)
    return array('d',bins) # format supported by ROOT.TH1

###########################
#### Event selections #####
###########################
from selections import *
#


####################
#### HLT paths #####
####################
def get_path_dict(year):
    #to complete
    if '18' in year:
        triggers = {
            'PFHT'            : 'PFHT450_SixPFJet36_PFBTagDeepJet_1p59',
            'DoublePFMuon'    : 'Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepJet_p71',
            'DoublePF'        : 'DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepJet_p71',
            'Quad'            : 'QuadPFJet103_88_75_15_DoublePFBTagDeepJet_1p3_7p7_VBF1',
            'DoublePhoton'    : 'Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90',
        }

    else:
        triggers = {
            # some selection already defined for these:
            'PFHT'            : 'PFHT450_SixPFJet36_PFBTagDeepJet_1p59', # selection OK
            'DoublePFMuon'    : 'Mu12_DoublePFJets40MaxDeta1p6_DoublePFBTagDeepJet_p71',
            'DoublePF'        : 'DoublePFJets128MaxDeta1p6_DoublePFBTagDeepJet_p71', # selection OK
            'Quad2btag'       : 'QuadPFJet103_88_75_15_DoublePFBTagDeepJet_1p3_7p7_VBF1', #selection ok
            'DoublePhoton90'  : 'Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90', # selection OK
            'PNetref'         : 'AK8PFJet230_SoftDropMass40', # selection ok
            'PNetbb'          : 'AK8PFJet250_SoftDropMass40_PFAK8ParticleNetBB0p35', #selection ok
            'PNettautau'      : 'AK8PFJet230_SoftDropMass40_PFAK8ParticleNetTauTau0p30',
            'PNetquad'        : 'QuadPFJet70_50_40_30_PFBTagParticleNet_2BTagSum0p65',

            # TO DO:
            'Quad1btag'      : 'QuadPFJet103_88_75_15_PFBTagDeepJet_1p3_VBF2',  #selection ok
            'Phot165'         : 'Photon165_R9Id90_HE10_IsoM',
            'Pho35_2pr'       : 'Photon35_TwoProngs35_v3',  # selection OK
            #'DoublePhoton_m55': 'Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_Mass55', # selection OK
            #'DoublePhoton'    : 'Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId', # selection OK
            #'Ele_AK8PNet'     : 'Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PFAK8ParticleNetBB0p35',

        }
    return triggers


class TrigBtagAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):

        ##################################
        #### Initializing some stuff #####
        ##################################
        Module.beginJob(self,histFile,histDirName)
        version =  str(histFile.GetName()).replace('histos_BTagTrigNanoAOD_RunD_','').replace('.root','')
        print('version: {}'.format(version))
        self.version = version.split('_')[2]
        self.period = version.split('_')[1]
        print("VERSION: {}".format(self.version), " PERIOD: {}".format(self.period))

        ################################
        #### Histograms definition #####
        ################################
        ###
        # save NPV for all triggers + utility histograms
        ################################################################################################################
        self.h_cutflow                = ROOT.TH1F("h_cutflow","; steps",10,-0.5,9.5)
        self.h_passreftrig            = ROOT.TH1F("h_passreftrig" , "; passed ref trigger" , 2 , 0. , 2. )
        self.addObject(self.h_cutflow)
        self.addObject(self.h_passreftrig )

        self.h_npv_all            = ROOT.TH1F("h_npv_all" ,            "; NPV" ,                   100,  0., 100.  )
        self.h_npv_passtrig       = ROOT.TH1F("h_npv_passtrig" ,       "; NPV" ,                   100,  0., 100.  )
        self.addObject(self.h_npv_all )
        self.addObject(self.h_npv_passtrig )

        ###
        # path-specific histograms
        ################################################################################################################
        if 'DoublePhoton' in self.version: # DoublePhoton, DoublePhoton90, DoublePhoton55
            self.h_all                = ROOT.TH1F("h_pt1_all" ,                "; Leading photon pT" ,     1000, 0., 1000. )
            self.h_passtrig           = ROOT.TH1F("h_pt1_passtrig" ,           "; Leading photon pT" ,     1000, 0., 1000. )
            self.h_sub_all            = ROOT.TH1F("h_pt2_all" ,            "; Sub-leading photon pT" , 1000, 0., 1000. )
            self.h_sub_passtrig       = ROOT.TH1F("h_pt2_passtrig" ,       "; Sub-leading photon pT" , 1000, 0., 1000. )
            self.h_myy_all            = ROOT.TH1F("h_myy_all" ,            "; m_{#gamma#gamma}" ,      1000, 0., 1000. )
            self.h_myy_passtrig       = ROOT.TH1F("h_myy_passtrig" ,       "; m_{#gamma#gamma}" ,      1000, 0., 1000. )
            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_sub_all )
            self.addObject(self.h_sub_passtrig )
            self.addObject(self.h_myy_all )
            self.addObject(self.h_myy_passtrig )

        ################################################################################################################
        elif 'PFHT' == self.version:
            self.h_all          = ROOT.TH1F("h_ht_all" ,                "; HT" ,     1000, 0., 1000. )
            self.h_passtrig     = ROOT.TH1F("h_ht_passtrig" ,           "; HT" ,     1000, 0., 1000. )
            self.h_tag_all      = ROOT.TH1F("h_tag_all" ,                "; Jet b-tag DeepFlavB" ,     1000, 0., 1. )
            self.h_tag_passtrig = ROOT.TH1F("h_tag_passtrig" ,           "; Jet b-tag DeepFlavB" ,     1000, 0., 1. )
            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_tag_all )
            self.addObject(self.h_tag_passtrig )

        ################################################################################################################
        elif 'DoublePF' == self.version:
            self.h_all          = ROOT.TH1F("h_pt1_all" ,           "; Leading jet pT" , 1500, 0., 1500.   )
            self.h_passtrig     = ROOT.TH1F("h_pt1_passtrig" ,      "; Leading jet pT" , 1500, 0., 1500.   )
            self.h_tag_all      = ROOT.TH1F("h_tag_all" ,      "; Jet b-tag DeepFlavB" ,      1000, 0., 1.)
            self.h_tag_passtrig = ROOT.TH1F("h_tag_passtrig" , "; Jet b-tag DeepFlavB" ,      1000, 0., 1.)
            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_tag_all )
            self.addObject(self.h_tag_passtrig )

        ################################################################################################################
        elif 'Quad' in self.version:
            self.h_all          = ROOT.TH1F("h_pt1_all" ,           "; Leading jet pT" , 1500, 0., 1500.   )
            self.h_passtrig     = ROOT.TH1F("h_pt1_passtrig" ,      "; Leading jet pT" , 1500, 0., 1500.   )
            self.h_tag_all      = ROOT.TH1F("h_tag_all" ,      "; Jet b-tag DeepFlavB" ,      1000, 0., 1.)
            self.h_tag_passtrig = ROOT.TH1F("h_tag_passtrig" , "; Jet b-tag DeepFlavB" ,      1000, 0., 1.)
            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_tag_all )
            self.addObject(self.h_tag_passtrig )

        ################################################################################################################
        elif 'PNet' in self.version:
            self.h_all           = ROOT.TH1F("h_pt1_all" ,           "; Fatjet pT" , 1500, 0., 1500.   )
            self.h_passtrig      = ROOT.TH1F("h_pt1_passtrig" ,      "; Fatjet pT" , 1500, 0., 1500.   )
            self.h_tag_all       = ROOT.TH1F("h_tag_all" ,      "; ParticleNet HbbvsQCD" , 1000, 0., 1.)
            self.h_tag_passtrig  = ROOT.TH1F("h_tag_passtrig" , "; ParticleNet HbbvsQCD" , 1000, 0., 1.)
            self.h_mass_all      = ROOT.TH1F("h_mass_all" ,      "; SoftDrop Mass" , 1500, 0., 1500.)
            self.h_mass_passtrig = ROOT.TH1F("h_mass_passtrig" , "; SoftDrop Mass" , 1500, 0., 1500.)

            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_tag_all )
            self.addObject(self.h_tag_passtrig )
            self.addObject(self.h_mass_all )
            self.addObject(self.h_mass_passtrig )

        ################################################################################################################
        else:
            self.h_all           = ROOT.TH1F("h_pt1_all" ,           "; Leading jet pT" , 1500, 0., 1500.   )
            self.h_passtrig      = ROOT.TH1F("h_pt1_passtrig" ,      "; Leading jet pT" , 1500, 0., 1500.   )
            self.h_tag_all       = ROOT.TH1F("h_tag_all" ,      "; Jet b-tag DeepFlavB" , 1000, 0., 1.)
            self.h_tag_passtrig  = ROOT.TH1F("h_tag_passtrig" , "; Jet b-tag DeepFlavB" , 1000, 0., 1.)

            self.addObject(self.h_all )
            self.addObject(self.h_passtrig )
            self.addObject(self.h_tag_all )
            self.addObject(self.h_tag_passtrig )

    ###########################
    #### Trigger analysis #####
    ###########################
    def analyze(self, event):
        met     = Object(event, "MET" )
        hlt     = Object(event, "HLT" )
        PV      = Object(event, "PV" )
        jets    = Collection(event, "Jet"     )
        fatjets = Collection(event, "FatJet"  )
        muons   = Collection(event, "Muon"    )
        photons = Collection(event, "Photon"  )
        trigobj = Collection(event, "TrigObj" )
        version = self.version
        period    = self.period


        #custom check for hlt, returning 0 if path not defined in NanoAOD
        def hlt_accept(path):
            if hasattr(hlt,path):
                return eval('hlt.{}'.format(path))
            else:
                return 0

        # Selection
        pass_selection = False
        self.h_cutflow.Fill(0)

        ################################################################################################################
        if 'PFHT' in version: ### OK
            triggerVersion = 'PFHT'
            pass_selection_npv = sel_pfht_forNpv(jets)
            pass_selection_ht = sel_pfht_ht_turnon(jets)
            pass_selection_tag = sel_pfht_btag_turnon(jets)
            pass_selection = pass_selection_npv or pass_selection_ht or pass_selection_tag
            ak4jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4] # PFHT

        ################################################################################################################
        elif 'DoublePFMuon' in version:
            triggerVersion = 'DoublePFMuon'
            pass_selection = pass_selection_doublePFMuon(jets,muons)
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] # doublePF(Muon) / Quad

        ################################################################################################################
        elif 'DoublePF' in version:
            triggerVersion = 'DoublePF'
            pass_selection_npv = sel_doublepf_forNpv(jets)
            pass_selection_pt  = sel_doublepf_leadpt_turnon(jets)
            pass_selection_tag = sel_doublepf_btag_turnon(jets)
            pass_selection = pass_selection_npv or pass_selection_pt or pass_selection_tag
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] # doublePF(Muon) / Quad

        ################################################################################################################
        elif 'Quad1btag' in version:
            triggerVersion = 'Quad1btag'
            pass_selection_npv = sel_quad1btag_forNpv(jets)
            pass_selection_pt  = sel_quad1btag_leadpt_turnon(jets)
            pass_selection_tag = sel_quad1btag_btag_turnon(jets)
            pass_selection = pass_selection_npv or pass_selection_pt or pass_selection_tag
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7]

        ################################################################################################################
        elif 'Quad2btag' in version:
            triggerVersion = 'Quad2btag'
            pass_selection_npv = sel_quad2btag_forNpv(jets)
            pass_selection_pt  = sel_quad2btag_leadpt_turnon(jets)
            pass_selection_tag = sel_quad2btag_btag_turnon(jets)
            pass_selection = pass_selection_npv or pass_selection_pt or pass_selection_tag
            ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7]

        ################################################################################################################
        elif 'DoublePhoton' in version: ### OK
            triggerVersion = version#'DoublePhoton'
            strmass = triggerVersion.replace('DoublePhoton','')
            if not strmass:
                mass = 0
            else:
                mass = int(strmass)
            pass_selection_npv  = sel_doublephoton_forNpv(mass,photons)
            pass_selection_mass = sel_doublephoton_forMass(photons)
            phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442)]
            phots.sort(key = lambda x: x.pt, reverse = True)
            pass_selection = pass_selection_npv or pass_selection_mass

        ################################################################################################################
        elif 'PNet' in version:
            triggerVersion = 'PNetbb'
            if 'PNet_ref' in version:
                triggerVersion = 'PNet_ref'
            pass_selection_npv  = sel_pnet_forNpv(fatjets)
            pass_selection_pt   = sel_pnet_pt_turnon(fatjets)
            pass_selection_mass = sel_pnet_mass_turnon(fatjets)
            pass_selection_tag  = sel_pnet_tag_turnon(fatjets)
            pass_selection = pass_selection_npv or pass_selection_pt or pass_selection_tag or pass_selection_mass

            ak8jets = [j for j in fatjets if (j.pt>15 and abs(j.eta)<2.4)]

        ################################################################################################################

        #########################
        #### Skim selection #####
        #########################
        if not pass_selection: # pass *at least* one trigger selection
            return False
        self.h_cutflow.Fill(1)

        ####################
        #### HLT paths #####
        ####################
        triggers = get_path_dict(period)

        #############################
        #### Reference triggers #####
        #############################
        refAccept = hlt_accept('IsoMu27')
        if 'DoublePhoton' in version:
            refAccept = (hlt_accept('PFJet40') or
                         hlt_accept('PFJet60') or
                         hlt_accept('PFJet80') or
                         hlt_accept('PFJet140') or
                         hlt_accept('PFJet200') or
                         hlt_accept('PFJet260') or
                         hlt_accept('PFJet320') or
                         hlt_accept('PFJet400') or
                         hlt_accept('PFJet450') or
                         hlt_accept('PFJet500') or
                         hlt_accept('PFJet550') or
                         hlt_accept('PFJetFwd15') or
                         hlt_accept('PFJetFwd25') or
                         hlt_accept('PFJetFwd40') or
                         hlt_accept('PFJetFwd60') or
                         hlt_accept('PFJetFwd80') or
                         hlt_accept('PFJetFwd140') or
                         hlt_accept('PFJetFwd200') or
                         hlt_accept('PFJetFwd260') or
                         hlt_accept('PFJetFwd320') or
                         hlt_accept('PFJetFwd400') or
                         hlt_accept('PFJetFwd450') or
                         hlt_accept('PFJetFwd500'))

        self.h_passreftrig.Fill(refAccept)

        if not refAccept:
           return False

        self.h_cutflow.Fill(2)

        #####################
        #### HLT accept #####
        #####################

        ###
        # check if trigger is passed
        sigAccept = hlt_accept(triggers[triggerVersion])

        ###
        # fill NPV hist for all triggers
        ################################################################################################################
        if pass_selection_npv:
            self.h_npv_all.Fill(PV.npvs)
            if sigAccept:
                self.h_npv_passtrig.Fill(PV.npvs)

        ###
        # trigger specific histogram filling
        ################################################################################################################
        if 'DoublePhoton' in version:
            tag_photon = phots[0]
            tag_sub_photon = phots[1]

            tlv1 = ROOT.TLorentzVector()
            tlv2 = ROOT.TLorentzVector()
            tlv1.SetPtEtaPhiM(tag_photon.pt,tag_photon.eta,tag_photon.phi,0)
            tlv2.SetPtEtaPhiM(tag_sub_photon.pt,tag_sub_photon.eta,tag_sub_photon.phi,0)
            tlv12 = tlv1+tlv2
            myy = tlv12.M()
            if pass_selection_npv:
                self.h_all.Fill(tag_photon.pt)
                self.h_sub_all.Fill(tag_sub_photon.pt)
            if pass_selection_mass:
                self.h_myy_all.Fill(myy)

            if sigAccept:
                if pass_selection_npv:
                    self.h_passtrig.Fill(tag_photon.pt)
                    self.h_sub_passtrig.Fill(tag_sub_photon.pt)
                if pass_selection_mass:
                    self.h_myy_passtrig.Fill(myy)

        ################################################################################################################
        elif 'PFHT' in version:
            ht = sum(j.pt for j in ak4jets)
            ak4jets.sort(key = lambda x: x.btagDeepFlavB, reverse = True)
            tag_jet = ak4jets[0]
            if pass_selection_ht:
                self.h_all.Fill(ht)
                if sigAccept:
                    self.h_passtrig.Fill(ht)
            if pass_selection_tag:
                self.h_tag_all.Fill(tag_jet.btagDeepFlavB)
                if sigAccept:
                    self.h_tag_passtrig.Fill(tag_jet.btagDeepFlavB)

        ################################################################################################################
        elif 'DoublePF' == version or 'Quad' in version:
            ak4jets.sort(key = lambda x: x.pt, reverse = True)
            lead_let = ak4jets[0]
            if pass_selection_pt:
                self.h_all.Fill(lead_let.pt)
                if sigAccept:
                    self.h_passtrig.Fill(lead_let.pt)
            ak4jets.sort(key = lambda x: x.btagDeepFlavB, reverse = True)
            tag_jet = ak4jets[0]
            if pass_selection_tag:
                self.h_tag_all.Fill(tag_jet.btagDeepFlavB)
                if sigAccept:
                    self.h_tag_passtrig.Fill(tag_jet.btagDeepFlavB)

        ################################################################################################################
        elif 'PNet' in version:
            if pass_selection_pt:
                self.h_all.Fill(ak8jets[0].pt)
                if sigAccept:
                    self.h_passtrig.Fill(ak8jets[0].pt)
            if pass_selection_tag:
                self.h_tag_all.Fill(ak8jets[0].particleNet_HbbvsQCD )
                if sigAccept:
                    self.h_tag_passtrig.Fill(ak8jets[0].particleNet_HbbvsQCD)
            if pass_selection_mass:
                self.h_mass_all.Fill(ak8jets[0].msoftdrop )
                if sigAccept:
                    self.h_mass_passtrig.Fill(ak8jets[0].msoftdrop)


        elif not 'PNet' in version:
            ak4jets.sort(key = lambda x: x.btagDeepFlavB, reverse = True)
            tag_jet = ak4jets[0]
            ak4jets.sort(key = lambda x: x.pt, reverse = True)
            lead_jet = ak4jets[0]

            self.h_all.Fill(tag_jet.btagDeepFlavB)
            self.h_lead_all.Fill(lead_jet.pt)

            if sigAccept:
                self.h_passtrig.Fill(tag_jet.btagDeepFlavB)
                self.h_lead_passtrig.Fill(lead_jet.pt)

        else:
            self.h_all.Fill(ak8jets[0].pt)
            self.h_pnet_all.Fill(ak8jets[0].particleNet_HbbvsQCD )
            if sigAccept:
                self.h_passtrig.Fill(ak8jets[0].pt)
                self.h_pnet_passtrig.Fill(ak8jets[0].particleNet_HbbvsQCD)

        return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Args')
    #parser.add_argument('--version', default='PFHT')
    parser.add_argument('--version', default='PNetbb')
    parser.add_argument('--era', default = '22D')
    parser.add_argument('--input', default = '/store/data/Run2022D/Muon/NANOAOD/PromptNanoAODv10_v2-v1/2530000/c774b6ab-d647-47cd-a019-897c28240572.root')
    #parser.add_argument('--input', default = '/store/data/Run2022D/JetMET/NANOAOD/PromptNanoAODv10_v2-v1/60000/4b1921e7-c619-4634-8199-3c9bd5ee5bc4.root')
    parser.add_argument('--outdir', default = './')
    parser.add_argument('--id', default = '')
    args = parser.parse_args()

    path_json = './data/golden_json/'
    jsons = {
        '22B': 'Cert_Collisions2022_eraB_355100_355769_Golden.json',
        '22C': 'Cert_Collisions2022_eraC_355862_357482_Golden.json',
        '22D': 'Cert_Collisions2022_eraD_357538_357900_Golden.json',
        '22E': 'Cert_Collisions2022_eraE_359022_360331_Golden.json',
        '22F': 'Cert_Collisions2022_eraF_360390_362167_Golden.json',
        '22G': 'Cert_Collisions2022_eraG_362433_362760_Golden.json',
        '18D': 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt',
    }
    preselection="1"

    files = ['root://cms-xrd-global.cern.ch/' + args.input if '/store/' in args.input else args.input]
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
        jsonInput= path_json + '' + jsons[args.era],
        #prefetch=True
    )

    p.run()

    ## to sort 'good files' from files victim of runtime failure
    hist_out = histFile.replace('/histos','/goodfiles/histos')
    os.popen('mv {} {}'.format(histFile, hist_out))
    print('Saving results in {}'.format(hist_out))
