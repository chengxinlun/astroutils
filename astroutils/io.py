from astropy.io import fits
import numpy as np


BLOCK_SIZE = 2880


def init_fits_bintable(fname, primary_header, ext_header, nsize):
    '''
    Initialize a fits bin table file fromm scratch

    Parameters
    ----------
    fname: str, filename of the new fits
    primary_header: astropy.io.fits.header, header for primary HDU
    ext_header: astropy.io.fits.header, header for extension HDU (the table)
    '''
    # Calculate header length
    phl = len(primary_header.tostring())
    ehl = len(ext_header.tostring())
    # Manualy set size
    ext_header['NAXIS1'] = nsize[0]
    ext_header['NAXIS2'] = nsize[1]
    # Write them to file
    with open(fname, 'wb+') as f:
        f.seek(0, 0)
        _fits_write_hdu(f, primary_header)
        _fits_write_hdu(f, ext_header)
        # Write EOF
        if nsize[0] * nsize[1] != f.tell() - phl - ehl:
            f.seek(-1, 1)
            f.write(b'\0')
        else:
            f.write(b'\x00' * (BLOCK_SIZE - 1))
            f.write(b'\0')
    return phl + ehl


def _fits_write_hdu(f, header):
    '''
    Write empty HDU according to header
    '''
    txt = header.tostring()
    f.write(txt.encode('ascii'))
    if header['NAXIS'] != 0:
        shape = tuple(header['NAXIS{0}'.format(ii)] 
                      for ii in range(1, header['NAXIS'] + 1))
        data_size = np.product(shape) * np.abs(header['BITPIX'] // 8)
        to_pad = (BLOCK_SIZE - (data_size % BLOCK_SIZE)) % BLOCK_SIZE
        f.seek(data_size + to_pad, 1)


def fits_write(f, ss, shift, array):
    '''
    Write n rows into fits file.
    Will be flushed each write, so try to write as much as possible

    Parameters
    ----------
    f: File, opened as rb+
    ss: intial shifting for primary and extension headers
    shift: shift in bytes to start writing
    array: numpy.ndarray, the array to write

    Returns
    -------
    None

    Raises
    ------
    None
    '''
    f.seek(ss + shift, 0)
    f.write(bytes(array))
    f.flush()
