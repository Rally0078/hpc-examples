import os
from dask_jobqueue.slurm import SLURMCluster
from dask.distributed import Client, wait
import socket
import dask.array as da
import time
import numpy as np

def run_test():
    python_path = os.path.expanduser('~/miniconda3/envs/ionogram_ml/bin/python')
    # Each "job" is a SLURM job that shows up as an individual entry in squeue
    cluster = SLURMCluster(
        queue='large',
        cores=32,   #Number of cores per SLURM job
        processes=1,    #Number of Dask worker processes per SLURM job 
        memory='128GB', #Memory allocated per SLURM job
        walltime='00:20:00',
        death_timeout=60,
        python=python_path,
        job_script_prologue=['--output=./dask_worker_%j.out', 'export PYTHONUNBUFFERED=1']
    )
    # Number of SLURM jobs as seen in squeue
    cluster.scale(jobs=4)

    client = Client(cluster)
    print(f"Waiting for 2 nodes", flush=True)
    print(f"Dashboard link: {client.dashboard_link}", flush=True)
    print(f"Hostname: {socket.gethostname()}", flush=True)
    client.wait_for_workers(n_workers=2, timeout=30)    #n_workers = processes * jobs
    print(f"Cluster ready! Workers: {len(client.scheduler_info()['workers'])}", flush=True)
    size=8192
    print(f"Multiplying two {size}x{size} matrices", flush=True)
    A = da.random.random((size, size), chunks=(2048, 2048))
    B = da.random.random((size, size), chunks=(2048, 2048))
    start_time = time.perf_counter()
    C = da.matmul(A,B).compute()
    end_time = time.perf_counter()
    print(f"Successful multiplication took {end_time - start_time:.2f} seconds on HPC", flush=True)
    start_time = time.perf_counter()
    print(f"Result matches with numpy: {np.allclose(C, A.compute() @ B.compute())}")
    end_time = time.perf_counter()
    print(f"Successful multiplication took {end_time - start_time:.2f} seconds on Numpy automatic vectorization", flush=True)

    print(f"Result shape: {C.shape}")
    client.close()
    cluster.close()
if __name__ == "__main__":
    run_test()