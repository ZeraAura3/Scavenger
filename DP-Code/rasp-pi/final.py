!pip install google-cloud-vision opencv-python-headless

from google.colab import files
uploaded = files.upload()
SERVICE_ACCOUNT_FILE = list(uploaded.keys())[0]

from google.cloud import vision
import io
import cv2
from google.colab.patches import cv2_imshow
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
import numpy as np
client = vision.ImageAnnotatorClient.from_service_account_json(SERVICE_ACCOUNT_FILE)

def capture_webcam_image():
    js = Javascript('''
        async function takePhoto() {
            const video = document.createElement('video');
            const stream = await navigator.mediaDevices.getUserMedia({video: true});
            document.body.appendChild(video);
            video.srcObject = stream;
            await video.play();

            // Adding delay to allow you time to adjust the material in the frame
            await new Promise(resolve => setTimeout(resolve, 5000));

            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getTracks().forEach(track => track.stop());
            video.remove();
            return canvas.toDataURL('image/jpeg');
        }
        takePhoto();
    ''')
    display(js)
    data = eval_js("takePhoto()")
    binary = b64decode(data.split(',')[1])
    img_array = np.frombuffer(binary, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def classify_image_with_vision_api(frame):
    # Save the captured frame as a temporary image file
    filename = "temp_image.jpg"
    cv2.imwrite(filename, frame)

    # Load the image file and send it to Google Vision API
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform label detection
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Display labels and score
    for label in labels:
        print(f'Description: {label.description}, Score: {label.score}')

    # Simple classification based on common waste keywords
    bio_keywords = ["organic", "food", "plant", "vegetable",'fruit', "biodegradable","book", "organic waste",'organic', "food waste",'food', "vegetable waste",'peel', "fruit peel", "banana peel",
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
    non_bio_keywords = ["plastic", "metal", "non-biodegradable", "synthetic", "glass",
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
    "plastic straws"
]

    # Check if labels contain any keywords
    bio_score = sum(label.score for label in labels if any(keyword in label.description.lower() for keyword in bio_keywords))
    non_bio_score = sum(label.score for label in labels if any(keyword in label.description.lower() for keyword in non_bio_keywords))

    if bio_score > non_bio_score:
        print("\nClassification: Biodegradable")
    else:
        print("\nClassification: Non-biodegradable")
while True:
    frame = capture_webcam_image()
    if frame is not None:
        cv2_imshow(frame)  # Display captured image
        classify_image_with_vision_api(frame)
    else:
        print("Failed to capture image")
        break
    # Press 'q' to stop the loop (only works when interacting manually)
    user_input = input("Press 'q' to quit or any other key to continue: ")
    if user_input.lower() == 'q':
        break