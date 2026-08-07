#!/bin/bash
#SBATCH --job-name=vimal_test
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=4

srun --mpi=pmi2 ./mpi_hello_world
