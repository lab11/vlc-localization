VLC Localization
================

The goal of this project is to address the indoor localization problem. Our
system achieves centimeter-scale accuracy using unmodified commercial
smartphones as receivers and commercial LED bulbs (with some minor
modifications) as transmitters.

In principle, the LED lights act like stars in the sky and depending on the
angle and orientation of visible constellations, the phone can recover its
location. The key insight was in finding a way to "label" the stars so the phone
can identify them. CMOS imagers use a rolling shutter, capturing a frame
line-by-line instead of in one shot. By duty-cycling each LED lights at a unique
frequency, the smartphone camera can detect each frequency while remaining
imperceptible to room occupants.

For more detail on the theory and technique, please see our [paper from MobiCom
2014](http://lab11.eecs.umich.edu/content/pubs/kuo14luxapose.pdf).

System Overview
---------------

To build an end-to-end localization demo requires pulling together a few pieces:

 * LED Light Sources
  * Instructions for building your own LED light sources or modifying existing
    commerical sources can be found in `lights/`
 * Image Capture
  * You will need a camera with a reasonably high resolution and the
    ability to manually fix ISO and exposure values. The exposure value is
    particularly important, anything slower than 1/8000 sec will not work.
  * We have built applications for Windows Phone 8 and iOS that will capture
    and upload images (see `apps/`).
 * Image Processing
  * `processing/image_proc.py`
  * This step scans a captured image, identifies each transmitter, and
    outputs a set of labeled coordinates (`tx_freq :: (px_x, px_y)`). These
    coordinates are in the pixel coordinate system of the captured image.
 * Localization
  * `processing/localize.py`
  * This step requires out-of-band knowledge of the transmitter locations.
    It takes a set of transmitter labels and coordinates in the
    transmitter coordinate system (e.g. meters) and the coordinates from
    the image processing step and solves for the image capture device's
    location in the transmitter coordinate system.
 * Cloud Service
  * `cloud_service/`
  * We have a very basic cloudlet app that will accept image uploads, process
    the image, and report localization results to [gatd].
 * Visualization
  * We have some initial visualization ideas in the `web/` folder. They
    rely on our cloud service and [gatd][gatd].

[gatd]: https://github.com/lab11/gatd/ "GATD Homepage"
