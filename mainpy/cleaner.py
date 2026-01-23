import pathlib as pal
import logging as lg
def clean(path):
    dir_path = pal.Path(path)
    for file in dir_path.glob("*.tmp"):
        file.stat()
        file.unlink(missing_ok=True)
