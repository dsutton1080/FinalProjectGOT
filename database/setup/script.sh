#! /bin/bash

for f in /setup/scripts/*
do
    mysql test -e "$(cat $f)"
done
