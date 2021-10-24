
import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import pyttsx3
from werkzeug.utils import redirect



engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio) 
    engine.runAndWait() 



path = 'AttendanceImg'
images = []     
className = []    
myList = os.listdir(path)
#print("Total Classes Detected:",len(myList))
for x,cl in enumerate(myList):
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        className.append(os.path.splitext(cl)[0])

speak("Enter the number of Students: ")
n_rows= int(input("Number of Students:"))
n_cols = 2

matrix = [ ]
print("Enter the Student name and his roll number in subsequent lines one by one for each student:")
speak("Enter the Student name and his roll number in subsequent lines one by one for each student")

for i in range(n_rows):
    a =[ ]

    for j in range(n_cols):      
         a.append((input()))
    matrix.append(a)

def rollnumber(name):
    i=0
    while i<=n_rows:
        if matrix[i][0]==name:
            return matrix[i][1]
        i=i+1    
    return -1

speak("Enter the time of your class")
hour=int(input("Enter the time of your class:"))
minute=int(input())

def late(hour,minute):
    now = datetime.now()
    today = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if today>now:
        return "on time"
    else: return "late"    

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList =[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in  line:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dt_string},{rollnumber(name)},{late(hour,minute)}')
            speak(name)
            speak('Your attendance is marked Your Roll number is ')
            speak(rollnumber(name))
            speak('You are ')
            speak(late(hour,minute))

        #print(myDataList)    


encodeListKnown = findEncodings(images)
#print('Encodings Complete')

cap = cv2.VideoCapture(0)





while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        
        

        if faceDis[matchIndex]< 0.50:
            name = className[matchIndex].upper()
            #print(name)
            markAttendance(name)
        else: 
            name = 'Unknown'
            #markAttendance(name)
            speak('I do not recognize you This database does not have your record.')

        
        y1,x2,y2,x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)            






    

                

        
        

