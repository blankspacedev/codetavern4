#!/bin/bash
rm $2
mpg123 -r 16000 -m -w $2 $1
