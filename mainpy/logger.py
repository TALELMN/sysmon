import logging as lg
import pathlib as pal
path = pal.Path(__file__).parent.parent/"logs"/"logs.log"
path.parent.mkdir(exist_ok=True)
def logger():
    lg.basicConfig(filename=path,level=lg.INFO,format='%(asctime)s - %(message)s')
if __name__=="__main__":
    logger()
    lg.info("working")
    print(f"Log file created at: {pal.Path(__file__).parent.parent / 'logs' / 'logs.log'}")