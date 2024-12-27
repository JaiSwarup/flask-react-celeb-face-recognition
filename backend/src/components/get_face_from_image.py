from mtcnn import MTCNN
from PIL import Image
import numpy as np

detector = MTCNN()
def get_face_from_image(image):
    faces = detector.detect_faces(np.array(image))
    if len(faces) == 0:
        return None
    face = faces[0]
    x, y, width, height = face['box']
    cropped_face = image.crop((x, y, x + width, y + height))
    return cropped_face

if __name__ == '__main__':
    image_path = r'src\test\ranbir_duplicate.png'
    face = get_face_from_image(image_path)
    face.show()