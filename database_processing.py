import json
import ast
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('C:/Users/casey/Desktop/Github/Recipe-Roulette-Backend/firebase_auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load and prepare data
df = pd.read_csv('C:/Users/casey/Desktop/Recipe Roulette/archive/recipesv2.csv')

# Deserialize columns that are expected to be lists or JSON objects
def deserialize_column(data):
    try:
        # This tries to convert a stringified list or JSON into a list or dict
        return json.loads(data.replace("'", "\""))
    except:
        return data  # Return the data as is if it's not a stringified list/JSON
    
def deserialize_column_insrtructions(data):
    try:
        # This will correctly parse strings that represent lists, using ast.literal_eval
        return ast.literal_eval(data)
    except:
        return data  # Return data as is if parsing fails
    
def lowercase_tags(tags):
    if tags is None or not isinstance(tags, list):
        return tags  # Return as is if it's None or not a list
    return [tag.lower() for tag in tags]

# Apply deserialization specifically to the 'instructions' column
df['instructions'] = df['instructions'].apply(deserialize_column_insrtructions)

columns_to_upload = ['description', 'images', 'ingredients', 'instructions', 'macronutrients', 'servings', 'tags', 'title']
for col in columns_to_upload:
    if df[col].dtype == 'object':  # Assuming all these columns are of object type
        df[col] = df[col].apply(deserialize_column)

# Assuming df is your DataFrame already loaded
df['tags'] = df['tags'].apply(lowercase_tags)

subset_df = df[columns_to_upload].head(1000)

# Upload function
def upload_to_firestore(row):
    # Convert row to dictionary and upload
    doc_ref = db.collection('recipes').add(row.to_dict())
    #print(f"Uploaded document with ID: {doc_ref[1].id}")

# Apply upload to each row
subset_df.apply(upload_to_firestore, axis=1)
