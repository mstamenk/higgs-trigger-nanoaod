#TRIGGERS="PFHT Quad"
TRIGGERS="PFHT"
#ERAS="22C 22D 22E 22F"
ERAS="22D"

WORKDIR=/home/llr/cms/portales/HIGtrigger/higgs-trigger-nanoaod/CMSSW_10_6_18/src/higgs-trigger-nanoaod/
DATA_DIR=${WORKDIR}/data/dataset_lists/

JOB_ID=0
for era in $ERAS
do
    FILE_LIST=${DATA_DIR}/Run${era}_Muon.txt
    cat $FILE_LIST | while read line
    do
	for trigger in $TRIGGERS
	do
	    EXPECTED_OUT=histo_files/tmp/${era}/goodfiles/histos_Run${era}_${trigger}_${JOB_ID}.root
	    if [ -f "$EXPECTED_OUT" ]; then
		echo $EXPECTED_OUT 'already exists.'
		let JOB_ID++
	    else
		/opt/exp_soft/cms/t3/t3submit -short -singleout condor_sub.sh ${WORKDIR} ${line} ${trigger} ${era} ${JOB_ID}
		let JOB_ID++
	    fi
	    #condor_submit condor_sub.sh ${WORKDIR} ${line} ${trigger} ${era}
	done
    done
done
