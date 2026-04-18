from __future__ import annotations

import logging
from pathlib import Path


def normalize_extensions(extensions: list[str]) -> set[str]:
    return {ext if ext.startswith(".") else f".{ext}" for ext in extensions}


def scan_junk(path: Path | str, extensions: list[str]) -> list[Path]:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Expected a directory: {root}")

    allowed_extensions = normalize_extensions(extensions)
    matches: list[Path] = []
    for candidate in root.rglob("*"):
        if candidate.is_file() and candidate.suffix.lower() in allowed_extensions:
            matches.append(candidate)
    return sorted(matches)


def cleanup_junk(
    path: Path | str, extensions: list[str], logger: logging.Logger
) -> dict[str, int]:
    deleted_count = 0
    freed_bytes = 0
    for file_path in scan_junk(path=path, extensions=extensions):
        file_size = file_path.stat().st_size
        file_path.unlink(missing_ok=True)
        deleted_count += 1
        freed_bytes += file_size
        logger.info("Deleted junk file %s (%s bytes)", file_path, file_size)

    return {"deleted_count": deleted_count, "freed_bytes": freed_bytes}


def clean(path: Path | str) -> int:
    """Backwards-compatible helper for the original stub API."""
    from .logger import get_logger

    result = cleanup_junk(path=path, extensions=[".tmp"], logger=get_logger())
    return result["freed_bytes"]


if __name__ == "__main__":
    from .logger import get_logger

    deleted = cleanup_junk(".", [".tmp"], logger=get_logger())
    print(f"Cleanup finished. Total freed: {deleted['freed_bytes'] / 1000:.1f} KB")

