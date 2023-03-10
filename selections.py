#!/usr/bin/env python
import ROOT

###
# (b-)jet requirements
###
def pass_njet(njetmin, ptmin, jets):
    # checking that Njet > njetmin (with pt > ptmin)
    ak4jets = [j for j in jets if j.pt > ptmin and abs(j.eta) < 2.4]
    return (len(ak4jets) >= njetmin)

def pass_ht(cut, jets):
    # checking that ht > cut
    ak4jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4] # PFHT
    ht = sum(j.pt for j in ak4jets)
    return (ht > cut)
    
def pass_Ntag_DeepJet(njet,jets):
    # checking that at least N jets have DeepJet score > 0.5
    ak4jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4]
    if len(ak4jets)<njet:
        return False
    if len(ak4jets)>6:
        ak4jets = ak4jets[0:6]
    ak4jets.sort(key = lambda x: x.btagDeepFlavB, reverse = True)
    return(ak4jets[njet-1].btagDeepFlavB>0.5)


###
# AK8jet requirements
###
def pass_nfatjet(njetmin,ptmin,fatjets):
    # checking that Nfatjet > njetmin (with pt > ptmin)
    ak8jets = [j for j in fatjets if (j.pt>ptmin and abs(j.eta)<2.4)]
    return (len(ak8jets) >= njetmin)
    
def pass_Ntag_AK8PNetBB(njet,fatjets):
    # checking that at least N fatjets have PNetBB score > 0.4
    ak8jets = [j for j in fatjets if j.pt > 15 and abs(j.eta) < 2.4]
    ak8jets.sort(key = lambda x: x.particleNet_HbbvsQCD, reverse = True)
    return(ak8jets[njet-1].particleNet_HbbvsQCD>0.4)

def pass_mass_fatjet(massmin,fatjets):
    ak8jets = [j for j in fatjets if (j.msoftdrop>massmin and abs(j.eta)<2.4)]
    return (len(ak8jets) > 0)

###
# photon requirements
###
def pass_nphoton(nphotonmin,ptmin,photons):
    # checking that Njet > njetmin (with pt > ptmin)
    phots = [j for j in photons if j.pt > ptmin and abs(j.eta) < 2.4]
    return (len(phots) >= npotonmin)

###
# VBF pair requirement
###
from itertools import combinations
def has_vbf_pair(mjjcut,detacut,jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets)<2:
        return False
    
    has_vbf = False
    for jet_pairs in combinations(ak4jets,2):
        p1 = jet_pairs[0]
        p2 = jet_pairs[1]
        if abs(p1.eta-p2.eta)>detacut:
            tlv1 = ROOT.TLorentzVector()
            tlv2 = ROOT.TLorentzVector()
            tlv1.SetPtEtaPhiM(p1.pt,p1.eta,p1.phi,0)
            tlv2.SetPtEtaPhiM(p2.pt,p2.eta,p2.phi,0)
            tlv12 = tlv1+tlv2
            mjj = tlv12.M()
            if mjj > mjjcut:
                has_vbf = True
    return has_vbf


############################
# selections for PFHT path #
############################
def sel_pfht_ht_turnon(jets):
    pass_njet_cut = pass_njet(6,40,jets)
    pass_1btag = pass_Ntag_DeepJet(1,jets)
    return (pass_njet_cut and pass_1btag)

def sel_pfht_btag_turnon(jets):
    pass_njet_cut = pass_njet(6,40,jets)
    pass_ht_cut = pass_ht(500,jets)
    return (pass_njet_cut and pass_ht_cut)

def sel_pfht_forNpv(jets):
    pass_njet_cut = pass_njet(6,40,jets)
    pass_ht_cut = pass_ht(500,jets)
    pass_1btag = pass_Ntag_DeepJet(1,jets)
    return (pass_njet_cut and pass_ht_cut and pass_1btag)
############################


####################################
# selections for DoublePFMuon path #
####################################
'''
TO DO
'''
####################################


################################
# selections for DoublePF path #
################################
def sel_doublepf_leadpt_turnon(jets):
    pass_njet_cut = pass_njet(2,80,jets)
    if not pass_njet_cut:
        return False
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    ak4jets.sort(key = lambda x : x.pt, reverse = True)
    pass_deta = (abs(ak4jets[0].eta - ak4jets[1].eta) < 1.6)
    pass_1btag = pass_Ntag_DeepJet(2,jets)
    return (pass_njet_cut and pass_1btag and pass_deta)

def sel_doublepf_btag_turnon(jets):
    pass_njet_cut = pass_njet(2,140,jets)
    if not pass_njet_cut:
        return False
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    ak4jets.sort(key = lambda x : x.pt, reverse = True)
    pass_deta = (abs(ak4jets[0].eta - ak4jets[1].eta) < 1.6)
    return (pass_njet_cut and pass_deta)

def sel_doublepf_forNpv(jets):
    pass_njet_cut = pass_njet(2,120,jets)
    if not pass_njet_cut:
        return False
    pass_2btag = pass_Ntag_DeepJet(2,jets)
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    ak4jets.sort(key = lambda x : x.pt, reverse = True)
    pass_deta = (abs(ak4jets[0].eta - ak4jets[1].eta) < 1.6)
    return (pass_njet_cut and pass_2btag and pass_deta)
################################

##################################
# selections for Quad_2btag path #
##################################
def sel_quad2btag_btag_turnon(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    has_vbf = has_vbf_pair(460.,3.5,jets)
    return (jet1.pt > 103 and jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and has_vbf)

def sel_quad2btag_leadpt_turnon(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    has_vbf = has_vbf_pair(460.,3.5,jets)
    pass_2btag = pass_Ntag_DeepJet(2,jets)    
    return (jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and pass_2btag and has_vbf)

def sel_quad2btag_forNpv(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    has_vbf = has_vbf_pair(460.,3.5,jets)
    pass_2btag = pass_Ntag_DeepJet(2,jets)    
    return (jet1.pt > 103 and jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and pass_2btag and has_vbf)


##################################

##################################
# selections for Quad_1btag path #
##################################
def sel_quad1btag_btag_turnon(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    has_vbf = has_vbf_pair(460.,3.5,jets)
    return (jet1.pt > 103 and jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and has_vbf)

def sel_quad1btag_leadpt_turnon(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    pass_1btag = pass_Ntag_DeepJet(1,jets) 
    has_vbf = has_vbf_pair(460.,3.5,jets)   
    return (jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and pass_1btag and has_vbf)

def sel_quad1btag_forNpv(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    pass_1btag = pass_Ntag_DeepJet(1,jets)  
    has_vbf = has_vbf_pair(460.,3.5,jets)  
    return (jet1.pt > 103 and jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15 and pass_1btag and has_vbf)
##################################


##############################
# selections for PNetBB path #
##############################
def sel_pnet_mass_turnon(fatjets):
    ak8jets = [j for j in fatjets if (j.pt>15 and abs(j.eta)<2.4)]
    if len(ak8jets)==0:
        return False
    j1 = ak8jets[0]
    ak8jets.sort(key = lambda x: x.particleNet_HbbvsQCD, reverse = True)
    bj1 = ak8jets[0]
    return (j1.pt>300. and bj1.particleNet_HbbvsQCD>0.8)
    
def sel_pnet_pt_turnon(fatjets):
    ak8jets = [j for j in fatjets if (j.pt>15 and abs(j.eta)<2.4)]
    if len(ak8jets)==0:
        return False
    j1 = ak8jets[0]
    ak8jets.sort(key = lambda x: x.particleNet_HbbvsQCD, reverse = True)
    bj1 = ak8jets[0]
    return (j1.msoftdrop>60. and bj1.particleNet_HbbvsQCD>0.8)

def sel_pnet_tag_turnon(fatjets):
    ak8jets = [j for j in fatjets if (j.pt>15 and abs(j.eta)<2.4)]
    if len(ak8jets)==0:
        return False
    j1 = ak8jets[0]
    return (j1.msoftdrop>60. and j1.pt>300.)

def sel_pnet_forNpv(fatjets):
    ak8jets = [j for j in fatjets if (j.pt>15 and abs(j.eta)<2.4)]
    if len(ak8jets)==0:
        return False
    j1 = ak8jets[0]
    ak8jets.sort(key = lambda x: x.particleNet_HbbvsQCD, reverse = True)
    bj1 = ak8jets[0]
    return (j1.msoftdrop>60. and j1.pt>300. and bj1.particleNet_HbbvsQCD>0.8)
##############################


##################################
# selections for PNetTauTau path #
##################################
'''
TO DO
'''
##################################


################################
# selections for PNetQuad path #
################################
'''
TO DO
'''
################################




########################################
# selections for DoublePhoton(_mX) path #
########################################
def sel_doublephoton_forNpv(mass,photons):
    phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442)]
    phots.sort(key = lambda x: x.pt, reverse = True)
    if len(phots) < 2:
        return False
    p1 = phots[0]
    p2 = phots[1]
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    tlv1.SetPtEtaPhiM(p1.pt,p1.eta,p1.phi,0)
    tlv2.SetPtEtaPhiM(p2.pt,p2.eta,p2.phi,0)
    tlv12 = tlv1+tlv2
    myy = tlv12.M()
    if p1.cutBased>2 and p2.cutBased>2:
        print("====> myy={},p1cb={},p2cb={}".format(myy, p1.cutBased,p2.cutBased))
    if mass==0:
        return (p1.cutBased>2 and p2.cutBased>2)
    return (myy>mass and p1.cutBased>2 and p2.cutBased>2)

def sel_doublephoton_forMass(photons):
    phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442)]
    phots.sort(key = lambda x: x.pt, reverse = True)
    if len(phots) < 2:
        return False
    p1 = phots[0]
    p2 = phots[1]
    return (p1.cutBased>2 and p2.cutBased>2)
########################################




###
# OLD SELECTIONS, STILL USED FOR MOST PATHS
###

def pass_selection_doublePhoton(photons):
    phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442)]
    phots.sort(key = lambda x: x.pt, reverse = True)
    if len(phots) < 2:
        return False
    p1 = phots[0]
    p2 = phots[1]
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    tlv1.SetPtEtaPhiM(p1.pt,p1.eta,p1.phi,0)
    tlv2.SetPtEtaPhiM(p2.pt,p2.eta,p2.phi,0)
    tlv12 = tlv1+tlv2
    myy = tlv12.M()
    return (myy>90 and p1.cutBased>2 and p2.cutBased>2)




def pass_selection_PFHT(jets):
    ak4jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4] # PFHT
    if len(ak4jets) == 0 :
        return False
    #ht = sum([j.pt for j in jets])
    ht = sum([j.pt for j in ak4jets])
    return (len(ak4jets) > 5 and ht > 500)

def pass_selection_PFHT_btag(jets):
    ak4jets = [j for j in jets if j.pt > 30 and abs(j.eta) < 2.4] # PFHT
    if len(ak4jets) == 0 :
        return False
    #ht = sum([j.pt for j in jets])
    ht = sum([j.pt for j in ak4jets])
    
    tagjet = ak4jets.sort(key = lambda x: x.btagDeepFlavB, reverse = True)[0]

    return (len(ak4jets) > 5 and tagjet.btagDeepFlavB>0.5)



    
def pass_selection_doublePFMuon(jets,muons):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    ak4jets.sort(key = lambda x : x.pt, reverse = True)
    if len(ak4jets) < 2:
        return False
    muons_sorted = [mu for mu in muons if mu.pt > 12]
    if len(muons_sorted) < 1 : 
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    muon = muons_sorted[0]
    return (jet1.pt > 40 and jet2.pt > 40 and abs(jet1.eta - jet2.eta) < 1.6 and muon.pt > 12)


def pass_selection_doublePF(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    ak4jets.sort(key = lambda x : x.pt, reverse = True)
    if len(ak4jets) < 2:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    return (jet1.pt > 116 and jet2.pt > 116 and abs(jet1.eta - jet2.eta) < 1.6)


def pass_selection_quad(jets):
    ak4jets = [j for j in jets if j.pt > 15 and abs(j.eta) < 4.7] 
    if len(ak4jets) < 4:
        return False
    jet1 = ak4jets[0]
    jet2 = ak4jets[1]
    jet3 = ak4jets[2]
    jet4 = ak4jets[3]
    return (jet1.pt > 103 and jet2.pt > 88 and jet3.pt > 75 and jet4.pt > 15)


def pass_selection_doublePhoton(photons):
    phots = [p for p in photons if (p.pt > 15 and abs(p.eta) < 1.4442)]
    phots.sort(key = lambda x: x.pt, reverse = True)
    if len(phots) < 2:
        return False
    p1 = phots[0]
    p2 = phots[1]
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    tlv1.SetPtEtaPhiM(p1.pt,p1.eta,p1.phi,0)
    tlv2.SetPtEtaPhiM(p2.pt,p2.eta,p2.phi,0)
    tlv12 = tlv1+tlv2
    myy = tlv12.M()
    return (myy>90 and p1.cutBased>2 and p2.cutBased>2)


def pass_selection_pnet(fatjets):
    ak8jets = [j for j in fatjets if (j.pt>15 and abs(j.eta)<2.4)]
    if len(ak8jets)==0:
        return False
    j1 = ak8jets[0]
    return (j1.pt>400. and j1.msoftdrop>50.)
    #return (j1.pt>400. and j1.msoftdrop>50. and j1.particleNet_HbbvsQCD>0.35)
