#!/bin/bash
#COBALT -q single-gpu
#COBALT -n 1
#COBALT -t 30
#COBALT --attrs filesystems=home,grand,eagle,theta-fs0
#COBALT -O install

. /etc/profile

module load conda/2021-11-30

conda create -p dhenv --clone base -y
conda activate dhenv/

# Install DeepHyper
pip install deephyper -I

# Install mpi4py
git clone https://github.com/mpi4py/mpi4py.git
cd mpi4py/
MPICC=mpicc python setup.py install
cd ..

# Copy activation of environment file
cp ../install/env.sh activate-dhenv.sh
echo "" >> activate-dhenv.sh
echo "conda activate $PWD/dhenv/" >> activate-dhenv.sh
