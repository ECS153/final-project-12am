# Lively: Facial Liveness Dectection and Recognition
A simple login authentication interface for iOS/Android app which recognizes and detects facial liveness of an user.

## Table of contents
* [General Info](#general-info)
* [Setup](#setup)
* [Repo Structure](#repo-structure)
* [Code Structure](#code-structure)
* [Significance and Result](#significance-and-result)

## General Info 
This is a project created by Team12AM, Huyen Pham, Linda Li, Tim Van and Liyin Li. It contains two main components. An frontend app which uses REACT Native and a Flask server as backend which encapsulates the two detection models. User can test the project through running the Expo app on iOS/Android phone or running the flask app on desktop.

## Repo Structure
```
final-project-12am /
  |- README.md
  |- proposal.md
  |- milestones.md
  |- design_docs.md
  |- final-presentation-12am.mp4
  |- faceID-frontend
    |- App.js
    |- ... 
  |- backend	
    |- server
      |- media
          |- images
          |- videos
      |- data
        |- Kenny
          |- frame1.jpg
          |- ...
      |- liveness
          |- liveness_detector.py
          |- ...
      |- detector.py
      |- templates
      |- app.py
      |- utils.py
      |- requirement.txt
```

## Code Structure
  - Frontend code is in folder `./faceID-frontend`.
  - Backend code is in folder `./backend/server` which contains two detectors. Facial recognition is in `detector.py` which uses Micorsoft Azure Face service. Liveness detection is in `liveness/liveness_detector.py`.

## Setup and Testing
To test the project, follow the instructions for fronend/backend repspectively to setup.

### For front end:

  - Run Expo to test on iOS/Android device
  
    1. Install locally using npm
        - go to directory `final-project-12am/faceID-frontend` run `cd ..` and `npm install expo-cli <--global>`

    2. Download Expo Client (in App Store on iphone device)
        - For iOS, open your camera, scan the code from expo bundle on your web browser, then open Expo.
        - For Android, scan the code with the barcode scanner within the Expo Client app.

### For backend:

  - Run Flsk api the two detection components to test on desktop
  
    1. Set up virtual environment LOCALLY (one dir above the whole project dir)
        - run `python -m venv venv`

    2. Activate your virtual environment    
        - run `source venv/bin/activate`
        - succeeded installed example: `(venv) KennydeMacBook-Pro:backend kennyli$` 
        - deactivaten by `deactivate venv`

    3. Install dependencies (first navigate to dir with requirements.txt)
        - run `pip install -r requirement`

    4. Run Flask App (first navigate to dir `server`)
        - run `flask run`

    5. *Mac Port-In-Used error
        - find port id: `ps -fA | grep python` 
        - copy the second number of the first line which is the <PID> you need
        - terminate process `sudo lsof -i:8080 | kill <PID>`

    6. *Other dependencies related errors
        - run `pip install <LIB> --upgrade`
        - or run `pip install --upgrade pip`
        
  - Now we can testing different functionality: 
    
    1. Training: 
        - Create or Delete a Person Group: go to `[LOCAL_HOST]/create` or `[LOCAL_HOST]/delete`
        - Train a person data in folder `./backend/server/data/[NAME]`: go to `[LOCAL_HOST]/train`
        
    2. Testing: 
        - Go to `[LOCAL_HOST]`, type the owner name of the trained data and upload a video from desktop 
        - Run the liveness and facial reocognition apis by naviagting to `[LOCAL_HOST]/detect`
        - Check the browser for the detection result
        - "True" means the video is lively and the faces detected belong to the authenticated user
    
## Significance and Result
We were able detect the liveness of the upload video and recognized whether the deteced face(s) in the video belong to a user face that we pretrained upon. However, the detection accuracy was not as high as using the Flask API directly when we were tesing on iOS decide using the Expo app. We found that it was due to the high resolution of the upload video. Since our traning data was limited in our models, detection failures could occur sometimes.
