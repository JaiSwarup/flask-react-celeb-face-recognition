import numpy as np
from keras_vggface.utils import preprocess_input

def get_embedding_from_face(face, model):
    face = face.resize((224, 224))
    face_array = np.asarray(face)
    face_array = face_array.astype('float32')

    expanded_array = np.expand_dims(face_array, axis=0)
    preprocessed_img = preprocess_input(expanded_array)

    result = model.predict(preprocessed_img).flatten()
    return result.tolist()
