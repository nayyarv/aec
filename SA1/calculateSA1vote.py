#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Varun Nayyar <nayyarv@gmail.com>"

"""
Non-trivial problem

"""
import os

import pandas as pd

import sys
fp = os.path.abspath(os.path.join(__file__, "..", ".."))
sys.path.insert(0, fp)

from util.info import STATES
from util.base import procdir


def sa1_pp_mapper(state):
    import ujson
    with open(os.path.join(procdir, f"sa1-pp-{state}-2016.json")) as f:
        mapper = ujson.load(f)
    return mapper


def pp_results(state):
    df = pd.read_csv(os.path.join(procdir, f"housefpp_{state}_2016.csv"))
    df.grn /= df.total
    df.lib /= df.total
    df.alp /= df.total
    df.other /= df.total
    return df


def sa1_vote_yielder(state):
    mapper = sa1_pp_mapper(state)
    polldf = pp_results(state)
    print("Finished reading")
    for sa1, ppmap in mapper.items():
        # drop the absent/prepoll etc locations since they don't exist
        ppmap.pop('0', None)
        max_poll = max(ppmap.items(), key=lambda x: x[1])[0]
        row = polldf[polldf.polid == int(max_poll)]
        try:
            dat = [round(row[party].item(), 3) for party in ["grn", "alp", "lib", "other"]]
        except ValueError:
            print(max_poll, sa1)
            raise

        yield [sa1] + dat


def sa1_vote(state_list):
    for state in state_list:
        print(f"Processing {state}")
        fintab = pd.DataFrame.from_records(sa1_vote_yielder(state),
                                           columns=["sa1", "grn", "alp", "lib", "other"])
        fintab.to_csv(os.path.join(procdir, f"sa1_vote_{state}.csv"), index=False)


if __name__ == '__main__':

    sa1_vote(STATES)
