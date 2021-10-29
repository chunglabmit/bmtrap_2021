"""coreg.py: Main entry point for Training"""
__author__      = "Minyoung Kim"
__license__ = "MIT"
__maintainer__ = "Minyoung Kim"
__email__ = "minykim@mit.edu"


import cv2
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

from phathom import io as pio
from bmtrap.preprocessing import BMPreprocessing as BMPrep
from bmtrap.util import *


class coReg(object):
    def __init__(self, params):
        """init
        :param params: BasicParams() object
        """
        self.params = params
        self.bmPrep = BMPrep()


    def load_data(self):
        """load zarr volumes, probability maps, and source cell coordinates"""
        self.src_vol = pio.zarr.open(self.params.src_zarrpath)
        self.dst_probs = pio.zarr.open(self.params.dst_probpath)
        self.dst_vol = pio.zarr.open(self.params.dst_zarrpath)
        self.src_cc = np.load(self.params.src_cc)
        

    def get_pp(self, cc, a_slice, thr=0.4):
        """get points overlapping with high-probability area of dest probMap
        :param cc: cell center coordinates
        :param a_slice: a XY-slice
        :param thr: threshold for filtering
        """

        # get overlap
        coPos = []
        for crd in cc:
            z, y, x = crd
            if a_slice[y, x] > thr:
                coPos.append(crd)
                
        return coPos


    def scale(self, image, factor=0.5, crd=None):
        """scale image and coordinates (OPTIONAL) by factor
        :param image: image to scale
        :param factor: scaling factor
        :param crd: coordinates (OPTIONAL)
        """
        y, x = image.shape
        y_r = int(y * factor)
        x_r = int(x * factor)
        res = cv2.resize(image, dsize=(x_r, y_r), interpolation=cv2.INTER_CUBIC)
        
        if crd is not None:
            res_crd = crd.copy()
            for ci in res_crd:
                ci[1] *= factor
                ci[2] *= factor
            
            return res, res_crd
            
        return res
        
        
    def find_coPos(self, clim=[100, 800], cmap='gray', viz=False, save=True):
        """find co-positive cells 
        :param clim: clim for plt plots
        :param cmap: plt color-map to use
        :param viz: plot intermittent results
        :param save: save list of co-positive cells into .npy and .json
        """

        def style_ax(ax, title, title_loc='center'):
            ax.set_title(title, color='w', loc=title_loc)
            ax.tick_params(colors='w', grid_color='w', grid_alpha=0.5)

        cc = self.src_cc
        num_slices, height, width = self.dst_probs.shape

        if viz:
            fig = plt.figure(figsize=(30, 8))
            ax1 = fig.add_subplot(141)
            ax2 = fig.add_subplot(142)
            ax3 = fig.add_subplot(143)
            ax4 = fig.add_subplot(144)
            factor = 0.3
            
        cp_ccl = []
        for i, slice_i in enumerate(tqdm(self.dst_probs, "CoPos")):
            ind = np.where(cc[:, 0] == i)
            cc_zi = cc[ind]
            
            if len(cc_zi):
                cp_cc = self.get_pp(cc_zi, slice_i, thr=self.params.threshold)
                cp_ccl.append(cp_cc)
            
                if len(cp_cc) > 50 and viz:
                    print("len(cp_cc): ", len(cp_cc))
                    print(self.src_vol[i].shape, self.dst_vol[i].shape, slice_i.shape)
                    
                    # scaledown images
                    print("scaling down..with {}".format(factor))
                    tdt_v_s, cc_zi_s = self.scale(self.src_vol[i], factor, cc_zi)
                    cfos_v_s = self.scale(self.dst_vol[i], factor)
                    slice_i_s, cp_cc_s = self.scale(slice_i, factor, cp_cc)
                    print("scaling down..with {}(done)".format(factor))
                    
                    # plot all (cFos slice | cFos ProbMap | cFos slice w/ tdTomato+ | tdTomato slice w/ CC)
                    ax1.imshow(cfos_v_s, cmap=cmap, clim=clim)
                    ax1.set_title("cFos_slice")
                    ax2.imshow(slice_i_s, cmap=cmap)
                    ax2.set_title("cFos_ProbMap")

                    xidx, yidx = (2, 1)
                    cp_cc_npy = np.array(cp_cc_s)
                    ax3.imshow(cfos_v_s, cmap=cmap, clim=clim)
                    ax3.scatter(cp_cc_npy[:, xidx], cp_cc_npy[:, yidx], alpha=0.7, s=10, color='red')
                    ax3.set_title("cFos_slice w/ tdTomato+")
                    
                    ax4.imshow(tdt_v_s, cmap=cmap, clim=clim)
                    ax4.scatter(cc_zi_s[:, xidx], cc_zi_s[:, yidx], alpha=0.7, s=10, color='red')
                    ax4.set_title("tdTomato with CC")

                    plt.show()
                    break

        stacked=[]
        for item in cp_ccl:
            stacked += [list(np.array(x, dtype=np.float)) for x in item]
        stacked_npy = np.array(stacked)

        # save
        if save:
            np.save(os.path.join(self.params.save_path,
                                 "CoPosCC_ccPos_thr_%.2f.npy"%self.params.threshold),
                    stacked_npy)

            # dump to json
            dump2json(os.path.join(self.params.save_path,
                                   "CoPosCC_ccPos_thr_%.2f.json"%self.params.threshold),
                      stacked)
            
            # save xyz-format
            stacked_xyz = stacked_npy.copy()
            stacked_xyz[:, 0] = stacked_npy[:, 2]
            stacked_xyz[:, 2] = stacked_npy[:, 0]
            dump2json(os.path.join(self.params.save_path,
                                   "CoPosCC_ccPos_thr_%.2f_xyz.json"%self.params.threshold),
                      stacked_xyz.tolist())

        return cp_ccl


    def get_subvol(self, xr, yr, zr):
        """return sub-volume based on XYZ ranges
        
        :param xr: X-range (list of 2 items)
        :param yr: Y-range (list of 2 items)
        :param zr: Z-range (list of 2 items)
        """
        x1, x2 = xr
        y1, y2 = yr
        z1, z2 = zr
        src_subvol = self.src_vol[z1:z2, y1:y2, x1:x2]
        dst_subvol = self.dst_vol[z1:z2, y1:y2, x1:x2]
        dst_subprobs = self.dst_probs[z1:z2, y1:y2, x1:x2]
        print("src_subvol: ", src_subvol.shape,
              "dst_subvol: ", dst_subvol.shape,
              "dst_subprobs: ", dst_subprobs.shape)

        return src_subvol, dst_subvol, dst_subprobs


    def get_cc_in_region(self, cc_list, xr, yr, zr, relative=False):
        """return cells within the ROI
        
        :param cc_list: list of coordinates
        :param xr: X-range (list of 2 items)
        :param yr: Y-range (list of 2 items)
        :param zr: Z-range (list of 2 items)
        :param relative: get relative coordinate if True
        """
        sub_cc = []
        for item in cc_list:
            z, y, x = item
            if x in range(xr[0], xr[1]):
                if y in range(yr[0], yr[1]):
                    if z in range(zr[0], zr[1]):
                        if relative:
                            sub_cc.append([z-zr[0], y-yr[0], x-xr[0]])
                        else:
                            sub_cc.append(item)
        return np.array(sub_cc)


    def visualize(self, src_vol, dst_vol, dst_probs, clim=[100, 1400]):
        """plot max-projection image of src, dst, and dst probmap
        
        :param src_vol: source volume (3D)
        :param dst_vol: destination volume (3D)
        :param dst_probs: destination probability map (3D)
        :param clim: clim for plt plot
        """

        # maxProj
        self.src_maxProj = self.bmPrep._max_proj(src_vol)
        self.dst_maxProj = self.bmPrep._max_proj(dst_vol)
        self.dst_pmap_maxProj = self.bmPrep._max_proj(dst_probs)

        # plot
        fig = plt.figure(figsize=(20, 5))
        plt.subplot(131)
        plt.imshow(self.src_maxProj, clim=clim)
        plt.subplot(132)
        plt.imshow(self.dst_maxProj, clim=clim)
        plt.subplot(133)
        plt.imshow(self.dst_pmap_maxProj)
        plt.suptitle("src (left), dst (middle), dst-Prob (right)")
        plt.show()
