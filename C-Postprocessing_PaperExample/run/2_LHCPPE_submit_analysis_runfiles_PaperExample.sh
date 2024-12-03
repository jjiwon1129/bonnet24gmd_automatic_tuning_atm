#!/bin/usr/env bash

# this script runs the analysis scripts for each of the parameter sets

filename=sample_PAPEREXAMPLE_Emid_Epen_Edd_Taumf_Pr_R0top #TODO to update

nrun=0
increm=1
file1=${filename}-Epen.txt
while read -r line; do
    JOBNAME=nrun_${nrun}-PaperExample #TODO to update
    echo ${JOBNAME}
    sbatch run_analysis_R2B5_1979-1980_${JOBNAME}.sh
    sbatch run_analysis_R2B5_1979-1980_${JOBNAME}_NAO.sh
    sbatch run_analysis_R2B5_1979-1980_${JOBNAME}_SOO.sh
    sbatch run_analysis_R2B5_1979-1980_${JOBNAME}_60N_10hPa.sh
    sbatch run_analysis_R2B5_1979-1980_${JOBNAME}_60S_10hPa.sh
    nrun=$(expr $nrun + $increm)
done < $file1

