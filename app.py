import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('500x500')
top.title("Let's start cartoonizing!")
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('Roboto Condensed',24,'bold'))

def upload():
    PathOfImage=easygui.fileopenbox()
    cartoonize(PathOfImage)


def cartoonize(PathOfImage):
    # This is to read the image
    InitialImage = cv2.imread(PathOfImage)
    InitialImage = cv2.cvtColor(InitialImage, cv2.COLOR_BGR2RGB)
    #This is for printing of Image  # Image is stored in form of numbers with the help of NumPy

    #Confirmation of correct input
    if InitialImage is None:
        print("Cannot find an image. Please enter a valid input")
        sys.exit()

    ReSized1 = cv2.resize(InitialImage, (1280, 720))
    #plt.imshow(ReSized1, cmap='gray')


    #Then image is converted to grayscale
    grayScaleImage= cv2.cvtColor(InitialImage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (1280, 720))
    #plt.imshow(ReSized2, cmap='gray')


    #Then smoothening is done using median blur
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 3)
    ReSized3 = cv2.resize(smoothGrayScale, (1280, 720))
    #plt.imshow(ReSized3, cmap='gray')

    #Thresholding is used to retrieve the edges 
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (1280, 720))
    #plt.imshow(ReSized4, cmap='gray')

    #Noise is removed by using bilateral filter and edges are sharpened
    colorImage = cv2.bilateralFilter(InitialImage, 9, 250, 250)
    ReSized5 = cv2.resize(colorImage, (1280, 720))
    #plt.imshow(ReSized5, cmap='gray')


    #Then masking of the edged image is done by using bitwise and
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (1280, 720))
    #plt.imshow(ReSized6, cmap='gray')

    # The whole transition has to be plotted
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save cartoonized image",command=lambda: save(ReSized6, PathOfImage),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',12,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def save(ReSized6, PathOfImage):
    #Image is saved using imwrite()
    newName="cartoonized_Image"
    path1 = os.path.dirname(PathOfImage)
    extension=os.path.splitext(PathOfImage)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top,text="Cartoonize an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('Roboto Condensed',12,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()



