#!/bin/bash

for FILENAME in hooks/* ; do
  if ! [ -a ".git/$FILENAME" ]; then
    link $FILENAME .git/$FILENAME  
  else
    echo ".git/$FILENAME already exists"
  fi
done
