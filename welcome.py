#!/usr/bin/env python3

import getpass
import os
import sys
import socket
import shutil
import psutil

from datetime import datetime
from termcolor import colored

sys.path.append('/usr/local/bin/todo-app')

import todo

"""
    TODO
    - replace print(colored(..))
    - fix "1 day" bug
    -   add percentage colors
"""

# welcome
username = getpass.getuser()
os_name = os.popen("sw_vers -productName").read().strip()
os_version = os.popen("sw_vers -productVersion").read().strip()

# date
date = datetime.now().strftime('%A %d %B %Y - %H:%M:%S %Z')

# battery
battery = psutil.sensors_battery()[0]

# disk usage
total_disk, _, free_disk = shutil.disk_usage("/")
used_disk = total_disk - free_disk

# cpu usage
usage_cpu = psutil.cpu_percent()

# memory usage
usage_memory = psutil.virtual_memory()[2] 

# swap usage
usage_swap = psutil.swap_memory()[3]

# uptime
uptime = os.popen("uptime").read().replace(',', '').split()
days = int(uptime[2]) if 'days' in uptime else 0
if 'mins' in uptime:
    hours = 0
    minutes = int(uptime[2])
else:
    if 'hrs' in uptime:
        hours = uptime[4]
        minutes = 0
    else:
        hours, minutes = map(int, uptime[4 if 'days' in uptime else 2].split(':'))
users_connected = uptime[3]

# shell
shell = os.environ['SHELL']

# hostname
hostname = socket.gethostname().split('.')[0]

# ip
ip = socket.gethostbyname(socket.gethostname())

# todos
todolist = todo.get('main')


# OUTPUT
username_color = "yellow"
os_color = "green"
date_color = "cyan"
attribute_color = "grey"
value_color = None 
todos_color = 'grey'

# clear screen
os.system('clear')

# welcome
print(colored("Welcome", attrs=["bold"]), colored(username, username_color, attrs=["bold"]), colored("to", attrs=["bold"]), colored(f"{os_name} {os_version}", os_color, attrs=["bold"]), colored("at", attrs=["bold"]), colored(f"{battery}% of battery", "red", attrs=["bold"]), "\n")

# date
print(colored("System information as of", attrs=["bold"]), colored(date, date_color, attrs=["bold"]), "\n")

# 1 x 1
# disk
print(colored('Usage of /:\t\t', attribute_color, attrs=['bold']), end='') 
print(colored(f'{used_disk // (2**30)} GB of {total_disk // (2**30)} GB', value_color, attrs=['bold']), end='\t\t')

# 1 x 2
# uptime
print(colored('Uptime:\t\t\t', attribute_color, attrs=['bold']), end='')
print(colored(
    (f'{days} days ' if days != 0 else "") +
    (f'{hours} hours  ' if hours != 0 else "") + 
    (f'{minutes} mins' if minutes != 0 else ""), 
    value_color, attrs=['bold']), end='\n')

# 2 x 1
# cpu
print(colored('CPU usage:\t\t', attribute_color, attrs=['bold']), end='')
print(colored(f'{usage_cpu}%', value_color, attrs=['bold']), end='\t\t\t')

# 2 x 2
# hostname
print(colored('Hostname:\t\t', attribute_color, attrs=['bold']), end='')
print(colored(hostname, value_color, attrs=['bold']), end='\n')

# 3 x 1
# memory
print(colored('Memory usage:\t\t', attribute_color, attrs=['bold']), end='')
print(colored(f'{usage_memory}%', value_color, attrs=['bold']), end='\t\t\t')

# 3 x 2
# ip
print(colored('IPv4 address for en0:\t', attribute_color, attrs=['bold']), end='')
print(colored(ip, value_color, attrs=['bold']), end='\n')

# 4 X 1
# swap
print(colored('Swap usage:\t\t', attribute_color, attrs=['bold']), end='')
print(colored(f'{usage_swap}%', value_color, attrs=['bold']), end='\t\t\t')


# 4 x 2
# users logged
print(colored('Users logged in:\t', attribute_color, attrs=['bold']), end='')
print(colored(users_connected, value_color, attrs=['bold']), end='\n')

# 5 x 1
# shell
print(colored('Shell:\t\t\t', attribute_color, attrs=['bold']), end='')
print(colored(shell, value_color, attrs=['bold']), end="\t\t")

# 5 x 2
print()


# TODOS
todo.print_list('get', todolist)
