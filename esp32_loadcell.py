import serial
import time

COM_PORT = "COM7"   # đổi thành COM Windows của bạn
BAUD_RATE = 9600

def main():
    print(f"Opening {COM_PORT} at {BAUD_RATE} baud...")
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # chờ ESP32 reboot khi mở cổng

    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print("ESP32:", line)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
