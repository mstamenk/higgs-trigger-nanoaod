# higgs-trigger-nanoaod
Framework to run on PromptNanoAOD to compute trigger efficiency curves

# Setting up
Setup CMSSW
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH="slc7_amd64_gcc700"
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv
git clone git@github.com:mstamenk/higgs-trigger-nanoaod.git
```

# Get NanoAOD tools
```
cd $CMSSW_BASE/src
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
scram b -j 4
cd $CMSSW_BASE/src/higgs-trigger-nanoaod
```

# Get samples list
Currently framework is using `cmsxrootd.fnal.gov` to access the samples from remote on `/store/`. To get the file list:
```
python get_muon_samples.py
```

This will store the list of available samples in `textfiles`

# Run trigger efficiency studies
```
python HLT_HT_BTAG.py --version DoublePhoton --era C
```
The script is done for some HLT path (also storing histograms comparing DeepCSV and DeepJet.

Small plotting maccro:
```
python BTag_Efficiency_Plotting.py
```



