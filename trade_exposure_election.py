# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:31:58 2016

@author: mwaugh
"""
# This code was done as a project of learn Python at the NYU-Stern-Econ 
# databoot camp course (http://databootcamp.nyuecon.com/)...
# It combines US 2016 Election data at the country level with the ADH(2013) 
# US Trade Exposure from China data In other words it asks:
# Did China Cause Trump?  

# This code does the following: It imports the 2016 Election Data and then 
# import the FIPS to Commuting zone mapping and then merges it with the ADH data
# which is performed at the commuting zone level. 

# I then regress, the local election outcomes on the china import exposure 
# measure....still to be done.

#%% 
import pandas as pd

#%%
folder = "C:\\Users\\mwaugh\\Dropbox"  
folder = folder + "\\Micro Price Data\\Election"

# One way to set this up is so the first folder is what we will have to adjust
# dependion upon the computer I'm using, then the second one is setup so that 
# puts us to the place we want to work...

#%%
# Rememer to use \\ backslashes...

csv_file = folder + "\\us-election-2016-results-by-county.csv"
election_results = pd.read_csv(csv_file)

stata_file = folder + "\\workfile_china.dta"
adh_data = pd.read_stata(stata_file)

# Load in the ADH data....

#%% OK, lets figure out who one the popular vote...

trump = election_results[election_results["Candidate"] == "Trump"]
clinton = election_results[election_results["Candidate"] == "Clinton"]

if trump.VoteCount.sum() > clinton.VoteCount.sum():
    print("\nTrump Won Popular Vote")
else:
    print("\nClinton Won Popular Vote")
    
#%%

# Now read in the commuting zone file. Note the way this idea about defining thing
# works, just take the old folder and add in the new thing we want to read in.
csv_file = folder + "\\czlma903.csv"
czs = pd.read_csv(csv_file)

#%%

test = election_results.merge(czs,how = 'outer',right_on = 'County FIPS Code', 
                       left_on = 'CountyFips', indicator = 'True')
                       
# This basically does the same, the ones that are not merged are all the alaska
# stuff and just appended two the end. This is basically because the county fips
# code is wrong, its just 2000. What I can not figure out is what happens to the 
# to the original alaska vots... the key is the how, the outer takes the union
            
#%% 

# Now I'm going to practince cleaning this...here is a way to drop a whol column
# need to figure out why the 1 is there...
# Note if ever need just a column test[[0,1]]...test2.head() to just get the 
# top part...
                     
test = test.drop("CZ80",1)

test = test.drop(test[test["True"]!='both'].index)

# Then this is a way to drop specific variables. So I take only the ones there
# both were not merged, use the .index to take that, then apply in the drop command
# and this 

trump_vote = test[test["Candidate"] == "Trump"].groupby(["CZ90"]).sum() 

# this doing the following (i) take only the trump part (ii) group by the 
# commuting zone and (iii) then sum and this will generate new data_frame 
# what is not clear is why the columns of the new data frame do not mimic 
# the ones from test. Is it because they are irrelavent when grouped?

clinton_vote = test[test["Candidate"] == "Clinton"].groupby(["CZ90"]).sum() 

#other_vote = test[test["Candidate"] != ("Clinton" and "Trump")].groupby(["CZ90"]).sum() 

# How to figure out how many candidates....
print("\n Number of Canidates", test.Candidate.unique())

#clinton_vote.VoteCount.sum()
#trump_vote.VoteCount.sum()
#%%

vote_by_cz = clinton_vote[[0]]

vote_by_cz["TotalVotes"] = trump_vote.CountyTotalVote
vote_by_cz["TrumpVote"] = trump_vote.VoteCount
vote_by_cz["ClintonVote"] = clinton_vote.VoteCount

vote_by_cz["TrumpShare"] = vote_by_cz.TrumpVote/vote_by_cz.TotalVotes

corr_mat = vote_by_cz.corr()

print("\n Correlation: Size and Trump Share", corr_mat.TrumpShare.TotalVotes)
print("\n")
#%%

# Now bring in the adh_data...drop the year 1990....

adh_data = adh_data.drop(adh_data[adh_data["yr"] == 1990].index)

# only keep the variables week care aboud...
k_adh_data = adh_data[["czone", "d_tradeusch_pw", "d_tradeotch_pw_lag", "timepwt48"]]

#%%

adh_election = vote_by_cz.merge(k_adh_data, how = 'outer',left_index = 'True', 
                       right_on = 'czone', indicator = 'True')

adh_election = adh_election.drop(adh_election[adh_election["True"]!="both"].index)

corr_mat = adh_election.corr()

print("\n Correlation: Trump Share and ADH Share", corr_mat.TrumpShare.d_tradeusch_pw)
print("\n")

print("\n Correlation: Trump Share and Other ADH Share", 
      corr_mat.TrumpShare.d_tradeotch_pw_lag)
print("\n")

#%%