#!bin/bash

WORKDIR=/home/llr/cms/portales/HIGtrigger/higgs-trigger-nanoaod/CMSSW_10_6_18/src/higgs-trigger-nanoaod/
DATA_DIR=${WORKDIR}/data/dataset_lists/

#JOB_ID=0

declare -A TRIGGERS_PER_ERA
#TRIGGERS_PER_ERA["22C"]="PNetbb"
#TRIGGERS_PER_ERA["22D"]="PNetbb"
#TRIGGERS_PER_ERA["22E"]="PNetbb"
#TRIGGERS_PER_ERA["22F"]="PNetbb"

#TRIGGERS_PER_ERA["22B"]="PNetbb DoublePhoton"
#TRIGGERS_PER_ERA["22C"]="PNetbb DoublePhoton"
#TRIGGERS_PER_ERA["22D"]="PNetbb DoublePhoton"
#TRIGGERS_PER_ERA["22E"]="PNetbb DoublePhoton"
#TRIGGERS_PER_ERA["22F"]="PNetbb DoublePhoton"
#TRIGGERS_PER_ERA["22G"]="PNetbb DoublePhoton"

#TRIGGERS_PER_ERA["22all"]="PNetbb DoublePhoton"
#TRIGGERS_PER_ERA["23all"]="PNetbb DoublePhoton"
TRIGGERS_PER_ERA["22all"]="DoublePhoton"
#TRIGGERS_PER_ERA["23all"]="PNetbb DoublePhoton"

#TRIGGERS_PER_ERA["23C"]="DoublePhoton"
#TRIGGERS_PER_ERA["23D"]="DoublePhoton"


#TRIGGERS_PER_ERA["22B"]="PNetbb PNetref DoublePhoton90 Quad1btag Quad2btag PFHT DoublePF"
#TRIGGERS_PER_ERA["22C"]="PNetbb PNetref DoublePhoton90 Quad1btag Quad2btag PFHT DoublePF"
#TRIGGERS_PER_ERA["22D"]="PNetbb PNetref DoublePhoton90 Quad1btag Quad2btag PFHT DoublePF"
#TRIGGERS_PER_ERA["22E"]="PNetbb PNetref DoublePhoton90 Quad1btag Quad2btag PFHT DoublePF"
#TRIGGERS_PER_ERA["22F"]="PNetbb PNetref DoublePhoton90 Quad1btag Quad2btag PFHT DoublePF"
#TRIGGERS_PER_ERA["22G"]="PNetbb PNetref DoublePhoton90 Quad1btag Quad2btag PFHT DoublePF"

#TRIGGERS_PER_ERA["22F"]="Quad PFHT"
#TRIGGERS_PER_ERA["22G"]="Quad PFHT"
#TRIGGERS_PER_ERA["22F"]="Quad"
#TRIGGERS_PER_ERA["22G"]="Quad"

#TRIGGERS_PER_ERA["18D"]="DoublePhoton Quad PFHT"
#TRIGGERS_PER_ERA["22C"]="PNet_ref"
#TRIGGERS_PER_ERA["22D"]="PNet_ref"
#TRIGGERS_PER_ERA["22E"]="PNet_ref"
#TRIGGERS_PER_ERA["22F"]="PNet_ref"


#NTOT=0
#NSUB=0
for era in ${!TRIGGERS_PER_ERA[@]};
do
    echo $era ${!TRIGGERS_PER_ERA[${era}]}
    for trigger in ${TRIGGERS_PER_ERA[${era}]}
    do
	echo ${era} $trigger
	if [[ "$trigger" == "DoublePhoton" ]]
	then
	    #if [[ "$era" == *"22"* ]]
	    #then
	    FILE_LIST=${DATA_DIR}/Run${era}_JetMET.txt
	    #else
	    #	FILE_LIST=${DATA_DIR}/Run${era}_JetHT.txt
	    #fi
	else
	    #if [[ "$era" == *"22"* ]]
	    #then
	    FILE_LIST=${DATA_DIR}/Run${era}_Muon.txt
	    #else
	    #	FILE_LIST=${DATA_DIR}/Run${era}_SingleMuon.txt
	    #fi
	fi

	JOB_ID=0
	cat $FILE_LIST | while read line
	do
	    EXPECTED_OUT=histofiles_Sep2023/tmp/${era}/goodfiles/histos_Run${era}_${trigger}_${JOB_ID}.root
	    (( NTOT++ ))
	    echo $NSUB / $NTOT
	    if [ -f "$EXPECTED_OUT" ]; then
		#echo $EXPECTED_OUT 'already exists.'
		let JOB_ID++
	    else
		#echo /opt/exp_soft/cms/t3/t3submit -short -singleout condor_sub.sh ${WORKDIR} ${line} ${trigger} ${era} ${JOB_ID}
		/opt/exp_soft/cms/t3/t3submit -short -singleout condor_sub.sh ${WORKDIR} ${line} ${trigger} ${era} ${JOB_ID}
		#condor_submit condor_sub.sh ${WORKDIR} ${line} ${trigger} ${era}
		let JOB_ID++
	        (( NSUB++ ))
	    fi
	    echo test1 $NSUB / $NTOT
	done
	    echo test2 $NSUB / $NTOT
    done
	    echo test3 $NSUB / $NTOT / $JOB_ID
done

echo "$((NSUB)) jobs submitted out of $((NTOT))"
