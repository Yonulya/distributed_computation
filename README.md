# Distributed Computation with Dask (Python)

This project is a **clean, production‑grade example** of how to build a **distributed Python application** using **Dask Distributed**, with:

- a **master** node (task submission + database writes)
- multiple **worker** nodes (parallel computation)
- a **shared Python package** (no import hacks, no `sys.path` tricks)
- a **local SQLite database** owned by the master
- full compatibility with **Windows + Linux**

If you followed the steps correctly, this setup:

✔ avoids `ModuleNotFoundError`
✔ avoids Dask deserialization errors
✔ avoids environment mismatches
✔ scales from 1 machine to many

---

## 🧠 Architecture Overview

```
                +--------------------+
                |   Dask Scheduler   |
                |  (task routing)    |
                +----------+---------+
                           |
          -----------------------------------------
          |                                       |
+--------------------+               +--------------------+
|   Worker Node 1    |               |   Worker Node N    |
|  ping computation |               |  ping computation |
+--------------------+               +--------------------+
                           |
                   +-------+-------+
                   |   Master Node |
                   | task submit + |
                   | SQLite write |
                   +---------------+
```

**Important rule:**
> Workers compute. The master writes to the database.

This avoids SQLite concurrency issues and keeps the system stable.

---

## 📁 Project Layout

```
distributed_computation/
├─ pyproject.toml
├─ requirements.txt
└─ src/
   └─ distributed_computation/
      ├─ __init__.py
      │
      ├─ common/
      │  ├─ __init__.py
      │  └─ ping.py          # shared ping logic
      │
      ├─ worker/
      │  ├─ __init__.py
      │  └─ tasks.py         # Dask worker tasks
      │
      └─ master/
         ├─ __init__.py
         ├─ db_writer.py     # SQLite writer
         └─ run_master.py   # entry point
```

### Why this layout matters

- The project is a **real Python package**
- It can be **installed with pip**
- Dask workers can **import code safely**
- No relative imports, no fragile hacks

---

## 📦 Installation

### 1️⃣ Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
```

### 2️⃣ Install the project (editable mode)

```bash
pip install -e .
```

This step is **mandatory** on:
- the scheduler machine
- every worker machine
- the master machine

> If a worker cannot `pip install` your code, Dask cannot run it.

---

## 🚀 Running the System

### 1️⃣ Start the Dask scheduler

```bash
dask scheduler
```

You should see:

```
Dashboard at: http://127.0.0.1:8787/status
```

---

### 2️⃣ Start one or more workers

On **any machine** (same network):

```bash
dask worker tcp://<scheduler-ip>:8786
```

Optional tuning:

```bash
dask worker tcp://<scheduler-ip>:8786 --nthreads 16 --memory-limit 8GB
```

To prevent Ubuntu client from sleeping : 
```bash
systemd-inhibit --what=sleep:idle --why="Dask worker running" dask worker tcp://<scheduler-ip>:8786 --nthreads 16 --memory-limit 8GB

---

### 3️⃣ Run the master

```bash
python -m distributed_computation.master.run_master \
  --scheduler tcp://<scheduler-ip>:8786 \
  --db hosts.db \
  --hosts hosts.txt
```

The master:
- loads hosts
- submits tasks to workers
- batches results
- writes to SQLite

---

## 🗄 Database Design

- **SQLite** is used for simplicity
- Only the **master writes** to the database
- Workers never touch the DB

Schema:

```sql
CREATE TABLE hosts (
  host TEXT PRIMARY KEY,
  status TEXT
);
```

Batch inserts are used for performance.

---

## 📊 Dask Dashboard

The Dask dashboard provides:

- task progress
- worker CPU / memory
- task stream
- scheduler health

### Dependency

The dashboard requires:

```
bokeh>=3.1.0
```

This dependency is declared in `pyproject.toml` and installed automatically.

Open the dashboard:

```
http://<scheduler-ip>:8787/status
```

---

## 🔒 Import & Serialization Rules (Very Important)

### ✅ Do

- Use **absolute imports**
- Install the package with `pip install -e .`
- Submit **functions**, not strings, to Dask

```python
client.map(ping_task, hosts)
```

### ❌ Never do

- `sys.path.append(...)`
- relative imports across packages
- `client.map("module.function", ...)`
- running files directly (`python file.py`)

---

## 🧠 Key Lessons Learned

- Dask workers are **independent Python processes**
- They do **not** inherit your working directory
- Code must be **installed**, not assumed
- Packaging correctly solves 95% of Dask errors

---

## 🛠 Troubleshooting

### Dashboard does not load

✔ Check `bokeh>=3.1.0` is installed
✔ Restart scheduler after installing

---

### `ModuleNotFoundError` on workers

✔ Package installed on worker machine
✔ Same Python version
✔ Same virtual environment

---

### SQLite locking issues

✔ Ensure only master writes
✔ Increase batch size

---

## 🚧 Next Steps / Improvements

- PostgreSQL instead of SQLite (multi‑writer)
- Docker / docker‑compose
- TLS‑secured scheduler
- Task retries & backpressure
- Async result handling
- Metrics & logging

---

## 🏁 Final Note

This project demonstrates the **correct way** to structure and run a distributed Python application with Dask.

Once your code is:

✔ installable
✔ importable
✔ environment‑consistent

Dask becomes boring — and that’s a good thing.

Happy distributed computing 🚀

