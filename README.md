## PythonSample

PythonSample is a python application which uses Deezer's Native SDK to play a song once a user was authenticated.

### Features

 - User authentication
 - Playing a Deezer content (track, album or playlist).

### Build instructions

* Download the latest version of the [Deezer Native SDK][1]
* Unzip it and place the folder, renamed into NativeSDK, at the root of this repository, such as shown below:
```
<native-sdk-samples>
├── NativeSDK
│      ├── Bins
│      └── Include
├── PythonSample
└── README.md
```

### Run this sample

```
> python app_start.py dzmedia:///CONTENT/CODE
```

To view a list of examples for the parameter:

```
> python app_start.py
```

 [1]: http://developers.deezer.com/sdk/native
