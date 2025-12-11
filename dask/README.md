# Dask Distributed Ping Project

This project demonstrates a safe distributed pinging pipeline using **Dask** with the following architecture:

* **Master (Windows 11)**

  * Runs Dask **scheduler** (or connects to remote scheduler) and the client script
  * Holds the local **SQLite** database and performs all writes
  * Gathers results from workers and writes to DB in batches

* **Worker (Ubuntu)**

  * Runs Dask **workers** that execute the ping tasks (no DB access)

---

## Files & Layout (single-file representation below)

```
project-root/
├─ README.md
├─ master/
│  ├─ requirements.txt
│  ├─ start_scheduler.ps1
│  ├─ run_master.py
│  ├─ db_writer.py
│  └─ hosts.txt   # optional input list
└─ worker/
   ├─ requirements.txt
   ├─ start_worker.sh
   └─ ping_task.py
```

---

## README (overview + quick start)


### Dask Distributed Ping Project

#### Overview
This example shows how to distribute ping tasks to remote workers using Dask. Workers do the pinging and return results to the master, which writes results into a local SQLite database in safe batched updates.

#### Quick start

##### On the master (Windows 11)
1. Install Python (3.9+) and create a venv.
2. Install dependencies:
    ```powershell
    pip install -r master/requirements.txt
    ```
3. Start the Dask scheduler (PowerShell):
    ```powershell
    .\master\start_scheduler.ps1
    ```
   Note the scheduler address (e.g. `tcp://192.168.1.10:8786`). Open the dashboard at `http://<MASTER-IP>:8787`.
4. Prepare `master/hosts.txt` with one host per line or edit `run_master.py` to generate hosts.
5. Run the master client which will distribute tasks and write to SQLite:
   ```powershell
   python master\run_master.py --scheduler tcp://<MASTER-IP>:8786 --db master\hosts.db --hosts master\hosts.txt
   ```

##### On the worker (Ubuntu)
1. Install Python (3.9+) and create a venv.
2. Install dependencies:
   ```bash
   pip install -r worker/requirements.txt
   ```
3. Start one or more workers and point them to the scheduler:
   ```bash
   ./worker/start_worker.sh tcp://<MASTER-IP>:8786
   ```

#### Notes

* Only the master writes to the SQLite DB (`master/hosts.db`).
* Workers are stateless and purely compute.
* The master performs batched `executemany()` updates to maximize performance.


#### Notes & Tuning

* **Firewall**: If you run scheduler on Windows, ensure port 8786 and 8787 are allowed on the Windows firewall for incoming connections from the worker.
* **Worker Count**: Tune `--nthreads` and `--memory-limit` to match the Ubuntu hardware. Use multiple workers/processes if you want more parallelism.
* **Batch sizes**: Tweak `chunk_size` and `batch_size` in `run_master.py` to constrain the number of outstanding futures and DB write frequency. Typical batch sizes: 1k-10k for writes.
* **Reliability**: The master script uses `as_completed` and tries to write results as they arrive. You can add retries or backoff policies easily.

---

#### Troubleshooting

* If workers cannot connect, check the scheduler address and firewall.
* If DB writes are slow, tune PRAGMAs in `db_writer.py` (e.g., `PRAGMA synchronous = OFF` for speed when you can tolerate data loss on crash).
* To debug tasks on workers, use the Dask Dashboard (port 8787) and the worker logs