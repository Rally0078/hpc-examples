#!/bin/bash
#SBATCH --job-name=cadidrv
#SBATCH --output=./cadi_drift/output.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:30:00
#SBATCH --partition='large'


# %j to indicate SLURM job number in filename, like mainscript_%j.out
# Load your miniconda environment
source ~/miniconda3/bin/activate ionogram_ml

# Run the driver script
cd ./cadi_drift
python generate_drifts.py