import os
import face_recognition
import cv2
from pathlib import Path

FACES_DIR = Path(__file__).parent.parent / "faces"

class FaceService:
    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self._load_known_faces()

    def _load_known_faces(self):
        """Load all registered faces from the faces directory"""
        FACES_DIR.mkdir(exist_ok=True)
        for file in FACES_DIR.glob("*.jpg"):
            name = file.stem
            image = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_faces.append(encodings[0])
                self.known_names.append(name)

    def register_face(self, name: str, image):
        """Register a new face"""
        # Save the image
        face_path = FACES_DIR / f"{name}.jpg"
        cv2.imwrite(str(face_path), image)
        
        # Add to known faces
        encoding = face_recognition.face_encodings(image)[0]
        self.known_faces.append(encoding)
        self.known_names.append(name)
        return True

    def recognize_faces(self, frame):
        """Recognize faces in a frame with error handling"""
        try:
            rgb_frame = frame[:, :, ::-1]  # BGR to RGB
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            recognized_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.6)
                name = "Unknown"
                
                if True in matches:
                    match_index = matches.index(True)
                    name = self.known_names[match_index]
                recognized_names.append(name)
                
            return face_locations, recognized_names
        except Exception as e:
            print(f"Recognition error: {str(e)}")
            return [], []