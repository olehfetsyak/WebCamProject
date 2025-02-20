from colorQuantifier import ColorQuantifier
from PIL import Image
import numpy
import cv2


vid_path = '/Users/pyProject/WebCamProject/testCam.mjpeg.avi'
check_image_every = 2  # In Seconds

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


def getImgArray(frame_number, vid_path, max_width, new_frame_number):
    capture = cv2.VideoCapture(vid_path)

    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    _, pixel1 = capture.read()
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number + 1)
    _, pixel2 = capture.read()

    #new_frame_number is used to save the image in the same iteration as previous
    cv2.imwrite(f'./img/frame{new_frame_number}.jpg', pixel1) 

    capture.release()

    height, width, _ = pixel1.shape
    aspect_ratio = height / width
    pixel1 = cv2.resize(pixel1, (max_width, int(max_width * aspect_ratio)), interpolation=cv2.INTER_LANCZOS4)
    pixel2 = cv2.resize(pixel2, (max_width, int(max_width * aspect_ratio)), interpolation=cv2.INTER_LANCZOS4)

    pixel1, pixel2 = cv2.cvtColor(pixel1, cv2.COLOR_BGR2LAB), cv2.cvtColor(pixel2, cv2.COLOR_BGR2LAB)

    return [pixel1, pixel2]

def generateMask(mask_image_path, image_path):
    mask_image = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(image_path)
    
    mask_image = cv2.medianBlur(mask_image, ksize=3) 
    # To-Do, move out of function so saved 0.png has blur built in
    mask_image = cv2.resize(mask_image, (image.shape[1], image.shape[0]))
    
    mask = cv2.inRange(mask_image, 1, 255)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    return result

def splitFrame(vid_path, time):
    capture = cv2.VideoCapture(vid_path)

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    capture.release()

    return (fps * time, frame_count)

frame_result = splitFrame(vid_path, check_image_every)
time_step, total_frames = frame_result[0], frame_result[1]
img_count = 0
for i in range(0, total_frames, time_step):
    pixel_array = getImgArray(i, vid_path, 80, img_count) 
    #To-Do having to pass an unneccesary variable,: img_count
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

    image.save(f"./img/{img_count}.png")

    cv2.imwrite(f'./img/result{img_count}.png', generateMask(f'./img/{img_count}.png', f'./img/frame{img_count}.jpg'))
    img_count += 1
