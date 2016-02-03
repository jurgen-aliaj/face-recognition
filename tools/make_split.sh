#!/bin/bash
mkdir training
mkdir testing
mkdir validation
for i in {0..99}
do
cp cropped/*_$i.* training
done
for i in {100..109}
do
cp cropped/*_$i.* testing
done
for i in {110..119}
do
cp cropped/*_$i.* validation
done
mv training testing validation ../
