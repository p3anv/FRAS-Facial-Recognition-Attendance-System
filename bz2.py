import bz2
import shutil

# Download the file first
import urllib.request
url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
urllib.request.urlretrieve(url, "shape_predictor_68_face_landmarks.dat.bz2")

# Decompress it
with bz2.BZ2File("shape_predictor_68_face_landmarks.dat.bz2") as fr:
    with open("shape_predictor_68_face_landmarks.dat", "wb") as fw:
        shutil.copyfileobj(fr, fw)