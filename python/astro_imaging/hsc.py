import astropy.units as u
import numpy as np
import os
import requests

paths_cutout = {
    'pdr1': 'https://hsc-release.mtk.nao.ac.jp/das_cutout/s16a/cgi-bin/cutout?',
    's16a': 'https://hsc-release.mtk.nao.ac.jp/das_cutout/s16a/cgi-bin/cutout?',
    'pdr2': 'https://hsc-release.mtk.nao.ac.jp/das_cutout/pdr2/cgi-bin/cutout?',
}
paths_psf = {
    'pdr1': 'https://hsc-release.mtk.nao.ac.jp/psf/s16a/cgi/getpsf?',
    's16a': 'https://hsc-release.mtk.nao.ac.jp/psf/s16a/cgi/getpsf?',
    'pdr2': 'https://hsc-release.mtk.nao.ac.jp/psf/pdr2/cgi/getpsf?',
}
release_default = 'pdr2'


def get_bands_weights_default():
    # See http://mips.as.arizona.edu/~cnaw/sun.html
    # grizy AB abs. mags: 5.07, 4.64, 4.52, 4.50, 4.50
    # x = 1/10**(-0.4*(np.array([5.07, 4.64, 4.52, 4.50, 4.50])-4.5)) = [1.69044093, 1.13762729, 1.01859139, 1., 1.])
    # x/np.mean(x) = [1.44564678, 0.97288654, 0.87108833, 0.85518917, 0.85518917]
    return {
        'HSC-G': 1.44564678,
        'HSC-R': 0.97288654,
        'HSC-I': 0.87108833,
        'HSC-Z': 0.85518917,
        'HSC-Y': 0.85518917,
    }


def get_defaults(band=None, type_img=None, rerun=None, release=None):
    if type_img is None:
        type_img = 'coadd'
    if band is None:
        band = 'HSC-R'
    if rerun is None:
        rerun = 'any'
    if release is None:
        release = release_default
    return band, type_img, rerun, release


def write_request(path_request, args, filename):
    request = '&'.join((f'{key}={value}' for key, value in args.items()))
    request = f'{path_request}{request}'
    rv = requests.get(request, stream=True)
    with open(filename, 'wb') as f:
        for chunk in rv:
            f.write(chunk)


def download_cutout(
        ra, dec, filename=None, half_width=None, half_height=None, type_img=None, get_image=True, get_mask=True,
        get_variance=True, band=None, rerun=None, release=None, path_cutout=None,
):
    band, type_img, rerun, release = get_defaults(band=band, type_img=type_img, rerun=rerun, release=release)
    if half_width is None:
        half_width = half_height if half_height is not None else 30.24*u.arcsec
    if half_height is None:
        half_height = half_width
    if path_cutout is None:
        path_cutout = paths_cutout[release]

    if filename is None:
        filename = f'{ra}_{dec}_{str(2*half_width).replace(" ","")}x{str(2*half_height).replace(" ","")}_{type_img}_' \
                   f'{band}.fits'

    args = {
        'ra': ra,
        'dec': dec,
        'sw': half_width,
        'sh': half_height,
        'type': type_img,
        'image': bool(get_image),
        'mask': bool(get_mask),
        'variance': bool(get_variance),
        'filter': band,
        'rerun': rerun,
    }

    write_request(path_request=path_cutout, args=args, filename=filename)


def download_psf(
        filename, ra, dec, type_img=None, centered=True, band=None, rerun=None, release=None, path_psf=None,
):
    band, type_img, rerun, release = get_defaults(band=band, type_img=type_img, rerun=rerun, release=release)
    if path_psf is None:
        path_psf = paths_psf[release]

    args = {
        'ra': ra,
        'dec': dec,
        'type': type_img,
        'centered': centered,
        'filter': band,
        'rerun': rerun,
    }

    write_request(path_request=path_psf, args=args, filename=filename)


def download_sources(
        sources, col_id, col_ra, col_dec, bands=None, midfix=None, cutout=True, psf=False, kwargs_cutout=None,
        kwargs_psf=None,
):
    if bands is None:
        bands = get_bands_weights_default().keys()
    if midfix is None:
        midfix = ''
    for source in sources:
        src = os.path.basename(source)
        if not os.path.exists(source):
            os.mkdir(source)
        idx = np.where(col_id == int(src))[0][0]
        print(f'Downloading {src} with cat index {idx}')
        ra, dec = (col[idx] for col in (col_ra, col_dec))
        for band in bands:
            filename = f'{src}{midfix}{band}'
            if cutout:
                download_cutout(
                    os.path.join(source, f'{filename}.fits'), ra=ra, dec=dec, band=band, **kwargs_cutout
                )
            if psf:
                download_psf(
                    os.path.join(source, f'{filename}-psf.fits'), ra=ra, dec=dec, band=band, **kwargs_psf
                )
