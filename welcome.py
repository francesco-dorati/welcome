import getpass
import os
import socket
import shutil
import psutil

from datetime import datetime
from termcolor import colored

"""
    TODO
    -   FIX uptime
    -   Hostname
    -   Swap usage
    -   TODO list
    
"""

# welcome
username = getpass.getuser()
os_name = os.popen("sw_vers -productName").read().strip()
os_version = os.popen("sw_vers -productVersion").read().strip()

# date
date = datetime.now().strftime('%A %d %B %Y - %H:%M:%S %Z')

# disk usage
total_disk, _, free_disk = shutil.disk_usage("/")
usage_disk = round((((total_disk - free_disk) / total_disk) * 100), 1)

# memory usage
usage_memory = psutil.virtual_memory()[2] 

# uptime
uptime = os.popen("uptime").read().replace(',', '')
days = int(uptime.split()[2])
if 'min' in uptime:
    hours = 0
    minutes = int(uptime[4])
else:
    hours, minutes = map(int, uptime.split()[4].split(':'))
users_connected = uptime[3]

# shell
shell = os.environ['SHELL']

# ip
ip = socket.gethostbyname(socket.gethostname())


# OUTPUT

username_color = "yellow"
os_color = "green"
date_color = "cyan"
attribute_color = "grey"
value_color = None 

# welcome
print(colored("Welcome", attrs=["bold"]), colored(username, username_color, attrs=["bold"]), colored("to", attrs=["bold"]), colored(f"{os_name} {os_version}", os_color, attrs=["bold"]), "\n")

# date
print(colored("System information as of", attrs=["bold"]), colored(date, date_color, attrs=["bold"]), "\n")

# 1 x 1
print(colored(f"Usage of /:\t\t", attribute_color, attrs=["bold"]), end='') 
print(colored(f"{usage_disk}% of {total_disk // (2**30)}GB", value_color, attrs=["bold"]), end="\t\t")

# 1 x 2
print(colored(f"Uptime:\t\t\t", attribute_color, attrs=["bold"]), end='')
print(colored(f"{days} days" if days != 0 else "" + f"{hour} hours" + f"{minute} minute", value_color, attrs=["bold"]), end='\n')

# 2 x 1
print(colored(f"Memory usage:\t\t", attribute_color, attrs=["bold"]), end='')
print(colored(f"{usage_memory}%", value_color, attrs=["bold"]), end="\t\t\t")

# 2 x 2
print(colored(f"Users logged in:\t", attribute_color, attrs=["bold"]), end='')
print(colored(f"{users_connected}", value_color, attrs=["bold"]), end='\n')

# 3 x 1
print(colored(f"Shell:\t\t\t", attribute_color, attrs=["bold"]), end='')
print(colored(f"{shell}", value_color, attrs=["bold"]), end="\t\t")

# 3 x 2
print(colored(f"IPv4 address for en0:\t", attribute_color, attrs=["bold"]), end='')
print(colored(f"{ip}", value_color, attrs=["bold"]), end='\n')

