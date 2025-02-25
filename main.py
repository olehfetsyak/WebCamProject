from colorQuantifier import ColorQuantifier
from captureImage import CaptureImage
from time import sleep
from datetime import datetime
import numpy
import cv2
import os


#vid_path = '/Users/pyProject/WebCamProject/testCam.mjpeg.avi'
#check_image_every = 2  # In Seconds

current_image = CaptureImage("./img/current_image.jpg", '/dev/cu.usbmodem1101', 115200)
approximate_cars = 0

image_text_font = cv2.FONT_HERSHEY_SIMPLEX

save_motion_capture = False
motion_capture_index = 0
video_index = 0

#-------------------- Functions --------------------#

def getImageBatch():
    current_image.captureImage()
    cv2.imwrite("./img/previous_image.jpg", cv2.imread(current_image.getImagePath()))
    sleep(0.3)
    current_image.captureImage()
    sleep(0.3)

def turnImgToArray():
    previous_image = cv2.imread("./img/previous_image.jpg")
    current_image = cv2.imread("./img/current_image.jpg")
   
    height, width, _ = previous_image.shape
    new_size = (int(width * 0.07), int(height * 0.07))

    previous_image = cv2.resize(previous_image, new_size, interpolation=cv2.INTER_AREA)
    current_image = cv2.resize(current_image, new_size, interpolation=cv2.INTER_AREA)

    previous_image = cv2.cvtColor(previous_image, cv2.COLOR_BGR2LAB)
    current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2LAB)
    return previous_image, current_image

def createImageMask(image_mask, image, approximate_cars):
    image_mask = cv2.resize(image_mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    
    _, image_mask = cv2.threshold(image_mask, 127, 255, cv2.THRESH_BINARY)
    image_mask = cv2.medianBlur(image_mask, ksize=3)

    contours, _ = cv2.findContours(image_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if (len(contours) > 0):
            approximate_cars += 1

    masked_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)

    return masked_image, approximate_cars

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
    return 0 if colorDifference.calculateDeltaE() < 15 else 1

def createVideoSnippet(index):
    import os
import cv2

def createVideoSnippet(index):
    image_folder = './video_capture'
    video_name = f'./vid_snippets/{index}.mp4'

    images = sorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])

    first_frame_path = os.path.join(image_folder, images[0])
    first_frame = cv2.imread(first_frame_path)

    height, width, _ = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 1

    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)

        video.write(frame)

        os.remove(img_path)

    cv2.destroyAllWindows()
    video.release()

def  checkForCorruption(img):
    img = cv2.imread(img)
    try:
        
        height, width, _ = img.shape
        new_size = (int(width * 0.07), int(height * 0.07))

        img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    except:
        return 1
    return 0

#-------------------- Main Proccess --------------------#
if __name__ == "__main__":
    getImageBatch() 

    for i in range(36):
        if i > 0:
            cv2.imwrite("./img/previous_image.jpg", cv2.imread("./img/current_image.jpg"))
            current_image.captureImage()

        if (checkForCorruption("./img/current_image.jpg")):
            cv2.imwrite("./img/current_image.jpg", cv2.imread("./img/previous_image.jpg"))
            print("The current captured image was corrupted")

        previous_image_arr, current_image_arr = turnImgToArray()
        
        new_image = []
        for x in range(previous_image_arr.shape[0]):
            row = []
            for y in range(previous_image_arr.shape[1]):
                difference = colorDifference(
                    previous_image_arr[x][y],
                    current_image_arr[x][y]
                )
                row.append(difference)
            new_image.append(row)
        
        masked_image = numpy.array(new_image, dtype=numpy.uint8) * 255
        masked_image, approximate_cars = createImageMask(masked_image, cv2.imread("./img/current_image.jpg"), approximate_cars)

        masked_image_height, masked_image_width, _ = masked_image.shape
        image_with_description = numpy.zeros((30, masked_image_width, 3), dtype=numpy.uint8)

        image_with_description = cv2.putText(image_with_description, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Estimated Cars: {approximate_cars}", 
            (5, 20), 
            image_text_font, 
            0.4,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        image_with_description = numpy.vstack((masked_image, image_with_description))

        cv2.imwrite("./img/motion_capture.jpg", image_with_description)
        cv2.imshow("./img/motion_capture.jpg", image_with_description)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Motion Capture interrupted")
            break
        elif key == ord('s'):
            if (not save_motion_capture):
                print("Saving Motion to video")
            else:
                print("Video Snipper Captured")
                createVideoSnippet(video_index)
                video_index += 1
                motion_capture_index = 0

            save_motion_capture = not save_motion_capture

        if (save_motion_capture):
            cv2.imwrite(f"./video_capture/{motion_capture_index}.jpg", image_with_description)
            motion_capture_index += 1

        sleep(0.5)

    cv2.destroyAllWindows()



#def getImgArray(frame_number, vid_path, max_width, new_frame_number):
#    capture = cv2.VideoCapture(vid_path)
#
#    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
#    _, pixel1 = capture.read()
#    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number + 1)
#    _, pixel2 = capture.read()#

#    #new_frame_number is used to save the image in the same iteration as previous
  #  cv2.imwrite(f'./img/frame{new_frame_number}.jpg', pixel1) 

 # capture.release()

 # height, width, _ = pixel1.shape
 # aspect_ratio = height / width
 # pixel1 = cv2.resize(pixel1, (max_width, int(max_width * aspect_ratio)), interpolation=cv2.INTER_LANCZOS4)
 #   pixel2 = cv2.resize(pixel2, (max_width, int(max_width * aspect_ratio)), interpolation=cv2.INTER_LANCZOS4)
#
  #  pixel1, pixel2 = cv2.cvtColor(pixel1, cv2.COLOR_BGR2LAB), cv2.cvtColor(pixel2, cv2.COLOR_BGR2LAB)
#
  #  return [pixel1, pixel2]
#
#def generateMask(mask_image_path, image_path):
 #   mask_image = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
 #   image = cv2.imread(image_path)
 #   
 #   mask_image = cv2.medianBlur(mask_image, ksize=3) 
 #   # To-Do, move out of function so saved 0.png has blur built in
 #   mask_image = cv2.resize(mask_image, (image.shape[1], image.shape[0]))
 #   
 #   mask = cv2.inRange(mask_image, 1, 255)
#
 #   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
 #   result = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
 #   return result

#def splitFrame(vid_path, time):
#    capture = cv2.VideoCapture(vid_path)
#
#    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
#    fps = int(capture.get(cv2.CAP_PROP_FPS))
#    capture.release()
#
#    return (fps * time, frame_count)

#frame_result = splitFrame(vid_path, check_image_every)
#time_step, total_frames = frame_result[0], frame_result[1]
#img_count = 0
#for i in range(0, total_frames - 1, time_step):
#    pixel_array = getImgArray(i, vid_path, 80, img_count) 
    #To-Do having to pass an unneccesary variable,: img_count
    #print(f"\nFirst Frame:\n{pixelArray[0]}")
    #print(f"\nSecond Frame:\n{pixelArray[1]}")

 #   new_image = []

 #   for x in range(pixel_array[0].shape[0]):
#        row = []
#        for y in range(pixel_array[0].shape[1]):
#            difference = colorDifference(
 #               pixel_array[0][x][y], 
 #               pixel_array[1][x][y]
 #           )
  #          row.append(difference)
  #      new_image.append(row)
 #   #print(new_image)
 #   array = numpy.array(new_image, dtype=numpy.uint8)
 #   image = Image.fromarray(array * 255, mode="L") 

 #   image.save(f"./img/{img_count}.png")

  #  cv2.imwrite(f'./img/result{img_count}.png', generateMask(f'./img/{img_count}.png', f'./img/frame{img_count}.jpg'))
 #   img_count += 1

current_image.closeSerial()