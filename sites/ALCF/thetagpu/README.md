# ThetaGPU

## Installation

To install DeepHyper on ThetaGPU, once logged on the Theta system, execute the following commands (replace the ``$PROJECT_NAME`` with the name of your project allocation, e-g: ``-A datascience``). Clone the repository:


```console
$ git clone https://github.com/deephyper/quickstart.git deephyper-quickstart
```

Move to the `thetagpu` folder:

```console
$ cd deephyper-quickstart/sites/ALCF/thetagpu/
```

Create the build folder ; this is where the conda environment will be installed:

```console
$ mkdir build && cd build
```

Submit a job to trigger the installation process:

```console
$ qsub-gpu -A $PROJECT_NAME ../install/install.sh
```

This will submit a job on ThetaGPU, wait for it to finish (you can follow the installation with the ``install.*`` cobaltlog files which will be created in the current ``build/`` folder).

## Execution

To execute the search, first locate yourself in ``sites/ALCF/thetagpu/src/`` :

```console
$ cd sites/ALCF/thetagpu/src/
```

You then simply have to submit the ``job-script.sh`` script (again replace the ``$PROJECT_NAME`` with the name of your project allocation, e-g: ``-A datascience``):

```console
$ qsub-gpu -A $PROJECT_NAME job-script.sh
```
