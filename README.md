# HPC examples
To use SSH tunneling to access Dask dashboard

```bash
ssh -N -L 8787:nodeX:8787 username@hpc-login-addr.net
```
Replace nodeX with the appropriate node hostname, username and hpc login with the correct details

To compile C

```sh
mpicc ./ompi_c/main.c -o ./ompi_c/a.out -cc=gcc
```

To compile Fortran90

```sh
mpif90 ./ompi_f/main.f90 -o ./ompi_f/a.out
```

## 1. ompi_c
A demo of OpenMPI using the C API

## 2. ompi_f
A demo of OpenMPI using the Fortran API

## 3. dask
A demo of Dask to perform distributed matrix multiplication. As an example of the speedup, see the following output:

```
Multiplying two 16384x16384 matrices
Successful multiplication took 44.17 seconds on HPC
Result matches with numpy: True
Successful multiplication took 124.87 seconds on Numpy automatic vectorization
```

## 4. cadi_drift
A script used to merge CADI rawdata's average height values with precomputed CADI drift velocities to give an estimate of the height of each drift. 

For a 16 core workstation running joblib, the estimated time for this merge is about ~1h25m. The following tqdm is from the workstation:

```
Processing iterations:   6%|▌         | 39840/715022 [05:00<1:22:54, 135.72it/s]
```

This script is used to speed up the merge by a significant amount. The following is the output from SLURM when using 6 nodes, 32 cores per node/SLURM job, 4 processes per node/SLURM job, creating 6 x 4 = 24 Dask workers with 32/4 = 8 threads for each Dask worker:

```
[########################################] | 100% Completed |  3min 57.1s
```

This is a speedup of about x21(*) compared to the single workstation machine.