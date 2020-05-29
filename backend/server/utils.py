import cv2
import os, shutil


def get_frames(username, path):
    """
        Get frames from .mp4 file
        sources: https://www.geeksforgeeks.org/extract-images-from-video-in-python/
    """
    username = username.lower()
    folder = 'data/' + username
    # The fps of .MOV is around 5 times of the fps of .mp4
    cam = cv2.VideoCapture(path)
    # Create dir for frames
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError:
        print('Error: Creating directory of data')
    currentframe = 0
    while True:
        ret, frame = cam.read()
        if ret:
            if currentframe % 10 == 0:
                rotateCode = cv2.ROTATE_90_CLOCKWISE
                frame = cv2.rotate(frame, rotateCode)
                filename = './' + folder + '/frame' + str(round(currentframe / 10)) + '.jpg'
                print(filename)
                cv2.imwrite(filename, frame)
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


def clear_frames(username):
    folder = 'data/' + username
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        # print("DEBUG: file path = ", file_path)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))