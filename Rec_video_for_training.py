""" SAMPLE RECORDER for FACE RECOGNITION
code to record sample video for face recognition database 
the recording lasts 33 seconds and directions are shown during recording

Created on Thu Mar  8 00:15:35 2018
@author: ghaza
"""

import cv2
import time 
import winsound
import os
import numpy as np        

person = "ara"
waittime = 8 #the duration of preparation time
numberofframes = 150 # number of frames to parse

name = person + '.mp4'
currentpath = os.getcwd()
currentpath = os.path.dirname(currentpath) + '\\datasets\\my_dataset_video_to_frames'
pathforvideos = currentpath + '\\videos'
if not os.path.exists(pathforvideos):
        os.makedirs(pathforvideos)
if os.path.isfile(pathforvideos + '\\' + name):
    flag = 1
    while flag:
        print('The video file with defined name exists \nDo you want to Overwrite (O), Rename (R) or Cancel the recording?')
        overwrite = {'overwrite','o', ''}
        rename = {'r','rename'}
        cancel = {'c','cancel'}
        choice = input().lower()
        if choice in overwrite:
            flag = 0
        elif choice in rename:
            i = 0
            while os.path.isfile(pathforvideos + '\\' + name):
                i+=1
                name = person + '_' + str(i) + '.mp4'
            flag = 0
        elif choice in cancel:
            exit()
        else:
           print("Please respond with 'O'-Overwite,'R'-Rename or 'C'-Cancel")
        
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MP4V') # fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object
out = cv2.VideoWriter(pathforvideos + '\\' + name,fourcc, 20.0, (640,480))
# instrucitons for recording
# add or modify according to needs. Each comand stays 1 second on
OrderOptions = ['Please follow the instructions while recording',
           'Please follow the instructions while recording',
           'Look streight',
           'Look streight',
           'Look streight',
           'Look RIGHT for 3 seconds',
           'Look RIGHT for 2 seconds',
           'Look RIGHT for 1 second',
           'Look LEFT for 3 seconds',
           'Look LEFT for 2 seconds',
           'Look LEFT for 1 second',
           'Look UP for 3 seconds',
           'Look UP for 2 seconds',
           'Look UP for 1 seconds',
           'Look DOWN for 3 seconds',
           'Look DOWN for 2 seconds',
           'Look DOWN for 1 seconds',
           'TILT LEFT for 3 seconds',
           'TILT LEFT for 2 seconds',
           'TILT LEFT for 1 seconds',
           'TILT RIGHT for 3 seconds',
           'TILT RIGHT for 2 seconds',
           'TILT RIGHT for 1 seconds',
           'SMILE :)',
           'SMILE :)',
           'SMILE :)',
           'GRIN :(',
           'GRIN :(',
           'GRIN :(',
           'Please say \"Yeelow Fox\"',
           'Please say \"Yeelow Fox\"',
           'Please say \"Yeelow Fox\"',
           'Please say \"Yeelow Fox\"',
]
rectime = len(OrderOptions)
text = OrderOptions[0]
textold = text[0:6]

tic = time.time()
flag = 1;
while flag:
    flag=cap.isOpened()
    ret, frame = cap.read()
    if ret==True:
        toc = time.time()
        tm = round(toc-tic)
        if tm < waittime: # wait and prepare for recording
            text = 'PlEASE PREPARE!!'
            cv2.putText(frame, text,(20, 20),cv2.FONT_HERSHEY_PLAIN,0.7,(0,0,255))
            text = 'the recording will start in '+ str(waittime-tm) +' seconds'
            cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255))
        else: # recording here
            out.write(frame) # save the frame
            text = 'recording time left '+ str(waittime+rectime-tm+1) + ' seconds'
            cv2.putText(frame, text,(20, 20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255))
            index = tm-waittime
            if index>len(OrderOptions)-1:
                index=len(OrderOptions)-1
            text = OrderOptions[index]
            if textold!=text[0:6]: # make a beep sound when instructions change
                winsound.Beep(2500, 250)  # Set Frequency To 2500 Hertz, Set Duration To 1000 ms == 1 second
                textold=text[0:6]
            cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(180,50,0))
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    if tm >waittime+rectime:
        flag = 0
# Release everything when job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

# parsing into frames 
#print ('Do you want to parse the video into frames?')
#flag = 1
#while flag:
#    print('The file with defined name exists \nDo you want to Overwrite the frames? (Yes/No)')
#    Yes = {'yes','ye', 'y', ''}
#    No = {'no','n'}
#    choice = input().lower()
#    if choice in Yes:
#        flag = 0
#    elif choice in No:
#        exit()
#        flag = 0
#    else:
#        print("Please respond with either 'Y'-Yes or 'N'-No")

pathtoframes = currentpath + '\\frames\\' + person
if not os.path.exists(pathtoframes):
    os.makedirs(pathtoframes)

videos = os.listdir(pathforvideos)
videos[0]
for video in videos:
    frameNum = numberofframes
    nextvid = 1
    video1 = os.path.splitext(video)[0]
    # check if frames with name of video exist and prompt for overwriting
    if os.path.isfile(pathtoframes + '\\' + video1 + '_0.jpg'):
        flag = 1
        while flag:
            print('Frames with names ' + video1 +'.jpg exist \nDo you want to Overwrite (O) or Cancel (C) the framing?')
            overwrite = {'overwrite','o', 'y',''}
            cancel = {'can','c','cancel'}
            choice = input().lower()
            if choice in overwrite:
                flag = 0
            elif choice in cancel:
                flag = 0
                nextvid = 0
            else:
               print("Please respond with 'O'-Overwite or 'C'-Cancel")
    if nextvid:
        video_capture = cv2.VideoCapture(pathforvideos +'\\'+ str(video))
        length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if length< frameNum: # calculate how many frames to skip
            frameNum = length
            framestoskip = 1
        else:
            framestoskip = round(length/frameNum)           
        ii=0
        count = 0
        ret = True
        while ret:
            ret, image = video_capture.read()
            if np.mod(count, framestoskip) == 0:
                cv2.imwrite(pathtoframes + '\\' + video1 +"_%d.jpg" % ii, image)
            else:
                pass
            count += 1
            ii += 1
