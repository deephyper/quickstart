#!/bin/bash
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:15:00
#PBS -q debug 
#PBS -A datascience

cd ${PBS_O_WORKDIR}

# activate Python environment
source ../build/activate-dhenv.sh

# Number of nodes
NNODES=`wc -l < $PBS_NODEFILE`

# Number of ranks per node (4 GPUs/node)
NRANKS_PER_NODE=4

# Number of CPU cores per rank
# 32 CPU cores per node - 1/4 for each rank
NDEPTH=8

# Total number of ranks
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} --depth=${NDEPTH} --cpu-bind depth \
    --envlist "LD_LIBRARY_PATH,PYTHONPATH,PATH" \
    python search.py