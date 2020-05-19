import asyncio
import io
import glob
import os
import sys
import time
import uuid
import random
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import (
    TrainingStatusType,
    Person,
    SnapshotObjectType,
    OperationStatusType,
)

# TODO: change the image to static
# TODO: set up PersonGroup

# MS Face Recognition
os.environ['FACE_SUBSCRIPTION_KEY'] = '50aaf75a5e464e1abb264a7aec7414c2'
os.environ['FACE_ENDPOINT'] = 'https://mycsresourceface.cognitiveservices.azure.com/'

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']

# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'linda'

# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4())  # assign a random ID (or name it anything)


class Analyzer:
    def __init__(self, name, test=1):
        # Create an authenticated FaceClient.
        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        # Detect a face in an image that contains a single face
        if test:
            self.videos_frames_test = [file for file in glob.glob('./data/' + name + '/*.jpg')]
            self.videos_frames_test = random.sample(self.videos_frames_test, k=10)
        else:
            self.videos_frames_train = [file for file in glob.glob('./data/' + name + '/*.jpg')]
            self.videos_frames_train = random.sample(self.videos_frames_train, k=10)
        self.face_ids = []
        self.image = ''
        self.name = name

    def create(self):
        # 1. Create the PersonGroup
        # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
        self.face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

    def detect(self, image):
        img = open(image, 'r+b')
        faces = self.face_client.face.detect_with_stream(img)
        face_ids = []
        for face in faces:
            face_ids.append(face.face_id)
        return face_ids

    def get_train_data(self):
        # Define me
        me = self.face_client.person_group_person.create(PERSON_GROUP_ID, self.name)

        # 2. Detect faces and register to correct person
        print(len(self.videos_frames_train))
        for image in self.videos_frames_train:
            w = open(image, 'r+b')
            if self.detect(image):
                print(image)
                self.face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, me.person_id, w)
            else:
                print(image, "no face detected")

    def train_data(self):
        # Train PersonGroup
        self.face_client.person_group.train(PERSON_GROUP_ID)
        while True:
            training_status = self.face_client.person_group.get_training_status(PERSON_GROUP_ID)
            if training_status.status is TrainingStatusType.succeeded:
                break
            elif training_status.status is TrainingStatusType.failed:
                sys.exit('Training the person group has failed.')
            time.sleep(5)

    def identify(self):
        # Identify a face against a defined PersonGroup
        confidence_sum = 0
        valid_num = 0
        for img in self.videos_frames_test:
            # Detect faces
            face_ids = self.detect(img)
            if not face_ids:
                continue
            valid_num += 1
            # Identify faces
            results = self.face_client.face.identify(face_ids, PERSON_GROUP_ID)
            confidence_list = [person.candidates[0].confidence for person in results]
            confidence = max(confidence_list)
            confidence_sum += confidence
        average_confidence = confidence_sum / valid_num

        print('Confidence level that the person in the video is me:',
                          average_confidence)  # Get topmost confidence score

    def delete(self):
        # Delete the main person group.
        self.face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)

    def verify(self, source_image=None, target_image=None):
        """
        :param source_image: image detect upon
        :param target_image: image compare against
        :return: confidence of whether the two persons are the same
        """
        source_image = 'sample1.jpg'
        target_image = 'frame0.jpg'

        # Detect face on two images and get face_id respectively
        source_image_fd = open('./media/images/' + source_image, 'r+b')
        target_image_fd = open('./data/' + target_image, 'r+b')
        detected_faces = self.face_client.face.detect_with_stream(source_image_fd)
        source_image_id = detected_faces[0].face_id
        detected_faces = self.face_client.face.detect_with_stream(target_image_fd)
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
