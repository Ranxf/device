#!/bin/sh

i=0
while true
do
    i=`expr $i + 1`
    echo $i
    ./aptest.py 3 3 > /dev/null
    sleep 25
done
