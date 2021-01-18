# Color Models

A [color models](https://en.wikipedia.org/wiki/Color_model) is an abstract mathematical model describing the way colors can be represented as tuples of numbers. We are used to working with RGB colorspaces like ACEScg or sRGB. These colorspaces use the RGB color model. There are many other ways to represent and encode color like `HSV` or `L*a*b*`. Different color models have different utility for image processing.

These nodes were implemented referencing the various whitepapers and other resources, as well as the [models module](https://github.com/colour-science/colour/tree/develop/colour/models) of the fantastic [colour-science python library](https://www.colour-science.org/)

- [Color Models](#color-models)
  - [CIE L*a*b*](#cie-lab)
  - [CIELuv](#cieluv)
  - [CIEYxy](#cieyxy)
  - [HSV](#hsv)
  - [HunterLab](#hunterlab)
  - [ICtCp](#ictcp)
  - [IgPgTg](#igpgtg)
  - [IHLS](#ihls)
  - [JzAzBz](#jzazbz)
  - [Oklab](#oklab)
  - [CIE CAM16 UCS](#cie-cam16-ucs)



## [CIE L*a*b*](./ColorModel_CIELab.nk)
[`CIE L*a*b*`](https://en.wikipedia.org/wiki/CIELAB_color_space) is a perceptually uniform opponent color model created by the [CIE](https://en.wikipedia.org/wiki/International_Commission_on_Illumination) in 1976. **L** represents perceptual lightness, **a** represents the red-green axis, **b** represents the blue-yellow axis.

## [CIELuv](./ColorModel_CIELuv.nk)
The [CIE 1976 L*, u*, v* color space](https://en.wikipedia.org/wiki/CIELUV) is a simple transform of the CIE 1931 XYZ colorspace, which aims to achieve increased perceptual uniformity. You may be familiar with this colorspace which is used to create the CIE 1976 u'v' Uniform Chromaticity Scale (UCS) diagram.

## [CIEYxy](./ColorModel_CIEYxy.nk)
Converts from CIE XYZ to CIE xyY colorspace.

## [HSV](./ColorModel_HSV.nk)
A cylindrical color model that represents color as Hue, Saturation, and Value.

## [HunterLab](./ColorModel_HunterLab.nk)
Hunter Lab is a [Richard Hunter's Lab color model](https://en.wikipedia.org/wiki/CIELAB_color_space#Hunter_Lab), similar to `CIE L*a*b*`

## [ICtCp](./ColorModel_ICtCp.nk)
[ICtCp](https://en.wikipedia.org/wiki/ICtCp) is an opponent color model developed by Dolby Labratories based on the IPT color model from Ebner and Fairchild. **I** represents intensity, **Ct** stands for chroma tritanopia and encodes blue-yellow, **Cp** stands for chroma protanopia, and encodes red-green.

References
- [ICtCp Whitepaper](https://www.dolby.com/us/en/technologies/dolby-vision/ICtCp-white-paper.pdf)
- [REC-BT.2100-2-201807](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2100-2-201807-I!!PDF-E.pdf)

## [IgPgTg](./ColorModel_IgPgTg.nk)
IgPgTg is a recent color model developed by the Munsell Color Science Labratory, described in the paper [Using Gaussian Spectra to Derive a Hue-linear Color Space by Luke Hellwig and Mark D. Fairchild](https://www.ingentaconnect.com/content/ist/jpi/2020/00000003/00000002/art00002?crawler=true&mimetype=application/pdf). Similar to IPT, it is a hue-uniform colorspace useful for gamut mapping applications.

## [IHLS](./ColorModel_IHLS.nk)
IHLS is a color model similar to HSV, except that it does not construct a cylindrical representation of saturation, instead opting for a more simple hexagonal representation. Based on the paper ["A 3D-polar Coordinate Colour Representation Suitable for Image Analysis" by Allan Hanbury and Jean Serra](https://www.researchgate.net/publication/243602454_A_3D-Polar_Coordinate_Colour_Representation_Suitable_for_Image_Analysis).

## [JzAzBz](./ColorModel_JzAzBz.nk)
JzAzBz is a perceptually uniform colorspace described in the paper ["Perceptually uniform color space for image signals including high dynamic range and wide gamut"](https://www.osapublishing.org/oe/fulltext.cfm?uri=oe-25-13-15131&id=368272). It has good iso-hue linearity.
https://observablehq.com/@jrus/jzazbz
https://downloads.bbc.co.uk/rd/pubs/whp/whp-pdf-files/WHP283.pdf


## [Oklab](./ColorModel_Oklab.nk)
Oklab is a perceptually uniform colorspace for image processing developed by Björn Ottosson, described in his post ["The Oklab Colorspace"](https://bottosson.github.io/posts/oklab/). 

## CIE CAM16 UCS
https://observablehq.com/@jrus/cam16?collection=@jrus/color


A few node implmentations for miscelaneous colorspace conversions. CIE XYZ to CIE Yxy to CIE Luv and back are now possible! There is also [a node](/toolsets/colorspace/Colorspace_IHLS.nk) implementing the [IHLS colorspace](https://www.researchgate.net/publication/243602454_A_3D-Polar_Coordinate_Colour_Representation_Suitable_for_Image_Analysis) which has a reprsentation of saturation more useful for scene linear images.
