# Utilities

- [Utilities](#utilities)
  - [Compress Shoulder](#compress-shoulder)
  - [Compress Toe](#compress-toe)
  - [Matrix Tools](#matrix-tools)
  - [Range Compress](#range-compress)


## Compress Shoulder
A couple of useful tonemapping operations which might serve you better than the `SoftClip` node. All curve types have the same controls:
- threshold: only values above this threshold will be affected.
- limit: the value which infinity is remapped to.

## Compress Toe
Similar to the CompressShoulder operator, but works on the toe, or shadow area of the image instead of the shoulder.or highlight area.


## Matrix Tools
![Matrix Tools](/images/MatrixTools_ui.png)

MatrixTools is a utility node that allows you to combine two or more 3x3 ColorMatrix nodes into one. It can also calculate the inverse of a single matrix. It can also pop up a window with the matrix in different formats, which is useful for pasting the matrix into an OCIO config for example. Better than copying the values from each cell individually! You can also save and load spimtx format files.


## Range Compress
Logarithmically compress values above 0.18 and below -0.18. Inspired by the [rangecompress function](https://github.com/OpenImageIO/oiio/blob/master/src/libOpenImageIO/imagebufalgo_pixelmath.cpp) in [OpenImageIO](https://github.com/OpenImageIO), which is used to compress overbrights in scene-linear for applying image filters with a sharpening component, or negative lobes. One would apply this as follows: RangeCompress -> Filter -> Inverse RangeCompress.

