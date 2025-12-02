# Standard library imports
import os
import tempfile
from typing import Dict

# Third-party imports  
import numpy as np
import tensorflow as tf
from PIL import Image
from supabase import create_client, Client


# Constants
supabaseUrl: str = "https://lgvelnkhepuokjbacqqx.supabase.co"
supabaseKey: str = ("sb_publishable_VwY13z1yliMQ698Km0fNYA_"
					"tgpwqZab")
snakeClassNames: list = [
	'Black Rat Snake', 'Eastern Garter Snake', 'Eastern Hognose Snake',
	'Eastern Massasauga Snake', 'Eastern Milk Snake', 
	'Eastern Ribbon Snake', 'Eastern Worm Snake', 
	'Northern Black Racer Snake', 'Northern Brown Snake',
	'Northern Copperhead Snake', 'Northern Water Snake', 'Queen Snake',
	'Red-Bellied Snake', 'Ring-Necked Snake', 'Rough Green Snake',
	'Smooth Green Snake', 'Timber Rattlesnake Snake'
]
imageSize224: int = 224
imageSize400: int = 400
normalizationFactor: float = 255.0


def downloadFileFromSupabase(supabaseClient: Client, 
							bucketName: str, 
							fileName: str, 
							fileExtension: str) -> str:
	"""Downloads a file from Supabase storage and saves to temp file.
	
	Args:
		supabaseClient: Authenticated Supabase client
		bucketName: Name of the storage bucket
		fileName: Name of the file to download
		fileExtension: File extension for temp file
		
	Returns:
		Path to the downloaded temporary file
	"""
	downloadedData = supabaseClient.storage.from_(bucketName).download(
		fileName)
	
	with tempfile.NamedTemporaryFile(delete=False, 
									suffix=fileExtension) as tempFile:
		tempFile.write(downloadedData)
		temporaryFilePath = tempFile.name
		
	return temporaryFilePath


def preprocessImageForModel(baseImage: Image.Image, 
						   targetSize: int) -> np.ndarray:
	"""Preprocesses an image for model prediction.
	
	Args:
		baseImage: PIL Image object to preprocess
		targetSize: Target size for image resize (width and height)
		
	Returns:
		Preprocessed numpy array ready for model prediction
	"""
	resizedImage = baseImage.resize((targetSize, targetSize))
	imageArray = tf.keras.preprocessing.image.img_to_array(resizedImage)
	expandedImageArray = np.expand_dims(imageArray, 0)
	normalizedImageArray = expandedImageArray / normalizationFactor
	
	return normalizedImageArray


def convertClassIndexToSnakeNumber(originalClassIndex: int) -> int:
	"""Converts class index to custom snake numbering system.
	
	Args:
		originalClassIndex: Original index in class names array
		
	Returns:
		Custom snake number (1-11, then 13-17, skipping 12)
	"""
	if originalClassIndex <= 10:
		snakeNumber = originalClassIndex + 1
	else:
		snakeNumber = originalClassIndex + 2
		
	return snakeNumber


def predictSnakeSpeciesDualModel(imageFilePath: str) -> Dict[int, float]:
	"""Predicts snake species using both 224x224 and 400x400 models.
	
	Args:
		imageFilePath: Path to the image file for prediction
		
	Returns:
		Dictionary mapping snake numbers to confidence scores
	"""
	predictionResults = {}
	
	# Load and convert image to RGB
	baseImage = Image.open(imageFilePath).convert('RGB')
	
	# Preprocess for both model sizes
	processedImage224 = preprocessImageForModel(baseImage, 
											   imageSize224)
	processedImage400 = preprocessImageForModel(baseImage, 
											   imageSize400)
	
	# Get predictions from both models
	model224Predictions = model224x224.predict(processedImage224, 
											  verbose=0)
	model400Predictions = model400x400.predict(processedImage400, 
											  verbose=0)
	
	# Calculate confidence scores
	confidenceScore224 = np.max(model224Predictions[0])
	confidenceScore400 = np.max(model400Predictions[0])
	
	# Combine predictions from both models
	combinedPredictions = {}
	
	# Add predictions from 224x224 model
	for classIndex, confidenceValue in enumerate(model224Predictions[0]):
		speciesName = snakeClassNames[classIndex]
		combinedPredictions[speciesName] = max(
			combinedPredictions.get(speciesName, 0), confidenceValue)
	
	# Add predictions from 400x400 model  
	for classIndex, confidenceValue in enumerate(model400Predictions[0]):
		speciesName = snakeClassNames[classIndex]
		combinedPredictions[speciesName] = max(
			combinedPredictions.get(speciesName, 0), confidenceValue)
	
	# Sort by confidence and get top 3
	sortedPredictions = sorted(combinedPredictions.items(), 
							  key=lambda prediction: prediction[1], 
							  reverse=True)[:3]
	
	# Convert to custom snake numbering system
	for ranking, (speciesName, confidenceValue) in enumerate(
		sortedPredictions):
		originalClassIndex = snakeClassNames.index(speciesName)
		snakeNumber = convertClassIndexToSnakeNumber(
			originalClassIndex)
		predictionResults[snakeNumber] = float(confidenceValue)
	
	return predictionResults


def main() -> None:
	"""Main execution function."""
	# Create Supabase client
	supabaseClient: Client = create_client(supabaseUrl, supabaseKey)
	
	# Download test image
	imageFilePath = downloadFileFromSupabase(
		supabaseClient, "SnakeImages/BlackRatSnake", 
		"blackrat2.jpg", ".jpg")
	
	# Download and load models
	model224Path = downloadFileFromSupabase(
		supabaseClient, "Keras", "model_stage_224.keras", ".keras")
	model400Path = downloadFileFromSupabase(
		supabaseClient, "Keras", "model_stage_400.keras", ".keras")
	
	global model224x224, model400x400
	model224x224 = tf.keras.models.load_model(model224Path)
	model400x400 = tf.keras.models.load_model(model400Path)
	
	# Run prediction
	results = predictSnakeSpeciesDualModel(imageFilePath)
	print(results)


if __name__ == "__main__":
	main()