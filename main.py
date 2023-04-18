from tkinter import *
import subprocess
import cv2
import numpy as np

tk = Tk()
tk.title('Btl AI')
tk.geometry('600x500')


fr =  open('file.txt','r') 

names = ['']*100
names.insert(0,'None')

for line in fr:
    id,name = line.rstrip().split('/')
    names.insert(int(id),name)

def actionButAdd(id,name):
    fw =  open('file.txt','a') 
    fw.write(id+'/'+name+'\n') 
    fw.close()
    for line in fr:
        id,name = line.rstrip().split('/')
        names.insert(int(id),name)

    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # For each person, enter one numeric face id
    face_id = id

    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    while(True):

        ret, img = cam.read()
        img = cv2.flip(img, 1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30: # Take 30 face sample and stop video
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    Label(tk,text='Đã thêm thành công User '+ id,font=('Times New Roman',15),fg='blue').place(x=30,y=190)
    entryId.delete(0,'end')
    entryName.delete(0,'end')
    subprocess.run(['python', '02_face_training.py'])

def actionButDetect():  
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    user = ' '


    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)  
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:

        ret, img =cam.read()
        img = cv2.flip(img, 1)
        # img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
           
        
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                user = id
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    Label(tk,text='Welcome User '+ user,font=('Times New Roman',13),fg='red').place(x=300,y=70)



labelAdd = Label(tk,text='Thêm khuôn mặt',font=('Times New Roman',18)).place(x=30,y=30)

labelId = Label(tk,text='Nhập Id: ',font=('Times New Roman',13)).place(x=30,y=70)
entryId = Entry(tk,width=10,font=('Times New Roman',13))
entryId.place(x=100,y=70)

labelName = Label(tk,text='Nhập tên: ',font=('Times New Roman',13)).place(x=30,y=110)
entryName = Entry(tk,width=10,font=('Times New Roman',13))
entryName.place(x=100,y=110)

butAdd = Button(tk,text='Them',font=('Times New Roman',13),command=lambda: actionButAdd(entryId.get(),entryName.get()))
butAdd.place(x=30,y=150)


labelDetect = Label(tk,text='Nhận diện khuôn mặt',font=('Times New Roman',18)).place(x=300,y=30)
butDetect = Button(tk,text='Nhận diện',font=('Times New Roman',13),command=lambda: actionButDetect())
butDetect.place(x=300,y=110)


tk.mainloop()