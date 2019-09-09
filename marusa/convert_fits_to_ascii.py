"""
Convert all .p08.fits files to ascii spectra.
"""

import numpy as np
from astropy.io import fits
import sys
import os

# PyWiFeS
import process_stellar as ps # WHEN running this without ssh -Y, I get RuntimeError: Invalid DISPLAY variable

root = '/priv/mulga1/marusa/2m3reduced/wifes/'

obsdate = sys.argv[1]

data_dir = os.path.join(root, obsdate)

#~ for path, subdirs, files in os.walk(data_dir):
    #~ for name in files:
        #~ print os.path.join(path, name)


#~ data_dir = os.path.join('/priv/mulga1/marusa/2m3reduced/wifes/', '%s/reduced_r'%sys.argv[1]) # 20190304

print data_dir
out_dir = os.path.join(data_dir, 'ascii')
if not os.path.isdir(out_dir) and not os.path.exists(out_dir):
    os.mkdir(out_dir)

for path, subdirs, files in os.walk(data_dir):
    for name in files:
        fl=os.path.join(path, name)
        if fl.endswith('.p08.fits'):
            print fl
            f=fits.open(fl)
            header = f[0].header
            objectid=header['OBJNAME']
            run=header['RUN']
            f.close()

            flux, wave = ps.read_and_find_star_p08(fl)
            spectrum, sig = ps.weighted_extract_spectrum(flux)

            if 'T2m3wr' in name:
                filename = '%s_%s_r.dat'%(obsdate, objectid)
            elif 'T2m3wb' in name:
                filename = '%s_%s_b.dat'%(obsdate, objectid)
            
            filename = filename.replace(' ', '_')
            
            fln=os.path.join(out_dir, filename)
            print fln
            print
            np.savetxt(fln, np.transpose([wave, spectrum]))
