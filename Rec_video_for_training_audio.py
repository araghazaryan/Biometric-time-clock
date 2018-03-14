""" SAMPLE RECORDER for FACE RECOGNITION
code to record sample video for face recognition database 
the recording lasts 33 seconds and directions are shown and pronounced during recording

Created on Thu Mar  8 00:15:35 2018
@author: ghaza
"""

import cv2
import time 
import os
import numpy as np     
import pyaudio
import wave

waittime = 8 #the duration of preparation time
numberofframes = 150 # number of frames to parse

person = "ara"
print('Please input the name of the person')
person = input().lower()
if len (person) == 0 :
    exit ()

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
        cancel = {'c','n','cancel'}
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
            flag = 0
            exit()
        else:
           print("Please respond with 'O'-Overwite,'R'-Rename or 'C'-Cancel")


# audio module: loads audio and plays piece by piece
chunk = 1024
wf = wave.open('voice_commands.wav', 'rb')
p = pyaudio.PyAudio()
stream = p.open(
    format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True)
data = wf.readframes(chunk)

cap = cv2.VideoCapture(0) # turn on the camera
#fourcc = cv2.VideoWriter_fourcc(*'MP4V') # fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object
out = cv2.VideoWriter(pathforvideos + '\\' + name,fourcc, 20.0, (640,480))
# instrucitons for recording. Be aware that they are adjusted to audio commands
# The command that will be displayed, the duration, flag = recording during or not
OrderOptions = ['PlEASE PREPARE!!', 5,0, # 5
                'The recording will start in %d seconds', 5,0, # 3.9
           'Look STREIGHT for %d seconds', 4,1, # 1.9
           'Look RIGHT for %d seconds',4,1, #2.7
           'Look LEFT for %d seconds',4,1, #2.3
           'Look UP for %d seconds',4,1, # 2.6
           'Look DOWN for %d seconds', 4,1, # 1.9
           'TILT LEFT for %d seconds',4,1, # 3.5
           'TILT RIGHT for %d seconds',4,1, # 2.6
           'SMILE :)', 4, 1, #3.1
           'GRIN :(', 4, 1, #1.9
           'Please say \"I am in love with you\" x2', 8,1,#3.8
           'We are done, thank you!', 5, 0] #3

# duration of each of audio command
AudPhraseDur = [5,
                3.8,
                2,
                2.7,
                2.3,
                2.5,
                1.8,
                3.6,
                2.7,
                3,
                2,
                3.6,
                3.2]

numem = int(len(OrderOptions)/3)

for i in range(numem): # cycle through all comands
    tunit = OrderOptions[i*3+1]
    flag=cap.isOpened()
    ret, frame = cap.read()
    if ret==True:
        tic = time.time()
        toc = tic
        tm = 0
        while tm<tunit:
            text =  OrderOptions[i*3]   
            if toc-tic<AudPhraseDur[i]:
                stream.write(data)
                data = wf.readframes(chunk)
            if '%' in text:
                text=text % (tunit-tm)
            if OrderOptions[i*3+2]: 
                # recording routine 
                cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(180,50,0))
                out.write(frame) # save the frame
            else: 
                cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
            cv2.imshow('frame',frame)    
            toc = time.time()
            tm = round(toc-tic)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
# Release everything when job is finished
stream.close()
p.terminate()
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
    if os.path.isfile(pathtoframes + '\\' + video1 + '_0.png'):
        flag = 1
        while flag:
            print('Frames with names ' + video1 +'.png exist \nDo you want to Overwrite (O) or Cancel (C) the framing?')
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
                cv2.imwrite(pathtoframes + '\\' + video1 +"_%d.png" % ii, image)
            else:
                pass
            count += 1
            ii += 1
