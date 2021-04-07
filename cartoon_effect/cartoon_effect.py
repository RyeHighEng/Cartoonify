# cartoon effect.
import tkinter as tk
import tkinter.filedialog
from PIL import Image,ImageTk
import numpy as np
from numpy import reshape,uint8,flipud
from scipy import ndimage
from skimage.transform import rescale, resize
from skimage.util import img_as_float, invert
from skimage import io, color, filters
from skimage.morphology import label as lb
from scipy.cluster.vq import kmeans,vq
import datetime, time
import sys,os
import re
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
class CartoonEffect:
    def __init__(self, sigx=0.8, sigb=0.6, p=0.98, k=1.6, style=1, epsilon=0, tau=0.98, n=20, phi = 10):
        self.sigx = sigx
        self.sigb = sigb
        self.p = p
        self.k = k
        self.style = style
        self.epsilon = epsilon
        self.n = n
        self.tau = tau
        self.phi = phi
    def dog_filter(self, img):
        gauss1 = filters.gaussian(img, self.sigx)
        gauss2 = filters.gaussian(img, self.k * self.sigx)
        # using Equation (4) to produce the difference of gaussian
        return gauss1 - self. tau * gauss2
    def xdog_filter(self, img):
        eps = self.epsilon
        img = img / img.max()
        # using Equation (5) to threshold
        e = 1 + np.tanh(self.p * (img - eps))
        e[e >= 1] = 1
        e[e <= 0] = 0 # potentially remove?
        return e.astype(np.uint8) * 255
    def stylize(self, img):
        new_img = img.copy()
        if img.ndim == 3:
            new_img = color.rgb2gray(new_img)
        new_img = filters.gaussian(new_img, sigma=self.sigb, multichannel=True)
        # Grouping and binning the pixel values
        im_min = np.amin(new_img)
        im_max = np.amax(new_img)
        im_diff = (im_max - im_min) / self.n
        n_bins = np.zeros((self.n + 1))
        for x in range(len(n_bins)):
            n_bins[x] = im_diff * x + im_min
        # Create a mask as well as L(x, y) and then apply
        mask = np.digitize(new_img,n_bins)
        level_set = np.zeros(new_img.shape)
        for i in range(len(mask)):
            level_set[i] = mask[i]
        if img.ndim ==2:
            c = level_set / self.n
            return c.astype(np.float32)
        # if img.ndim == 3:
        #     c = np.zeros((img.shape))
        #     labels, num = lb(level_set, return_num = True)
        #     blur = filters.gaussian(img, self.sigb)
        #     # im_float = img_as_float(img)
        #     im_float = img_as_float(blur)
        #     for i in range(len(labels)):
        #         mask = level_set == i
        #         c[mask, :] = im_float[mask, :].mean(axis=0)
        #     c = c / c.max()
        # Performing Color Quantization using K-Means Algorithm.
        if img.ndim == 3:
            img = img_as_float(img)
            # reshaping the pixels matrix
            pixel = reshape(img,(img.shape[0]*img.shape[1],3))
            # performing the clustering
            centroids,_ = kmeans(pixel, self.n)
            qnt,_ = vq(pixel,centroids)
            # reshaping the result of the quantization
            centers_idx = reshape(qnt,(img.shape[0],img.shape[1]))
            c = centroids[centers_idx]
            c = c / c.max()
            return c.astype(np.float32)

    ''' This function actually perfroms the cartoonify of an image'''
    def cartoonify(self, img):
        newimg = img
        if img.ndim == 3:
            newimg = color.rgb2gray(img)
        #Compute DoG Filter:
        dog = self.dog_filter(newimg)
        #Compute XDoG filter:
        xdog = self.xdog_filter(dog)
        xdog = xdog.astype(np.float32) / 255
        c = self.stylize(img)
        if c.ndim == 2:
            self.style = c * xdog
            self.style = np.clip(self.style,0, 1)
            self.style = self.style * 255
        elif c.ndim == 3:
            self.style = np.dstack((c[:,:,0] * xdog, c[:,:,1] * xdog, c[:,:,2] * xdog))
        # # Compute the Final stylized image I_style(x, y)
        # self.style = C * xdog
        # # Plot the output
        fig = plt.figure(figsize=(8, 9))
        gs = GridSpec(2, 2)
        ax0 = fig.add_subplot(gs[0, 0])
        ax1 = fig.add_subplot(gs[0, 1])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])

        ax0.imshow(img, cmap='gray')
        ax0.set_title('Original Image')
        ax1.imshow(xdog, cmap='gray')
        ax1.set_title('XDoG')
        if c.ndim == 2:
            ax2.imshow(c, cmap='gray')
            ax2.set_title('C(x,y)')
            ax3.imshow(self.style, cmap='gray')
            ax3.set_title('Cartoon')
        if c.ndim == 3:
            ax2.imshow(c,)
            ax2.set_title('C(x,y)')
            ax3.imshow(self.style)
            ax3.set_title('Cartoon')
        for a in (ax0, ax1, ax2, ax3):
            a.axis('off')
        plt.tight_layout()
        plt.plot()
        plt.show()