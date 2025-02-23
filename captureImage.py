import serial 
from time import sleep

class CaptureImage:
    def __init__(self, ImagePath, SerialPort, BaudRate):
        self.image_path = ImagePath
        self.ser = serial.Serial(SerialPort, BaudRate, timeout=2)
        print("WARNING: INCLUDE A SLEEP TIMEOUT AFTER USING captureImage \nto prevent data corruption")

    def cutImage(self, image_data):
        start_index = image_data.find(b'\xFF\xD8')
        final_index = image_data.rfind(b'\xFF\xD9')

        image_data = image_data[start_index:final_index + 2]

        with open(self.image_path, "wb") as img:
            img.write(image_data)

        print("Saved Image")

    def captureImage(self):
        image_data = bytearray()

        print("Awaiting Camera")

        self.ser.reset_input_buffer()
        sleep(0.05)
        while True:
            image_data += self.ser.read(1)

            if image_data[-2:] == b'\xFF\xD9':
                break
        
        self.cutImage(image_data)

    def getImagePath(self):
        return self.image_path

    def closeSerial(self):
        self.ser.close()


