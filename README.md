# SysMon

SysMon is a lightweight Python system monitoring and cleanup CLI built for day-to-day machine visibility and as a clean portfolio project. It gives a quick system summary, ranks busy processes, generates a simple health report, exports JSON snapshots, and safely cleans removable junk files.

## Features

- `summary` prints a concise machine health overview.
- `processes` shows the top running processes by CPU or memory.
- `doctor` scores the system and suggests simple actions.
- `export` writes a JSON report you can keep or showcase.
- `cleanup` scans or deletes temporary junk files in a target folder.
- File logging is built in through `logs/logs.log`.

## Tech Stack

- Python 3.10+
- `psutil`
- Standard library modules such as `argparse`, `json`, `logging`, and `pathlib`

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m mainpy.main summary
```

## Commands

```bash
python -m mainpy.main summary
python -m mainpy.main processes --sort cpu --limit 8
python -m mainpy.main doctor
python -m mainpy.main export --output reports/system_report.json
python -m mainpy.main cleanup --path . --extensions .tmp .bak
python -m mainpy.main cleanup --path . --extensions .tmp .bak --delete
```

## Sample Use Cases

- Create a JSON report before and after a cleanup run.
- Demo process monitoring on your portfolio or in interviews.
- Use `doctor` to show how the app turns raw metrics into a simple health score.

## Project Structure

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

## Testing

```bash
python -m unittest discover -s tests -v
```

## Portfolio Notes

This project intentionally stays simple in setup while still showing:

- clean CLI design
- modular Python structure
- file handling and logging
- JSON export
- test coverage for core logic
- practical use of a third-party systems library
