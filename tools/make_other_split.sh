#!/bin/bash
mkdir training
mkdir testing
mkdir validation
for i in {0..9}
do
if [ $((i%2)) -eq 0 ]
then
	cp others_cropped/*_$i.* testing
else
	cp others_cropped/*_$i.* validation
fi
done
mv training testing validation ../
