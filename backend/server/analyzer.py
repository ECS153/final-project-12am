import glob
import os
import sys
import time
import random
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import (
    TrainingStatusType,
    Person,
    SnapshotObjectType,
    OperationStatusType,
)

from liveness.liveness_detector import *

# MS Face Recognition
os.environ['FACE_SUBSCRIPTION_KEY'] = '50aaf75a5e464e1abb264a7aec7414c2'
os.environ['FACE_ENDPOINT'] = 'https://mycsresourceface.cognitiveservices.azure.com/'

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']
TRAIN_DATA_NUM = 8


class Analyzer:
    def __init__(self, name):
        # Create an authenticated FaceClient.
        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        # Initialize testing/training data
        self.videos_frames = [file for file in glob.glob('./data/' + name + '/*.jpg')]
        self.videos_frames = random.sample(self.videos_frames, k=TRAIN_DATA_NUM)
        self.person_group_id = name.lower()  # must be lower case, alphanumeric, and/or with '-', '_'.
        self.person_id = name.lower()
        self.name = name

    def create(self):
        """
        Create a PersonGroup and a Person.
        """
        print("DEBUG: Person created: ",self.person_group_id)
        self.face_client.person_group.create(person_group_id=self.person_group_id, name=self.person_group_id)

    def detect(self, image):
        """
        Detect faces in a image.
        :return: detected face ids list
        """
        image_fd = open(image, 'r+b')
        faces = self.face_client.face.detect_with_stream(image_fd)
        face_ids = []
        for face in faces:
            face_ids.append(face.face_id)
        return face_ids

    def get_train_data(self):
        # Detect faces and register to correct person
        me = self.face_client.person_group_person.create(self.person_group_id, self.person_id)
        print("DEBUG: Person created: ", self.person_group_id, "person ID: ",self.person_id)
        print("MY ID: ",me.person_id)
        for image in self.videos_frames:
            image_fd = open(image, 'r+b')
            if self.detect(image):
                # print("person_ID:",me.person_id)
                self.face_client.person_group_person.add_face_from_stream(self.person_group_id, me.person_id, image_fd)
            else:
                print(image, "no face detected")

    def train(self):
        """
        Train a defined PersonGroup.
        """
        self.face_client.person_group.train(self.person_group_id)
        while True:
            training_status = self.face_client.person_group.get_training_status(self.person_group_id)
            if training_status.status is TrainingStatusType.succeeded:
                break
            elif training_status.status is TrainingStatusType.failed:
                sys.exit('Training the person group has failed.')
            time.sleep(5)

    def identify(self):
        """
        Identify a face against a defined PersonGroup.
        :return: average confidence of identified faces in input frames (against PersonGroup)
        """
        confidence_sum = 0
        valid_num = 0
        for img in self.videos_frames:
            # Detect faces
            face_ids = self.detect(img)
            if not face_ids:
                continue

            # Identify faces
            print("DEBUG: person group ID Identify",self.person_group_id)
            results = self.face_client.face.identify(face_ids, self.person_group_id)
            confidence_list = [] # initial val in case confidence_list is empty
            for person in results:
                if person.candidates:
                    confidence_list.append(person.candidates[0].confidence)
            if confidence_list:
                confidence = max(confidence_list)
                valid_num += 1
                confidence_sum += confidence
        if confidence_sum == 0:
            average_confidence = 0
        else:
            average_confidence = confidence_sum / valid_num
        print('Confidence level that the person in the video is me:', average_confidence)
        return average_confidence

    def delete(self):
        """
        Delete the main person group.
        """
        self.face_client.person_group.delete(person_group_id=self.person_group_id)

    def verify(self, source_image=None, target_image=None):
        """
        Verify whether the two faces in source and target are the same person.
        :param source_image: image detect upon
        :param target_image: image compare against
        :return: confidence of whether the two persons are the same
        """
        source_image = 'sample1.jpg'
        target_image = 'frame0.jpg'

        # Detect face on two images and get face_id respectively
        detected_faces = self.detect('./media/images/' + source_image)
        source_image_id = detected_faces[0].face_id
        detected_faces = self.detect('./data/' + target_image)
        target_faces_id = detected_faces[0].face_id
        print('{} face(s) detected from image {}.'.format(len(detected_faces), source_image))

        # Verification for faces of the same person
        verify_result_same = self.face_client.face.verify_face_to_face(source_image_id, target_faces_id)
        print('Faces from {} & {} are of the same person, with confidence: {}'
              .format(source_image, target_image, verify_result_same.confidence)
              if verify_result_same.is_identical
              else 'Faces from {} & {} are of a different person, with confidence: {}'
              .format(source_image, target_image, verify_result_same.confidence))
        return verify_result_same.confidence

    @staticmethod
    def detect_liveness(path):
        print("DEBUG: detecting livenese of file, ", path)
        res = detect_liveness(path)
        print("DEBUG: liveness result = ", res)
        if res:
            return True
        return False
