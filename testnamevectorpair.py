import psycopg2
from deepface import DeepFace
import os

# Function to list images in a directory
def list_images_in_directory(directory):
    # Supported image formats
    image_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.svg']

    # List to hold image file names and formats
    images = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file extension is in the list of supported image formats
            if any(file.lower().endswith(format) for format in image_formats):
                # Append the file name and format to the images list
                images.append((file, os.path.join(root, file)))

    return images

# Directory containing the images
directory = r'C:\Users\alex\simple_path'

# Get the list of images and their paths
images = list_images_in_directory(directory)

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    host='localhost',
    password='Test',
    port='5432'  # Specify the port if it's different from the default
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Iterate over the images
for image_name, image_path in images:
    # Load the face embeddings
    face_embedding = DeepFace.represent(img_path=image_path)

    # Extract the embedding values
    face_embedding_values = face_embedding[0]['embedding']

    # Save the image name and the embedding values to the database
    cur.execute("INSERT INTO embeddings (name, embedding) VALUES (%s, %s)", (image_name, face_embedding_values))

# Commit the transaction
conn.commit()

# Close communication with the database
cur.close()
conn.close()
