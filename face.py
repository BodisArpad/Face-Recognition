
import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import os
import sys

known_face_encodings = []
known_face_names = []
imagini_cunoscute = os.listdir(sys.argv[1])
imagini_necunoscute = os.listdir(sys.argv[2])
for i in imagini_cunoscute:
    image_path = sys.argv[1]
    if not image_path.endswith('/'):
        image_path += "/"
    image_path += i
    img = face_recognition.load_image_file(image_path)
    known_face_encodings.append(face_recognition.face_encodings(img)[0])
    known_face_names.append(i.split('.')[0])
print("Fete cunoscute:" + str(known_face_names))

#arpi_image = face_recognition.load_image_file("./Arpi.jpg")
#arpi_face_encoding = face_recognition.face_encodings(arpi_image)[0]

print("recunoastere imagini:")
for i in imagini_necunoscute:
    
    image_path = sys.argv[2]
    if not image_path.endswith('/'):
        image_path += "/"
    image_path += i

    # imagine cu fata necunoscuta
    print(image_path)
    unknown_image = face_recognition.load_image_file(image_path)

    #gaseste fetele
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)


    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)

    # verifica daca fetel se potrivesc
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "NECUNOSCUT"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # incadreaza fata
        draw.rectangle(((left, top), (right, bottom)), outline=(48, 63, 159))

        # deseneaza eticheta
        
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(48, 63, 159), outline=(48, 63, 159))
        draw.text((left + 6, bottom - text_height -6 ), name, fill=(355, 355, 355, 0))



    del draw

    pil_image.show()
    
