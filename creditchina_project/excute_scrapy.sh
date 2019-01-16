#!/bin/bash python
scrapyname=$1
echo "${scrapyname}"
nohup python -m ${scrapyname} >log.txt 2>&1 &
echo "over"

