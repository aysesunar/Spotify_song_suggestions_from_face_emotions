##################
# With much help from https://github.com/bnsreenu/python_for_microscopists/blob/master/241_live_age_gender_emotion_detection/241_live_age_gender_emotion_detection_V2.0.py
###################

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
import cv2
import numpy as np
import os

class emotion_detector_from_image:

    def detect_emotion(self):
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        emotion_model = load_model(f'{os.getcwd()}\\face_emotion_detection\\saved_models\\emotion_detection_model_100epochs.h5')
        print("CURRENT WORKING DIR:")
        print(f'{os.getcwd()}\\face_emotion_detection\\saved_models\\emotion_detection_model_100epochs.h5')

        class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

        emotion_mapper = {"Angry": 'angry', "Disgust": "angry", "Fear": "sad", "Happy": "happy", "Neutral": "relaxed", "Sad": "sad", "Surprise":"happy"}

        faces, frame,cap = self.get_image(face_classifier)

        emotion = "relaxed"
        while len(faces) < 1:
            faces, frame, cap = self.get_image(face_classifier)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            # Get image ready for prediction
            roi = roi_gray.astype('float') / 255.0  # Scale
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)  # Expand dims to get it ready for prediction (1, 48, 48, 1)

            preds = emotion_model.predict(roi)[0]  # Yields one hot encoded result for 7 classes
            label = class_labels[preds.argmax()]  # Find the label
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
            emotion = emotion_mapper[label]
            print(f'predicted {emotion}')

        cv2.imshow('Emotion Detector', frame)
        cv2.waitKey(0)

        cap.release()
        cv2.destroyAllWindows()

        return emotion, frame

    def get_image(self, face_classifier):
        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        return faces, frame, cap