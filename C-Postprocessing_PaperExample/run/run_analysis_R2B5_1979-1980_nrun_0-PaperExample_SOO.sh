#!/bin/ksh
#=============================================================================
# =====================================
# mistral batch job parameters
#-----------------------------------------------------------------------------
#SBATCH --account=bd1179
#SBATCH --job-name=run_analysis_R2B5_1979-1980_nrun_0-PaperExample
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --threads-per-core=2
#SBATCH --mem=0
#SBATCH --output=/work/bd1179/b309216/icon/ICON-2.6.4/icon-tuning-analysis/Postprocessing_PaperExample/logs/LOG.err.run_analysis_R2B5_1979-1980_nrun_0-PaperExample_SOO.%j.o 
#SBATCH --error=/work/bd1179/b309216/icon/ICON-2.6.4/icon-tuning-analysis/Postprocessing_PaperExample/logs/LOG.err.run_analysis_R2B5_1979-1980_nrun_0-PaperExample_SOO.%j.err
#SBATCH --exclusive
#SBATCH --time=00:30:00
#
#SBATCH --mail-type=ALL

#########
# Common
#########
gridinfofile=/pool/data/ICON/grids/public/mpim/0019/icon_grid_0019_R02B05_G.nc
LSMask=/pool/data/ICON/grids/public/mpim/0019/land/r0001/bc_land_frac_1976.nc

EXP=1979-1980_nrun_0-PaperExample #TODO Setup
Ana=SOO
EXPAna=${EXP}_${Ana} #TODO Setup
ICON_GRID=R2B5
EXP_DATA=/work/bd1179/b309216/icon/ICON-2.6.4/2.6.4/experiments/atm_amip_${ICON_GRID}_${EXP}/
YY1=1979
YY2=1980 #TODO Setup

SCRIPTS_FOLDER=/work/bd1179/b309216/icon/ICON-2.6.4/icon-tuning-analysis/Postprocessing_PaperExample
###############
# Make seasonal
###############

# use a temporary location to store the processed ICON outputs: here the scratch folder 
WD_TMP_PROCESSED=/scratch/b/b309216/tmp/icon/tuning/processed #TODO Setup

# Run script
source ${SCRIPTS_FOLDER}/1-postprocessing/make_seasonal 

############
# make Tables
############

TYP=ANN # MODIFIED BY PREVIOUS SCRIPTS
WEBPAGE=1
NAME=EXP_${EXP}_${ICON_GRID}_POST_${YY1}-${YY2}_${TYP}_${Ana}
# Run script
source ${SCRIPTS_FOLDER}/2-analysis/Tables_regional_tauu_EditExpName.sh
exit
