import cv2
import os.path

faceCascadeDB = cv2.CascadeClassifier("Data/haarcascade_frontalface_default.xml")
# capture frames from a camera with device index=0
cap = cv2.VideoCapture(0)
counterPhoto = 0
counterVideo = 0
avi = cv2.VideoWriter_fourcc('M','J','P','G')
# mp4 = cv2.VideoWriter_fourcc(* 'XVID')
# Получить информацию о размере кадра
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = 10
_isRecording = False

while True:
    counterPhoto += 1
    if not os.path.exists(f"Images/image_{counterPhoto}.png"):
        break
while True:
    counterVideo += 1
    pathToVideo = f"Videos/video_{counterVideo}.avi"
    if not os.path.exists(pathToVideo):
        break
# loop runs if capturing has been initialized
while True:
    # reads frame from a camera
    ret, frame = cap.read()
    success, frameCopy = cap.read()
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
        if cv2.imwrite(f"Images/image_{counterPhoto}.png", frameCopy):
            counterPhoto += 1
    elif pressKey & 0xFF == ord('c'):
        if not _isRecording:
            pathToVideo = f"Videos/video_{counterVideo}.avi"
            outputVideo = cv2.VideoWriter(pathToVideo, avi, fps, frame_size)
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
