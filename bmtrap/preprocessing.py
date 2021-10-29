"""preprocessing.py: preprocessing class for Brain-Mapping Image Data"""
__author__      = "Minyoung Kim"
__license__ = "MIT"
__maintainer__ = "Minyoung Kim"
__email__ = "minykim@mit.edu"
__date__ = "10/19/2018"

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_float
from skimage import exposure
from scipy.ndimage import zoom


# internal
from bmtrap.const import NormalizationType


class BMPreprocessing(object):
    """Class for handling preprocessing of medical image (16bit, grayscale)"""
    def __init__(self):
        matplotlib.rcParams['font.size'] = 8
        pass


    @staticmethod
    def _clip(array, _min=0, _max=65536):
        """clip array with min and max

        Params
        ---------
        array: numpy array
        """

        return np.clip(array, _min, _max)


    @staticmethod
    def _enhance(array, _val):
        """multiply a float number to values of array

        Params
        ---------
        array: numpy array
        """

        return array * _val


    @staticmethod
    def _resize(array, scale):
        """scale array to a new size

        Params
        ---------
        array: numpy array
        scale: a tuple of (y_scale, x_scale)
        """

        return zoom(array, scale)


    @staticmethod
    def _max_proj(vol):
        d, h, w = vol.shape
        mzproj = np.zeros((h, w))
        for i in range(h):
            for j in range(w):
                mzproj[i][j] = np.max(vol[:, i, j])

        return mzproj


    @staticmethod
    def _normalize(array, cmin=None, cmax=None, percentile=None,
                   clip=False, ntype=NormalizationType.MONE_AND_ONE):

        """normalize array from range [cmin, cmax] to be in range [0.0, 1.0]
           if clip is set, then clip values that is out of boundary

           NOTE: if percentile is provided, cmin and cmax will be overwritten by percentile values.

        Parameters
        ----------
        array: numpy array
            input data
        cmin: integer, float
            clim min
        cmax: integer, float
            clim max
        percentile: 1x2 tuple
            set min and max by getting value in each percentile
        clip: boolean
            clip out of bound values or not
        """
        if cmin is not None:
            assert cmin != cmax
        assert isinstance(array, np.ndarray)

        if cmin is None:
            cmin = np.min(array)

        if cmax is None:
            cmax = np.max(array)

        if percentile is not None:
            min_p, max_p = percentile
            if min_p is not None and max_p is not None:
                cmin = np.percentile(array, min_p)
                cmax = np.percentile(array, max_p)

        cmin = float(cmin)
        cmax = float(cmax)
        if cmax - cmin == 0:
            arr = array
        elif ntype == NormalizationType.ZERO_AND_ONE:
            # values from 0 to 1
            arr = (array - cmin) * 1. / (cmax - cmin)
        elif ntype == NormalizationType.MONE_AND_ONE:
            # values from -1 to 1
            arr = 2 * (array - cmin) * 1. / (cmax - cmin) - 1
        elif ntype == NormalizationType.ZERO_MEAN:
            # values from ? to ?, but mean at 0
            arr = (array - array.mean()) * 1. / array.std()
        else:
            assert ValueError("Unknown normalization method.")

        if clip:
            if ntype == NormalizationType.ZERO_AND_ONE:
                arr = np.clip(arr, 0., 1.)
            elif ntype == NormalizationType.MONE_AND_ONE:
                arr = np.clip(arr, -1., 1.)
            else:
                assert ValueError("Can't clip on zero_mean normalization")

        return arr


    @staticmethod
    def _rescale_intensity(_img, _percentile=(2, 98)):
        """do Constrast Stretchint on image with percentiles

        Parameters
        ----------
        _img: numpy array
            input image
        _percentile: a tuple
            range of percentile (low, high)
        """

        pl, pm = np.percentile(_img, _percentile)
        return exposure.rescale_intensity(_img, in_range=(pl, pm))


    @staticmethod
    def _equalize_hist(_img):
        """apply histogram equalization

        Parameters
        ----------
        _img: numpy array
            input image
        """

        return exposure.equalize_hist(_img)


    @staticmethod
    def _equalize_adapthist(_img, _clip_limit=0.03):
        """apply adaptive histogram equalization

        Parameters
        ----------
        _img: numpy array
            input image
        _clip_limit: float
        """
        return exposure.equalize_adapthist(_img, clip_limit=_clip_limit)


    def test_on_all(self, _img, _isTest=False):
        """run every preprocessing algorithm and visualize using pyplot

        Parameters
        ----------
        _img: numpy array
            input image
        """

        plt.ion()
        img = _img.copy()

        isLowContrast = exposure.is_low_contrast(img)
        img_norm = self._normalize(img, ntype=NormalizationType.ZERO_AND_ONE)

        # Contrast stretching
        img_rescale = self._rescale_intensity(img, (0.05, 99.9))     # best for microglia images (E10.5)

        # Equalization
        img_eq = self._equalize_hist(img)

        # Adaptive Equalization
        img_adapteq = self._equalize_adapthist(img_norm)

        if not _isTest:
            # Display results
            fig = plt.figure(figsize=(10, 6))
            axes = np.zeros((2, 4), dtype=np.object)
            axes[0, 0] = fig.add_subplot(2, 4, 1)
            for i in range(1, 4):
                axes[0, i] = fig.add_subplot(2, 4, 1+i, sharex=axes[0,0], sharey=axes[0,0])
            for i in range(0, 4):
                axes[1, i] = fig.add_subplot(2, 4, 5+i)

            ax_img, ax_hist, ax_cdf = self.plot_img_and_hist(img, axes[:, 0])
            ax_img.set_title('Original')

            y_min, y_max = ax_hist.get_ylim()
            ax_hist.set_ylabel('# of pixels')
            ax_hist.set_yticks(np.linspace(0, y_max, 5))

            ax_img, ax_hist, ax_cdf = self.plot_img_and_hist(img_rescale, axes[:, 1])
            ax_img.set_title('Contrast stretching (0.05, 99.9)')

            ax_img, ax_hist, ax_cdf = self.plot_img_and_hist(img_eq, axes[:, 2])
            ax_img.set_title('Hist EQ')

            ax_img, ax_hist, ax_cdf = self.plot_img_and_hist(img_adapteq, axes[:, 3])
            ax_img.set_title('Adaptive EQ')

            ax_cdf.set_ylabel('Fraction of total intensity')
            ax_cdf.set_yticks(np.linspace(0, 1, 5))

            # prevent overlap of y-axis labels
            fig.tight_layout()
            plt.show()
            plt.ioff()

        return img, img_rescale, img_eq, img_adapteq, isLowContrast



    def plot_img_and_hist(self, _image, _axes, _bins=65536):
        """Plot an image along with its histogram and cumulative histogram.

        Parameters
        ----------
        _img: numpy array
            input image
        _axes: tuple
            a pair of raw data and histogram
        _bins: integer
            number of bins for histogram used
        """

        image = img_as_float(_image)
        ax_img, ax_hist = _axes
        ax_cdf = ax_hist.twinx()

        # Display image
        #ax_img.imshow(image, cmap=plt.cm.gray)
        ax_img.imshow(image, cmap=plt.cm.viridis)
        ax_img.set_axis_off()
        ax_img.set_adjustable('box-forced')

        # Display histogram
        ax_hist.hist(image.ravel(), bins=_bins, histtype='step', color='black')
        ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
        ax_hist.set_xlabel('Pixel intensity')
        ax_hist.set_xlim(-1, 1)
        ax_hist.set_yticks([])

        # Display cumulative distribution
        img_cdf, bins = exposure.cumulative_distribution(image, _bins)
        ax_cdf.plot(bins, img_cdf, 'r')
        ax_cdf.set_yticks([])

        return ax_img, ax_hist, ax_cdf
