#!/usr/bin/env bash

# play.sh N URL file_name

SNAKE1 = 

echo $1
echo $2
echo $3

for ((i = 0 ; i < $1 ; i++)); do
    battlesnake play --name Snake1 --url $2 --name Snake2 --url $2 --name Snake3 --url $2 --name Snake4 --url $2 --output $3$i.log
    echo $i/$1
done
