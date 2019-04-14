#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Varun Nayyar <nayyarv@gmail.com>"

import os

import pandas as pd

from util import cachedir
from util.info import STATES


def grouper(tsdf):
    for divID, electorateG in tsdf.groupby("DivisionID"):
        for polid, pollGroup in electorateG.groupby("PollingPlaceID"):
            total = pollGroup.OrdinaryVotes.sum()
            grn = pollGroup[pollGroup.PartyAb == "GRN"].OrdinaryVotes.sum()
            alp = pollGroup[pollGroup.PartyAb == "ALP"].OrdinaryVotes.sum()
            lib = pollGroup[pollGroup.PartyAb == "LP"].OrdinaryVotes.sum()
            lib += pollGroup[pollGroup.PartyAb == "CLP"].OrdinaryVotes.sum()
            other = total - (grn + alp + lib)
            yield divID, polid, grn, alp, lib, other, total


def main(state_list=STATES):
    year = 2016
    for state in state_list:
        print(f"Processing {state}")
        fpp = os.path.join(cachedir, "data", "{year}", "{state}", "houseFPP")
        tsdf = pd.read_csv(fpp.format(year=year, state=state), skiprows=1)

        simplified = pd.DataFrame.from_records(
            grouper(tsdf), columns=["divID", "polid", "grn", "alp", "lib", "other", "total"])
        simplified.to_csv(os.path.join(cachedir, "processedData", f"housefpp_{state}_{year}.csv"))


def sa1_pp_json():
    import ujson
    sa1info = os.path.join(cachedir, "data", "2016", "census_SA1", "polling-place-by-sa1s-2016.xlsx")
    print("Reading excel file")
    df = pd.read_excel(sa1info)
    print("Finished reading the excel file")
    for state, statedf in df.groupby("state_ab"):
        print(f"Collating {state}")
        sa1_pp = {}
        for sa1, sa1df in statedf.groupby("SA1_id"):
            # make sure we're getting an Sa1 with population
            if sum(sa1df.votes) > 100:
                sa1_pp[sa1] = dict(zip(sa1df.pp_id, sa1df.votes))
                sa1_pp[sa1][0] = sum(sa1df[sa1df.pp_id == 0].votes)
        print(f"Writing collation for {state} out")
        with open(os.path.join(cachedir, "processedData", f"sa1-pp-{state}-2016.json"), 'w') as f:
            ujson.dump(sa1_pp, f)


if __name__ == '__main__':
    main(["WA"])
