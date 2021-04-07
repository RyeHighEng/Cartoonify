import tkinter as tk
import tkinter.filedialog
from PIL import Image,ImageTk
import numpy as np
from numpy import reshape,uint8,flipud
from scipy import ndimage
from skimage.transform import rescale, resize
from skimage.util import img_as_float
from scipy.cluster.vq import kmeans,vq
from skimage import io, color, filters
import datetime, time
import sys,os
import re
import frame
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from cartoon_effect import cartoon_effect

if __name__ == '__main__':
    app = frame.MainApplication()
