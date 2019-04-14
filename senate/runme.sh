#!/usr/bin/env bash

# untested, may not work
cd ..
senate/downloader.py
sed -i '$ d' data/*/*/*.csv
util/aggregateDat.py
cd senate