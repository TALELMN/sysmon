# SysMon

SysMon is a small Python command-line project for checking basic system health, listing busy processes, exporting reports, and cleaning up simple junk files. I built it to stay approachable and easy to demo while still feeling like a complete portfolio project instead of a one-file script.

## What it does

- Shows a quick system summary with CPU, memory, disk, uptime, network usage, and battery when available
- Lists the top running processes by CPU or memory usage
- Generates a simple "doctor" report with a score and plain-English recommendations
- Exports a JSON report that can be reused for demos or future dashboard ideas
- Scans for removable junk files and can delete them when needed
- Writes activity logs to `logs/logs.log`

## Stack

- Python 3.10+
- `psutil`
- Standard library modules including `argparse`, `json`, `logging`, and `pathlib`

## Setup

From the project folder:

```powershell
cd C:\Users\Talel\Desktop\Docs\Sysmon
C:\Program Files\Python310\python.exe -m pip install -r requirements.txt
```

If `python` is already available in your terminal, this also works:

```powershell
pip install -r requirements.txt
```

## How To Use

This version of the project is meant to be run as a script:

```powershell
C:\Program Files\Python310\python.exe mainpy\main.py summary
```

### Main commands

```powershell
C:\Program Files\Python310\python.exe mainpy\main.py summary
C:\Program Files\Python310\python.exe mainpy\main.py processes --sort cpu --limit 8
C:\Program Files\Python310\python.exe mainpy\main.py processes --sort memory --limit 5
C:\Program Files\Python310\python.exe mainpy\main.py doctor
C:\Program Files\Python310\python.exe mainpy\main.py doctor --json
C:\Program Files\Python310\python.exe mainpy\main.py export --output reports\system_report.json
C:\Program Files\Python310\python.exe mainpy\main.py cleanup --path . --extensions .tmp .bak
C:\Program Files\Python310\python.exe mainpy\main.py cleanup --path . --extensions .tmp .bak --delete
```

### What each command does

- `summary` prints a quick overview of the current machine state
- `processes` shows the busiest processes and lets you choose CPU or memory sorting
- `doctor` gives the machine a simple health score and suggestions
- `export` saves a JSON snapshot to the `reports` folder
- `cleanup` scans for junk files first, and only deletes them when `--delete` is included

## Example workflow

```powershell
C:\Program Files\Python310\python.exe mainpy\main.py summary
C:\Program Files\Python310\python.exe mainpy\main.py doctor
C:\Program Files\Python310\python.exe mainpy\main.py processes --sort memory --limit 5
C:\Program Files\Python310\python.exe mainpy\main.py export --output reports\system_report.json
```

That gives you a quick snapshot, a basic health assessment, a short process table, and a report file you can keep.

## Testing

```powershell
C:\Program Files\Python310\python.exe -m unittest discover -s tests -v
```

## Project Layout

```text
Sysmon/
|-- mainpy/
|   |-- cleaner.py
|   |-- logger.py
|   |-- main.py
|   |-- processes.py
|   `-- stats.py
|-- tests/
|-- logs/
|-- README.md
`-- requirements.txt
```

## Why this project works well in a portfolio

- It solves a real problem without being overbuilt
- It shows modular Python code instead of one large script
- It includes CLI design, logging, file handling, and JSON export
- It has test coverage for core parts of the app
- It is easy to explain and demo live
