import serial 
from time import sleep

ser = serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=2)
captured_image_path = "captured_image.jpg"

def cut_image(image_data, image_path):
    start_index = image_data.find(b'\xFF\xD8')
    final_index = image_data.rfind(b'\xFF\xD9')

    image_data = image_data[start_index:final_index + 2]

    with open(image_path, "wb") as img:
        img.write(image_data)

    print("Saved Image")


def capture_image():
    image_data = bytearray()

    print("Awaiting Camera")
    
    ser.reset_input_buffer()
    while True:
        image_data += ser.read(1)

        if image_data[-2:] == b'\xFF\xD9':
            print("Image Captured")
            break

    cut_image(image_data, captured_image_path)
    sleep(3)

for i in range (3):
    capture_image()
    

ser.close()
