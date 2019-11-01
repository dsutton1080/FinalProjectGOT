#! /usr/bin/python3

import subprocess
import time

command = "docker run --rm --name database -p 3306:3306 database_image"
command2 = "docker exec -d database cat /setup/scripts/* > script.sql && mysql -uroot -ppassword < script.sql"

if subprocess.call(command, shell=True) != 0:
    print("Database container deployed")

time.sleep(20)

if subprocess.call(command2, shell=True) != 0:
    print("Scripts executed")