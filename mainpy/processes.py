import psutil as ps
def processes():
    procs = []
    for proc in ps.process_iter(attrs=['pid','name','cpu_percent','memory_info'])
        