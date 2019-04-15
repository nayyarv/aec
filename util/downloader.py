#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

__author__ = "Varun Nayyar <nayyarv@gmail.com>"

import wget
import os
import zipfile

import click

from base import cachedir
from info import STATES, YRMAP, HOUSE_MAP

YRMP_STR = [str(y) for y in YRMAP]
AEC_DL = ("https://results.aec.gov.au/{yrid}/Website/{loc}/"
          "{house}StateFirstPrefsByPollingPlaceDownload-{yrid}-{state}.{ftype}")

RAW_DIR = os.path.join(cachedir, "data")


def download_zips(house, years, states):
    webHouse = HOUSE_MAP[house]
    loc = "External"
    for year in years:
        for state in states:
            print(f"Downloading zip for {state}:{year}")
            wget.download(AEC_DL.format(house=webHouse, state=state, yrid=YRMAP[year],
                                        ftype="zip", loc="External"),
                          f"{RAW_DIR}/zip/senate_{state}_{year}.zip")
            print("Unzipping")
            with zipfile.ZipFile(f"{RAW_DIR}/zip/{house}_{state}_{year}.zip") as zf:
                zf.extractall(f"{RAW_DIR}/{year}/{state}")


def download_csvs(house, years, states):
    #             print("https://results.aec.gov.au/20499/Website/Downloads/HouseStateFirstPrefsByPollingPlaceDownload-20499-NSW.csv")
    webHouse = HOUSE_MAP[house]
    for year in years:
        for state in states:
            dl = AEC_DL.format(house=webHouse, state=state, yrid=YRMAP[year], ftype="csv",
                               loc="Downloads")
            os.makedirs(f"{RAW_DIR}/{year}/{state}", exist_ok=True)
            dest = f"{RAW_DIR}/{year}/{state}/houseFPP"
            print(f"Downloading csv for {state}:{year} to {dest}")
            print(dl)
            wget.download(dl, dest)


@click.command()
@click.argument("house", type=click.Choice(["senate", "hor"]))
@click.option("--state", "-s", type=click.Choice(STATES), default=STATES, multiple=True)
@click.option("--year", "-y", type=click.Choice(YRMP_STR), default=YRMP_STR, multiple=True)
def main(house, state, year):
    year = {int(y) for y in year}
    print(house, year, state)
    print(cachedir)
    if house == "senate":
        download_zips(house, year, state)
    else:
        download_csvs(house, year, state)


if __name__ == '__main__':
    main()
