# 1. what problem are you solving:

The problem statement we are tackling is a lack of depth detection on low-end phones with facial detection. The lack of a depth sensor prevents the facial recognition software from differentiating between a picture of the user and the user themselves. The threat model and assumptions within this problem statement is that the attacker has access to the user’s photos or videos (either through social media or other means), physical access to the user’s phone (stolen or otherwise), and that the attacker does not have extensive knowledge about computer security.

# 2. why is it important:

This is important as most phones do not have depth sensors, especially on the low/budget end, which includes more affordable android phones and iPhones (iPhone SE 2020, iPhone 8, etc.). With market trends increasingly shifting towards facial biometrics as opposed to the fingerprints, this project serves to aid in the transition at the low end using only the camera and computer vision.

# 3. what do you plan to build:

We plan to build a component/API that leverages Computer Vision and ML to determine if a subject is a photo or a real human, or the subject’s “liveness.” This API will then be used in conjunction with existing facial recognition software to build a more robust system to protect against intrusions with the user’s photos. The final product will be called Lively, a facial detection system with a liveness detector.

# 4. what are your expected results:

The result of this project is that we should have a working app that showcases a facial recognition system that cannot be tricked by a photo. Due to assumptions made about the attacker, it will not defend against realistic masks (even iPhone’s FaceID does not defend against this). Furthermore, the attacker does not have the technical capacity to create a false API response (operating system is uncompromised). 
