Apps
====

This folder holds the application development for apps on each of the major
platforms. Currently we only have a Windows Phone app. Neither the Android nor
iOS APIs provide sufficient access to the camera hardware for our application.
In particular, we require the ability to manually set exposure time and ISO
values.

Winphone
--------

Our windows phone application is very alpha-quality, but is capable of capturing
images that work in our system. The app can capture individual images or send a
continuous stream to a server.

The winphone app is maintained by Pat ( @ppannuto ).


iOS
---

The iOS app supports all of the features of the winphone app. In addition, the
iOS app will scan for BLE advertisements. Any advertisement that matches
`luxapose: <location>` will cause the app to pass the `<location>` as a hint
of current location to the cloud service (e.g. to identify which room the phone
is currently in).

The iOS app is maintained by Noah ( @nklugman ).


Android
-------

We do not currently support Android. From a recent e-mail conversation, it looks
like Android 5 may have added the required APIs:

> As for the Android, I think the new version (Lollipop or version 5.0) offers a greater amount of options when it comes to controlling the camera parameters. I mean the exposure time and ISO which are the ones that you also need to control based on your paper. I have read that it can be done using the newly introdunced "android.hardware.camera2" package (https://developer.android.com/reference/android/hardware/camera2/package-summary.html). An example project can be found in the following link: https://github.com/PkmX/lcamera
> However, they claim that these parameters can be set only in the Nexus 5 or 6 but I am not entirely sure about it. You can also have a look at:
> https://developer.android.com/reference/android/hardware/camera2/CaptureRequest.html
> Look for the "SENSOR_SENSITIVITY" and "SENSOR_EXPOSURE_TIME".

Developing an Android app is not currently a priority, however we welcome contributions.

