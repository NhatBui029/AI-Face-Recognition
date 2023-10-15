import cv2
import os
import subprocess
import sys

# a = int(sys.argv[1])
# b = int(sys.argv[2])

# print(a+b)

# sys.stdout.flush()

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = int(sys.argv[1])

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

with open('file.txt', 'a', encoding='utf-8') as fw:
    fw.write(str(face_id)  + '/' + sys.argv[2] + '\n')

fw.close()

cam.release()
cv2.destroyAllWindows()

subprocess.run(['python', '02_face_training.py'])

sys.stdout.reconfigure(encoding='utf-8')
print('\u0110ã thêm thành công Sinh viên :', sys.argv[2])
sys.stdout.flush()
