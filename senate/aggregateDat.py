#  -*- coding: utf-8 -*-
__author__ = "Varun Nayyar <nayyarv@gmail.com>"

import glob
import collections
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


def yearDictToList(yeardict):
    for vals in yeardict.values():
        yield list(vals.values())


def main(states=STATES):
    for state in states:
        baseDict = {}
        yearResDict = collections.defaultdict(lambda: {2010: 0, 2013: 0, 2016:0})
        for year in YEARS:
            fl = get_file(year, state)
            print(f"Reading {fl}")

            # top row is some trash metadata
            df = pd.read_csv(fl, skiprows=1)
            # some files don't use PartyNm
            df = df.rename({"Party": "PartyNm"}, axis=1)
            for divID, divgroup in df.groupby("DivisionID"):
                for pollplace, subg in divgroup.groupby("PollingPlaceID"):
                    totalV = subg.OrdinaryVotes.sum()
                    greens = subg[subg.PartyNm == "The Greens"].OrdinaryVotes.sum() + \
                            subg[subg.PartyNm == "Australian Greens"].OrdinaryVotes.sum()
                    if totalV:
                        perc = greens / totalV
                    else:
                        perc = 0

                    row = subg.iloc[0]
                    if pollplace not in baseDict:
                        baseDict[pollplace] = [row.StateAb, row.DivisionID, row.DivisionNm,
                                               row.PollingPlaceID, row.PollingPlaceNm]
                    yearResDict[pollplace][year] = perc

        percdf = pd.DataFrame.from_records(list(yearDictToList(yearResDict)),
                                           yearResDict.keys(), columns=YEARS)
        basedf = pd.DataFrame.from_records(list(baseDict.values()), baseDict.keys(),
                                           columns=["State", "DivisionID", "DivisionNm",
                                                    "PollingPlaceID", "PollingPlaceNm"])

        combed = pd.concat([basedf, percdf], axis=1)
        print(f"Writing {state} to processedData/senate_greens_{state}.csv")
        combed.to_csv(f"processedData/senate_greens_{state}.csv", index=False)


if __name__ == '__main__':
    main()
