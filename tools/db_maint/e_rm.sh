#!/bin/sh

for e in $@
do
for n in `cat e/$e`
do
rm m/$n
done
rm e/$e
done
