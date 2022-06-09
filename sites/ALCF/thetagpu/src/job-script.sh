#!/bin/bash
#COBALT -q full-node
#COBALT -n 1
#COBALT -t 60
#COBALT --attrs filesystems=home,grand,eagle,theta-fs0
#COBALT -O job_script

export RANKS_PER_NODE=8
export COBALT_JOBSIZE=1

# activate Python environment
source ../build/activate-dhenv.sh

echo "mpirun -x LD_LIBRARY_PATH -x PYTHONPATH -x PATH -n $(( $COBALT_JOBSIZE * $RANKS_PER_NODE )) -N $RANKS_PER_NODE --hostfile $COBALT_NODEFILE python search.py";

mpirun -x LD_LIBRARY_PATH -x PYTHONPATH -x PATH -n $(( $COBALT_JOBSIZE * $RANKS_PER_NODE )) -N $RANKS_PER_NODE --hostfile $COBALT_NODEFILE python search.py