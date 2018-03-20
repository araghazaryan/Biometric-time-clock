# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 10:53:32 2018

@author: ghaza
"""
"""  A supplement code to dissect any video to frames

Works in two modes 
with uniqueFlag = 0 it dissects certain number of frames
with uniqueFlag = 1 it dissects the frames that are unique, omitting similar frames

Created on Thu Mar  20 00:15:35 2018
@author: Ara Ghazaryan
"""

#pathforvideos = 'C:\\Users\\ghaza\\Desktop\\SCYLLA'
import os
import tkinter as tk
import numpy as np
import cv2
from tkinter import filedialog
from tkinter import messagebox


uniqueFlag = 1 # set this to 0 to cut unto unique frames 
               # or to 1 to cut into certain number of frames
differencelevel = 60 # the level of difference threshold

my_filetypes = [('Video files', "*.avi;*.mp4"),('all files', '.*')]
# query the video file to be cut into frames 

data_dir = os.getcwd()
#data_dir = "D:\\Videos\\"

root = tk.Tk()
root.withdraw()
root.focus_force()

video_capture_path = filedialog.askopenfilename(parent = root, initialdir=data_dir, filetypes=my_filetypes)
if video_capture_path=='':
    root.destroy()
    exit()        
   
pathforvideos = os.path.dirname(video_capture_path)
pathtoframes = pathforvideos + '\\Frames'
if not os.path.exists(pathtoframes):
    os.makedirs(pathtoframes)
video_name = os.path.splitext(os.path.basename(video_capture_path))[0]
video_capture = cv2.VideoCapture(video_capture_path)
length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

if not (length>0):
    quit()
    
print('Total number of frames: ' + str(length))
uniqueFlag = messagebox.askyesno("Dissection mode","Do you want to dissect the video into unique frames?")

ii=0
count = 0
reportFlag = 0
ret = 1
#errorarray=[0]
    
if uniqueFlag:
    # Save unique frames 
    flag_start = 1
    while ret: 
        ret, image = video_capture.read()
        if flag_start:
            imageold=image
            flag_start =0
            cv2.imwrite(pathtoframes + '\\' + video_name +"_%d.png" % ii, image)
        else:
            if ret:
                err = np.sum((image.astype("float") - imageold.astype("float")) ** 2)
                err /= float(image.shape[0] * imageold.shape[1])
                #errorarray.append(err)
                # print (str(count)+' out of ' + str(ii))
                if err>differencelevel:                
                    cv2.imwrite(pathtoframes + '\\' + video_name +"_%d.png" % ii, image)
                    count += 1
                ii += 1
                imageold = image
                percent = int(100*ii/length)
                if np.mod(percent, 10)>0:
                    reportFlag = 1
                if reportFlag and np.mod(percent, 10)==0: 
                    print ('done: ' + str(percent) +'%')
                    reportFlag = 0
else:                    
    # Save certain number of frames 
    # Prompt the number of frames desired
    master = tk.Tk()
    def close_window(): 
        master.destroy()
    master.title("Number of frames")
    tk.Label(master, text="Enter the number of desired frames (1-%s)\n (Or leave empty to get all frames)." % length).grid(row=0)
    e1 = tk.Entry(master)
    e1.insert(5,0)
    e1.grid(row=0, column=1)
    numberofframes = e1.get()
    tk.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky='w', pady=4)
    tk.Button(master, text='Enter', command=master.quit).grid(row=3, column=2, sticky='w', pady=4)
    tk.mainloop()
    numberofframes = str(e1.get())
    master.destroy()
    if numberofframes.isdigit():
        numberofframes=int(numberofframes)
    else:
        numberofframes=1    
    if length< numberofframes: # calculate how many frames to skip
        frameNum = length
        framestoskip = 1
    else:
        framestoskip = round(length/numberofframes)    
    while ret:       # saving the frames     
        ret, image = video_capture.read()
        if np.mod(count, framestoskip) == 0:
            cv2.imwrite(pathtoframes + '\\' + video_name +"_%d.png" % ii, image)
        else:
            pass
        count += 1
        ii += 1
        percent = int(100*ii/length)
        if np.mod(percent, 10)>0:
            reportFlag = 1
        if reportFlag and np.mod(percent, 10)==0: 
            print ('done: ' + str(percent) +'%')
            reportFlag = 0

print ('Done!')
    



