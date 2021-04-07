# This contains the class required to create the tkinter application.
import tkinter as tk
import tkinter.filedialog
from PIL import Image,ImageTk
import numpy as np
from scipy import ndimage
from skimage.transform import rescale, resize
from skimage.util import img_as_float
from skimage import io, color, filters
from skimage.morphology import label as lb
from numpy import reshape,uint8,flipud
from scipy.cluster.vq import kmeans,vq
import datetime, time
import sys,os
import re
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from cartoon_effect import cartoon_effect

'''This class is used to create the tkinter window i.e. the GUI. '''
class MainApplication():
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("ELE882 Final Project: Cartoonify an Image! by Chris Jarvis")
        self.main_window.geometry('550x550')
        self.main_window.configure(background='white')
        # Cartoonify the selected image.
        self.button1 = tk.Button(self.main_window, text="Cartoonify an Image", command = self.upload, padx=10,pady=5)
        self.button1.configure(background='#364156', foreground='white',font = ('calibri',10,'bold'))
        self.button1.pack(side= tk.TOP,pady=50)
        # Change the default paramters (optional).
        self.param1= tk.Button(self.main_window,text="Change parameters ",command= self.sigma,padx=30,pady=5)
        self.param1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
        self.param1.pack(side=tk.TOP,pady=50)
        # Save the image.
        self.save1= tk.Button(self.main_window,text="Save cartoon image",command=self.save,padx=30,pady=5)
        self.save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
        self.save1.pack(side=tk.TOP,pady=50)
        # creating an object of class cartoon effect
        self.cartoon = cartoon_effect.CartoonEffect()
        # Create a label to show the default parameters
        main_label = tk.Label(self.main_window, text=f"Default Parameters: σb = {self.cartoon.sigb}, \
σx = {self.cartoon.sigx}, ρ = {self.cartoon.p}, Ɛ = {self.cartoon.epsilon}, N = {self.cartoon.n}, k = {self.cartoon.k} ")
        main_label.configure(background='#364156', foreground='white',font=('calibri',11,'bold'))
        main_label.pack(side=tk.TOP, pady=50)
        tk.mainloop()


    def error_message(self, txt):
        self.error = tk.Tk()
        self.error.title("Error")
        self.error.geometry('400x100')
        err_label = tk.Label(self.error, text= txt)
        err_label.configure(background='#364156', foreground='white',font=('calibri',11,'bold'))
        err_label.place(x=150, y=25, anchor='center')


    def upload(self):
        self.sub_window = tk.Tk()
        im_loc = tk.filedialog.askopenfilenames(parent=self.sub_window, title='Choose an Image')
        name = im_loc[0]
        img = io.imread(im_loc[0])
        self.sub_window.destroy()
        if name.lower().endswith(('.jpg', '.png', '.jfif')):
            self.cartoon.cartoonify(img)
        else:
            self.error_message("Please select an image with a proper format.")

        '''This function creates an openfiledialog box from tkinter
        which the user can use to select an image. Once an image is chosen
        it will then be passed to the cartoonify function where it will be converted.
        Next the image will be passed to a display function where it will be shown on the screen.
        Input: None
        output: the converted image.'''


    def save(self):
        '''This function will take the cartoonified image and will give the option to save the image
        to a file.
        Input: Cartoonified image
        Output: None, saved the image to specified path.'''
        if type(self.cartoon.style) != np.ndarray:
            self.error_message('Error: You must cartoonify an image before trying to save it.')
        else:
            self.sub_window = tk.Tk()
            # out = tk.filedialog.asksaveasfile(parent =self.sub_window, title='Save Image', mode='a')
            out = tk.filedialog.asksaveasfilename(parent =self.sub_window, title='Save Image')
            self.sub_window.destroy()
            if  out.lower().endswith(('.jpg', '.png', '.jfif')):
                io.imsave(out, self.cartoon.style)
            elif not out.lower().endswith(('.jpg', '.png', '.jfif')):
                add_extension = out + '.jpg'
                io.imsave(add_extension, self.cartoon.style)
            else:
                raise TypeError("Unknown")


    def sigma(self):
        # function which will get the data from the input fields
        def getData(window):
            sigmax = e1.get()
            sigmab = e.get()
            pval = p.get()
            kval = k.get()
            nval = n.get()
            epval = ep.get()
            if sigmax != "":
                self.cartoon.sigx = float(sigmax)
            if sigmab != "":
                self.cartoon.sigb = float(sigmab)
            if pval != "":
                self.cartoon.p = float(pval)
            if kval != "":
                self.cartoon.k = float(kval)
            if nval != "":
                self.cartoon.n = int(nval)
            if epval != "":
                self.cartoon.epsilon = float(epval)
            window.destroy()

        self.select_window = tk.Tk()
        self.select_window.title("Change Variables")
        main_label = tk.Label(self.select_window, text = "Please leave boxes blank if you do not wish to change that variable.")
        main_label.configure(background='#364156', foreground='white',font=('calibri',11,'bold'))
        main_label.grid(row = 0, column=0, columnspan=4, padx = 10, pady = 10)
        # e is the textbox and label for changing σb
        e_label = tk.Label(self.select_window, text = "Change σb (Gaussian Blur)")
        e_label.grid(row = 1, column=0, columnspan=1, padx = 10, pady = 10)
        e = tk.Entry(self.select_window, width = 35, borderwidth = 5)
        e.grid(row = 2, column=0, columnspan=1, padx = 10, pady = 10)
        # e1 is the label and textbox for changing σx
        e1_label = tk.Label(self.select_window, text = "Change σx (XDoG)")
        e1_label.grid(row = 3, column=0, columnspan=1, padx = 10, pady = 10)
        e1 = tk.Entry(self.select_window, width = 35, borderwidth = 5)
        e1.grid(row = 4, column=0, columnspan=1, padx = 10, pady = 10)
        # p is the textbox and label to change ρ
        p_label = tk.Label(self.select_window, text = "Change thresholding parameter, ρ")
        p_label.grid(row = 1, column=3, columnspan=1, padx = 10, pady = 10)
        p = tk.Entry(self.select_window, width = 35, borderwidth = 5)
        p.grid(row = 2, column=3, columnspan=1, padx = 10, pady = 10)
        # k is the textbox and label to change k
        k_label = tk.Label(self.select_window, text = "Change variable k")
        k_label.grid(row = 3, column=3, columnspan=1, padx = 10, pady = 10)
        k = tk.Entry(self.select_window, width = 35, borderwidth = 5)
        k.grid(row = 4, column=3, columnspan=1, padx = 10, pady = 10)
        # n is the textbox and label to change N
        n_label = tk.Label(self.select_window, text = "Change number of bins, N")
        n_label.grid(row = 5, column=0, columnspan=1, padx = 10, pady = 10)
        n = tk.Entry(self.select_window, width = 35, borderwidth = 5)
        n.grid(row = 6, column=0, columnspan=1, padx = 10, pady = 10)
        # ep is the textbox and label to change Ɛ
        ep_label = tk.Label(self.select_window, text = "Change thresholding parameter, Ɛ")
        ep_label.grid(row = 5, column=3, columnspan=1, padx = 10, pady = 10)
        ep = tk.Entry(self.select_window, width = 35, borderwidth = 5)
        ep.grid(row = 6, column=3, columnspan=1, padx = 10, pady = 10)
        '''we need to pass the window as an arugument to getData() in order to be able to destroy it after we
        read the data from the input fields (without manually having to close the window).'''
        self.submit1 = tk.Button(self.select_window,text="Submit Changes",command= lambda: getData(self.select_window),padx=30,pady=5)
        self.submit1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
        self.submit1.grid(row = 9, column=1, columnspan=2, padx = 10, pady = 10)
        self.select_window.mainloop()