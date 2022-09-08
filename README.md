# Statistical-analysis-and-visualization-of-seismic-magnitude-and-depth-quantities
## Python libraries used:
- Pandas
- Numpy
- Matplotlib
- scipy

## Project discription
Reads a seismic catalogue and generates various statistics for selected quantities (mean, standard deviation, minima and maxima). Plots the distribution of the following quantities (user selection):

- Depth (in km)
- Magnitude
- Origin Time's Root Mean Square (RMS, in s)
- Horizontal location error (dh, in km)
- Vertical (depth) location error (dz, in km)

Finally, it overlays functions of expected distributions (normal, lognormal and chi2) to visually determine their fit.

Sample data (sample_catalog.cat) where acquired from the Seismological Laboratory of the National and Kapodistrian University of Athens at:

http://www.geophysics.geol.uoa.gr/stations/gmapv3_db/index.php?lang=en

## Sample outputs
### Depth (km)
![](img/NKUA_SL_thiva_sample_catalogue_DEP.png)
### Magnitude
![](img/NKUA_SL_thiva_sample_catalogue_MAGNITUDE.png)
### Origin Time's Root Mean Square (RMS, in s)
![](img/NKUA_SL_thiva_sample_catalogue_RMS.png)
### Horizontal location error (dh, in km)
![](img/NKUA_SL_thiva_sample_catalogue_DH.png)
### Vertical (depth) location error (dz, in km)
![](img/NKUA_SL_thiva_sample_catalogue_DZ.png)
