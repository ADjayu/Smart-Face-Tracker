import cv2
import serial,time
import datetime
import pyttsx3

engine= pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning Sir !")
  
    elif hour>= 12 and hour<18:
        speak("Good Afternoon Sir !")  
  
    else:
        speak("Good Evening Sir !") 
  
    face_tracker_name =("nina")
    speak("I am your smart face tracker")
    speak(face_tracker_name)


face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
fourcc= cv2.VideoWriter_fourcc(*'XVID')
# ArduinoSerial=serial.Serial('COM4',9600,timeout=0.1)
out= cv2.VideoWriter('face detection4.avi',fourcc,20.0,(640,480))

time.sleep(1)

wishMe()
while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1)  #mirror the image
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,5)  #detect the face
    for x,y,w,h in faces:
        #sending coordinates to Arduino
        string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
        print(string)
        # ArduinoSerial.write(string.encode('utf-8'))
        
        #plot the roi
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    
     
    out.write(frame)
    cv2.imshow('img',frame)
    cv2.imwrite('output_img.jpg',frame)
    '''for testing purpose
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    time.sleep(0.05)
    print('data from arduino:'+read)
    '''
    # press q to Quit
    if cv2.waitKey(10)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

