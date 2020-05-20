import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Button } from 'react-native';
import { Camera } from 'expo-camera';
import { render } from 'react-dom';

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [recording, setRecording] = useState(false);
  const [cameraRef, setCameraRef] = useState(null);
  const camera_options = {
    mute: true,
    maxDuration: 1,
  }
  
  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}> Face ID </Text>
      
      <View style={styles.cameraContainer}>
        <Camera style={styles.camera} type={Camera.Constants.Type.front} ref={ref => {
          setCameraRef(ref);
        }}></Camera>
        <TouchableOpacity style={recording ? styles.recorderButtonStarted : styles.recorderButton}
        onPress={async() => {
            setRecording(true);
            const video = await cameraRef.recordAsync(camera_options);
            //console.log('video', video);
            setRecording(false);

            //uploading vid to server
            var formData = new FormData();
            formData.append('file', {
              uri: video.uri,
              name: Date.now().toString() + ".mov"
            });
            
            fetch('https://flask-server12am.herokuapp.com/upload', {
              method: 'POST',
              body: formData
            }).then((res) => {
              res.json().then((result) => {
                console.log(result);
              }).catch(error => {
                console.log("Inner Error ", error);
              })
            }).catch(err => {
              console.log("Error ", err);
            });

            setRecording(false);
        }}>
        </TouchableOpacity>
      </View>

      <Text style={styles.instructionText}> Please face the camera and press on recording button </Text>
      
    </View>
  );
  
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
    alignItems: 'center',
    //justifyContent: 'center',
  },
  cameraContainer: {
    flex: 0.8,
    alignItems: 'center',
    width: '80%',
    height: '50%',
    backgroundColor: 'black',
    marginBottom: 20,
  },
  title: {
    padding: 60,
    fontSize: 70,
  },
  recorderButton: {
    marginTop: 15,
    borderWidth: 5,
    borderColor: 'white',
    width: 60,
    height: 60,
    borderRadius: 50,
    backgroundColor: 'red',
    alignItems: 'center',
  },
  recorderButtonStarted: {
    marginTop: 15,
    borderWidth: 5,
    borderColor: 'white',
    width: 60,
    height: 60,
    borderRadius: 50,
    backgroundColor: 'black',
    alignItems: 'center',
  },
  camera: {
    width: '100%',
    height: '80%',
  },
  instructionText: {
    width: '80%',
    textAlign: 'center',
  },
});
