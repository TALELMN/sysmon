from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .cleaner import cleanup_junk, scan_junk
from .logger import configure_logging, get_logger
from .processes import get_top_processes
from .stats import build_health_report, collect_system_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sysmon",
        description="Simple portfolio-ready system monitor and cleanup utility.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("summary", help="Show an overview of system health.")

    process_parser = subparsers.add_parser(
        "processes", help="List top running processes."
    )
    process_parser.add_argument(
        "--sort",
        choices=["cpu", "memory"],
        default="cpu",
        help="Sort the process table by CPU or memory usage.",
    )
    process_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of processes to display.",
    )

    doctor_parser = subparsers.add_parser(
        "doctor", help="Assess system health and provide a simple score."
    )
    doctor_parser.add_argument(
        "--json", action="store_true", help="Emit the doctor report as JSON."
    )

    cleanup_parser = subparsers.add_parser(
        "cleanup", help="Scan or delete temporary files in a folder."
    )
    cleanup_parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Directory to scan for junk files.",
    )
    cleanup_parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete matched files. Without this flag, cleanup is a dry run.",
    )
    cleanup_parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".tmp", ".bak", ".old", ".cache"],
        help="File extensions to treat as removable junk.",
    )

    export_parser = subparsers.add_parser(
        "export", help="Export a system report as JSON."
    )
    export_parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/system_report.json"),
        help="Output JSON file path.",
    )
    export_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of processes to include in the export.",
    )

    return parser


def format_bytes(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def print_snapshot(snapshot: dict[str, Any]) -> None:
    lines = [
        "System Summary",
        f"OS: {snapshot['system']} {snapshot['release']}",
        f"Hostname: {snapshot['hostname']}",
        f"CPU Usage: {snapshot['cpu_percent']}%",
        f"Memory Usage: {snapshot['memory_percent']}%",
        f"Disk Usage: {snapshot['disk_percent']}%",
        f"Processes Running: {snapshot['process_count']}",
        f"Boot Time: {snapshot['boot_time']}",
        f"Uptime Hours: {snapshot['uptime_hours']}",
        f"Network Sent: {format_bytes(snapshot['bytes_sent'])}",
        f"Network Received: {format_bytes(snapshot['bytes_received'])}",
    ]
    battery = snapshot.get("battery_percent")
    if battery is not None:
        lines.append(f"Battery: {battery}%")
    print("\n".join(lines))


def print_processes(sort_by: str, limit: int) -> None:
    processes = get_top_processes(limit=limit, sort_by=sort_by)
    print(f"Top {len(processes)} Processes by {sort_by.upper()}")
    print("-" * 72)
    print(f"{'PID':>6}  {'Name':<28} {'CPU %':>8} {'Memory MB':>12} {'Status':>10}")
    print("-" * 72)
    for process in processes:
        print(
            f"{process['pid']:>6}  "
            f"{process['name'][:28]:<28} "
            f"{process['cpu_percent']:>8.1f} "
            f"{process['memory_mb']:>12.1f} "
            f"{process['status'][:10]:>10}"
        )


def print_doctor_report(as_json: bool) -> None:
    report = build_health_report(collect_system_snapshot())
    if as_json:
        print(json.dumps(report, indent=2))
        return

    print("SysMon Doctor")
    print(f"Score: {report['score']}/100")
    print(f"Status: {report['status']}")
    print("Notes:")
    for note in report["notes"]:
        print(f"- {note}")
    print("Recommendations:")
    for recommendation in report["recommendations"]:
        print(f"- {recommendation}")


def handle_cleanup(path: Path, delete: bool, extensions: list[str]) -> None:
    logger = get_logger()
    if delete:
        result = cleanup_junk(path=path, extensions=extensions, logger=logger)
        print(f"Deleted files: {result['deleted_count']}")
        print(f"Space freed: {format_bytes(result['freed_bytes'])}")
    else:
        matches = scan_junk(path=path, extensions=extensions)
        print(f"Found {len(matches)} junk file(s) in {path.resolve()}")
        for file_path in matches[:20]:
            print(f"- {file_path}")
        if len(matches) > 20:
            print(f"... and {len(matches) - 20} more")


def handle_export(output: Path, limit: int) -> None:
    snapshot = collect_system_snapshot()
    report = {
        "summary": snapshot,
        "doctor": build_health_report(snapshot),
        "top_processes": get_top_processes(limit=limit, sort_by="cpu"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report exported to {output.resolve()}")


def main() -> None:
    configure_logging()
    args = build_parser().parse_args()

    if args.command == "summary":
        print_snapshot(collect_system_snapshot())
    elif args.command == "processes":
        print_processes(sort_by=args.sort, limit=args.limit)
    elif args.command == "doctor":
        print_doctor_report(as_json=args.json)
    elif args.command == "cleanup":
        handle_cleanup(path=args.path, delete=args.delete, extensions=args.extensions)
    elif args.command == "export":
        handle_export(output=args.output, limit=args.limit)


if __name__ == "__main__":
    main()
