#!/bin/bash
#COBALT -q full-node
#COBALT -n 1
#COBALT -t 15
#COBALT --attrs filesystems=home,grand,eagle,theta-fs0
#COBALT -O job_script

# we consider 1 worker per GPU
export RANKS_PER_NODE=8
# we consider 1 node of thetagpu, this parameter should always match the value of "qsub-gpu -n 1"
export COBALT_JOBSIZE=1

# activate Python environment
source ../build/activate-dhenv.sh

mpirun -x LD_LIBRARY_PATH -x PYTHONPATH -x PATH -n $(( $COBALT_JOBSIZE * $RANKS_PER_NODE )) -N $RANKS_PER_NODE --hostfile $COBALT_NODEFILE python search.py