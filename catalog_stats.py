# -*- coding: utf-8 -*-

pt_catalog = 'NKUA_SL_thiva_sample_catalogue.cat'

dict_stats_quantities = {  # values are the x labels of each histo
'Dep':'Depth (km)', 'Magnitude':'Magnitude',     # microseismic parameters
'RMS':'RMS (s)', 'dh':'dz (km)', 'dz':'dz (km)'  # errors, dh = sqrt(dx ** 2 + dy ** 2)
}

nbins = 30  # number of bins for each quantitiy's histogram, EXCEPT
			# rms & magnitude (which always have a step of 0.1)


######################################################
"""

Read a seismic catalogue and generate statistics of
various quantities (magnitude, depth, errors).

"""


#-- imports
import os
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt

#--
if pt_catalog.endswith('cat'):
    # read the NKUA-SL `cat` format
    df = pd.read_csv(pt_catalog, delim_whitespace=True)
    # rename columns for compatibility
    df.rename(columns={'Mag': 'Magnitude'}, inplace=True)
else:
    df = pd.read_csv(pt_catalog)

#-- iterate over quantities
columns = ['quantity', 'N', 'mean', 'sdev', 'min', 'max']
df_otp = pd.DataFrame(columns=columns)
for quant in sorted(dict_stats_quantities):	
	
	print(f'>> working on "{quant}"')
	
	# store data to a `ndarray`
	if quant != 'dh':
		data = df[quant].to_numpy()
	elif quant == 'dh':
		data = np.sqrt(df['dy'] ** 2 + df['dx'] ** 2).to_numpy()	
	
	# get desired stats
	mean = round(data.mean(), 4)
	std = round(data.std(), 4)

	#-- get the probability density function of a normal distribution
	npdf = stats.norm.pdf(data, mean, std)
	lpdf = stats.lognorm.pdf(data, mean, std)
	cpdf = stats.chi2.pdf(data, mean, std)

	# index to sort values for plotting
	idx = data.argsort()

	#-- plot the histogram and pdf

	_bins_ = np.arange(data.min(), data.max() + 0.1, 0.1) if quant in ['Magnitude', 'RMS'] else nbins

	plt.close()
	n, b, p = plt.hist(
		data,
		bins=_bins_,
		ec='k',
		fc='r'
		)

	# get the total area of the histogram to 
	# "denormalize" PDF in plot
	a = np.sum(np.diff(b) * n)

	plt.plot(data[idx], a * npdf[idx], color='k', label='norm')
	plt.plot(data[idx], a * lpdf[idx], color='k', ls='--', label='lognorm')
	plt.plot(data[idx], a * cpdf[idx], color='k', ls='dotted', label='chi2')
	
	#-- prettify
	plt.title('mu={:.4f} | s={:.4f} (N={:,})'.format(mean, std, data.size))
	plt.xlabel(dict_stats_quantities[quant])
	plt.ylabel('#')
	plt.grid(ls='--', alpha=0.7)
	plt.legend(loc='upper right')

	pt_output = os.path.splitext(pt_catalog)[0] + f'_{quant.upper()}.png'
	print(f'>> Saving fig @ "{pt_output}"')
	plt.savefig(pt_output, bbox_inches='tight', dpi=300)
	
	#-- add stats to the output `DataFrame`
	df_otp.at[len(df_otp)] = dict(
		quantity=quant,
		N=data.size,
		mean=mean,
		sdev=std,
		min=round(np.nanmin(data), 4),
		max=round(np.nanmax(data), 4)
		)

print('~~~~~~~~~~~~~~~~~\nFinal Statistics')
print(df_otp)

#-- write `DataFrame` to a csv
pt_otp_csv = os.path.splitext(pt_catalog)[0] + '_stats.csv'
print(f'>> Writing stats @ "{pt_otp_csv}"')
df_otp.to_csv(pt_otp_csv, index=False)