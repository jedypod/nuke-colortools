# Chromaticity Tools

- [Chromaticity Tools](#chromaticity-tools)
  - [Gamut to XYZ](#gamut-to-xyz)
  - [Gamut Convert](#gamut-convert)
  - [Whitepoint](#whitepoint)
  - [Gamut Compress](#gamut-compress)


## Gamut to XYZ
![GamuttoXYZ](/images/GamutToXYZ_ui.png)

Calculates a 3x3 matrix for converting from a source colorspace to CIE XYZ or the inverse. The source colorspace is specified by supplying xy chromaticity coordinates for the R, G, and B primaries as well as the whitepoint. A number of common colorspaces are included in the presets, but you could theoretically make your own!

I coded this based on the AMPAS CTL for purposes of learning. It is similar to the `PrimariesToXYZ` tool that comes with Alex Fry's [ParametricOutputTransform](https://github.com/alexfry/PureNukeACES/blob/master/Transforms/ACES_ODT_ParametricPrototype.nk) node, but rewritten without python callbacks and based on the CTL C++ code instead.


## Gamut Convert
![Gamut Convert](/images/GamutConvert_ui.png)

Similar to [GamutToXYZ](#gamut-to-xyz), but supports an arbitrary output color gamut and chromatic adaptation to convert between different whitepoints. 

GamutConvert calculates a 3x3 matrix given the xy chromaticity coordinates of the R G and B primaries and whitepoints of a source and target color gamut. It also provides the option of calculating a chromatic adaptation transform. Basically the above two tools in one. Many common colorspaces are provided as presets but you can enter your own chromaticity coordinates if you have a colorspace that is missing. 

There is also [a live version](/toolsets/chromaticity/GamutConvert_live.nk) which calculates automatically using a knobChanged python callback if you need this functionality.


## Whitepoint
![Whitepoint](/images/Whitepoint_ui.png)

Chromatic adaptation is the ability of the human eye to achieve constant color appearance under different illumination conditions. A Chromatic Adaptation (CAT) function tries to simulate this behavior by shifting colors to perceptually match under a new color of light.

Whitepoint calculates a 3x3 CAT matrix given a source and target whitepoint as xy chromaticity coordinates. A number of different chromatic adaptation methods are provided, such as Bradford, Cat02, CmcCat2000, Sharp, and vonKries.

The node also supports calculating an xy coordinate from a blackbody color temperature on the planckian locus, and also sampling an arbitrary color from an input image. (Hopefully something resembling a neutral color or your results may vary!)


## Gamut Compress
![Gamut Compress](/images/GamutCompress_ui.png)
This tool compresses out of gamut colors back into gamut. See the [full github repo here](https://github.com/jedypod/gamut-compress).

**Background**

Out of gamut colors can ocurr with modern digital cinema cameras.  Using the original camera gamut, there would be no problem, but often when doing visual effects or grading, we need to work in a different colorspace like ACEScg. Since ACEScg is designed to operate within the spectral locus, this is where out of gamut colors can appear

Cameras can generate color outside of the spectral locus because the spectral response curves of the camera do not match the spectral response curves of the human eye, making the camera a  non-colorimetric device which does not satisfy the Luther-Ives criterion.

Out of gamut colors often ocurr with highly saturated light sources like police lights, neon, or lasers. Re-mapping these colors back into gamut is necessary for pleasing color reproduction, and for working

**Usage**

Method specifies the type of compression curve to use. Tanh is a hyperbolic tangent function which has a very  smooth rolloff. This method tends to preserve the appearance of colors very well. Simple has a more aggressive slope, and tends to change the appearance of colors a bit more, but can be good when used with creative intent
Threshold is the percentage of the core gamut to affect. A value of 0 would be a hard clip, a value of 0.2 would affect  the outer 20% of the gamut's most  saturated colors

The cyan / magenta / yellow limits allow you to adjust the amount of compression per color component.  For example increasing the magenta limit will push blues more cyan. A value of 0 is no compression. A value of 1 compresses asymptotically to the gamut boundary. And values above 1 up to a max of 1/(1-threshold) will compress more than the  gamut boundary. Note a value at max will be a hard clip at the  gamut boundary and is probably not something you want

Inverting the gamut compression is also possible but should be used with an excess of caution. An exact inversion doesn't appear to be possible if you only have the gamut compressed source image, due to rounding errors and the asymptotic behavior of the compression functions. You can get an exact inversion if you use the original source image as an extra input however.

**About** 

This tool was [built with help](https://community.acescentral.com/t/rgb-saturation-gamut-mapping-approach-and-a-comp-vfx-perspective) from the [ACES Gamut Mapping Virtual Working Group](https://community.acescentral.com/c/aces-development-acesnext/vwg-aces-gamut-mapping-working-group)
