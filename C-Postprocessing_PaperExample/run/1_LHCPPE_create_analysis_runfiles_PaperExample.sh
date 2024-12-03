#!/bin/usr/env bash

# this script create the analysis scripts for each parameter sets

# todo: to iterate over the correct number of runs, copy one parameter files in the pwd:
# cp /work/bd1179/b309216/icon/ICON-2.6.4/2.6.4/run/PaperExample/PARAMETER_SAMPLES/sample_PAPEREXAMPLE_Emid_Epen_Edd_Taumf_Pr_R0top-Epen.txt 

filename=sample_PAPEREXAMPLE_Emid_Epen_Edd_Taumf_Pr_R0top #TODO to update

nrun=0
increm=1
file1=${filename}-Epen.txt
while read -r line; do
    JOBNAME=nrun_${nrun}-PaperExample #TODO to update
    echo ${JOBNAME}
    
    #all outputs global analysis - physics outputs and psl (dynamic output)
    cp  template_runanalysisR2B5_1979-1980.sh run_analysis_R2B5_1979-1980_${JOBNAME}.sh
    sed -i 's/JOBNAME/'${JOBNAME}'/' run_analysis_R2B5_1979-1980_${JOBNAME}.sh
    
    #only tauu local - dynamic outputs
    cp  template_runanalysisR2B5_1979-1980_NAO_SOO.sh run_analysis_R2B5_1979-1980_${JOBNAME}_NAO_SOO.sh
    sed -i 's/JOBNAME/'${JOBNAME}'/' run_analysis_R2B5_1979-1980_${JOBNAME}_NAO_SOO.sh

    #then update the analysis part
    ANA1=NAO
    cp run_analysis_R2B5_1979-1980_${JOBNAME}_NAO_SOO.sh run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA1}.sh
    sed -i 's/ANA/'${ANA1}'/' run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA1}.sh

    ANA2=SOO
    cp run_analysis_R2B5_1979-1980_${JOBNAME}_NAO_SOO.sh run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA2}.sh
    sed -i 's/ANA/'${ANA2}'/' run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA2}.sh

    #only tauu local
    cp template_runanalysis_R2B5_1979-1980_60NandS_10hPa.sh template_run_analysis_R2B5_1979-1980_${JOBNAME}_60NandS_10hPa.sh
    sed -i 's/JOBNAME/'${JOBNAME}'/' template_run_analysis_R2B5_1979-1980_${JOBNAME}_60NandS_10hPa.sh

    #then update the analysis part
    ANA3=60N_10hPa
    cp template_run_analysis_R2B5_1979-1980_${JOBNAME}_60NandS_10hPa.sh run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA3}.sh
    sed -i 's/ANA/'${ANA3}'/' run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA3}.sh

    ANA4=60S_10hPa
    cp template_run_analysis_R2B5_1979-1980_${JOBNAME}_60NandS_10hPa.sh run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA4}.sh
    sed -i 's/ANA/'${ANA4}'/' run_analysis_R2B5_1979-1980_${JOBNAME}_${ANA4}.sh
    
    nrun=$(expr $nrun + $increm)
done < $file1

