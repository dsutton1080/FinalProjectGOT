## Local Database Instructions
### Must be Installed:
* Docker (community edition)
* MySQL Client Tool

### Steps:
1. Navigate to the database directory (this directory) in the repository
2. Run the following command:
```bash
python3 spawn_db.py
```
3. Wait 1 minute for the database container to start its MySQL service
4. <p>Check whether the database container is running with the following command:
```bash
docker ps
```
If the container is running, there should be a line with the NAME as 'database'</p>

5. Navigate to the FinalProjectGOT/database/setup/scripts folder
6. Run the following command to create our database, called 'test':
```bash
mysql -h 127.0.0.1 -P 3306 -uroot -ppassword -e "CREATE DATABASE test;"
```
7. <p>For each file '#.sql', run the following command (in number order of the files):
```bash
mysql -h 127.0.0.1 -P 3306 -uroot -ppassword test < #.sql
```
                                                         ...where # is in {1,2,3,4,5,6,7}</p>
8. <p>Navigate back to the FinalProjectGOT/database folder and test the database connection by running:
```bash
python3 connect_test.py
```
If 'Success' appears, then it should have worked.</p> 
