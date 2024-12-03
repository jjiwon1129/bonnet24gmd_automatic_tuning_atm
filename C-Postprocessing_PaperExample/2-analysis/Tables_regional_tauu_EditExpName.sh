#!/bin/ksh
#=============================================================================
# =====================================
# mistral batch job parameters
#-----------------------------------------------------------------------------
#SBATCH --account=bd1179
#SBATCH --job-name=Dyquick
#SBATCH --partition=prepost
#SBATCH --nodes=1
#SBATCH --threads-per-core=2
#####SBATCH --constraint=512G
#SBATCH --mem=0
#SBATCH --output=/scratch/b/b309198/tmp/icon/tuning/Quickplots/logs/LOG.out.quick.%j.o
#SBATCH --error=/scratch/b/b309198/tmp/icon/tuning/Quickplots/logs/LOG.err.quick.%j.o
#SBATCH --exclusive
#SBATCH --time=01:30:00
#
set -e
#####################################################
# This script loads the necessary modules and runs the TABLE script
#
#----------------------------------------------------
# A valid swift-token is required to start the job. 
# Please check it with the command:
#           module load swift
# If your token is expire, follow the instructions.
#----------------------------------------------------
#
# The following modules are loaded :
# - cdo/2.0.5-gcc-11.2.0 (levante)
# - ncl/6.6.2-gcc-11.2.0 (levante)
# maybe you must change it; check it with:
# "module avail cdo" and "module avail ncl"

echo "############################################"
echo SCRIPT Table_regional
echo "############################################"

set -ex
DATDIR=${WD_TMP_PROCESSED}

Timeofrun=$(date +"%d%m%Y_%H%M%S")

GrdInfoFile=${gridinfofile}

#
#######################################################
#
# ERA5 (time frame: 1979-2019)
ERAystrt=$YY1
ERAylast=$YY2
if [ "$ERAylast" -lt "1979"  -o "$ERAylast" -gt "2019"  ]
then
ERAylast=2019
fi
if [ "$ERAystrt" -lt "1979" -o "$ERAystrt" -gt "2019" ]
then
ERAystrt=1979
fi

export ERAystrt
echo ERAystrt path $ERAystrt
export ERAylast
echo ERAylast path $ERAylast

#--- Observation path 

   obsDir=/pool/data/ICON/post/QuickPlots_1x1_1.4.0.0/CERES/
export obsDir
#--- ERA5 path 
   Era5Dir=/pool/data/ICON/post/QuickPlots_1x1_1.4.0.0/ERA5/
export Era5Dir


QUELLE=${SCRIPTS_FOLDER}/3-make-tables/
export QUELLE
echo QUELLE path $QUELLE

export GrdInfoFile
echo GrdInfoFile path $GrdInfoFile

  PLTDIR=${SCRIPTS_FOLDER}/tables/${NAME}_${Timeofrun}
  export PLTDIR
  if [ ! -d ${PLTDIR} ] ; then
    mkdir ${PLTDIR}
    echo ${PLTDIR}
  fi

cd ${PLTDIR}
pwd

# Load modules 

    CDO_MODULE=cdo/2.0.5-gcc-11.2.0 #if there is an error, check which version should be loaded "$ module avail cdo"

    MODULES="$MODULES $CDO_MODULE"

    NCL_MODULE=ncl/6.6.2-gcc-11.2.0 #if there is an error, check which version should be loaded "$ module avail ncl"


    MODULES="$MODULES $NCL_MODULE"

    . $MODULESHOME/init/ksh
    module unload cdo
    module unload ncl
    module load $MODULES

which cdo 
which ncl

#
#--------------- TABLE --------------------------
if [ "$TAB" = "1" ]
then

${QUELLE}TABLE_tauu_${Ana}.job $TYP $NAME $EXP $DATDIR $SCRIPTS_FOLDER 

fi
echo '####################################################'
echo  you find your table on
echo ${PLTDIR}
echo '#####################################################'

