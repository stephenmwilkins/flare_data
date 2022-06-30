
import os

import numpy as np
from astropy.table import Table, Column, vstack
import astropy.units as u



indir = 'Yung_2019'

redshifts = [4,5,6,7,8,9,10]



tables = []

for z in redshifts:

    # print(z, f)

    data = np.loadtxt(f'original_data/{indir}/SFRF_z{z}.dat').T

    X = data[0]
    Y = data[1]
    s = ~np.isnan(Y)

    if np.sum(s)>0:
        t = Table()
        t.add_column(Column(data = z*np.ones(np.sum(s)), name = 'z'))
        t.add_column(Column(data = X[s], name = 'log10SFR', unit = 'dex(Msun yr^-1)'))
        t.add_column(Column(data = Y[s], name = 'phi', unit = 'Mpc^-3 dex^-1'))

        tables.append(t)

table = vstack(tables)

table.meta['x'] = 'log10SFR'
table.meta['y'] = 'phi'
table.meta['name'] = 'Santa Cruz SAM'
table.meta['redshifts'] = list(set(table['z']))
table.meta['type'] = 'binned'
table.meta['references'] = ['2019MNRAS.490.2855Y']

out_name = 'scsam'

table.write(f'models/binned/{out_name}.ecsv', format = 'ascii.ecsv', overwrite=True)