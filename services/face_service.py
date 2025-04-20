# attendance_system/services/face_service.py
import os
import face_recognition
import cv2
from pathlib import Path
from models.database import get_student

class FaceService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_roll_numbers = []
        self.known_names = []
        self._load_known_faces()
    
    def _load_known_faces(self):
        """Load all registered faces from the faces directory"""
        faces_dir = Path(__file__).parent.parent / "faces"
        faces_dir.mkdir(exist_ok=True)
        
        for student_dir in faces_dir.iterdir():
            if student_dir.is_dir():
                roll_number = student_dir.name.split('_')[0]
                student_info = get_student(roll_number)
                
                if student_info:
                    first_name = student_info[1]
                    last_name = student_info[2]
                    full_name = f"{first_name} {last_name}"
                    
                    for image_file in student_dir.glob("*.jpg"):
                        image = face_recognition.load_image_file(image_file)
                        encodings = face_recognition.face_encodings(image)
                        
                        if encodings:
                            self.known_face_encodings.append(encodings[0])
                            self.known_roll_numbers.append(roll_number)
                            self.known_names.append(full_name)

    def recognize_faces(self, frame):
        """Recognize faces in a frame and return roll numbers"""
        rgb_frame = frame[:, :, ::-1]  # BGR to RGB
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        recognized_roll_numbers = []
        recognized_names = []
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding,
                tolerance=0.6
            )
            
            roll_number = "Unknown"
            name = "Unknown"
            
            if True in matches:
                match_index = matches.index(True)
                roll_number = self.known_roll_numbers[match_index]
                name = self.known_names[match_index]
            
            recognized_roll_numbers.append(roll_number)
            recognized_names.append(name)
            
        return face_locations, recognized_roll_numbers, recognized_names