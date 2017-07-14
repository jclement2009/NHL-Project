# NHL-Project
This repository houses a statistical project involving National Hockey League data.  The file NHLDataFetcher.py fetches aggregate statistics from https://www.mysportsfeeds.com, which span the NHL regular seasons from 2008 to 2016 (Season End Years).  The raw data are in separate CSVs by regular season year and are accessible through the MySportsFeeds web API.  Note that these data are for noncommercial use as part of the MySportsFeeds terms of service for a free account.  

USING THE FETCHER (NHLDataFetcher.py)
1. Sign up at https://www.mysportsfeeds.com for a free account.
2. Execute the fetcher.
3. Input your MySportsFeed username and password when prompted to begin pulling and merging the data.  A successful pull is indicated by the HTTP response code 200.  
4. The merged file is named "NHLOverall Team Standings 2008-2016.csv" and is stored in the same directory as the executable file.

Future Plans
The fetcher currently does not support merges over missing years (for example, if the data from the year 2010 was missing over the 2008-2016 span, the fetcher will not merge the csv files).  This will be resolved in a future update.  
