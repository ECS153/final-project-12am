import cv2
import os


def get_frames():
    """
        Get frames from .mp4 file
        sources: https://www.geeksforgeeks.org/extract-images-from-video-in-python/
    """

    # The fps of .MOV is around 5 times of the fps of .mp4
    # cam = cv2.VideoCapture('./media/video/sample1.mp4')
    cam = cv2.VideoCapture('C:/Users/caiqi/Downloads/video-1589835617.mp4')
	# C:/Users/caiqi/Downloads/video-1589835617.mp4

    # Create dir for frames
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print('Error: Creating directory of data')

    currentframe = 0
    while True:
        ret, frame = cam.read()
        if ret:
            if currentframe % 10 == 0:
                name = './images/Linda/frame' + str(round(currentframe / 10)) + '.jpg'
                print('Creating...' + name)
                cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


