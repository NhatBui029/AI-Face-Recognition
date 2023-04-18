''''
Training Multiple Faces stored on a DataBase:
	==> Each face should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model will be saved on trainer/ directory. (if it does not exist, pls create one)
	==> for using PIL, install pillow library with "pip install pillow"

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18   

'''

import cv2 # dùng để xử lý ảnh và video
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'

# có thể được sử dụng để nhận dạng khuôn mặt trong ảnh hoặc video. 
# Nó sử dụng mô hình ma trận Local Binary Patterns (LBP) để trích xuất đặc trưng từ ảnh khuôn mặt 
# và sau đó tạo ra histogram của các giá trị LBP để mã hóa các đặc trưng đó.
recognizer = cv2.face.LBPHFaceRecognizer_create()

# là một phương thức được sử dụng để tạo ra một bộ phân loại cascade (làn sóng) để nhận dạng khuôn mặt.
# với tên tệp là "haarcascade_frontalface_default.xml". Tệp XML này chứa các thông tin về các bộ lọc cascade 
# được huấn luyện để nhận dạng khuôn mặt, bao gồm các kích thước, tọa độ, hình dạng và màu sắc của khuôn mặt.
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # mở một tệp ảnh và chuyển đổi nó sang chế độ ảnh xám (grayscale).
        img_numpy = np.array(PIL_img,'uint8') # đổi một ảnh PIL (Pillow Image) sang một mảng NumPy kiểu dữ liệu 'uint8'
                                              # (uint8 - các giá trị pixel của ảnh được chuyển đổi sang các số nguyên không dấu có giá trị từ 0 đến 255)

        id = int(os.path.split(imagePath)[-1].split(".")[1]) # lấy ra mã của người nào đó
        
        faces = detector.detectMultiScale(img_numpy) # phát hiện các khuôn mặt trong ảnh img_numpy 
                                                     # Kết quả trả về là danh sách các hình chữ nhật (bounding boxes) chứa các khuôn mặt được phát hiện trong ảnh, 
                                                     # trong đó mỗi hình chữ nhật được biểu diễn bởi một tuple (x, y, w, h), 

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w]) # cắt ra từng khuôn mặt 
            ids.append(id)                             # thêm id của ng dùng tương ứng vs khuôn mặt

    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids)) # Phương thức train được sử dụng để huấn luyện mô hình máy học để nhận diện khuôn mặt

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # được sử dụng để ghi mô hình máy học đã được huấn luyện vào một tập tin YAML.

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
