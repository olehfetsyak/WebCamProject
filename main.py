from colorQuantifier import ColorQuantifier
from PIL import Image
import numpy
import cv2

vid_path = '/Users/pyProject/WebCamProject/testCam.gif'

def colorDifference(color1, color2): 
    colorDifference = ColorQuantifier(
        color1[0], 
        color1[1], 
        color1[2], 

        color2[0], 
        color2[1], 
        color2[2],   
    )
    deltaE = colorDifference.calculateDeltaE()
    return 0 if colorDifference.calculateDeltaE() < 2 else 1


#-------------------- Break --------------------#


def getImgArray(frame_number, vid_path, max_width):
    with Image.open(vid_path) as img:
        width, height = img.size
        aspect_ratio = height / width

        img.seek(frame_number)
        resized_img1 = img.resize((max_width, int(max_width * aspect_ratio)), Image.Resampling.LANCZOS)
        pixel1 = numpy.asarray(resized_img1, dtype=numpy.uint8).copy()
        pixel1= pixel1[..., :3]
        pixel1 = cv2.cvtColor(pixel1, cv2.COLOR_RGB2BGR)
        pixel1  = cv2.cvtColor(pixel1, cv2.COLOR_BGR2LAB)

        img.seek(frame_number + 1)
        resized_img2 = img.resize((max_width, int(max_width * aspect_ratio)), Image.Resampling.LANCZOS)
        pixel2 = numpy.asarray(resized_img2, dtype=numpy.uint8).copy()
        pixel2 = pixel2[..., :3]
        pixel2 = cv2.cvtColor(pixel2, cv2.COLOR_RGB2BGR)
        pixel2 = cv2.cvtColor(pixel2, cv2.COLOR_BGR2LAB)

        return [pixel1, pixel2]
    

for i in range(8):
    pixelArray = getImgArray(i, vid_path, 20)
#print(f"\nFirst Frame:\n{pixelArray[0]}")
#print(f"\nSecond Frame:\n{pixelArray[1]}")

    new_image = []

    for x in range(pixelArray[0].shape[0]):
        row = []
        for y in range(pixelArray[0].shape[1]):
            difference = colorDifference(
                pixelArray[0][x][y], 
                pixelArray[1][x][y]
            )
            row.append(difference)
        new_image.append(row)
            



    array = numpy.array(new_image, dtype=numpy.uint8)
    image = Image.fromarray(array * 255, mode="L") 

    image.save(f"./WebCamProject/img/{i}.png")






