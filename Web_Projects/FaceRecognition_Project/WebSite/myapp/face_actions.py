import numpy as np
import face_recognition as fr
import cv2
from datetime import datetime, timedelta
from core.settings import BASE_DIR
import os

def face_recognizer(image_url,username):
    image_url = image_url[1:]
    current_time = datetime.now()
    stop_time = current_time + timedelta(0,5)

    video_capture = cv2.VideoCapture(0)
    user_image = fr.load_image_file(image_url)
    user_face_encoding = fr.face_encodings(user_image)[0]
    known_face_encondings = [user_face_encoding]
    known_face_names = [username]

    while True: 
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encondings, face_encoding)
            name = "Unknown"
            face_distances = fr.face_distance(known_face_encondings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                return True
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Webcam_facerecognition', frame)

        if datetime.now()>=stop_time:
            print(datetime.now())
            video_capture.release()
            cv2.destroyAllWindows()
            return False

def take_photo(img_name):
    current_time = datetime.now()
    stop_time = current_time + timedelta(0,3)
    video_capture = cv2.VideoCapture(0)
    path = os.path.join(BASE_DIR, 'media\head_images')
    print("Path inside take_photo", path)
    print("Inside of take_photo: ", img_name)
    while True: 
        ret, frame = video_capture.read()
        cv2.waitKey(1)
        cv2.imshow('Webcam_facerecognition', frame)
        if datetime.now()>=stop_time:
            os.path.join(path , 'waka.jpg')
            img_name += ".png"
            cv2.imwrite(os.path.join(path , img_name),frame)
            break
    video_capture.release()
    cv2.destroyAllWindows()
    print("Inside of take photo, final url:", img_name)
    img_name = "head_images/" + img_name
    return img_name