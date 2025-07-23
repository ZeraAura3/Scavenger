import serial
import time

# Initialize serial connection
arduino = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)  # Adjust to the correct port
time.sleep(2)  # Wait for Arduino to initialize

# Test communication
print("Sending data to Arduino...")
arduino.write(b"Test message from Raspberry Pi\n")  # Send data to Arduino
time.sleep(1)  # Give Arduino time to respond

# Read response
#if arduino.in_waiting > 0:
    #response = arduino.read(arduino.in_waiting).decode('utf-8').strip()
    #print("Response from Arduino:")
    #print(response)
#else:
    #print("No response from Arduino.")

arduino.close()
