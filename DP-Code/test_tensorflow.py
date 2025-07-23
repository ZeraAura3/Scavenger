import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input

# Load the TensorFlow/Keras model (.h5 file)
model = load_model("D:/VS_CODE/DP/waste_classification_model.h5")

# Define image pre-processing function
def preprocess_image(image):
    image = cv2.resize(image, (60,60))  # Resize to match the input size of your model (60x60 for VGG16)
    image = img_to_array(image)  # Convert image to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = preprocess_input(image)  # Pre-process for VGG16 if using that, adjust if using another model
    return image

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open webcam")
    exit()

while True:
    # Capture a frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Display the live feed from the webcam
    cv2.imshow('Press "C" to Capture Image', frame)

    # Wait for the key press to capture or quit
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # When 'C' is pressed, capture the image
        # Preprocess the captured frame
        processed_frame = preprocess_image(frame)

        # Make prediction
        predictions = model.predict(processed_frame)
        class_label = "Biodegradable" if predictions[0][0] < 0.5 else "Non-biodegradable"
        confidence = predictions[0][0] if predictions[0][0] >= 0.5 else 1 - predictions[0][0]

        # Display the classification result on the frame
        label_text = f"{class_label} ({confidence:.2f})"
        cv2.putText(frame, label_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the captured image with the classification result
        cv2.imshow('Captured Image', frame)

        # Save the captured image (optional)
        cv2.imwrite('captured_image.jpg', frame)
        print(f'Captured image saved as captured_image.jpg')
        print(f"{class_label} ({confidence:.2f})")

        # Wait for any key to close the result window
        cv2.waitKey(0)

    # Press 'q' to quit the loop and stop capturing from the camera
    if key == ord('q'):
        print("Exiting...")
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
