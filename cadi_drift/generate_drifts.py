from dask.distributed import Client, progress
from dask_jobqueue.slurm import SLURMCluster
from tqdm import tqdm
import numpy as np
import socket
import pandas as pd
import os

python_path = os.path.expanduser('~/miniconda3/envs/ionogram_ml/bin/python')

cluster = SLURMCluster(
    queue='large',
    cores=32,       # Number of cores per SLURM job
    processes=4,    # Number of Dask worker processes per SLURM job 
    memory='128GB', # Memory allocated per SLURM job
    walltime='02:20:00',
    death_timeout=60,
    python=python_path,
    job_script_prologue=[
        '--output=./dask_worker_%j.out', 
        'export PYTHONUNBUFFERED=1',
        'export OMP_NUM_THREADS=8',
        'export OPENBLAS_NUM_THREADS=8',
        'export MKL_NUM_THREADS=8'
    ]
)

cluster.scale(jobs=6)

client = Client(cluster)
print(f"Waiting for 6 nodes...", flush=True)
print(f"Dashboard link: {client.dashboard_link}", flush=True)
print(f"Hostname: {socket.gethostname()}", flush=True)
client.wait_for_workers(n_workers=6*4, timeout=30)    # n_workers = processes * jobs
print(f"Cluster ready! Workers: {len(client.scheduler_info()['workers'])}", flush=True)

print("Reading index structure from LustreFS...", flush=True)
df_final_output_temp = pd.read_parquet('driftvels.pa')
unique_timestamps = np.unique(df_final_output_temp.index)
del df_final_output_temp

def process_timestamp_batch(timestamps_chunk, freq_list):
    df_final_output = pd.read_parquet('driftvels.pa')
    df_raw_year_pd = pd.read_parquet('rawyear.pa')
    
    batch_results = []
    for timestamp in timestamps_chunk:
        for freq_selection in freq_list:
            try:
                df_current_time_raw = df_raw_year_pd.loc[timestamp]
                df_current_time_drift = df_final_output.loc[timestamp]

                df_singlefreq = df_current_time_drift[df_current_time_drift['freq (Hz)'] == freq_selection]
                df_raw_onefreq = df_current_time_raw[df_current_time_raw['freq (Hz)'] == freq_selection]

                if df_raw_onefreq.empty or df_singlefreq.empty:
                    continue
                else:
                    datetime_level = 'datetime' if isinstance(df_raw_onefreq.index, pd.DatetimeIndex) or 'datetime' in df_raw_onefreq.index.names else df_raw_onefreq.index.name
                    
                    min_heights = df_raw_onefreq.groupby(level=datetime_level)['height (km)'].transform('min')
                    filtered_raw = df_raw_onefreq[df_raw_onefreq['height (km)'] < 1.8 * min_heights]
                    
                    if not filtered_raw.empty:
                        final_df = filtered_raw.groupby(level=datetime_level).median()
                        
                        merged_df = pd.merge(df_singlefreq, final_df, left_index=True, right_index=True, how='left')
                    else:
                        merged_df = pd.DataFrame()
                
                    if not merged_df.empty:
                        batch_results.append(merged_df)
            except KeyError:
                continue
                
    if not batch_results:
        return pd.DataFrame()
    return pd.concat(batch_results)

freq_list = [2000000., 3000000., 4000000., 5000000., 6000000., 7000000., 18000000.]
batch_size = 288    # Approximately 1 day of data
timestamp_batches = np.array_split(unique_timestamps, max(1, len(unique_timestamps) // batch_size))

print(f"Submitting {len(timestamp_batches)} batch tasks to Dask...", flush=True)
futures = [
    client.submit(process_timestamp_batch, chunk, freq_list)
    for chunk in timestamp_batches
]

progress(futures)
results = client.gather(futures)

print("Aggregating results...", flush=True)
df_height_drift = [res for res in results if res is not None and not res.empty]
if df_height_drift:
    df_height_drift = pd.concat(df_height_drift)
    df_height_drift.to_parquet('driftvel_height.pa')
    print("Saved 'driftvel_height.pa' successfully.", flush=True)
else:
    print("No valid results found to save.", flush=True)

try:
    client.close()
    cluster.close()
except Exception:
    pass