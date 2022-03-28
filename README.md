![](https://img.shields.io/badge/SDK-v12.10.0)

# Differential solver
Sample app for visualizing profiles caused by different differential equations

In this app simulating profiles of different differentials is made easy. The applications was made for predicting
chemical reaction profiles, but many applications where differentials need to be solved can qualify. The app
contains two tables, one to define the reactions (notation Reaction: k1*A*B/k2*B*clorine, Rate constant: 0.1/0.542)
and one to define the species (notation Name: A/chlorine, Species concentration: 1/3.56, Applicable reactions:
-r1+r2/r4-r3+r6**2). There are also input fields to define reaction time, and plot resolution. Since the program finds 
and matches strings it can be easy to use abbreviations for the reaction input table. There is one last table
where these abbreviations can be subsituted with their full names in the plot. Since the program matches strings
input names should not contain other input names, for example species 1: catalyst, and species 2:active catalyst.
For input examples see the .png in the manifest


![](manifest/ODE_interface.png)
