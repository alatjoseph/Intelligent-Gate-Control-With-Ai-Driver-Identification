import os

import cv2

import face_comparision


# //herferf
def perform_face_comparison(fname,):
    user_image_path = os.path.join("static", "user_img", fname)
    known_faces_directory= "static/admin_img"
    def encode_face(image):
        face_encodings = face_comparision.face_encodings(image)
        if face_encodings:
            return face_encodings[0]
        else:
            return None

    def compare_faces(known_face_encoding, unknown_face_encoding):
        if known_face_encoding is not None and unknown_face_encoding is not None:
            match = face_comparision.compare_faces([known_face_encoding], unknown_face_encoding)[0]
            return match
        else:
            return False

    def calculate_accuracy(known_face_encoding, unknown_face_encoding):
        if known_face_encoding is not None and unknown_face_encoding is not None:
            distance = face_comparision.face_distance([known_face_encoding], unknown_face_encoding)
            accuracy = (1 - distance[0]) * 100
            return accuracy
        else:
            return 0.0

    # Load known faces
    known_face_encodings = []
    known_face_names = []

    # Load and encode known faces from a directory
    for filename in os.listdir(known_faces_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(known_faces_directory, filename)
            image = cv2.imread(image_path)
            face_encoding = encode_face(image)
            if face_encoding is not None:
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])

    # Load the user image to be compared
    unknown_image = cv2.imread(user_image_path)

    # Encode the unknown face
    unknown_face_encoding = encode_face(unknown_image)

    best_match_name = ""
    best_match_accuracy = 0.0

    # Compare the unknown face with known faces
    for known_face_encoding, name in zip(known_face_encodings, known_face_names):
        match = compare_faces(known_face_encoding, unknown_face_encoding)
        if match:
            accuracy = calculate_accuracy(known_face_encoding, unknown_face_encoding)
            if accuracy > best_match_accuracy:
                best_match_accuracy = accuracy
                best_match_name = name+'.jpg'

    # Return the best match
    if best_match_accuracy > 50:
        print(f"Best match: Name - {best_match_name}, Accuracy - {best_match_accuracy:.2f}%")
        return best_match_name
    else:
        return ""
