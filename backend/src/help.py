from PIL import Image
import base64

image_path = r'./data/Sidharth_Malhotra/Sidharth_Malhotra.106.jpg'
Image.open(image_path).show()

with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print(encoded_string.decode('utf-8'))