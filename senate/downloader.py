#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

__author__ = "Varun Nayyar <nayyarv@gmail.com>"

import wget
import os
import zipfile

from typing import Set
from senate.info import STATES, YRMAP

AEC_SENATE_BASE = "https://results.aec.gov.au/{yrid}/Website/External/SenateStateFirstPrefsByPollingPlaceDownload-{yrid}-{state}.zip"

cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache"))
rawdir = os.path.join(cachedir, "data")

def download_zips(years: Set[int], states: Set[str]):
    if not years:
        years = YRMAP.keys()
    else:
        # filter what we have
        years &= YRMAP.keys()
    if not states:
        states = STATES
    else:
        # filter those in both
        states &= STATES

    for year in years:
        for state in states:
            print(f"Downloading zip for {state}:{year}")
            wget.download(AEC_SENATE_BASE.format(state=state, yrid=YRMAP[year]),
                          f"{rawdir}/zip/senate_{state}_{year}.zip")
            print("Unzipping")
            with zipfile.ZipFile(f"{rawdir}/zip/senate_{state}_{year}.zip") as zf:
                zf.extractall(f"{rawdir}/{year}/{state}")


if __name__ == '__main__':
    download_zips({}, {})
