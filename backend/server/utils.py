import cv2
import os


def get_frames(user_name):
    """
        Get frames from .mp4 file
        sources: https://www.geeksforgeeks.org/extract-images-from-video-in-python/
    """

    # The fps of .MOV is around 5 times of the fps of .mp4
    # cam = cv2.VideoCapture('./media/video/linda-real.mp4')
    cam = cv2.VideoCapture('./media/test/sample1.mp4')

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
                file_name = './data/' + user_name + '/frame' + str(round(currentframe / 10)) + '.jpg'
                print('Creating...' + file_name)
                cv2.imwrite(file_name, frame)
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


def delete_frames():
    pass
