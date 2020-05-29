# USAGE
# python liveness_demo.py --model liveness.model --le le.pickle --detector face_detector

# import the necessary packages
from imutils.video import VideoStream
from keras.preprocessing.image import img_to_array
from keras.models import load_model
# from keras.models import load_model
# from tensorflow.keras.models import load_model
import numpy as np
import imutils
import pickle
import time
import cv2
import os

confidence_threshhold = 0.5
liveness_threshold = 0.9


def check_liveness(vs, net, model, le):
    # variables used to find the confidence in liveness
    real = 0
    total = 0

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 600 pixels
        res, frame = vs.read()
        if not res:
            break
        frame = imutils.resize(frame, width=600)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > confidence_threshhold:
                # compute the (x, y)-coordinates of the bounding box for
                # the face and extract the face ROI
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ensure the detected bounding box does fall outside the
                # dimensions of the frame
                startX = max(0, startX)
                startY = max(0, startY)
                endX = min(w, endX)
                endY = min(h, endY)

                # extract the face ROI and then preproces it in the exact
                # same manner as our training data
                face = frame[startY:endY, startX:endX]

                face = cv2.resize(face, (32, 32))
                face = face.astype("float") / 255.0
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)
                # pass the face ROI through the trained liveness detector
                # model to determine if the face is "real" or "fake"
                preds = model.predict(face)[0]
                j = np.argmax(preds)
                label = le.classes_[j]

                #print("prediciton: ", preds, "confidence: ", confidence, 'label: ', label) #Debug
                
                if label == 'real':
                    real += 1 * confidence
                total += 1

                
                # draw the label and bounding box on the frame
                label = "{}: {:.4f}".format(label, preds[j])
                cv2.putText(frame, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                

        # show the output frame and wait for a key press
        
        '''
        #Debug
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        '''
        
    return float(real) / total if total > 0 else 0


def detect_liveness(path):
    # load our serialized face detector from disk
    print("[INFO] loading face detector...")
    
    protoPath = os.path.sep.join(["liveness", "face_detector", "deploy.prototxt"])
    modelPath = os.path.sep.join(["liveness", "face_detector",
                                  "res10_300x300_ssd_iter_140000.caffemodel"])
    '''
    #Direct testing
    protoPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
    modelPath = os.path.sep.join(["face_detector",
                                  "res10_300x300_ssd_iter_140000.caffemodel"])
    '''


    net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    # load the liveness detector model and label encoder from disk
    print("[INFO] loading liveness detector...")
    
    model = load_model("./liveness/liveness.model")
    le = pickle.loads(open("./liveness/le.pickle", "rb").read())
    '''
    #Direct testing
    model = load_model("liveness.model")
    le = pickle.loads(open("le.pickle", "rb").read())
    '''

    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(path)  # TODO: Changed to path to video
    # time.sleep(2.0)

    res = check_liveness(vs, net, model, le)

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.release()

    return res >= liveness_threshold
