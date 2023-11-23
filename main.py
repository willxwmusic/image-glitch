import tifffile as tiff
import imageio.v3 as iio

import random
import numpy
import shutil

from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image

def clampSize(n, bound): 
    if n < 0: 
        return 0
    elif n > bound: 
        return bound
    else: 
        return n 

def colourbend(data,redOffset,greenOffset,blueOffset,altColourBend,randomnessAmount):
    if altColourBend == 1:
        print("alt method done")

        for x in range(0, imgwidth):

            redRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            greenRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            blueRandomness = random.uniform(-randomnessAmount,randomnessAmount)

            for y in range(0, imgheight):

                data[y][x][0] -= redOffset * redRandomness
                data[y][x][1] -= greenOffset * greenRandomness
                data[y][x][2] -= blueOffset * blueRandomness
    else:
        print("old method done")

        for x in range(0, imgwidth):

            for y in range(0, imgheight):

                redRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1
                greenRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1
                blueRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1

                data[y][x][0] -= redOffset * redRandomness
                data[y][x][1] -= greenOffset * greenRandomness
                data[y][x][2] -= blueOffset * blueRandomness

def pixelShift(frequency_exponent,horizontalOffset):
    frequency = 2^round(frequency_exponent)
    for i in range(0,(frequency)):
        print(horizontalOffset/2)
        print(horizontalOffset)
        offset = random.randint(round(horizontalOffset/2),horizontalOffset)
        for y in range(int(i*imgheight/frequency),int((i+1)*imgheight/frequency)):
            for x in range(0,imgwidth):
                if x-offset > 0:
                    data[y][x] = original[y][x-offset]
                else:
                    data[y][x] = original[y][(imgwidth-1) + (x-offset)]

def open_image():
    global file_path
    file_path = filedialog.askopenfilename(initialdir="file_path", title="Hola", filetypes=(("All files","*.*"),("png","*.png")))
    print(file_path)

    global original 
    if file_path.endswith(".png"):
        original = iio.imread(file_path)
    else:
        original = tiff.imread(file_path)

    global image
    image = PhotoImage(file=file_path)
    global imgwidth
    imgwidth = original.shape[1]
    global imgheight
    imgheight = original.shape[0]

def apply_processing():
    if file_path.endswith(".png"):
        data = iio.imread(file_path)
    else:
        data = tiff.imread(file_path)
    print(data[100][100][2])
    if do_pixel_shift.get() == 1:
        pixelShift(pixel_shift_slider.get(),round(imgwidth/2))
    if do_colour_bend.get() == 1:
        colourbend(data,red_offset_slider.get(),green_offset_slider.get(),blue_offset_slider.get(),alt_colour_bend.get(),randomness_offset_slider.get())
    if file_path.endswith(".png"):
        iio.imwrite("./temp.png", data, photometric='rgb')
        edited_image=PhotoImage(file="./temp.png").subsample(subasmple_ratio)
        edited_image_display.config(image=edited_image)
        edited_image_display.image = edited_image

    print(data[100][100][2])

def save_image():
    save_directory = filedialog.asksaveasfilename(initialdir="file_path", title="Hola", filetypes=(("PNG","*.png"),("TIFF","*.tiff"),("All files","*.*")))
    shutil.copyfile("./temp.png",save_directory)
    
def add_button(button_text,button_command,button_row,button_column):
    Button(tool_bar,text=button_text,command=button_command).grid(row=button_row,column=button_column,padx=5,pady=5)

def add_slider(slider_window, slider_text, slider_min, slider_max, slider_row, slider_column):
    new_slider_label = Label(slider_window, text=slider_text)
    new_slider_label.grid(row=slider_row,column=slider_column)
    new_slider = ttk.Scale(slider_window, from_=slider_min, to=slider_max, orient=HORIZONTAL)
    new_slider.grid(row=(slider_row+1),column=slider_column)
    return new_slider

root = Tk()
root.title("imagekenesis")
root.geometry("1920x500")
root.config(bg="#222222")

left_frame = Frame(root, width=400, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)
middle_frame = Frame(root, width=650, height=400, bg='grey')
middle_frame.grid(row=0, column=1, padx=10, pady=5)
right_frame = Frame(root, width=400, height=400, bg='grey')
right_frame.grid(row=0, column=2, padx=10, pady=5)

# Create frames and labels in left_frame
Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

open_image()

# load image to be "edited"

average_image_size = (imgheight+imgwidth) / 2
subasmple_ratio = round(average_image_size / 400)
original_image = image.subsample(subasmple_ratio * 2)
edited_image = image.subsample(subasmple_ratio)

original_image_display = Label(left_frame, image=original_image)
original_image_display.grid(row=1, column=0, padx=5, pady=5)
edited_image_display = Label(middle_frame, image=edited_image)
edited_image_display.grid(row=0,column=0, padx=5, pady=5)

# Create tool bar frame
tool_bar = Frame(left_frame, width=180, height=185)
tool_bar.grid(row=2, column=0, padx=5, pady=5)
filter_bar = Frame(right_frame, width=180, height=185)
filter_bar.grid(row=2, column=0, padx=5, pady=5)

# File menu
Label(tool_bar, text="File", relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
open_button = add_button("Open",open_image,1,0)
apply_button = add_button("Apply",apply_processing,2,0)
save_button = add_button("Save",save_image,3,0)

#Tools menu
Label(tool_bar, text="Tools", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

#Filters menu
Label(filter_bar, text="Colour", relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
do_colour_bend = IntVar()
colour_bend_checkbox = Checkbutton(filter_bar, text='Colour Bending',variable=do_colour_bend, onvalue=True, offvalue=False)
colour_bend_checkbox.grid(row=1,column=0)
alt_colour_bend = IntVar()
alt_colour_bend_checkbox = Checkbutton(filter_bar, text='Alt. Colour Bending',variable=alt_colour_bend, onvalue=True, offvalue=False)
alt_colour_bend_checkbox.grid(row=2,column=0)
red_offset_slider = add_slider(filter_bar,'Red Offset',0,255,3,0)
green_offset_slider = add_slider(filter_bar,'Green Offset',0,255,5,0)
blue_offset_slider = add_slider(filter_bar,'Blue Offset',0,255,7,0)
randomness_offset_slider = add_slider(filter_bar,'Randomness Offset',0,1,9,0)
alpha_offset_slider = add_slider(filter_bar,'Alpha Offset',0,1,11,0)

#Shifting Menu
Label(filter_bar, text="Shifting", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)
do_pixel_shift = IntVar()
pixel_shift_checkbox = Checkbutton(filter_bar, text='Pixel Shifting',variable=do_pixel_shift, onvalue=True, offvalue=False)
pixel_shift_checkbox.grid(row=1,column=1)
pixel_shift_slider = add_slider(filter_bar,'Shift Offset',0,1,2,1)

# File Menu
root.mainloop()