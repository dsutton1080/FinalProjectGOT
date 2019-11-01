import subprocess
import time

command1 = "docker build -t database_image ./setup"
command2 = "docker run -d --rm --name database -p 3306:3306 database_image"
command3 = "docker exec -d database cat /setup/scripts/* > script.sql && mysql -uroot < script.sql"


if subprocess.call(command1, shell=True) != 0:
    print("Image built")

time.sleep(10)

if subprocess.call(command2, shell=True) != 0:
    print("Database container deployed")

# time.sleep(50)

# if subprocess.call(command3, shell=True) != 0:
#     print("Scripts executed")