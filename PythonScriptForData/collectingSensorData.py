import sqlite3
import serial
import time
import os

def main():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('Data1.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            temperatureSensor INTEGER NOT NULL,
            heightSensor INTEGER NOT NULL,
            lightIntensitySensor INTEGER NOT NULL
        )
    ''')
    conn.commit()
    print("\nDatabase has been opened/created.")

    # Set up serial connection (adjust 'COM3' and baud rate as necessary)
    # Replace 'COM3' with the COM port your Bluetooth module is connected to
    serial_port = 'COM4'  # Example COM port; change this to your actual port
    baud_rate = 9600      # Ensure this matches the baud rate in your Arduino code

    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {serial_port}: {e}")
        return

    last_print_time = time.time()
    try:
        while True:
            # Read data from serial port if available
            
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                # Assuming data is comma-separated: temp, height, light, humidity
                data = line.split(',')
                if len(data) == 4:
                    try:
                        temperatureSensor = float(data[0])
                        heightSensor = float(data[1])
                        lightIntensitySensor = float(data[2])
                        humiditySensor = float(data[3])

                        # Insert data into database
                        cursor.execute('''
                            INSERT INTO sensor_data (temperatureSensor, heightSensor, lightIntensitySensor, humiditySensor)
                            VALUES (?, ?, ?, ?)
                        ''', (temperatureSensor, heightSensor, lightIntensitySensor, humiditySensor))
                        conn.commit()
                    except ValueError:
                        print("Received invalid data format.")
                else:
                    print("Received data with incorrect number of fields.")

            # Sleep for 1 millisecond
            time.sleep(1)

            # Every second, clear console and print the table again
            current_time = time.time()
            if current_time - last_print_time >= 1:
                # Clear console
                os.system('cls' if os.name == 'nt' else 'clear')

                # Fetch the latest 10 entries from the database
                # cursor.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 10')
                cursor.execute('SELECT * FROM sensor_data ORDER BY id')
                rows = cursor.fetchall()

                # Print the table header
                print("{:<5} {:<20} {:<15} {:<20} {:<15}".format(
                    'ID', 'Temperature', 'Height', 'Light Intensity', 'Humidity'))
                print("-" * 80)

                # Print each row
                for row in rows:
                    print("{:<5} {:<20} {:<15} {:<20} {:<15}".format(
                        row[0], row[1], row[2], row[3], row[4]))

                last_print_time = current_time

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()
        conn.close()

if __name__ == '__main__':
    main()
