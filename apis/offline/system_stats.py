import os
import psutil
from math import log, pow, floor

from GPUtil import getGPUs

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terrabytes", "Pedabytes")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_gpu_usage():
    gpus = getGPUs()
    if not gpus:
        return "N/A"
    return round(gpus[0].load * 100, 2)

def get_ram_usage():
    memory = psutil.virtual_memory()
    used_ram = convert_size(memory.used)
    total_ram = convert_size(memory.total)
    return used_ram, total_ram

def get_disk_usage():
    disk = psutil.disk_usage('/')
    used_disk = convert_size(disk.used)
    total_disk = convert_size(disk.total)
    return used_disk, total_disk

def system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    gpu_usage = get_gpu_usage()
    used_ram, total_ram = get_ram_usage()
    used_disk, total_disk = get_disk_usage()

    final_res = (f"Sir, currently I am using {cpu_usage}% of CPU, {gpu_usage}% of GPU and "
                 f"{used_ram} of {total_ram} RAM, and {used_disk} of {total_disk} Disk storage.")
    return final_res

############################################################################

if __name__ == "__main__":
    logging.debug(system_stats())