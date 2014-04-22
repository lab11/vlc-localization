Processing
==========

This folder contains all of the logic for the VLC localization system.

Things are still a bit in flux, but things are starting to separate out cleanly.


Installation
------------

### Mac OS X

```
sudo port install py27-numpy py27-scipy
sudo port install opencv +python27
sudo pip install termcolor matplotlib
```

### Ubuntu

```
sudo apt-get install python-opencv python-scipy
sudo pip install termcolor matplotlib
```

### Fedora

```
sudo yum install opencv-python scipy python-matplotlib
sudo pip install termcolor
```

Usage
-----


    ./run.py


Command line usage:

```
./run.py --help
usage: run.py [-h] [-f FILENAME] [-c CAMERA] [-m METHOD] [-r ROOM]
              [--only-image]

Program Action: Run image processing

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        image to process
  -c CAMERA, --camera CAMERA
                        phone type; must be in phones/
  -m METHOD, --method METHOD
                        image processing method; must be in processors/
  -r ROOM, --room ROOM  room the image was taken in; must be in rooms/
  --only-image          stop after image processing (do not attempt
                        localization)

Control debug level with DEBUG evinronment environment variable.
  Default: no debugging
  DEBUG=1: print debugging information
  DEBUG=2: print debugging information and write out intermediate images to /tmp (slow)
```

Camera Data
-----------

Camera-specific data is stored in `phones/<phone>/<camera>`. Cameras must define:
 * `Zf`: Focal length in pixels.
  * The focal length is the distance from the imager to the center of the lens.
    This distance should be reported in pixels relative the imager used by this
    camera.
 * `rolling_shutter_r`: The column scan rate in seconds.
  * This is the speed of the rolling shutter for this camera. This is a
    reasonably easy value to measure given a high-quality image of a transmitter
    of a known frequency, we should probably add a configuration tool for this.

Room Data
---------

Room-specific data is stored in `rooms/<room>`. A room is defined by a mapping
of transmitter frequencies to locations in 3d space. A frequency may specify
multiple locations if there are multiple transmitters with the same frequency in
the same room. The localization algorithm will automatically select the most
likely set of transmitters seen (defined as the set of locations with the
smallest bounding box).

Processing
----------

There are a few competing image processing methods we are exploring, in
particular for maximizing the recoverability of the transmitted frequency. These
are found in the `processing/` folder and a method can be selected using the
`-m` flag.

Localization
------------

Our localization scheme relies on some basic geometry and lens optics. Each
transmitter projects an image along a straight ray onto the imager (camera)
plane. Each transmitter (_t<sub>0</sub>_) can be expressed as coordinates in
both the transmitter coordinate system (_x<sub>0</sub>_, _y<sub>0</sub>_,
_z<sub>0</sub>_) and its projection (_t'<sub>0</sub>_) the imager coordinate
system (_u<sub>0</sub>_, _v<sub>0</sub>_, _w<sub>0</sub>_). For each pair, there
is a distinct scaling factor (_K<sub>0</sub>_) that maps
_t'<sub>0</sub>_&nbsp;&#8594;&nbsp;_t<sub>0</sub>_. The goal is to solve for
these scaling factors (_K_'s). Once we have a translation between coordinate
systems, we can use some basic geometry to solve for the camera's location and
orientation with respect to the transmitters.

Our current solution `aoa.py` solves this by computing the pairwise difference
between each of the transmitters using their "native" coordinates and their
coordinates from the pixel plane translated into the transmitter coordinate
plane and then minimizing the difference between these two. This is a fairly
standard technique borrowed from the robotics / vision community, but we have
some extra heuristics in place to try to deal with the fact that lights are
often found in grid patterns, which can cause location estimates to get stuck in
local minima (in particular reflections across axes formed by the transmitter
grid; the problem is exacerbated when the camera is near co-linear with such an
axis).

The `aoa_full.py` script stitches the image processing and localization
together. It's biggest responsibility is mapping the estimated frequencies to
transmitter coordinates.
