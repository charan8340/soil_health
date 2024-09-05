import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Ensure enough arguments are provided
if len(sys.argv) != 5:
    print("Error: Expected 4 arguments, got", len(sys.argv) - 1)
    sys.exit(1)

crop_name = sys.argv[1]
soil_type = sys.argv[2]
humidity = float(sys.argv[3])
moisture = float(sys.argv[4])

print(f"Received inputs: Crop Name: {crop_name}, Soil Type: {soil_type}, Humidity: {humidity}, Moisture: {moisture}")

# Load the dataset
df = pd.read_csv('data.csv')

# Correct column names if necessary
df.rename(columns={
    'Humidity ': 'Humidity',
    'Soil Type': 'Soil_Type',
    'Crop Type': 'Crop_Type',
    'Fertilizer Name': 'Fertilizer'
}, inplace=True)

# Encode categorical variables
label_encoder_soil = LabelEncoder()
df['Soil_Type'] = label_encoder_soil.fit_transform(df['Soil_Type'])

label_encoder_crop = LabelEncoder()
df['Crop_Type'] = label_encoder_crop.fit_transform(df['Crop_Type'])

label_encoder_fertilizer = LabelEncoder()
df['Fertilizer'] = label_encoder_fertilizer.fit_transform(df['Fertilizer'])

# Store mappings for later use
crop_type_mapping = dict(zip(label_encoder_crop.classes_, label_encoder_crop.transform(label_encoder_crop.classes_)))
fertilizer_name_mapping = dict(zip(label_encoder_fertilizer.transform(label_encoder_fertilizer.classes_), label_encoder_fertilizer.classes_))

# Define features and target variable
X = df[['Soil_Type', 'Crop_Type', 'Humidity', 'Moisture']]
y = df['Fertilizer']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Function to predict fertilizer based on crop name and soil type
def predict_fertilizer(crop_name, soil_type, humidity, moisture):
    crop_encoded = label_encoder_crop.transform([crop_name])[0]
    soil_encoded = label_encoder_soil.transform([soil_type])[0]
    
    input_data = pd.DataFrame([[soil_encoded, crop_encoded, humidity, moisture]], 
                              columns=['Soil_Type', 'Crop_Type', 'Humidity', 'Moisture'])
    
    fertilizer_encoded = model.predict(input_data)[0]
    fertilizer_name = label_encoder_fertilizer.inverse_transform([fertilizer_encoded])[0]
    return fertilizer_name

# Make prediction and print result
recommended_fertilizer = predict_fertilizer(crop_name, soil_type, humidity, moisture)
print(f"Recommended Fertilizer for {crop_name}: {recommended_fertilizer}")

