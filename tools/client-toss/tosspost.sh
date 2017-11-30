#!/bin/sh

PAUTH=guest
IIURL=http://127.0.0.1:62220/u/point

wget $IIURL -O - --post-data "pauth=$PAUTH&tmsg=$(cat $1)"
