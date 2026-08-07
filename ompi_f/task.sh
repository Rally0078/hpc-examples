#!/bin/bash
#SBATCH --job-name=vimal_test
#SBATCH --output=./ompi_f/output.txt
#SBATCH --error=./ompi_f/error.txt
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=4
cd ompi_f
srun --mpi=pmi2 ./a.out
