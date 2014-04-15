Cloud Service
=============

This is a basic service that stitches together the pieces of our VLC pipeline.
It will accept image uploads from our app, run them through our processing steps
and then emit a localization result for that image. Results are both printed to
stdout and sent to [gatd][gatd].

Images are saved in `img/` and processing output / results are saved in `result/`.

[gatd]: https://github.com/lab11/gatd/ "GATD Homepage"
