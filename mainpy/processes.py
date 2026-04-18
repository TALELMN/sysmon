from __future__ import annotations

from typing import Any

import psutil


def get_top_processes(limit: int = 10, sort_by: str = "cpu") -> list[dict[str, Any]]:
    processes: list[dict[str, Any]] = []

    for process in psutil.process_iter(
        attrs=["pid", "name", "cpu_percent", "memory_info", "status"]
    ):
        try:
            info = process.info
            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"] or "Unknown",
                    "cpu_percent": float(info["cpu_percent"] or 0.0),
                    "memory_mb": round(
                        (info["memory_info"].rss if info["memory_info"] else 0)
                        / (1024 * 1024),
                        2,
                    ),
                    "status": info.get("status", "unknown"),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    key = "memory_mb" if sort_by == "memory" else "cpu_percent"
    return sorted(processes, key=lambda item: item[key], reverse=True)[:limit]


def processes(limit: int = 10, sort_by: str = "cpu") -> list[dict[str, Any]]:
    return get_top_processes(limit=limit, sort_by=sort_by)


if __name__ == "__main__":
    for process in get_top_processes():
        print(process)
