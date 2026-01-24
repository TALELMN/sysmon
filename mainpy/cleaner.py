import pathlib as pal
import logging as lg
import logger
def clean(path):
    dir_path = pal.Path(path)
    total = 0
    for file in dir_path.glob("*.tmp"):
        size = file.stat().st_size
        total += size
        file.unlink(missing_ok=True)
        lg.info(f"file deleted: {file} size cleared: {size}")
        return total
if __name__ == "__main__":
    logger.logger()
    deleted_bytes = clean(".")
    print(f"Cleanup finished. Total freed: {deleted_bytes/1000} Kb")

