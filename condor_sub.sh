#!/bin/bash

# read arguments
WORKDIR=$1
SAMPLE=$2
TRIGGER=$3
ERA=$4
ID=$5

# create directories if not existing
cd $WORKDIR
mkdir ./histo_files/tmp/${ERA}
mkdir ./histo_files/tmp/${ERA}/goodfiles/

# setup
export X509_USER_PROXY=~/.t3/my_proxy.cert
source /cvmfs/cms.cern.ch/cmsset_default.sh
export XRD_NETWORKSTACK=IPv4
cd ../
source /cvmfs/cms.cern.ch/cmsset_default.sh
export CRAM_ARCH=slc7_amd64_gcc700
eval `scram r -sh`
cd $WORKDIR
ls -lrth $X509_USER_PROXY
voms-proxy-info -all

# run cmd
python HLT_HT_BTAG_condor.py --era ${ERA} --version ${TRIGGER} --input ${SAMPLE} --outdir ./histofiles_Sep2023/tmp/${ERA} --id ${ID}
