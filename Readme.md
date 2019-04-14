# README

AEC download and munging utilities.

## Senate data

Downloads the senate first preference data from federal elections 2010,2013,2016 
and reports on percentage of first preferences at each polling place

Run `sed -i '$ d' data/*/*/*.csv` after the download stage. The unzipping results in 
files with null characters and a blank last line that doesn't play nice with pandas et al.
Sed can handle this quite well.

