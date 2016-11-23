# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 16:06:46 2016

@author: mwaugh
"""
# This code was done as a project of learn Python at the NYU-Stern-Econ 
# databoot camp course (http://databootcamp.nyuecon.com/)...
# It combines US 2016 Election data at the country level with the ADH(2013) 
# US Trade Exposure from China data In other words it asks:
# Did China Cause Trump?  

# This code does the following: It imports the 2016 Election Data, the 2012
# election data, and then imports the FIPS to Commuting zone mapping and 
# then merges it with the ADH data which is performed at the commuting zone level. 

# I then regress, the change in election outcomes on the trade exposure measure

#%% 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import numpy as np

#%%
#folder = "C:\\Users\\mwaugh\\Dropbox" 
folder = "C:\\Users\\mwaugh.NYC-STERN\\Dropbox"
folder = folder + "\\Micro Price Data\\Election"

# One way to set this up is so the first folder is what we will have to adjust
# dependion upon the computer I'm using, then the second one is setup so that 
# puts us to the place we want to work...

#%%
# Rememer to use \\ backslashes...

csv_file = folder + "\\us-election-2012-results-by-county.csv"

election_2012results = pd.read_csv(csv_file)

print("\n 2012 Election Results")

obama = election_2012results[election_2012results.LastName == "Obama"]
romney = election_2012results[election_2012results.LastName == "Romney"]

if obama.Votes.sum() > romney.Votes.sum():
    print("\nObama Won Popular Vote")
    print(obama.Votes.sum())
    print(romney.Votes.sum())
else:
    print("\nRomney Won Popular Vote")
    print(obama.Votes.sum())
    print(romney.Votes.sum())
    
# Check who one the Popular Vote
#%%
    
csv_file = folder + "\\czlma903.csv"
czs = pd.read_csv(csv_file)

test2012 = election_2012results.merge(czs,how = 'outer',right_on = 'County FIPS Code', 
                       left_on = 'FipsCode', indicator = 'True')

test2012 = test2012.drop(test2012[test2012["True"]!='both'].index)

romney_vote = test2012[test2012["LastName"] == "Romney"].groupby(["CZ90"]).sum() 
obama_vote = test2012[test2012["LastName"] == "Obama"].groupby(["CZ90"]).sum() 

# How to figure out how many candidates....
print("\n 2012 Number of Canidates", test2012.LastName.unique())

#%%

vote_by_2012cz = obama_vote[[0]].copy()

vote_by_2012cz["TotalVotes2012"] = romney_vote.CountyTotalVotes
vote_by_2012cz["RomneyVote"] = romney_vote.Votes
vote_by_2012cz["ObamaVote"] = obama_vote.Votes

vote_by_2012cz["RomneyShare"] = vote_by_2012cz.RomneyVote/vote_by_2012cz.TotalVotes2012

corr_mat = vote_by_2012cz.corr()

print("\nCorrelation: Size and Romney Share", corr_mat.RomneyShare.TotalVotes2012)

#%%

csv_file = folder + "\\us-election-2016-results-by-county.csv"
election_2016results = pd.read_csv(csv_file)

trump = election_2016results[election_2016results["Candidate"] == "Trump"]
clinton = election_2016results[election_2016results["Candidate"] == "Clinton"]

if trump.VoteCount.sum() > clinton.VoteCount.sum():
    print("\nTrump Won Popular Vote")
    print(trump.VoteCount.sum())
    print(clinton.VoteCount.sum())
else:
    print("\nClinton Won Popular Vote")
    print(trump.VoteCount.sum())
    print(clinton.VoteCount.sum())
            
#%% 

test2016 = election_2016results.merge(czs,how = 'outer',right_on = 'County FIPS Code', 
                       left_on = 'CountyFips', indicator = 'True')
                     
test2016 = test2016.drop(test2016[test2016["True"]!='both'].index)

trump_vote = test2016[test2016["Candidate"] == "Trump"].groupby(["CZ90"]).sum() 

clinton_vote = test2016[test2016["Candidate"] == "Clinton"].groupby(["CZ90"]).sum() 

#other_vote = test[test["Candidate"] != ("Clinton" and "Trump")].groupby(["CZ90"]).sum() 

# How to figure out how many candidates....
print("\n 2016 Number of Canidates", test2016.Candidate.unique())
print("\n")

#%%

vote_by_2016cz = clinton_vote[[0]].copy()

vote_by_2016cz["TotalVotes2016"] = trump_vote.CountyTotalVote
vote_by_2016cz["TrumpVote"] = trump_vote.VoteCount
vote_by_2016cz["ClintonVote"] = clinton_vote.VoteCount

vote_by_2016cz["TrumpShare"] = vote_by_2016cz.TrumpVote/vote_by_2016cz.TotalVotes2016

corr_mat = vote_by_2016cz.corr()

print("\n Correlation: Size and Trump Share", corr_mat.TrumpShare.TotalVotes2016)
print("\n")

#%%

# Now merge everything to gether....

vote_by_cz = vote_by_2016cz.merge(vote_by_2012cz, how = "outer", 
                                  left_index = "True", right_index = "True", indicator = "True")

vote_by_cz["Diff20162012"] = vote_by_cz.TrumpShare-vote_by_cz.RomneyShare
 
vote_by_cz["TurnoutDiff"]= (vote_by_cz.TotalVotes2016 - vote_by_cz.TotalVotes2012)/vote_by_cz.TotalVotes2012

corr_mat = vote_by_cz.corr()

print("\n Correlation: Romney and Trump Share", corr_mat.TrumpShare.RomneyShare)
print("\n")

print("\n Correlation: Trunout Difference and Flip", corr_mat.Diff20162012.TurnoutDiff)
print("\n")


#%%
stata_file = folder + "\\workfile_china.dta"
adh_data = pd.read_stata(stata_file)

# Now bring in the adh_data...drop the year 1990....

adh_data = adh_data.drop(adh_data[adh_data["yr"] == 1990].index)

# only keep the variables week care aboud...
k_adh_data = adh_data[["czone", "d_tradeusch_pw", "d_tradeotch_pw_lag", "timepwt48"]]

#%%

adh_election = vote_by_cz.merge(k_adh_data, how = 'outer', right_on = 'czone', 
                       left_index = 'True')

adh_election = adh_election.drop(adh_election[adh_election["True"]!="both"].index)

corr_mat = adh_election.corr()

print("\n Correlation: Trump Share and ADH Share", 
      corr_mat.Diff20162012.d_tradeusch_pw)
print("\n")

print("\n Correlation: Trump Share and Other ADH Share", 
      corr_mat.Diff20162012.d_tradeotch_pw_lag)
print("\n")

#

# County Characteristics
#https://www.census.gov/popest/data/counties/asrh/2015/CC-EST2015-ALLDATA.html

#%%

adh_election["lg_d_tradeusch_pw"] = np.log(adh_election.d_tradeusch_pw)
adh_election["lg_TotalVotes2012"] = np.log(adh_election.TotalVotes2012)

elec_beta = sm.ols(formula=
'Diff20162012 ~ d_tradeusch_pw + lg_TotalVotes2012', 
                   data=adh_election).fit()


#print("\n Elasticity w.r. China Trade Growth\n", elec_beta.params)
#print("\nConfidence Interval\n", elec_beta.conf_int(alpha=0.01))
print("\nSummary of Regression\n", elec_beta.summary())


adh_election.plot(kind='scatter', x='Diff20162012', y='d_tradeusch_pw')



#btest = sm.wls(formula = 'Diff20162012 ~ lg_d_tradeusch_pw', 
#               weights = adh_election.TotalVotes2012,
#data = adh_election).fit()


















