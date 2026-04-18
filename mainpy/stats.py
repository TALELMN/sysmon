from __future__ import annotations

from datetime import datetime
import platform
import socket
from typing import Any

import psutil


def get_ram() -> float:
    return round(psutil.virtual_memory().percent, 1)


def get_disk() -> float:
    return round(psutil.disk_usage("/").percent, 1)


def get_cpu() -> float:
    return round(psutil.cpu_percent(interval=0.5), 1)


def systeminf() -> str:
    return platform.system()


def collect_system_snapshot() -> dict[str, Any]:
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")
    net_io = psutil.net_io_counters()
    battery = psutil.sensors_battery()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_hours = round((datetime.now() - boot_time).total_seconds() / 3600, 2)

    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "cpu_percent": get_cpu(),
        "memory_percent": round(virtual_memory.percent, 1),
        "memory_used_gb": round(virtual_memory.used / (1024**3), 2),
        "memory_total_gb": round(virtual_memory.total / (1024**3), 2),
        "disk_percent": round(disk_usage.percent, 1),
        "disk_used_gb": round(disk_usage.used / (1024**3), 2),
        "disk_total_gb": round(disk_usage.total / (1024**3), 2),
        "bytes_sent": int(net_io.bytes_sent),
        "bytes_received": int(net_io.bytes_recv),
        "process_count": len(psutil.pids()),
        "boot_time": boot_time.isoformat(timespec="seconds"),
        "uptime_hours": uptime_hours,
        "battery_percent": None if battery is None else round(battery.percent, 1),
    }


def build_health_report(snapshot: dict[str, Any]) -> dict[str, Any]:
    score = 100
    notes: list[str] = []
    recommendations: list[str] = []

    cpu_percent = snapshot["cpu_percent"]
    memory_percent = snapshot["memory_percent"]
    disk_percent = snapshot["disk_percent"]

    if cpu_percent >= 90:
        score -= 30
        notes.append("CPU usage is critically high.")
        recommendations.append("Close or investigate the busiest CPU-heavy processes.")
    elif cpu_percent >= 70:
        score -= 15
        notes.append("CPU usage is elevated.")
        recommendations.append("Watch background tasks or lower load before demos.")
    else:
        notes.append("CPU usage is in a healthy range.")

    if memory_percent >= 90:
        score -= 30
        notes.append("Memory pressure is critically high.")
        recommendations.append("Free RAM by closing browsers, VMs, or idle apps.")
    elif memory_percent >= 75:
        score -= 15
        notes.append("Memory usage is moderately high.")
        recommendations.append("Consider closing a few heavy applications.")
    else:
        notes.append("Memory usage looks stable.")

    if disk_percent >= 95:
        score -= 30
        notes.append("Disk space is almost exhausted.")
        recommendations.append("Run cleanup and remove large unused files.")
    elif disk_percent >= 80:
        score -= 10
        notes.append("Disk usage is getting high.")
        recommendations.append("Archive or delete old files before storage fills up.")
    else:
        notes.append("Disk usage is within a safe range.")

    status = "Excellent"
    if score < 90:
        status = "Good"
    if score < 70:
        status = "Needs Attention"
    if score < 50:
        status = "Critical"

    if not recommendations:
        recommendations.append("No immediate action needed. The system looks healthy.")

    return {
        "score": max(score, 0),
        "status": status,
        "notes": notes,
        "recommendations": recommendations,
    }
