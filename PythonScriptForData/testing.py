import firebase_admin
from firebase_admin import credentials, db
import time
import random

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('D:\HackTheHill2ProjFolder\PythonScriptForData\datameasuringdb-firebase-adminsdk-voca3-8928b5f533.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://datameasuringdb-default-rtdb.firebaseio.com/'
})

# Initialize starting values
temperature = 1.2
height = 1.2
lightIntensity = 1.2
humidity = 1.2

# Function to update values
def update_sensor_data():
    global temperature, height, lightIntensity, humidity
    
    # Increment height slightly
    height += random.uniform(0.01, 0.05)  # Slowly increase height
    
    # Other values may fluctuate slightly, including potential decrease
    temperature += random.uniform(-0.1, 0.1)
    lightIntensity += random.uniform(-0.2, 0.2)
    humidity += random.uniform(-0.3, 0.3)
    
    # Ensure values do not go below zero
    temperature = max(0, temperature)
    lightIntensity = max(0, lightIntensity)
    humidity = max(0, humidity)
    
    # Create new data with updated values
    test_data = {
        'temperature': round(temperature, 2),
        'height': round(height, 2),
        'lightIntensity': round(lightIntensity, 2),
        'humidity': round(humidity, 2),
        'timestamp': time.time()  # Add a timestamp
    }
    
    return test_data

# Reference to the 'sensor_data' node in your database
ref = db.reference('sensor_data')

# Loop to push new data every second
try:
    while True:
        # Update the sensor data
        test_data = update_sensor_data()
        
        # Create a unique key using the current timestamp
        timestamp = str(int(time.time())) 
        
        # Push the test data to Firebase
        ref.child(timestamp).set(test_data)
        
        print("Test data sent to Firebase:", test_data)
        
        # Wait for 1 second before sending the next data point
        time.sleep(5)

except KeyboardInterrupt:
    print("Data push interrupted by user.")
