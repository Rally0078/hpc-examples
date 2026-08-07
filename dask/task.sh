#!/bin/bash
#SBATCH --job-name=daskdemo
#SBATCH --output=./dask/mainscript.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --partition='large'


# %j to indicate SLURM job number in filename, like mainscript_%j.out
# Load your miniconda environment
source ~/miniconda3/bin/activate ionogram_ml

# Run the driver script
cd ./dask
python test_dask.py