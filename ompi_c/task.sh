#!/bin/bash
#SBATCH --job-name=vimal_test
#SBATCH --output=./ompi_c/output.txt
#SBATCH --error=./ompi_c/error.txt
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=4
cd ompi_c
srun --mpi=pmi2 ./a.out
