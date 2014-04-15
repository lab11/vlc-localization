Camera Explorer
===============

This application is built by modifying the (extremely useful) Nokia
[Camera Explorer](https://github.com/nokia-developer/camera-explorer) app.

Our modified application was built for an ongoing research project, it is not
remotely production-quality, but should build and run correctly at least on
Lumia-brand phones, if not all Windows Phones.

The additions that our app makes are:
 * The ability to upload (POST) pictures to a url
 * Show the full range of Lumia-powered camera settings (requires Nokia-specific API)
 * A 'continous-sample' mode that will take and upload pictures as fast as it can

The remainder of this README is from the original Nokia project and should be
sufficient to get things up an running.

For more information on implementation and porting, visit Nokia Lumia
Developer's Library:
http://developer.nokia.com/Resources/Library/Lumia/#!imaging/advanced-photo-capturing/camera-explorer.html


1. Instructions
-------------------------------------------------------------------------------

This is a simple build-and-run solution. Learn about Windows Phone 8
camera features by trying out the application. 

**Building and deploying to phone**

In Windows Phone 8 SDK:

1. Open the SLN file: File > Open Project, select the file `CameraExplorer.sln`.
2. Select the target 'Device'.
3. Press F5 to build the project and run it on the device.

Please see official documentation for deploying and testing applications on
Windows Phone devices:
http://msdn.microsoft.com/en-us/library/gg588378%28v=vs.92%29.aspx


2. Implementation
-------------------------------------------------------------------------------

**Folders:**

* The root folder contains the project file, the license information and this
  file (release_notes.txt).
* `CameraExplorer`: Root folder for the implementation files.
 * `Assets`: Graphic assets like icons and tiles.
 * `Properties`: Application property files.
 * `Resources`: Application resources.


**Important files and classes:**

| File | Description |
| ---- | ----------- |
| MainPage.xaml(.cs) | The main page with viewfinder and overlays. |
| SettingsPage.xaml(.cs) | The page that is used to modify camera parameters. |
| Parameter.cs | Implementations for binding. |
| RangeParameter.cs | PhotoCameraDevice API properties to XAML. |
| ArrayParameter.cs | controls in the SettingsPage UI. |


**Required Capabilities:**


* `ID_CAP_ISV_CAMERA`
* `ID_CAP_MEDIALIB_PHOTO`


3. License
-------------------------------------------------------------------------------

See the license text file delivered with this project. The license file is also
available online at 
https://github.com/nokia-developer/camera-explorer/blob/master/Licence.txt


4. Related documentation
-------------------------------------------------------------------------------

An article "Advanced Photo Capturing" published on Nokia Lumia Developer's Library
(http://www.developer.nokia.com/Resources/Library/Lumia/#!advanced-photo-capturing.html) 
describes the usage of PhotoCaptureDevice properties in more detail.


5. Version history
-------------------------------------------------------------------------------

* Version 1.3.1: Minor bug fixes.
* Version 1.3: Support for devices without front camera, flash setting fixed,
  half-pressing camera key now reactivates auto-focus after tap-to-focus,
  settings (for each sensor) are now persistent.
* Version 1.2: Bug fix to tap-to-focus (Ticket #5).
* Version 1.1: Tap-to-focus and Lens Picker integration added.
* Version 1.0: The first release.
