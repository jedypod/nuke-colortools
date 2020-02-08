## ACES OutputTransform
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_OutputTransform.png)

The ACES_OutputTransform node applies the ACES output transform, matching the latest [ACES version (v1.2_rc1)](https://github.com/ampas/aces-dev/releases). 

An Inverse OutputTransform node is also supplied, which reverses the output transform back into scene linear. Note that data may be lost depending on the dynamic range and gamut of the display device.
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_OutputTransform_graph.png)

I created this node to gain a deeper understanding of how the ACES color transforms work internally. I am releasing it in the off-chance that it might help someone else gain a better understanding of the ACES system. There are a number of display presets which should set up the node to be a 1:1 match with the AMPAS CTL and the ACES OCIO config.

![ACES OutputTransform Presets](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_OutputTransform_presets.png)

ACES 1.1 introduced a new Tonescale algorithm for HDR display rendering transforms called the Single Stage Tonescale. In ACES 1.2 rc1 the SDR display transforms still use the older tonescale system. The older system consists of two parts. Part 1 is the RRT or Reference Rendering Transform. The RRT takes in scene-linear ACES 2065-1 data, and outputs OCES or Output Color Encoding Specification. Then an ODT or Output Device Transform is applied. The RRT in the old system uses an algorithm in the `ACESlib.Tonescales.ctl` called `segmented_spline_c5_fwd()`. The first step of the ODT is to apply a similar algorithm in the same CTL module called `segmented_spline_c9_fwd()`. 

In the new SSTS system these two steps have been combined into one, the "RRT+ODT", which could theoretically handle all display output scenarios. However at this time only HDR display outputs use this system.

The included presets are loyal to the OCIO config and should match 1 to 1. Please report any issues you notice! There may still be bugs.

If you want to play around with the SSTS parameters for SDR output, they are exposed and available. I have included a few different contrast presets to get you started. Note this is for interest learning, not for production use!

For the SDR display presets, the SSTS is bypassed and it's parameters are not active. This is the case when the use SegmentedSpline_c9 checkbox is active.



## ACES 1.0.3 OutputTransform
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_103_OutputTransform.png)

The ACES_103_OutputTransform node applies the ACES output transform, matching ACES v1.0.3. An Inverse OutputTransform node is also supplied.

This node is the same idea as the previous but matches the ACES 1.0.3 config. It has a more limited set of HDR output transforms, and does not use the SSTS algorithm.


## RGBtoXYZ
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/RGBtoXYZ.png)

Calculates a 3x3 matrix for converting from a source colorspace to CIE XYZ or the inverse. The source colorspace is specified by supplying xy chromaticity coordinates for the R, G, and B primaries as well as the whitepoint. A number of common colorspaces are included as presets.

I coded this based on the AMPAS CTL for learning. It is similar to the `PrimariesToXYZ` tool that comes with Alex Fry's [ParametricOutputTransform](https://github.com/alexfry/PureNukeACES/blob/master/Transforms/ACES_ODT_ParametricPrototype.nk) node, but rewritten without python callbacks and based on the CTL C++ code instead.



## ChromaticAdaptationMatrix
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ChromaticAdaptationMatrix.png)

Calculates a chromatic adaptation matrix given a source and target whitepoint as xy chromaticity coordinates. A number of different chromatic adaptation methods are provided, such as Bradford, Cat02, CmcCat2000, Sharp, and vonKries Hunter-Point-Estevez D65 Normalized.


## Chromaticity Converter
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ChromaticityConverter.png)

Calculates a 3x3 matrix for converting from a source to a target colorspace given the xy chromaticity coordinates of the R G and B primaries and whitepoints. Also provides the option of calculating a chromatic adaptation transform. Basically the above two tools in one. Many common colorspaces are provided as presets but you can enter your own chromaticity coordinates if you have a colorspace that is missing.

