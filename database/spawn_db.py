import subprocess
import time

command1 = "docker build -t database_image ./setup"
command2 = "docker run -p 3306:3306 -d --rm --name database database_image"
command3 = "sudo docker exec -it database /bin/sh -c '/setup/script.sh'"


if subprocess.call(command1, shell=True) != 0:
    print("Image built")

time.sleep(10)

if subprocess.call(command2, shell=True) != 0:
    print("Database container deployed")

# time.sleep(60)

# if subprocess.call(command3, shell=True) != 0:
#     print("Scripts executed")


    