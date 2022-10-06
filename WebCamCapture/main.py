import cv2, os.path, numpy as np

faceCascadeDB = cv2.CascadeClassifier("Lab_3/data/haarcascade_frontalface_default.xml")
# capture frames from a camera with device index=0
cap = cv2.VideoCapture(1)
counterPhoto = 0
counterVideo = 0
# avi = cv2.VideoWriter_fourcc('M','J','P','G')
mp4 = cv2.VideoWriter_fourcc(* 'XVID')
# Получить информацию о размере кадра
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = 10
_isRecording = False

# hsv_min = np.array((0, 0, 170), np.uint8)
# hsv_max = np.array((360, 40, 210), np.uint8)
hsv_min = np.array((98, 0, 142), np.uint8)
hsv_max = np.array((234, 155, 255), np.uint8)

while True:
    counterPhoto += 1
    if not os.path.exists(f"Lab_3/images/image_{counterPhoto}.png"):
        break
while True:
    counterVideo += 1
    pathToVideo = f"Lab_3/videos/video_{counterVideo}.mp4"
    if not os.path.exists(pathToVideo):
        break
# loop runs if capturing has been initialized
while True:
    # reads frame from a camera
    success, frame = cap.read()
    frameCopy = frame.copy()
    
    # поиск прямоугольных объектов
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # меняем цветовую модель с BGR на HSV
    thresh = cv2.inRange(hsv, hsv_min, hsv_max) # применяем цветовой фильтр
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры в цикле
    for cnt in contours:
        rect = cv2.minAreaRect(cnt) # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect) # поиск четырех вершин прямоугольника
        box = np.int0(box) # округление координат
        area = int(rect[1][0]*rect[1][1]) # вычисление площади
        if area > 8000:
            cv2.drawContours(frame,[box],0,(0,255,0),2)
    
    # поиск лиц 
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascadeDB.detectMultiScale(frameGray, 1.1, 19)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
    cv2.imshow('Camera', frame)
    # Wait for 20ms
    pressKey = cv2.waitKey(1)

    if pressKey & 0xFF == ord('q'):
        break
    elif pressKey & 0xFF == ord('s'):
        if cv2.imwrite(f"Lab_3/images/image_{counterPhoto}.png", frameCopy):
            counterPhoto += 1
    elif pressKey & 0xFF == ord('c'):
        if not _isRecording:
            pathToVideo = f"Lab_3/videos/video_{counterVideo}.mp4"
            outputVideo = cv2.VideoWriter(pathToVideo, mp4, fps, frame_size)
            if success:
                print("Запись пошла!")
                outputVideo.write(frameCopy)
                _isRecording = True
            else:
                print("Ошибка начала записи!")
                outputVideo.release()
                _isRecording = False
        else:
            if success:
                outputVideo.write(frameCopy)
            print("Запись остановлена и сохранена!")
            counterVideo += 1
            _isRecording = False
            outputVideo.release()
    elif _isRecording:
        if success:
            outputVideo.write(frameCopy)

if _isRecording:
    outputVideo.release()
# release the camera from video capture
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()
