# ''''
# Real Time Face Recogition
# 	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
# 	==> LBPH computed model (trained faces) should be on trainer/ dir
# Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

# Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

# '''

# import cv2
# import numpy as np
# import os 

# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read('trainer/trainer.yml')
# cascadePath = "haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascadePath)

# font = cv2.FONT_HERSHEY_SIMPLEX

# #iniciate id counter
# id = 0

# # names related to ids: example ==> Marcelo: id=1,  etc
# names = ['None','Nhat','iu ThanhTam','nhat dz']

# # Initialize and start realtime video capture
# cam = cv2.VideoCapture(0)  
# cam.set(3, 640) # set video widht
# cam.set(4, 480) # set video height

# # Define min window size to be recognized as a face
# minW = 0.1*cam.get(3)
# minH = 0.1*cam.get(4)

# while True:

#     ret, img =cam.read()
#     # img = cv2.flip(img, -1) # Flip vertically

#     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#     faces = faceCascade.detectMultiScale( 
#         gray,
#         scaleFactor = 1.2,
#         minNeighbors = 5,
#         minSize = (int(minW), int(minH)),
#        )

#     for(x,y,w,h) in faces:

#         cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

#         id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
       
#         # Check if confidence is less them 100 ==> "0" is perfect match 
#         if (confidence < 100):
#             id = names[id]
#             confidence = "  {0}%".format(round(100 - confidence))
            
#         else:
#             id = "unknown"
#             confidence = "  {0}%".format(round(100 - confidence))
        
#         cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
#         cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
#     cv2.imshow('camera',img) 

#     k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
#     if k == 27:
#         break

# # Do a bit of cleanup
# print("\n [INFO] Exiting Program and cleanup stuff")
# cam.release()
# cv2.destroyAllWindows()

''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os 

# khởi tạo và cấu hình các đối tượng và tệp tin cần thiết cho việc nhận diện khuôn mặt trong OpenCV.

recognizer = cv2.face.LBPHFaceRecognizer_create() # Tạo một đối tượng recognizer sử dụng thuật toán nhận diện khuôn mặt LBPHFaceRecognizer của OpenCV.
recognizer.read('trainer/trainer.yml') # Đọc các thông tin về việc huấn luyện từ tệp 'trainer/trainer.yml' và lưu trữ vào biến recognizer. Tệp này chứa thông tin về các khuôn mặt đã được huấn luyện.
cascadePath = "haarcascade_frontalface_default.xml"# Tạo một biến cascadePath để lưu đường dẫn tới tệp haarcascade_frontalface_default.xml. Tệp này chứa các thông tin về các đặc trưng của khuôn mặt, được sử dụng để phát hiện khuôn mặt trong hình ảnh.
faceCascade = cv2.CascadeClassifier(cascadePath) # Tạo một đối tượng faceCascade từ CascadeClassifier của OpenCV, sử dụng tệp haarcascade_frontalface_default.xml để phát hiện khuôn mặt trong hình ảnh.

font = cv2.FONT_HERSHEY_SIMPLEX
# Khai báo kiểu font chữ sử dụng trong việc vẽ các thông tin nhận diện khuôn mặt lên hình ảnh. 
# Trong trường hợp này, sử dụng font chữ SIMPLEX của OpenCV. Kiểu font chữ này là một kiểu font đơn giản và dễ đọc,
# thường được sử dụng trong các ứng dụng đơn giản nhưng hiệu quả. Bằng cách sử dụng câu lệnh này, 
# chúng ta có thể dễ dàng sử dụng font chữ SIMPLEX để hiển thị các thông tin nhận diện khuôn mặt trên hình ảnh.

#khởi tạo giá trị ban đầu của biến id
id = 0

# tên của người nhận diện, tính từ 1
names = ['None','Nhat','Nam','Quang','Trung']

#  khởi tạo đối tượng VideoCapture của OpenCV với camera mặc định
cam = cv2.VideoCapture(0)  
cam.set(3, 640) # cài đặt chiều cao
cam.set(4, 480) # cài đặt chiều dài

# Định nghĩa kích thước cửa sổ tối thiểu được nhận diện là một khuôn mặt
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    # đọc dữ liệu khung hình từ camera được kết nối trước đó
    # Trong đó, cam là đối tượng VideoCapture đã được khởi tạo trước đó để kết nối với camera, ret là biến lưu trạng thái trả về của việc đọc khung hình từ camera (True nếu thành công và False nếu không thành công), img là một mảng NumPy lưu trữ khung hình đọc được từ camera.
# Sau khi thực hiện câu lệnh này, biến ret sẽ lưu trạng thái đọc khung hình từ camera, và biến img sẽ chứa khung hình đó để sử dụng cho các thao tác xử lý tiếp theo.
    ret, img =cam.read()
    # img = cv2.flip(img, -1) # Lật ảnh


    # chuyển đổi một hình ảnh từ không gian màu BGR (Blue-Green-Red) sang không gian màu xám (grayscale).
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # sử dụng thuật toán phát hiện khuôn mặt để tìm kiếm các khuôn mặt trong hình ảnh xám 
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        # vẽ một hình chữ nhật xung quanh khuôn mặt
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        # nhận diện khuôn mặt đó và trả về id và mức độ tin cậy (confidence) của khuôn mặt đó
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
       
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        #  tìm kiếm tên tương ứng với id trong danh sách tên và hiển thị tên và mức độ tin cậy trên khuôn mặt 
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    # hiển thị khung hình hiện tại được chụp bởi máy ảnh
    cv2.imshow('camera',img) 
    # biến k được gán bằng giá trị trả về của hàm cv2.waitKey(10) & 0xff. Hàm này đọc phím nhập từ bàn phím và chờ cho đến khi phím được nhấn. Nếu phím nhấn là ESC (mã ASCII là 27), vòng lặp sẽ bị thoát, chương trình dừng lại
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# giải phóng tài nguyên và đóng tất cả các cửa sổ đang mở trong chương trình
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
