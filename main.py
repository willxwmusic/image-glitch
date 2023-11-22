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

def colourbend(redOffset,greenOffset,blueOffset,alphaOffset,randomiseOffset,randomnessAmount):

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
    colourbend(red_offset_slider.get(),green_offset_slider.get(),blue_offset_slider.get(),alpha_offset_slider.get(),alt_colour_bend,randomness_offset_slider.get())
    applied_notification = Label(root, text="Processing Applied!")
    applied_notification.place(x=150, y=500)

def save_image():
    save_directory = filedialog.asksaveasfilename(initialdir="file_path", title="Hola", filetypes=(("TIFF","*.tiff"),("All files","*.*")))
    tiff.imwrite(save_directory, data, photometric='rgb')
    
def add_button(button_text,button_command,button_x,button_y):
    new_button = Button(root, text =button_text, command = button_command)
    new_button.place(x=button_x,y=button_y)

def add_slider(slider_text, slider_min, slider_max, slider_x, slider_y):
    new_slider_label = Label(root, text=slider_text)
    new_slider_label.place(x=slider_x,y=slider_y)
    new_slider = ttk.Scale(root, from_=slider_min, to=slider_max, orient=HORIZONTAL)
    new_slider.place(x=(slider_x+150), y=slider_y)
    return new_slider

root = Tk()
root['background']='#222222'
root.minsize(width="400", height="600")

open_button = add_button("Open",open_image,0,0)
apply_button = add_button("Apply",open_image,100,0)
save_button = add_button("Save",open_image,200,0)

do_pixel_shift = IntVar
pixel_shift_checkbox = Checkbutton(root, text='Pixel Shifting',variable=do_pixel_shift, onvalue=True, offvalue=False)

do_colour_bend = IntVar
colour_bend_checkbox = Checkbutton(root, text='Colour Bending',variable=do_colour_bend, onvalue=True, offvalue=False)

alt_colour_bend = IntVar
alt_colour_bend_checkbox = Checkbutton(root, text='Alt. Colour Bending',variable=alt_colour_bend, onvalue=True, offvalue=False)

colour_bend_checkbox.place(x=0,y=50)
alt_colour_bend_checkbox.place(x=0,y=75)

red_offset_slider = add_slider('Red Offset',0,255,10,100)

green_offset_slider = add_slider('Green Offset',0,255,10,150)

blue_offset_slider = add_slider('Blue Offset',0,255,10,200)

alpha_offset_slider = add_slider('Alpha Offset',0,1,10,250)

radnomness_offset_slider = add_slider('Randomness Offset',0,1,10,300)

pixel_shift_checkbox.place(x=0,y=375)

root.mainloop()


