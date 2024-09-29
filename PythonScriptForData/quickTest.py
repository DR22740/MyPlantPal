import serial
import time

# Open the serial port (replace 'COM3' with your actual port)
ser = serial.Serial('COM4', 9600, timeout=1)  # Adjust 'COM3' for Windows or '/dev/ttyUSB0' for Linux

time.sleep(2)  # Wait for connection to establish

try:
    while True:
        if ser.in_waiting > 0:  # Check if there is data waiting in the buffer
            # Read a line from the serial port and decode it
            line = ser.readline().decode('utf-8').rstrip()
            print("Data received:", line)

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    ser.close()  # Close the serial connection