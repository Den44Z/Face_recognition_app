import psycopg2
from deepface import DeepFace
import os
import numpy as np

# Load the face embedding for the image
query_embedding = DeepFace.represent(img_path=r'C:\Users\alex\testpath\denizyeni.jpg')
query_embedding_values = query_embedding[0]['embedding']

# Convert the query embedding values to NumPy array
query_embedding_values = np.array(query_embedding_values, dtype=np.float32)

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

# Retrieve embeddings from the database
cur.execute("SELECT name, embedding FROM embeddings")
rows = cur.fetchall()

# Initialize variables to store the closest embedding and its distance
closest_embedding = None
closest_distance = float('inf')
closest_name = None

# Set the similarity threshold
threshold = 0.55

# Iterate over the rows
for row in rows:
    name = row[0]
    db_embedding_values = np.array(row[1], dtype=np.float32)

    # Calculate the cosine similarity
    similarity = np.dot(query_embedding_values, db_embedding_values) / (np.linalg.norm(query_embedding_values) * np.linalg.norm(db_embedding_values))

    # Check if the similarity is greater than or equal to the threshold
    if similarity >= threshold and similarity < closest_distance:
        closest_embedding = db_embedding_values
        closest_distance = similarity
        closest_name = name

# Print the result based on the threshold
if closest_name is not None:
    print(f"The closest match to 'denizyeni.jpg' is '{closest_name}' with a similarity of {closest_distance}")
else:
    print("No match found in the database.")

# Close communication with the database
cur.close()
conn.close()
