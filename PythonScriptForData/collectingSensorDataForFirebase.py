import serial
import time
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate('D:\HackTheHill2ProjFolder\PythonScriptForData\datameasuringdb-firebase-adminsdk-voca3-8928b5f533.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://datameasuringdb-default-rtdb.firebaseio.com/'
})

# Your web app's Firebase configuration
# For Firebase JS SDK v7.20.0 and later, measurementId is optional


# // Initialize Firebase
# const app = initializeApp(firebaseConfig);
# const analytics = getAnalytics(app);
def main():
    # Set up serial connection
    serial_port = 'COM4'  # Replace with your actual port
    baud_rate = 9600      # Must match the Arduino code

    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {serial_port}: {e}")
        return
    counter = 0
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                data = line.split(',')
                if len(data) == 4:
                    try:
                        # if(counter > 1):
                        #     #units for height are in 
                            
                        temperatureSensor = float(data[0])
                        heightSensor = float(data[1])
                        lightIntensitySensor = float(data[2])
                        humiditySensor = float(data[3])
  
                        # Create the sensor_data dictionary
                        sensor_data = {
                            'temperature': temperatureSensor,
                            'height': heightSensor,
                            'lightIntensity': lightIntensitySensor,
                            'humidity': humiditySensor,
                            'timestamp': time.time()
                        }

                        # Reference to the 'sensor_data' node
                        ref = db.reference('sensor_data')

                        # Push the data to Firebase
                        ref.push(sensor_data)

                        print("Data sent to Firebase:", sensor_data)
                    except ValueError:
                        print(f"Invalid data received: {line}")
                else:
                    print(f"Incorrect data format: {line}")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()