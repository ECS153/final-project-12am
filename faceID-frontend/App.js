import React, { useState, useEffect } from 'react';
import 'react-native-gesture-handler';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StyleSheet, Text, View, TouchableOpacity, Alert, Button, TextInput } from 'react-native';
import { Camera } from 'expo-camera';



function Name({navigation}) {
  const [text, setText] = useState('');
  
  return (
    <View style={styles.nameView}>
      <Text style={styles.instructionTextForName}>Please Enter Your Username</Text>
      <TextInput
        style={styles.usernameInput}
        placeholder="Type your username here"
        onChangeText={text => setText(text)}
        defaultValue={text}
        maxLength={70}
      />
      <TouchableOpacity onPress={() => {
        if (text=="" || text=="Type your username here") {

        } else {
          navigation.navigate('Cam', {username: text,})
        }
      }}>
        <View style={styles.nextButton}>
          <Text style={styles.buttonText}>
            Next
          </Text>
        </View>
      </TouchableOpacity>
      
    </View>
  );
}

function Cam({route}) {
  console.log("username is ", route.params);
  const [hasPermission, setHasPermission] = useState(null);
  const [recording, setRecording] = useState(false);
  const [cameraRef, setCameraRef] = useState(null);
  const camera_options = {
    mute: true,
    maxDuration: 1,
  };
  
  var createResultAlert = function (alertTitle, alertMsg) {
    Alert.alert(
      alertTitle,
      alertMsg,
      [
        {
          text: "Cancel",
          onPress: () => console.log("Cancel Pressed"),
          style: "cancel"
        }
      ],
      { cancelable: false }
    );
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
              console.log('video', video);
              
              setRecording(false);
          }}>
          </TouchableOpacity>
        </View>

        <Text style={styles.instructionText}> Please face the camera and press on recording button </Text>
        
      </View>
    ); 
  
}

function uploadInfo(username, video) {
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
       const answer = result["result"];
       console.log(answer)
       if (answer == "True") {
         console.log("Accept");
         createResultAlert("Access Granted", "Welcome Back!");
       } else {
         console.log("Denied");
         createResultAlert("Access Denied", "We cannot verify your log in. Please try again with username and password");
       }

     }).catch(error => {
       console.log("Json error ", error);
     })
   }).catch(err => {
     console.log("Error ", err);
   });
}

const Stack = createStackNavigator();
export default function App() {
  
  return (
    <NavigationContainer>
      {/* Rest of your app code */}
      <Stack.Navigator initialRouteName="Username">
        <Stack.Screen name="Cam" component={Cam}/>
        <Stack.Screen name="Username" component={Name} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
// export default function App() {
  
// }

const styles = StyleSheet.create({
  nameView: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  instructionTextForName: {
    fontSize: 20
  },
  usernameInput: {
    minWidth: 200,
    height: 50,
    borderWidth: 1,
    borderColor: "black",
    padding: 10,
    margin: 50
  },
  nextButton: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: 100,
    height: 50,
    borderWidth: 1,
    borderRadius: 10, 
    borderColor: "white",
    backgroundColor: "#89cff0",
    color: "white"
  },
  buttonText: {
    color: "white",
    fontSize: 20
  },
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
