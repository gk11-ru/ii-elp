#!/bin/sh

mkdir -p cp/m
mkdir -p cp/e

for e in $@
do
cp e/$e cp/e/$e
for n in `cat e/$e`
do
cp m/$n cp/m/$n
done
done