from colorQuantifier import ColorQuantifier
from PIL import Image
import numpy
import cv2


vid_path = '/Users/pyProject/WebCamProject/testCam.mjpeg.avi'

def colorDifference(color1, color2): 
    colorDifference = ColorQuantifier(
        color1[0], 
        color1[1], 
        color1[2], 

        color2[0], 
        color2[1], 
        color2[2],   
    )
    #deltaE = colorDifference.calculateDeltaE()
    return 0 if colorDifference.calculateDeltaE() < 5 else 1


#-------------------- Break --------------------#


def getImgArray(frame_number, vid_path, max_width):
    capture = cv2.VideoCapture(vid_path)

    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, pixel1 = capture.read()
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number + 1)
    ret, pixel2 = capture.read()

    cv2.imwrite(f'./img/frame{frame_number}.jpg', pixel1)

    capture.release()

    height, width, _ = pixel1.shape
    aspect_ratio = height / width
    pixel1 = cv2.resize(pixel1, (max_width, int(max_width * aspect_ratio)), interpolation=cv2.INTER_LANCZOS4)
    pixel2 = cv2.resize(pixel2, (max_width, int(max_width * aspect_ratio)), interpolation=cv2.INTER_LANCZOS4)

    pixel1 = cv2.cvtColor(pixel1, cv2.COLOR_BGR2LAB)
    pixel2 = cv2.cvtColor(pixel2, cv2.COLOR_BGR2LAB)

    return [pixel1, pixel2]

def generateMask(mask_image_path, image_path):
    mask_image = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(image_path)

    mask_image = cv2.resize(mask_image, (image.shape[1], image.shape[0]))

    mask = cv2.inRange(mask_image, 1, 255)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    return result

for i in range(8):
    pixel_array = getImgArray(i, vid_path, 80)
#print(f"\nFirst Frame:\n{pixelArray[0]}")
#print(f"\nSecond Frame:\n{pixelArray[1]}")

    new_image = []

    for x in range(pixel_array[0].shape[0]):
        row = []
        for y in range(pixel_array[0].shape[1]):
            difference = colorDifference(
                pixel_array[0][x][y], 
                pixel_array[1][x][y]
            )
            row.append(difference)
        new_image.append(row)
    #print(new_image)
    array = numpy.array(new_image, dtype=numpy.uint8)
    image = Image.fromarray(array * 255, mode="L") 

    image.save(f"./img/{i}.png")

    cv2.imwrite(f'./img/result{i}.png', generateMask(f'./img/{i}.png', f'./img/frame{i}.jpg'))

