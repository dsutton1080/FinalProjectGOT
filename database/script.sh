#! /bin/bash

mysql -h 127.0.0.1 -P 3306 -uroot -ppassword -e "CREATE DATABASE test;"

for f in ./setup/scripts/*
do
    mysql -h 127.0.0.1 -P 3306 -uroot -ppassword test -e "$(cat $f)"
done
