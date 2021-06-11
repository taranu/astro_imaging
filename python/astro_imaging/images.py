from astropy.io import fits
from astropy.visualization import make_lupton_rgb
import config
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os


def func_path_default(source, band, paths: config.Paths = None, postfix=None):
    """ Return a file path to data for a source in a given band.

    Parameters
    ----------
    source : `str` or `int`
        A source name or label.
    band : `str`
        A bandpass filter name.
    paths : `config.Paths`
        A class with an `images` attribute pointing to a writeable path.
    postfix : `str`
        A postfix to append to the name. Default `.fits`.

    Returns
    -------
    path : `str`
        The path to the file to write or read.
    """
    if paths is None:
        paths = config.paths_default
    if postfix is None:
        postfix = ".fits"
    return os.path.join(paths.images, f'{source}{band}{postfix}')


def make_img_rgb(
        source, bands_weights, func_path=None, write=False, kwargs_make_rgb=None, plot=False,
        return_imgs=False, return_imgs_fits=False, format_img=None, midfix=None, **kwargs,
):
    """ Make an RGB image with arbitrary color balance.

    Parameters
    ----------
    source : `int` or `str`
        A source ID or name.
    bands_weights : `dict` [`str`, `float`]
        A dict of weights per band name.
    func_path : function
        A function that returns a path for a source in a given band.
    write : `bool`
        Whether to write the file to disk.
    kwargs_make_rgb : `dict`
        Keyword args to pass to `make_lupton_rgb`.
    plot : `bool`
        Whether to plot the generated image.
    return_imgs : `bool`
        Whether to return the input images (rescaled single-band).
    return_imgs_fits : `bool`
        Whether to return the original FITS files as read from disk.
        Ignored if `return_imgs` is False.
    format_img : `str`
        Image format. Default "png".
    midfix : `str`
        A name for the RGB image. Default is unseparated bands,
        surrounded by underscores (i.e. "_RGB_").
    kwargs
        Additional keyword arguments to pass to `func_path`.

    Returns
    -------
    img_rgb
    """
    if not hasattr(bands_weights, 'items'):
        bands_weights = {key: 1. for key in bands_weights}
    if func_path is None:
        func_path = func_path_default
    if kwargs_make_rgb is None:
        kwargs_make_rgb = {}
    if format_img is None:
        format_img = 'png'
    if midfix is None:
        midfix = f"_{''.join(bands_weights)}_"

    imgs = {}
    imgs_fits = {}
    name_source = f'{source}'
    for band, weight in bands_weights.items():
        img_fits = fits.open(f'{func_path(name_source, band, **kwargs)}')
        if return_imgs_fits:
            imgs_fits[band] = img_fits
        imgs[band] = weight*img_fits[1].data

    img_rgb = make_lupton_rgb(*list(imgs.values()), **kwargs_make_rgb)
    if write:
        imageio.imwrite(
            os.path.join(
                config.paths_default['images'],
                name_source,
                func_path(source, midfix, postfix=f'.{format_img}', **kwargs)
            ),
            np.flip(img_rgb, axis=0),
        )
    if plot:
        plt.imshow(img_rgb)
    if return_imgs:
        return img_rgb, imgs, imgs_fits if return_imgs_fits else None
    return img_rgb
