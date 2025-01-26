import os

import cv2
import face_recognition


def compare_images(image1_path, image2_path, tolerance=0.6):
    """
    Compares two images to determine if they contain the same person.

    Args:
        image1_path: Path to the first image.
        image2_path: Path to the second image.
        tolerance: Distance threshold for face comparison. 

    Returns:
        A tuple (result, distance) where:
        - result: True if the images likely contain the same person, False otherwise.
        - distance: The face distance between the two images, or None if comparison couldn't be made.
    """

    def encode_face(image):
        """Encodes the face in the given image.

        Args:
            image: The image to encode.

        Returns:
            The face encoding, or None if no face is found.
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_image)
        if len(face_encodings) > 1:
            print("Warning: More than one face detected in the image. Using the first face found.")
        return face_encodings[0] if face_encodings else None

    # Load the two images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Handle cases where images could not be loaded
    if image1 is None or image2 is None:
        raise FileNotFoundError("One or both images could not be loaded. Check the file paths.")

    # Get face encodings for both images
    encoding1 = encode_face(image1)
    encoding2 = encode_face(image2)

    # Compare the face encodings
    if encoding1 is not None and encoding2 is not None:
        results = face_recognition.compare_faces([encoding1], encoding2)
        distance = face_recognition.face_distance([encoding1], encoding2)[0]
        print(f"Face distance: {distance}")  # Optional debug output
        return results[0] and distance <= tolerance, distance
    else:
        print("No face detected in one or both images.")
        return False, None


# Example Usage
image1_path = os.path.join("static", "images", "alat.jpg")  # Replace with your first image path
image2_path = os.path.join("static", "images", "IMG20230122111651.jpg")  # Replace with your second image path

result, distance = compare_images(image1_path, image2_path)
if result:
    print("The images likely contain the same person.")
else:
    print("The images likely contain different people.")
if distance is not None:
    print(f"Distance between faces: {distance}")
