#!/bin/bash
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:10:00
#PBS -q debug 
#PBS -A datascience

cd ${PBS_O_WORKDIR}

module load conda/2022-07-19

# Copy activation of environment file
cp ../install/env.sh activate-dhenv.sh
echo "" >> activate-dhenv.sh
echo "conda activate base" >> activate-dhenv.sh
