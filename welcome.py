#!/usr/bin/env python3

import getpass
import os
import sys
import socket
import shutil
import psutil

from datetime import datetime
from termcolor import colored, cprint

sys.path.append('/usr/local/bin/todo-app')

import todo

"""
    TODO
    - fix "1 day" bug
    - fix memory usage
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
bold = lambda text, color=None: cprint(text, color, attrs=["bold"], end="")
username_color = "yellow"
os_color = "green"
battery_color = "green" if battery > 50 else ("yellow" if battery > 20 else "red")
date_color = "cyan"
attribute_color = "grey"
value_color = None 
todos_color = 'grey'

# clear screen
os.system('clear')

# welcome
bold("Welcome ")
bold(username, username_color)
bold(" to ")
bold(os_name + " " + os_version, os_color)
bold(" at ")
bold(str(battery) + "% of battery\n", battery_color)

# date
bold("System information as of ")
bold(date + "\n\n", date_color)

# disk
bold('Usage of /:\t\t', attribute_color) 
bold(f'{used_disk // (2**30)} GB of {total_disk // (2**30)} GB\n', value_color)

# cpu
bold('CPU usage:\t\t', attribute_color)
bold(str(usage_cpu) + "%\n", value_color)

# memory
bold('Memory usage:\t\t', attribute_color)
bold(str(usage_memory) + "%\n", value_color)

# swap
bold('Swap usage:\t\t', attribute_color)
bold(str(usage_swap) + "%\n", value_color)

# ip
bold('IPv4 address for en0:\t', attribute_color)
bold(ip + "\n", value_color)

# uptime
bold('Uptime:\t\t\t', attribute_color)
bold(
    (f'{days} days ' if days != 0 else "") +
    (f'{hours} hours ' if hours != 0 else "") + 
    (f'{minutes} mins' if minutes != 0 else "") + "\n", 
    value_color)

# shell
bold('Shell:\t\t\t', attribute_color)
bold(shell + "\n", value_color)

# hostname
# bold('Hostname:\t\t', attribute_color)
# bold(hostname + "\n", value_color)

# users logged
# bold('Users logged in:\t', attribute_color)
# bold(users_connected + "\n", value_color)


# TODOS
todo.print_list('get', todolist)
