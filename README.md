# Did-China-Cause-Trump
This code is part of a project (for me) to learn Python through the NYU-Stern-Econ databoot camp course (http://databootcamp.nyuecon.com/). It combines US 2016 Election data at the county level with the Autor, Dorn, and Hanson (2013) US Trade Exposure from China data. Basically, it asks: Did China Trade Cause Trump?

This code does the following: It imports the 2016 Election Data, 2012 Election, imports a Country FIPS code to Commuting Zone mapping and then merges it with the ADH data which measures the exposure of a commuting zone to Chinese trade. 

It then correlates the change in the republican vote with the trade exposure measure.

This relies upon four public data sets that are in the site, but can be found here:

1) 2016 US election data : https://data.world/aaronhoffman/us-general-election-2016

2) 2012 US election data: https://data.world/aaronhoffman/us-general-election-2012

2) County FIPS to Communting Zones: http://www.ers.usda.gov/data-products/commuting-zones-and-labor-market-areas/

3) Autor, Dorn, and Hanson data: http://www.ddorn.net/data.htm

