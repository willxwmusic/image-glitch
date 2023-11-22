import tifffile as tiff
import random
import numpy

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from PIL import ImageTk, Image

def clampSize(n, bound): 
    if n < 0: 
        return 0
    elif n > bound: 
        return bound
    else: 
        return n 

def colourbend(redOffset,greenOffset,blueOffset,alphaOffset, randomiseOffset, randomnessAmount):

    if randomiseOffset == True:

        for x in range(0, imgwidth):

            redRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            greenRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            blueRandomness = random.uniform(-randomnessAmount,randomnessAmount)

            for y in range(0, imgheight):

                data[y][x][0] -= redOffset * redRandomness
                data[y][x][1] -= greenOffset * greenRandomness
                data[y][x][2] -= blueOffset * blueRandomness
                data[y][x][3] -= alphaOffset
    else:

        for x in range(0, imgwidth):

            for y in range(0, imgheight):

                redRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1
                greenRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1
                blueRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1

                data[y][x][0] -= redOffset * redRandomness
                data[y][x][1] -= greenOffset * greenRandomness
                data[y][x][2] -= blueOffset * blueRandomness
                data[y][x][3] -= alphaOffset

def pixelShift(frequency_exponent,horizontalOffset):
    frequency = 2^frequency_exponent
    for i in range(0,(frequency)):
        offset = random.randint(horizontalOffset/2,horizontalOffset)
        for y in range(int(i*imgheight/frequency),int((i+1)*imgheight/frequency)):
            for x in range(0,imgwidth):
                if x-offset > 0:
                    data[y][x] = original[y][x-offset]
                else:
                    data[y][x] = original[y][(imgwidth-1) + (x-offset)]

def open_image():
    file_path = filedialog.askopenfilename(initialdir="file_path", title="Hola", filetypes=(("All files","*.*"),("tiff","*.tiff")))
    print(file_path)

    global original 
    original = tiff.imread(file_path)
    global data
    data = tiff.imread(file_path)
    global imgwidth
    imgwidth = original.shape[1]
    global imgheight
    imgheight = original.shape[0]

    loaded_filename = Label(root, text=file_path)
    loaded_filename.place(x=150,y=0)

def apply_processing():
    pixelShift(16,imgwidth/2)
    colourbend(red_offset_slider.get(),green_offset_slider.get(),blue_offset_slider.get(),alpha_offset_slider.get(),alt_colour_bend,0.2)
    applied_notification = Label(root, text="Processing Applied!")
    applied_notification.place(x=150, y=500)


def save_image():
    save_directory = filedialog.asksaveasfilename(initialdir="file_path", title="Hola", filetypes=(("TIFF","*.tiff"),("All files","*.*")))
    tiff.imwrite(save_directory, data, photometric='rgb')

root = Tk()
root['background']='#222222'
root.minsize(width="400", height="600")
open_button = Button(root, text ="Open", command = open_image)
apply_button = Button(root, text ="Apply", command = apply_processing)
save_button = Button(root, text ="Save", command = save_image)

open_button.place(x=0,y=0)
apply_button.place(x=100,y=0)
save_button.place(x=200, y=0)

do_pixel_shift = IntVar
pixel_shift_checkbox = Checkbutton(root, text='Pixel Shifting',variable=do_pixel_shift, onvalue=True, offvalue=False)

do_colour_bend = IntVar
colour_bend_checkbox = Checkbutton(root, text='Colour Bending',variable=do_colour_bend, onvalue=True, offvalue=False)

alt_colour_bend = IntVar
alt_colour_bend_checkbox = Checkbutton(root, text='Alt. Colour Bending',variable=alt_colour_bend, onvalue=True, offvalue=False)

colour_bend_checkbox.place(x=0,y=50)
alt_colour_bend_checkbox.place(x=0,y=75)

red_offset_slider_label = Label(root, text="Red Offset")
red_offset_slider_label.place(x=0,y=115)
red_offset_slider = ttk.Scale(root, from_=0, to=255, orient=HORIZONTAL)
red_offset_slider.place(x=150, y=115)

green_offset_slider_label = Label(root, text="Green Offset")
green_offset_slider_label.place(x=0,y=165)
green_offset_slider = ttk.Scale(root, from_=0, to=255, orient=HORIZONTAL)
green_offset_slider.place(x=150, y=165)

blue_offset_slider_label = Label(root, text="Blue Offset")
blue_offset_slider_label.place(x=0,y=215)
blue_offset_slider = ttk.Scale(root, from_=0, to=255, orient=HORIZONTAL)
blue_offset_slider.place(x=150, y=215)

alpha_offset_slider_label = Label(root, text="Alpha Offset")
alpha_offset_slider_label.place(x=0,y=265)
alpha_offset_slider = ttk.Scale(root, from_=0, to=1, orient=HORIZONTAL)
alpha_offset_slider.place(x=150, y=265)

randomness_slider_label = Label(root, text="Randomness")
randomness_slider_label.place(x=0,y=315)
randomness_slider = ttk.Scale(root, from_=0, to=1, orient=HORIZONTAL)
randomness_slider.place(x=150, y=315)

pixel_shift_checkbox.place(x=0,y=375)

green_offset_slider_label = Label(root, text="Pixel Shift Amount")
green_offset_slider_label.place(x=0,y=415)
green_offset_slider = ttk.Scale(root, from_=0, to=4, orient=HORIZONTAL)
green_offset_slider.place(x=150 , y=415)



root.mainloop()


