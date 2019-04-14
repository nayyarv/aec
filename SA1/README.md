# SA1

This directory does the work of downloading and parsing
the SA1 info for the 2016 election.

We are given from the AEC

   1. SA1 to Polling Place ID numbers. Ie for the 300-500 residents, where did they vote
    Use the downloader script for this. 
   2. Counts of votes in each polling Place ID: https://www.aec.gov.au/elections/federal_elections/2016/files/polling-place-by-sa1s-2016.xlsx
   put this in aec/.cache/data/2016/census_SA1 for it to be processed
   
## Caveats

Note that each electorate has around 350 SA1s while only a handful of polling places. 
We basically form a system of Linear equations with more unknowns (vote rate of each SA1)
than equations. 

To find an answer would require us to optimise a cost function

1. Minimize absolute vote difference between SA1s sharing a border. This would be optimal 
way of solving this problem. However, this would require the 
2. 