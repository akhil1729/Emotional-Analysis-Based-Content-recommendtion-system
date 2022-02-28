#import all the packages
import PySimpleGUI as sg
from os import startfile
from deepface import DeepFace
import cv2 as cv
import matplotlib.pyplot as plt

#Gui for choosing a file
sg.theme('DarkAmber')
fname = sg.popup_get_file('Select a video file')
startfile(fname)

#Deepface Emotional Analysis
cap=cv.VideoCapture(0)
result_new=[]

while(True):
    _, img =cap.read()
    result_new.append(DeepFace.analyze(img,actions=['emotion']))
    cv.imshow('img',img)
    if(cv.waitKey(1) & 0xFF==ord('q')):
        break

cap.release()

#determining captured emotions
emotion_set=[i['dominant_emotion'] for i in result_new]
dominant_emotions=dict()
fear=0
neutral=0
sad=0
happy=0
angry=0
surprise=0

#existing emotions list
emotion_li=['fear','neutral','sad','happy','angry','surprise']

#finding out emotion occurences
for i in emotion_li:
    dominant_emotions[i]=0
for i in emotion_set:
    if(i in dominant_emotions):
        dominant_emotions[i]+=1

#Matplotlib to plot emotions
fig=plt.figure()
ax = fig.add_axes([0,0,1,1])
x=emotion_li
y=[dominant_emotions[i] for i in dominant_emotions]
ax.bar(x,y,color='r')
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+0.4, \
            str(round((i.get_height()), 2)), fontsize=11, color='black',
                rotation=0)

#emotion values based on arousal and valence of emotions
emotion_matrix={'fear': -5, 'neutral': 0, 'sad': -3, 'happy': 5, 'angry': -4, 'surprise': 2}

#finding out emotion's cummulative value
arr=[]
for j in dominant_emotions:
    arr.append(dominant_emotions[j]*emotion_matrix[j])
value=sum(arr)

#if emotion is positive
if(value>10):
    layout = [  [sg.Text("Yay! This film can be recommended! \U0001f600",auto_size_text=True,size=(35, 1), font=("Calibri", 24), text_color='green')],
              [sg.Text("This would make a great watch!",auto_size_text=True,size=(35, 1), font=("Calibri", 18), text_color='cyan')]]
    sg.theme('DarkAmber')
    window=sg.Window("Recommendations",layout)
    event, values = window.read()
    window.close()

#if emotion is negative
else:
    layout = [  [sg.Text("Nay! This can't be recommended! \U0001F614",auto_size_text=True,size=(35, 1), font=("Calibri", 24), text_color='red')],
             [sg.Text("We would suggest few trims!",auto_size_text=True,size=(35, 1), font=("Calibri", 18), text_color='yellow')]]
    sg.theme('DarkAmber')
    window=sg.Window("Recommendations",layout)
    event, values = window.read()
    window.close()

