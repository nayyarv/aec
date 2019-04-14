#!/usr/bin/env bash

# untested, may not work
cd ..
senate/downloader.py
sed -i '$ d' data/*/*/*.csv
senate/aggregateDat.py
cd senate