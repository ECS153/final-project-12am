import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Button } from 'react-native';
import { Camera } from 'expo-camera';
import { render } from 'react-dom';

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);

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
        <Camera style={styles.camera} type={Camera.Constants.Type.front}></Camera>
        <TouchableOpacity style={styles.recorderButton}></TouchableOpacity>
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
  camera: {
    width: '100%',
    height: '80%',
  },
  instructionText: {
    width: '80%',
    textAlign: 'center',
  },
});
