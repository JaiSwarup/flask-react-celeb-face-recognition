import os
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(1)


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from src.components.get_face_from_image import get_face_from_image
from src.components.get_embedding_from_face import get_embedding_from_face
from PIL import Image
import base64
from keras_vggface.vggface import VGGFace
from pinecone import Pinecone
from dotenv import load_dotenv



load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")
print(api_key)

pc = Pinecone(api_key=api_key)

index = pc.Index("face-features")

client_path = os.path.join(os.getcwd(), 'backend','client')
print(client_path)


app = Flask(__name__, static_folder=client_path, static_url_path='/')
CORS(app, resources={r"/api/*": {"origin" : "*"}})

@app.route('/api/get_celeb', methods=['POST'])
def get_celeb():
    if 'file' not in request.files:
        return jsonify({'error': 'No file received'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File name Empty'}), 400

    # show the image
    image = Image.open(file)
    face = get_face_from_image(image)
    if face is None:
        return jsonify({'error': 'No face detected'}), 400
    # face.show()

    # get the embedding
    embedding = get_embedding_from_face(face, model=VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg'))
    # print(embedding)

    # search for the embedding
    results = index.query(vector=embedding, top_k=5, namespace="first", include_values=False, include_metadata=True)

    if results['matches'] == []:
        return jsonify({'error': 'No match found'}), 400
    
    actors = []
    # store unique actors only along with their max scores
    for result in results['matches']:
        unique = True
        for actor in actors:
            if actor['name'] == result['metadata']['actor']:
                unique = False
                break
        if unique:
            secure_path = result['id'].replace('/', '\\').replace("..\\..", '')
            base_path = os.path.dirname(os.path.abspath(__file__))
            # print(base_path)
            secure_path = base_path + secure_path
            # print(secure_path)
            actors.append({'name': result['metadata']['actor'], 'score': result['score'], 'image_path': secure_path})
    
    for actor in actors:
        # open image from image path and convert it to base64
        # check if the file exists
        if not os.path.isfile(actor['image_path']):
            print(f"File {actor['image_path']} does not exist")
        with open(actor['image_path'], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            actor['image'] = encoded_string.decode('utf-8')
    
        
    response = jsonify({'actors': actors})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.static_folder, 'index.html')


PORT = os.getenv("PORT", default='5000')
HOST = os.getenv("HOST", default='0.0.0.0')

if __name__ == '__main__':
    app.run(port=PORT, host=HOST)