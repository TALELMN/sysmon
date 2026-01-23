import psutil as ps
import platform as pl
def get_ram():
    return ps.virtual_memory().percent
def get_disk():
    return ps.disk_usage("/").percent
def get_cpu():
    return ps.cpu_percent(interval=1)
def systeminf():
    return pl.system()

if __name__=="__main__":
    cpu = get_cpu()
    ram = get_ram()
    disk = get_disk()
    sys= systeminf()
    print("cpu: ",cpu,"ram: ",ram,"disk: ",disk,"system: ",sys)
