#  -*- coding: utf-8 -*-
__author__ = "Varun Nayyar <nayyarv@gmail.com>"

import glob
import pandas as pd

from senate.info import YRMAP, STATES
YEARS = YRMAP.keys()

FGLOB = "data/{year}/{state}/*.csv"


def get_file(year, state):
    fls = glob.glob(FGLOB.format(year=year, state=state))
    print(f"glob: {FGLOB.format(year=year, state=state)}")

    if len(fls) != 1:
        raise ValueError(f"Too many files found {fls}")
    return fls[0]


def main():
    for state in STATES:
        baseDict = {}
        yearResDict = {}
        for year in YEARS:
            fl = get_file(year, state)
            df = pd.read_csv(fl, skiprows=1)
            # dfDict[year] =
            for pollplace, subg in df.groupby("PollingPlaceID"):
                totalV = subg.OrdinaryVotes.sum()
                greens = subg[subg.PartyNm=="The Greens"].OrdinaryVotes.sum()
                perc = greens/totalV
                # baseDict[pollplace] =



if __name__ == '__main__':
    main()