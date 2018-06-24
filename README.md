# IAV-GPS
Preparing GPS files to be used in Google Earth\
Script written in Python 3.6\
The goal behind this project is to define the projection of three different shapefiles:\
    <tab>PTOPO18 : Topographic Points<\tab>\
    LAMP18: Lampe\
    REG18: Regard\
These points have been collected in the IAV using a GPS. The projection used is :\
    'Lambert Conformal Conique-Morocco Zone 1"\
The professor forgot to give us the projection files, so i had to define the projection and reproject it to a projection that in\ order to display it properly in on top of Google Earth Pro.\
The procedure is as follow:\
1- Make a backup for everything in the directory\
2- Define the projection for the three shapefiles\
3- Reproject the datasets to WGS 84\
4- Plot the original files and the re-projected ones
