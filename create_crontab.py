
from crontab import CronTab
import os
import sys
import getpass


def check_venv(arguments, actual_path):
    if len(arguments) >= 2:
        if arguments[1] == 'local':
            return os.path.join(actual_path, 'venv/bin/python3')
        return arguments[1]
    return os.path.join(actual_path, 'venv/bin/python3')


username = getpass.getuser()
actual_path = os.getcwd()
python_file_path = os.path.join(actual_path, 'corona.py')

venv_python_path = check_venv(sys.argv, actual_path)

cron_command = f'{venv_python_path} {python_file_path}'

for argument in sys.argv[2:]:
    cron_command += f' {argument}'


cron = CronTab(user=username)
new_job = cron.new(command=cron_command)
new_job.minute.every(20)

check = 0
for job in cron:
    if job == new_job:
        check += 1
    if check == 2:
        exit()

cron.write()
