#!/bin/bash

while read url; do
    #echo $url
    wget $url
    #break
done < data_urls2.txt