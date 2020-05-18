import asyncio
import io
import glob
import os
import sys
import time
import uuid
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
PERSON_GROUP_ID = 'mygroup'

# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4())  # assign a random ID (or name it anything)


def get_rectangle(face_dict):
    # Convert width height to a point in a rectangle
    rect = face_dict.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return (left, top), (right, bottom)


class Analyzer:
    def __init__(self):
        # Create an authenticated FaceClient.
        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        # Detect a face in an image that contains a single face
        self.single_face_image_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
        self.single_image_name = os.path.basename(self.single_face_image_url)
        self.face_ids = []
        self.image = ''

    def detect(self):
        detected_faces = self.face_client.face.detect_with_url(url=self.single_face_image_url)
        if not detected_faces:
            raise Exception('No face detected from image {}'.format(self.single_image_name))

        # Optional:
        # Save this ID for use in Find Similar
        first_image_face_ID = detected_faces[0].face_id

        return detected_faces

    def show_face_img(self, faces):
        # Download the image from the url
        response = requests.get(self.single_face_image_url)
        img = Image.open(BytesIO(response.content))

        # For each face returned use the face rectangle and draw a red box.
        print('DEBUG: Drawing rectangle around face... see popup for results.')
        draw = ImageDraw.Draw(img)
        for face in faces:
            draw.rectangle(get_rectangle(face), outline='red')

        img.show()

    def get_train_data(self):
        print("DEBUG: In init_train_data()")
        # 1. Create the PersonGroup

        # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
        print('Person group:', PERSON_GROUP_ID)
        self.face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

        # Define woman friend
        woman = self.face_client.person_group_person.create(PERSON_GROUP_ID, "Woman")
        man = self.face_client.person_group_person.create(PERSON_GROUP_ID, "Man")
        child = self.face_client.person_group_person.create(PERSON_GROUP_ID, "Child")

        # 2. Detect faces and register to correct person

        # Find all jpeg images of friends in working directory
        woman_images = [file for file in glob.glob('*.jpg') if file.startswith("woman")]
        man_images = [file for file in glob.glob('*.jpg') if file.startswith("man")]
        child_images = [file for file in glob.glob('*.jpg') if file.startswith("child")]

        # Add to a woman person
        for image in woman_images:
            w = open(image, 'r+b')
            self.face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, woman.person_id, w)

        # Add to a man person
        for image in man_images:
            m = open(image, 'r+b')
            self.face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, man.person_id, m)

        # Add to a child person
        for image in child_images:
            ch = open(image, 'r+b')
            self.face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, child.person_id, ch)

    def train_data(self):
        print("DEBUG: In train_data()")
        # Train PersonGroup
        print('DEBUG: Training the person group...')
        self.face_client.person_group.train(PERSON_GROUP_ID)

        while True:
            training_status = self.face_client.person_group.get_training_status(PERSON_GROUP_ID)
            print("DEBUG: Training status: {}.".format(training_status.status))
            if training_status.status is TrainingStatusType.succeeded:
                break
            elif training_status.status is TrainingStatusType.failed:
                sys.exit('Training the person group has failed.')
            time.sleep(5)

    def get_test_data(self):
        print("DEBUG: In get_test_data()")
        # Identify a face against a defined PersonGroup

        # Group image for testing against
        group_photo = 'test-image-person-group.jpg'
        IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        print('DEBUG: IMAGES_FOLDER = ', IMAGES_FOLDER)

        # Get test image
        test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
        # self.image = open(test_image_array[0], 'r+b')
        test_image = open(test_image_array[0], 'r+b')
        # print('DEBUG: type = ', type(test_image))

        # Detect faces
        faces = self.face_client.face.detect_with_stream(test_image)
        for face in faces:
            self.face_ids.append(face.face_id)

        print('DEBUG: ids = ', self.face_ids)

        print("DEBUG: In identify()")

        # Identify faces
        results = self.face_client.face.identify(self.face_ids, PERSON_GROUP_ID)
        print('DEBUG: Identifying faces in {}'.format(os.path.basename(test_image.name)))
        if not results:
            print(
                'No person identified in the person group for faces from {}.'.format(os.path.basename(test_image.name)))
        for person in results:
            print('DEBUG: Person for face ID {} is identified in {} with a confidence of {}.' \
                  .format(person.face_id, os.path.basename(test_image.name),
                          person.candidates[0].confidence))  # Get topmost confidence score

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
