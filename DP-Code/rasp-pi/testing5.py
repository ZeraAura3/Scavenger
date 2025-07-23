import time
import subprocess
from google.cloud import vision
import io
from serial import Serial  # Import pyserial to communicate with Arduino
import serial
import cv2  # Import OpenCV for motion detection
import numpy as np

# Initialize Arduino serial communication
# arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with your serial port
# arduino = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyUSB0' with your serial port
arduino = serial.Serial('/dev/ttyAMA0', 9600)  # Replace '/dev/ttyUSB0' with your serial port
time.sleep(2)  # Wait for Arduino to initialize

# Setup vision client
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/myenv/waste-classification-441308-e1823ce93688.json"
client = vision.ImageAnnotatorClient()

# Waste classification lists (biodegradable and non-biodegradable items)
biodegradable_items = ['Organic', 'Food', 'Plant', 'Vegetable', 'Fruit', 'Biodegradable', 'Book', 'Organic waste', 'Organic', 'Food waste', 'Food', 'Vegetable waste', 'Peel', 'Fruit peel', 'Banana peel', 'Apple core', 'Apple', 'Tomato', 'Carrot peel', 'Carrot', 'Onion', 'Onion skin', 'Garlic skin', 'Garlic', 'Patato', 'Potato peel', 'Cucumber peel', 'Cucumber', 'Coconut', 'Coconut shell', 'Coconut husk', 'Leaves', 'Flower', 'Flowers', 'Wood', 'Paper', 'Cardboard', 'Tissue', 'Paper napkin', 'Napkin', 'Cotton', 'Cotton fabric', 'Bamboo', 'Compostable plate', 'Compostable cutlery', 'Paper bag', 'Tea bag', 'Used tea bag', 'Food waste', 'Leftover food', 'Vegetable scraps', 'Fruit peels', 'Fruit scraps', 'Vegetable waste', 'Vegetable peels', 'Food scraps', 'Egg shells', 'Coffee grounds', 'Tea bags', 'Tea leaves', 'Bread', 'Cereal', 'Pasta', 'Rice', 'Dairy products', 'Meat scraps', 'Bones', 'Fish scraps', 'Paper towel', 'Napkins', 'Tissues', 'Paper cups', 'Paper plates', 'Compostable cups', 'Compostable plates', 'Compostable packaging', 'Compostable utensils', 'Cardboard', 'Paper waste', 'Cardboard boxes', 'Notebook paper', 'Recycled paper', 'Leaf litter', 'Dried leaves', 'Branches', 'Flowers', 'Plant waste', 'Grass clippings', 'Soil', 'Wood shavings', 'Sawdust', 'Cotton fabric', 'Wool fabric', 'Linen fabric', 'Natural fibers', 'Compostable bags', 'Bamboo', 'Jute bags', 'Hemp products', 'Cotton swabs', 'Wooden chopsticks', 'Toothpicks', 'Cork', 'Compostable gloves', 'Feathers', 'Hair', 'Nail clippings', 'Burlap', 'Straw', 'Animal waste', 'Pet hair', 'Biodegradable bags', 'Palm leaves', 'Bamboo products', 'Mulch', 'Corn husks', 'Wheat straw', 'Peanut shells', 'Sunflower seeds', 'Rice husks', 'Coconut shells', 'Cotton wool', 'Plant roots', 'Compostable straws', 'Compostable packaging material', 'Wooden stirrers', 'Sugarcane bagasse', 'Palm fiber', 'Coconut fiber', 'Banana peels', 'Orange peels', 'Apple cores', 'Grape stems', 'Stems', 'Plant trimmings', 'Cucumber peels', 'Tomato stems', 'Flower petals', 'Seeds', 'Sugarcane stalks', 'Corn stalks', 'Bamboo sticks', 'Biodegradable cutlery', 'Biodegradable packaging', 'Biodegradable plates', 'Biodegradable cups', 'Natural paper', 'Wood scraps', 'Wood chips', 'Wicker', 'Clay pots', 'Compostable paper', 'Pine needles', 'Natural sponges', 'Cereal grains', 'Popcorn kernels', 'Pistachio shells', 'Orange rinds', 'Vegetable stems', 'Biodegradable containers', 'Compostable containers', 'Compostable paper towels', 'Biodegradable napkins', 'Hemp cloth', 'Compostable labels', 'Biodegradable cotton balls', 'Biodegradable wraps', 'Pressed leaves', 'Pasta scraps', 'Rice paper', 'Wrapping paper', 'Gourds', 'Biodegradable mailers', 'Mushroom stems', 'Natural dyes', 'Flowers', 'Herbs', 'Seasonal trimmings', 'Organic trimmings', 'Eco-friendly cloth', 'Corn starch-based packaging', 'Potato starch-based materials', 'Corn husk packaging', 'Coffee grounds', 'Bread', 'Chapati', 'Roti', 'Idli', 'Food scraps', 'Leftover food', 'Egg shells', 'Fish bones', 'Chicken bones', 'Meat scraps', 'Egg carton', 'Used towel', 'Used cloth', 'Pencil shavings', 'Hair', 'Feathers', 'Soil', 'Mud', 'Plant stem', 'Vegetable stems', 'Herbs', 'Spinach', 'Curry leaves', 'Mint leaves', 'Papaya peel', 'Apple', 'Banana', 'Orange', 'Mango', 'Papaya', 'Guava', 'Grapes', 'Watermelon', 'Muskmelon', 'Pomegranate', 'Pineapple', 'Lemon', 'Lime', 'Chikoo', 'Jackfruit', 'Coconut', 'Custard apple', 'Fig', 'Pear', 'Peach', 'Plum', 'Lychee', 'Kiwi', 'Strawberry', 'Blackberry', 'Blueberry', 'Raspberry', 'Tamarind', 'Amla', 'Cucumber', 'Tomato', 'Onion', 'Potato', 'Garlic', 'Ginger', 'Carrot', 'Radish', 'Beetroot', 'Cabbage', 'Cauliflower', 'Broccoli', 'Spinach', 'Fenugreek', 'Coriander', 'Mint', 'Lettuce', 'Pumpkin', 'Bottle gourd', 'Bitter gourd', 'Ridge gourd', 'Snake gourd', 'Ash gourd', 'Pointed gourd', 'Ivy gourd', 'Drumstick', 'Brinjal', 'Okra', 'Capsicum', 'Chili pepper', 'Green beans', 'Peas', 'Corn', 'Sweet potato', 'Yam', 'Turnip', 'Spring onion', 'Kale', 'Mushroom', 'Celery', 'Zucchini', 'Chayote', 'Leeks', 'Bell pepper', 'Kohlrabi', 'Mustard greens', 'Amaranth leaves', 'Arugula', 'Sweet lime', 'Sapota', 'Mulberry', 'Taro root', 'Mango seed', 'Banana peel', 'Orange peel', 'Pomegranate peel', 'Lemon peel', 'Apple core', 'Papaya seeds', 'Cantaloupe', 'Peach pit', 'Mango pit', 'Jackfruit seed', 'Bitter melon', 'Tindora', 'Karela', 'Squash', 'Garlic skin', 'Ginger peel', 'Carrot tops', 'Beet greens', 'Cauliflower stem', 'Cabbage core', 'Potato peels', 'Onion skin', 'Brinjal stem', 'Okra stem', 'Corn husk', 'Pea pods', 'Mustard leaves', 'Turnip greens', 'Radish greens', 'Mint stalk', 'Celery leaves', 'Pumpkin seeds', 'Melon rind', 'Orange peel', 'Peach pit', 'Kiwi peel', 'Avocado pit', 'Lemon peel', 'Fruit rind', 'Dried flowers', 'Greenery', 'Plant waste', 'Garden waste', 'Grass clippings', 'Used napkins', 'Used paper towel', 'Cotton swab', 'Bamboo toothbrush', 'Dried herbs', 'Sugarcane bagasse', 'Wooden chopsticks', 'Worn clothes', 'Compostable packaging', 'Biodegradable cup', 'Biodegradable plastic', 'Biodegradable packaging', 'Compostable bag']
non_biodegradable_items =  ['Plastic', 'Metal', 'Non-biodegradable', 'Synthetic', 'Glass', 'Material propertyplastic waste', 'Plastic bag', 'Plastic bottle', 'Plastic container', 'Plastic cap', 'Plastic spoon', 'Plastic fork', 'Plastic knife', 'Plastic cup', 'Plastic plate', 'Plastic straw', 'Plastic wrapper', 'Plastic packaging', 'Plastic lid', 'Polythene', 'Polystyrene', 'Styrofoam', 'Polypropylene', 'Watch', 'Plastic film', 'Plastic sheet', 'Plastic tray', 'Chips packet', 'Pen', 'Biscuit wrapper', 'Chocolate wrapper', 'Plastic food wrapper', 'Plastic packaging tape', 'Aluminum foil', 'Aluminum can', 'Tin can', 'Metal can', 'Glass bottle', 'Glass jar', 'Ceramic', 'Porcelain', 'Stainless steel', 'Iron', 'Steel scrap', 'Electronics', 'E-waste', 'Batteries', 'Phone charger', 'Toothbrush', 'Razor', 'Disposable razor', 'Marker', 'Pen', 'Plastic pen', 'Highlighter', 'Sketch pen', 'Permanent marker', 'Ballpoint pen', 'Sponges', 'Plastic toothbrush', 'Plastic toys', 'Plastic watch', 'Plastic bags', 'Diaper', 'Sanitary pad', 'Plastic gloves', 'Rubber bands', 'Rubber tire', 'Vinyl', 'Pvc pipe', 'Plastic pipe', 'Nylon', 'Polyester', 'Acrylic', 'Spandex', 'Synthetic fabric', 'Balloon', 'Plastic bottle cap', 'Blister pack', 'Cd', 'Dvd', 'Old wires', 'Cables', 'Bottle caps', 'Old toys', 'Plastic comb', 'Plastic storage box', 'Plastic bucket', 'Plastic liner', 'Plastic garbage bag', 'Plastic packaging', 'Plastic wrap', 'Thermal receipt paper', 'Plastic mailer', 'Shoes', 'Clothing', 'Sneakers', 'Rubber gloves', 'Plastic film', 'Bubble wrap', 'Polystyrene foam', 'Plastic cups', 'Styrofoam cups', 'Plastic sheet', 'Plastic packaging film', 'Toothpaste tube', 'Plastic toothpaste container', 'Hair ties', 'Clamshell packaging', 'Plastic tray', 'Toiletry packaging', 'Cosmetic packaging', 'Furniture wrap', 'Plastic tags', 'Disposable cup', 'Single-use plastic', 'Plastic utensils', 'Plastic cutlery', 'Clothing tags', 'Packing peanuts', 'Plastic film wrap', 'Disposable face mask', 'Disposable gloves', 'Synthetic shoes', 'Plastic straws', 'Chips packet', 'Biscuit wrapper', 'Chocolate wrapper', 'Plastic food wrapper', 'Plastic packaging tape', 'Aluminum foil', 'Aluminum can', 'Tin can', 'Metal can', 'Glass bottle', 'Glass jar', 'Ceramic', 'Porcelain', 'Stainless steel', 'Iron', 'Steel scrap', 'Electronics', 'E-waste', 'Batteries', 'Phone charger', 'Toothbrush', 'Razor', 'Disposable razor', 'Marker', 'Pen', 'Plastic pen', 'Highlighter', 'Sketch pen', 'Permanent marker', 'Ballpoint pen', 'Sponges', 'Plastic toothbrush', 'Plastic toys', 'Plastic watch', 'Diaper', 'Sanitary pad', 'Plastic gloves', 'Rubber bands', 'Rubber tire', 'Vinyl', 'Pvc pipe', 'Plastic pipe', 'Nylon', 'Polyester', 'Acrylic', 'Spandex', 'Synthetic fabric', 'Balloon', 'Blister pack', 'Cd', 'Dvd', 'Old wires', 'Cables', 'Old toys', 'Plastic comb', 'Plastic storage box', 'Plastic bucket', 'Plastic liner', 'Plastic garbage bag', 'Plastic mailer', 'Shoes', 'Clothing', 'Sneakers', 'Rubber gloves', 'Bubble wrap', 'Polystyrene foam', 'Styrofoam cups', 'Plastic sheet', 'Plastic packaging film', 'Toothpaste tube', 'Plastic toothpaste container', 'Hair ties', 'Clamshell packaging', 'Plastic tray', 'Toiletry packaging', 'Cosmetic packaging', 'Furniture wrap', 'Plastic tags', 'Disposable cup', 'Single-use plastic', 'Plastic utensils', 'Plastic cutlery', 'Clothing tags', 'Packing peanuts', 'Plastic film wrap', 'Disposable face mask', 'Disposable gloves', 'Synthetic shoes', 'Plastic straws', 'Chips packet', 'Biscuit wrapper', 'Chocolate wrapper', 'Plastic food wrapper', 'Plastic packaging tape', 'Aluminum foil', 'Aluminum can', 'Tin can', 'Metal can', 'Glass bottle', 'Glass jar', 'Ceramic', 'Porcelain', 'Stainless steel', 'Iron', 'Steel scrap', 'Electronics', 'E-waste', 'Batteries', 'Phone charger', 'Toothbrush', 'Razor', 'Disposable razor', 'Marker', 'Pen', 'Plastic pen', 'Highlighter', 'Sketch pen', 'Ballpoint pen', 'Sponges', 'Plastic toothbrush', 'Plastic toys', 'Toys', 'Diaper', 'Sanitary pad', 'Plastic gloves', 'Rubber bands', 'Rubber tire', 'Vinyl', 'Pvc pipe', 'Plastic pipe', 'Nylon', 'Polyester', 'Acrylic', 'Spandex', 'Synthetic fabric', 'Balloon', 'Blister pack', 'Cd', 'Dvd', 'Wires', 'Cables', 'Plastic comb', 'Plastic storage box', 'Combplastic bucket', 'Plastic liner', 'Plastic garbage bag', 'Plastic mailer', 'Shoes', 'Clothing', 'Sneakers', 'Rubber gloves', 'Bubble wrap', 'Polystyrene foam', 'Styrofoam cups', 'Plastic sheet', 'Plastic packaging film', 'Toothpaste tube', 'Plastic toothpaste container', 'Hair ties', 'Clamshell packaging', 'Plastic tray', 'Toiletry packaging', 'Cosmetic packaging', 'Furniture wrap', 'Plastic tags', 'Disposable cup', 'Single-use plastic', 'Plastic utensils', 'Plastic cutlery', 'Clothing tags', 'Packing peanuts', 'Plastic film wrap', 'Disposable face mask', 'Disposable gloves', 'Synthetic shoes', 'Utensilsplastic straws', 'Snacks', 'Junk food', 'Fried food', 'Bottle', 'Nail', 'Communication device']
    
waste_mapping = {}

# Add items from biodegradable list to the mapping
for item in biodegradable_items:
    waste_mapping[item.lower()] = "biodegradable"

# Add items from non-biodegradable list to the mapping
for item in non_biodegradable_items:
    waste_mapping[item.lower()] = "non-biodegradable"
    
def capture_image():
    """Capture an image using libcamera."""
    image_path = "/tmp/captured_image.jpg"
    subprocess.run(["libcamera-still", "-o", image_path, "--width", "1280", "--height", "720", "-t", "5000"])
    return image_path

def analyze_image(image_path):
    """Analyze the captured image using Google Cloud Vision API."""
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    for label in labels:
        print(label.description)
    return labels

def main():
    """Main function to run the waste classification process when motion is detected."""
    cap = cv2.VideoCapture(0)  # Initialize camera capture
    time.sleep(2)  # Warm up the camera

    # Read the first frame
    ret, previous_frame = cap.read()
    if not ret:
        print("Failed to grab initial frame")
        return

    while True:
        # Read the next frame
        ret, current_frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert frames to grayscale
        gray_prev = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        gray_current = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference between frames
        frame_diff = cv2.absdiff(gray_current, gray_prev)
        # Apply Gaussian blur to reduce noise and improve detection
        frame_diff = cv2.GaussianBlur(frame_diff, (5, 5), 0)
        # Threshold the difference
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        # Dilate the threshold image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        # Find contours on thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are detected, motion is present
        if len(contours) > 0:
            print("Motion detected, capturing and classifying image")
            image_path = capture_image()
            if not image_path:
                break

            # Analyze and classify the image
            labels = analyze_image(image_path)
            bio_score = 0
            non_bio_score = 0
            for label in labels:
                description = label.description.lower().strip()
                classification = waste_mapping.get(description, 'unknown')
                print(f"Label: {label.description} | Classification: {classification}")
                if classification == 'biodegradable':
                    bio_score += label.score
                elif classification == 'non-biodegradable':
                    non_bio_score += label.score

            print("Sending data to Arduino...")
            print(f"\nBiodegradable score: {bio_score}\n")
            time.sleep(1)
            print(f"\nNon-biodegradable score: {non_bio_score}\n")
            time.sleep(1)

            # Determine waste type and send to Arduino
            if bio_score > non_bio_score:
                waste_type = 'biodegradable\n'
            elif non_bio_score > bio_score:
                waste_type = 'non-biodegradable\n'
            else:
                waste_type = 'unknown\n'

            print(f"The waste is classified as {waste_type}")
            arduino.write(waste_type.encode('utf-8'))
            time.sleep(2)

        # Wait for a specific time interval before next detection
        time.sleep(0.5)
        # Update previous frame
        previous_frame = current_frame.copy()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")