
mysql -h 127.0.0.1 -P 3306 -uroot -ppassword -e "CREATE DATABASE test;"

FOR %%f in (setup\scripts\*) DO (
    mysql -h 127.0.0.1 -P 3306 -uroot -ppassword test -e %cat %f%%
)