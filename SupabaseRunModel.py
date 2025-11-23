import os
import tensorflow as tf
import numpy as np
from supabase import create_client, Client
import tempfile
from PIL import Image

url = "https://lgvelnkhepuokjbacqqx.supabase.co"
key = "sb_publishable_VwY13z1yliMQ698Km0fNYA_tgpwqZab"

supabase: Client = create_client(url, key)

# Download an image to display
imgRes = supabase.storage.from_("SnakeImages/BlackRatSnake").download("blackrat2.jpg")

# Save image to temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as imgTmp:
    imgTmp.write(imgRes)
    imgPath = imgTmp.name

# Download the 224x224 model
res224 = supabase.storage.from_("Keras").download("model_stage_224.keras")
# Save to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as tmp:
    tmp.write(res224)
    tmpPath = tmp.name
model224 = tf.keras.models.load_model(tmpPath)


# Download the 400x400 model
res400 = supabase.storage.from_("Keras").download("model_stage_400.keras")
# Save to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as tmp:
    tmp.write(res400)
    tmpPath = tmp.name
model400 = tf.keras.models.load_model(tmpPath)


def predictSnakeDual(imagePath):
    """Predict using both 224x224 and 400x400 models, show the one with higher confidence"""

    returnStatement = {}
    
    # Load the base image once and convert to RGB (removes alpha channel if present)
    from PIL import Image
    baseImg = Image.open(imagePath).convert('RGB')
    
    # Resize and preprocess for 224x224 model
    img224 = baseImg.resize((224, 224))
    imgArray224 = tf.keras.preprocessing.image.img_to_array(img224)
    imgArray224 = np.expand_dims(imgArray224, 0)
    imgArray224 = imgArray224 / 255.0  # simple_preprocessing
    
    # Resize and preprocess for 400x400 model
    img400 = baseImg.resize((400, 400))
    imgArray400 = tf.keras.preprocessing.image.img_to_array(img400)
    imgArray400 = np.expand_dims(imgArray400, 0)
    imgArray400 = imgArray400 / 255.0  # simple_preprocessing
    
    # Get predictions from both models
    predictions224 = model224.predict(imgArray224, verbose=0)
    predictions400 = model400.predict(imgArray400, verbose=0)
    
    # Get confidence scores and class names
    confidence224 = np.max(predictions224[0])
    confidence400 = np.max(predictions400[0])
    
    # Define class names (snake species)
    classNames = [
        'Black Rat Snake', 'Eastern Garter Snake', 'Eastern Hognose Snake',
        'Eastern Massasauga Snake', 'Eastern Milk Snake', 'Eastern Ribbon Snake',
        'Eastern Worm Snake', 'Northern Black Racer Snake', 'Northern Brown Snake',
        'Northern Copperhead Snake', 'Northern Water Snake', 'Queen Snake',
        'Red-Bellied Snake', 'Ring-Necked Snake', 'Rough Green Snake',
        'Smooth Green Snake', 'Timber Rattlesnake Snake'
    ]
    
    # Show predictions from both models
    predictedClass224 = np.argmax(predictions224[0])
    predictedClass400 = np.argmax(predictions400[0])
    predictedSnake224 = classNames[predictedClass224]
    predictedSnake400 = classNames[predictedClass400]
    
    # print(f"224x224 Model: {predictedSnake224} ({confidence224:.2%})")
    # print(f"400x400 Model: {predictedSnake400} ({confidence400:.2%})")
    
    # Choose the model with higher confidence
    if confidence224 > confidence400:
        chosenPredictions = predictions224[0]
        chosenConfidence = confidence224
        chosenModel = "224x224"
        displayImg = img224
    else:
        chosenPredictions = predictions400[0]
        chosenConfidence = confidence400
        chosenModel = "400x400" 
        displayImg = img400
    
    # Get chosen prediction details
    predictedClass = np.argmax(chosenPredictions)
    predictedSnake = classNames[predictedClass]
    
    # Combine predictions from both models and show top 3 overall
    combinedPredictions = {}
    
    # Add predictions from 224x224 model
    for i, confidence in enumerate(predictions224[0]):
        snakeName = classNames[i]
        combinedPredictions[snakeName] = max(combinedPredictions.get(snakeName, 0), confidence)
    
    # Add predictions from 400x400 model
    for i, confidence in enumerate(predictions400[0]):
        snakeName = classNames[i]
        combinedPredictions[snakeName] = max(combinedPredictions.get(snakeName, 0), confidence)
    
    # Sort by confidence and get top 3
    sortedPredictions = sorted(combinedPredictions.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # print(f"Model Used: {chosenModel}")
    # print(f"Top 3 predictions (combined from both models):")
    for rank, (snakeName, confidence) in enumerate(sortedPredictions):
        # Find the original index of this snake in classNames
        originalIndex = classNames.index(snakeName)
        
        # Convert to custom index: 1-11 for positions 0-10, then 13-17 for positions 11-16
        if originalIndex <= 10:  # positions 0-10
            snakeIndex = originalIndex + 1  # indices 1-11
        else:  # positions 11-16
            snakeIndex = originalIndex + 2  # indices 13-17 (skipping 12)
        
        returnStatement[snakeIndex] = float(confidence)
    # print(returnStatement)
    

# Run prediction on the downloaded image
predictSnakeDual(imgPath)