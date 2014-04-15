Processing
==========

This folder contains all of the logic for the VLC localization system.

Currently it's a bit of a mess, there's a lot of hard-coded logic and
assumptions, as well as duplicated code. It's on the agenda to modularize this
and clean it up, but things should mostly work (ish).

Currently, the `aoa_full.py` script will do end-to-end localization for an
image captured on our testbed.
