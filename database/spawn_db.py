#! /usr/bin/python3

import subprocess

command = "docker run --rm --name database -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password docker.io/mariadb"

if subprocess.call(command, shell=True) != 0:
    print("Success")