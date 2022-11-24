WORKDIR=$1
SAMPLE=$2
TRIGGER=$3
ERA=$4
ID=$5

cd $WORKDIR
mkdir ./histo_files/tmp/${ERA}
mkdir ./histo_files/tmp/${ERA}/goodfiles/

cd ..
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram r -sh`
cd $WORKDIR
export X509_USER_PROXY=~/.t3/proxy.cert

python HLT_HT_BTAG_condor.py --era ${ERA} --version ${TRIGGER} --input ${SAMPLE} --outdir ./histo_files/tmp/${ERA} --id ${ID}
