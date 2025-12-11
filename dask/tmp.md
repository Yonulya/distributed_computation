
## Notes & Tuning

* **Firewall**: If you run scheduler on Windows, ensure port 8786 and 8787 are allowed on the Windows firewall for incoming connections from the worker.
* **Worker Count**: Tune `--nthreads` and `--memory-limit` to match the Ubuntu hardware. Use multiple workers/processes if you want more parallelism.
* **Batch sizes**: Tweak `chunk_size` and `batch_size` in `run_master.py` to constrain the number of outstanding futures and DB write frequency. Typical batch sizes: 1k-10k for writes.
* **Reliability**: The master script uses `as_completed` and tries to write results as they arrive. You can add retries or backoff policies easily.

---

## Troubleshooting

* If workers cannot connect, check the scheduler address and firewall.
* If DB writes are slow, tune PRAGMAs in `db_writer.py` (e.g., `PRAGMA synchronous = OFF` for speed when you can tolerate data loss on crash).
* To debug tasks on workers, use the Dask Dashboard (port 8787) and the worker logs