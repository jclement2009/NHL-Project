#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 11:01:57 2017

@author: Joseph
"""

import base64
import requests as rq
import pandas as pd
import io
import os
import getpass

#Sportsfeed.com requires a registered username and password to pull the data
usernameInput = input("Username:\n")
passwordInput = getpass.getpass("Password:\n")


#Based on season end years, choose the range you want to fetch the data
firstendyear = 2008
lastendyear = 2017


#Custom function for calling a csv file
def callcsv(csvname):
    #csvfilename = directory + str(csvname) + ".csv"
    csvname1 = "NHL" + str(csvname) + ".csv"
    csvfilename = os.path.abspath(os.path.join(csvname1))
    return csvfilename
    
#Custom function that will take csv file name and convert it directly into a dataframe
def createdf(name):
    stuff = callcsv(name)
    converter = pd.read_csv(stuff)
    df = pd.DataFrame(converter)
    return df


#Fetching NHL data from mysportsfeed.com API within above year range
print("***Obtaining Files from Sportsfeed.com***")
for endyear in range(firstendyear, lastendyear, 1):
    startyear = endyear - 1
    
    #Pulling Data via Sportsfeed API
    filename = "https://www.mysportsfeeds.com/api/feed/pull/nhl/"+ str(startyear) + "-" + str(endyear) + "-regular/overall_team_standings.csv"
    print(filename)
    response = rq.get(filename, 
                      headers={
                "Authorization": "Basic " + base64.b64encode('{}:{}'.format(usernameInput , passwordInput).encode('utf-8')).decode('ascii')
            }
        )
    
    #Notification if pull was successful
    preface = "NHL Data Season: " + str(startyear) + "-" + str(endyear)
    print(preface)
    print(response.status_code)
    
    #Initializing the datafiles
    datafile = callcsv(endyear)
    print(datafile)
    
    #If the data is successfully fetched, write into csv file named after the end year of the Hockey Season
    if response.status_code == 200:
        urlData = response.content 
        rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
        NHLScores = pd.DataFrame(rawData)
        
        #Droping excess column and inserting the end of season year as column
        NHLScores1 = NHLScores.drop(NHLScores.columns[[0]], axis=1)
        NHLScores1.insert(0, '#End Year', endyear)
        filename1 = "NHL" + str(endyear) + ".csv"
        NHLScores1.to_csv(filename1)

#Deleting password
usernameInput = None
passwordInput = None
        
#Need to merge all files in the data range, start with first csv and append all consecutive files
print(" ")
print("***Merging Collected Data***")  
firstendyear1 = str(firstendyear)
df1 = createdf(firstendyear1)


#Iteration for merge
for endyear1 in range(firstendyear+1, lastendyear, 1):
    joiningdata = createdf(endyear1)
    frames = [df1, joiningdata]
    df1 = pd.concat(frames)

  
#Saving the unified data
print(" ")
print("***Saving Merged Data***") 
finalname = "Overall Team Standings " + str(firstendyear) + "-" + str(lastendyear - 1)
unifieddata = callcsv(finalname)
df1.to_csv(unifieddata)

#Deleting all of the unjoined data
print(" ")
print("***Deleting Unjoined Files***") 
for endyear2 in range(firstendyear, lastendyear, 1):
    os.remove(callcsv(endyear2))
    print(callcsv(endyear2))
    print("Deleted")

#Alerting user to the merged csv name    
print("\n Merged file saved as " + finalname)
    

