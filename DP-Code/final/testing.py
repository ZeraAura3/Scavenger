import time
import subprocess
from google.cloud import vision
import io
from serial import Serial  # Import pyserial to communicate with Arduino
from gpiozero import LED  # For controlling the GPIO pin on the Raspberry Pi

# Setup vision client
client = vision.ImageAnnotatorClient()
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/myenv/waste-classification-441308-e1823ce93688.json"

# Setup serial communication (assuming Arduino is connected to /dev/ttyUSB0)
#arduino = Serial('/dev/ttyUSB0', 9600)  # Update with your actual Arduino port

def capture_image():
    """Capture an image using libcamera."""
    image_path = "/tmp/captured_image.jpg"
    
    # Capture image using libcamera
    subprocess.run(["libcamera-still", "-o", image_path,"--width","1280","--height","720","-t","5000"])
    
    return image_path

def analyze_image(image_path):
    """Analyze the captured image using Google Cloud Vision API."""
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
        
    image = vision.Image(content=content)
    
    # Call Google Vision API to detect labels in the image
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    print('Labels:')
    for label in labels:
        print(label.description)

    return labels

def classify_waste(labels):
    """Classify the waste as biodegradable or non-biodegradable."""
    biodegradable_items = ["organic", "food", "plant", "vegetable",'fruit', "biodegradable","book", "organic waste",'organic', "food waste",'food', "vegetable waste",'peel', "fruit peel", "banana peel",
    "apple core",'apple', "tomato", "carrot peel",'carrot','onion', "onion skin", "garlic skin",'garlic','patato', "potato peel",
    "cucumber peel",'cucumber','coconut', "coconut shell", "coconut husk", "leaves", "flower", "flowers",
    "wood", "paper", "cardboard", "tissue", "paper napkin",'napkin', "cotton", "cotton fabric",
    "bamboo", "compostable plate", "compostable cutlery", "paper bag",'tea bag', "used tea bag","food waste", "leftover food", "vegetable scraps", "fruit peels", "fruit scraps",
    "vegetable waste", "vegetable peels", "food scraps", "egg shells", "coffee grounds",
    "tea bags", "tea leaves", "bread", "cereal", "pasta", "rice", "dairy products",
    "meat scraps", "bones", "fish scraps", "paper towel", "napkins", "tissues", "paper cups",
    "paper plates", "compostable cups", "compostable plates", "compostable packaging",
    "compostable utensils", "cardboard", "paper waste", "cardboard boxes", "notebook paper",
    "recycled paper", "leaf litter", "dried leaves", "branches", "flowers", "plant waste",
    "grass clippings", "soil", "wood shavings", "sawdust", "cotton fabric", "wool fabric",
    "linen fabric", "natural fibers", "compostable bags", "bamboo", "jute bags", "hemp products",
    "cotton swabs", "wooden chopsticks", "toothpicks", "cork", "compostable gloves", "feathers",
    "hair", "nail clippings", "burlap", "straw", "animal waste", "pet hair", "biodegradable bags",
    "palm leaves", "bamboo products", "mulch", "corn husks", "wheat straw", "peanut shells",
    "sunflower seeds", "rice husks", "coconut shells", "cotton wool", "plant roots",
    "compostable straws", "compostable packaging material", "wooden stirrers", "sugarcane bagasse",
    "palm fiber", "coconut fiber", "banana peels", "orange peels", "apple cores",
    "grape stems", "stems", "plant trimmings", "cucumber peels", "tomato stems",
    "flower petals", "seeds", "sugarcane stalks", "corn stalks", "bamboo sticks",
    "biodegradable cutlery", "biodegradable packaging", "biodegradable plates", "biodegradable cups",
    "natural paper", "wood scraps", "wood chips", "wicker", "clay pots", "compostable paper",
    "pine needles", "natural sponges", "cereal grains", "popcorn kernels", "pistachio shells",
    "orange rinds", "vegetable stems", "biodegradable containers", "compostable containers",
    "compostable paper towels", "biodegradable napkins", "hemp cloth", "compostable labels",
    "biodegradable cotton balls", "biodegradable wraps", "pressed leaves", "pasta scraps",
    "rice paper", "wrapping paper", "gourds", "biodegradable mailers", "mushroom stems",
    "natural dyes", "flowers", "herbs", "seasonal trimmings", "organic trimmings", "eco-friendly cloth",
    "corn starch-based packaging", "potato starch-based materials", "corn husk packaging",
    "coffee grounds", "bread", "chapati", "roti", "idli", "food scraps", "leftover food",
    "egg shells", "fish bones", "chicken bones", "meat scraps", "egg carton", "used towel",
    "used cloth", "pencil shavings", "hair", "feathers", "soil", "mud", "plant stem",
    "vegetable stems", "herbs", "spinach", "curry leaves", "mint leaves", "papaya peel", "apple", "banana", "orange", "mango", "papaya", "guava", "grapes", "watermelon",
    "muskmelon", "pomegranate", "pineapple", "lemon", "lime", "chikoo", "jackfruit",
    "coconut", "custard apple", "fig", "pear", "peach", "plum", "lychee", "kiwi",
    "strawberry", "blackberry", "blueberry", "raspberry", "tamarind", "amla", "cucumber",
    "tomato", "onion", "potato", "garlic", "ginger", "carrot", "radish", "beetroot",
    "cabbage", "cauliflower", "broccoli", "spinach", "fenugreek", "coriander", "mint",
    "lettuce", "pumpkin", "bottle gourd", "bitter gourd", "ridge gourd", "snake gourd",
    "ash gourd", "pointed gourd", "ivy gourd", "drumstick", "brinjal", "okra", "capsicum",
    "chili pepper", "green beans", "peas", "corn", "sweet potato", "yam", "turnip",
    "spring onion", "kale", "mushroom", "celery", "zucchini", "chayote", "leeks",
    "bell pepper", "kohlrabi", "mustard greens", "amaranth leaves", "arugula",
    "sweet lime", "sapota", "mulberry", "taro root", "mango seed", "banana peel",
    "orange peel", "pomegranate peel", "lemon peel", "apple core", "papaya seeds",
    "cantaloupe", "peach pit", "mango pit", "jackfruit seed", "bitter melon",
    "tindora", "karela", "squash", "garlic skin", "ginger peel", "carrot tops",
    "beet greens", "cauliflower stem", "cabbage core", "potato peels", "onion skin",
    "brinjal stem", "okra stem", "corn husk", "pea pods", "mustard leaves", "turnip greens",
    "radish greens", "mint stalk", "celery leaves", "pumpkin seeds",
    "melon rind", "orange peel", "peach pit", "kiwi peel", "avocado pit", "lemon peel",
    "fruit rind", "dried flowers", "greenery", "plant waste", "garden waste", "grass clippings",
    "used napkins", "used paper towel", "cotton swab", "bamboo toothbrush", "dried herbs",
    "sugarcane bagasse", "wooden chopsticks", "worn clothes", "compostable packaging",
    "biodegradable cup", "biodegradable plastic", "biodegradable packaging", "compostable bag"]
    non_biodegradable_items =  ["plastic", "metal", "non-biodegradable", "synthetic", "glass","Material property"
    "plastic waste", "plastic bag", "plastic bottle", "plastic container", "plastic cap",
    "plastic spoon", "plastic fork", "plastic knife", "plastic cup", "plastic plate",
    "plastic straw", "plastic wrapper", "plastic packaging", "plastic lid", "polythene",
    "polystyrene", "styrofoam", "polypropylene",'watch', "plastic film", "plastic sheet", "plastic tray",
    "chips packet",'pen', "biscuit wrapper", "chocolate wrapper", "plastic food wrapper",
    "plastic packaging tape", "aluminum foil", "aluminum can", "tin can", "metal can",
    "glass bottle", "glass jar", "ceramic", "porcelain", "stainless steel", "iron", "steel scrap",
    "electronics", "e-waste", "batteries", "phone charger", "toothbrush", "razor", "disposable razor",
    "marker", "pen", "plastic pen", "highlighter", "sketch pen", "permanent marker", "ballpoint pen",
    "sponges", "plastic toothbrush", "plastic toys", "plastic watch", "plastic bags", "diaper",
    "sanitary pad", "plastic gloves", "rubber bands", "rubber tire", "vinyl", "PVC pipe",
    "plastic pipe", "nylon", "polyester", "acrylic", "spandex", "synthetic fabric", "balloon",
    "plastic bottle cap", "blister pack", "CD", "DVD", "old wires", "cables", "bottle caps",
    "old toys", "plastic comb", "plastic storage box", "plastic bucket", "plastic liner",
    "plastic garbage bag", "plastic packaging", "plastic wrap", "thermal receipt paper",
    "plastic mailer", "shoes", "clothing", "sneakers", "rubber gloves", "plastic film", "bubble wrap",
    "polystyrene foam", "plastic cups", "styrofoam cups", "plastic sheet", "plastic packaging film",
    "toothpaste tube", "plastic toothpaste container", "hair ties", "clamshell packaging", "plastic tray",
    "toiletry packaging", "cosmetic packaging", "furniture wrap", "plastic tags", "disposable cup",
    "single-use plastic", "plastic utensils", "plastic cutlery", "clothing tags", "packing peanuts",
    "plastic film wrap", "disposable face mask", "disposable gloves", "synthetic shoes", "plastic straws",
    "chips packet", "biscuit wrapper", "chocolate wrapper", "plastic food wrapper",
    "plastic packaging tape", "aluminum foil", "aluminum can", "tin can", "metal can",
    "glass bottle", "glass jar", "ceramic", "porcelain", "stainless steel", "iron", "steel scrap",
    "electronics", "e-waste", "batteries", "phone charger", "toothbrush", "razor", "disposable razor",
    "marker", "pen", "plastic pen", "highlighter", "sketch pen", "permanent marker", "ballpoint pen",
    "sponges", "plastic toothbrush", "plastic toys", "plastic watch", "diaper",
    "sanitary pad", "plastic gloves", "rubber bands", "rubber tire", "vinyl", "PVC pipe",
    "plastic pipe", "nylon", "polyester", "acrylic", "spandex", "synthetic fabric", "balloon",
    "blister pack", "CD", "DVD", "old wires", "cables", "old toys", "plastic comb", "plastic storage box",
    "plastic bucket", "plastic liner", "plastic garbage bag", "plastic mailer", "shoes", "clothing",
    "sneakers", "rubber gloves", "bubble wrap", "polystyrene foam", "styrofoam cups", "plastic sheet",
    "plastic packaging film", "toothpaste tube", "plastic toothpaste container", "hair ties", "clamshell packaging",
    "plastic tray", "toiletry packaging", "cosmetic packaging", "furniture wrap", "plastic tags",
    "disposable cup", "single-use plastic", "plastic utensils", "plastic cutlery", "clothing tags",
    "packing peanuts", "plastic film wrap", "disposable face mask", "disposable gloves", "synthetic shoes",
    "plastic straws",    "chips packet", "biscuit wrapper", "chocolate wrapper", "plastic food wrapper",
    "plastic packaging tape", "aluminum foil", "aluminum can", "tin can", "metal can",
    "glass bottle", "glass jar", "ceramic", "porcelain", "stainless steel", "iron", "steel scrap",
    "electronics", "e-waste", "batteries", "phone charger", "toothbrush", "razor", "disposable razor",
    "marker", "pen", "plastic pen", "highlighter", "sketch pen", "ballpoint pen",
    "sponges", "plastic toothbrush", "plastic toys", "toys", "diaper",
    "sanitary pad", "plastic gloves", "rubber bands", "rubber tire", "vinyl", "PVC pipe",
    "plastic pipe", "nylon", "polyester", "acrylic", "spandex", "synthetic fabric", "balloon",
    "blister pack", "CD", "DVD", "wires", "cables", "plastic comb", "plastic storage box", 'comb'
    "plastic bucket", "plastic liner", "plastic garbage bag", "plastic mailer", "shoes", "clothing",
    "sneakers", "rubber gloves", "bubble wrap", "polystyrene foam", "styrofoam cups", "plastic sheet",
    "plastic packaging film", "toothpaste tube", "plastic toothpaste container", "hair ties", "clamshell packaging",
    "plastic tray", "toiletry packaging", "cosmetic packaging", "furniture wrap", "plastic tags",
    "disposable cup", "single-use plastic", "plastic utensils", "plastic cutlery", "clothing tags",
    "packing peanuts", "plastic film wrap", "disposable face mask", "disposable gloves", "synthetic shoes", 'utensils'
    "plastic straws","snacks","junk food","fried food","bottle","Nail","Communication Device"]
    
    bio_score = sum(label.score for label in labels if any(keyword in label.description.lower() for keyword in biodegradable_items))
    non_bio_score = sum(label.score for label in labels if any(keyword in label.description.lower() for keyword in non_biodegradable_items))
    
    print("\nBio Score:", bio_score)
    print("\nNon-Bio Score:", non_bio_score)
    
    if bio_score > non_bio_score:
        print("\nClassification: Biodegradable")
        return 'biodegradable'
    else:
        print("\nClassification: Non-biodegradable")
        return 'non-biodegradable'
    
    return 'unknown'

def send_signal_to_arduino(waste_type):
    """Send signal to Arduino based on waste type."""
    if waste_type == 'biodegradable':
        print('Sending signal to open biodegradable bin...')
        #arduino.write(b'B')  # Send 'B' for biodegradable
    elif waste_type == 'non-biodegradable':
        print('Sending signal to open non-biodegradable bin...')
        #arduino.write(b'N')  # Send 'N' for non-biodegradable
    else :
        print('Sending signal to open unknown bin...')
        #arduino.write(b'u')  # Send 'u' for unknown

def main():
    """Main function to run the waste classification process."""
    while True:
        # Capture the image using libcamera
        image_path = capture_image()

        # Analyze the image using Google Vision API
        labels = analyze_image(image_path)

        # Classify the waste based on the image labels
        waste_type = classify_waste(labels)

        send_signal_to_arduino(waste_type)     # Send signal to Arduino to control the motor

        # Wait for 10 seconds before capturing the next image
        time.sleep(10)

if __name__ == '__main__':
    main()
