# Documentation

## Overview
![ACES Output Transform](#aces-output-transform)
![ACES 1.0.3 OutputTransform](#aces-1.0.3-outputtransform)
![RGB to XYZ](#rgb-to-xyz)
![Chromatic Adaptation](#chromatic-adaptation)
![Chromaticity Converter](#chromaticity-converter)
![Plot Chromaticity](#plot-chromaticity)
![Plot Waveform](#plot-waveform)
![Matrix Tools](#matrix-tools)
![Log2 Shaper](#log2-shaper)
![DolbyPQ Shaper](#dolbypq-shaper)
![Misc Conversions](#misc-conversions)


## ACES Output Transform
![ACES OutputTransform UI](/images/ACES_OutputTransform.png)

The ACES_OutputTransform node applies the ACES output transform, matching the latest [ACES version (v1.2)](https://github.com/ampas/aces-dev). 

An Inverse OutputTransform node is also supplied, which reverses the output transform back into scene linear. Note that data may be lost depending on the dynamic range and gamut of the display device.
![ACES OutputTransform UI](/images/ACES_OutputTransform_graph.png)

I created this node to gain a deeper understanding of how the ACES color transforms work internally. I am releasing it in the off-chance that it might help someone else gain a better understanding of the ACES system. There are a number of display presets which should set up the node to be a 1:1 match with the AMPAS CTL and the ACES OCIO config.

![ACES OutputTransform Presets](/images/ACES_OutputTransform_presets.png)

ACES 1.1 introduced a new Tonescale algorithm for HDR display rendering transforms called the Single Stage Tonescale. In ACES 1.2 the SDR display transforms still use the older tonescale system. The older system consists of two parts. Part 1 is the RRT or Reference Rendering Transform. The RRT takes in scene-linear ACES 2065-1 data, and outputs OCES or Output Color Encoding Specification. Then an ODT or Output Device Transform is applied. The RRT in the old system uses an algorithm in the `ACESlib.Tonescales.ctl` called `segmented_spline_c5_fwd()`. The first step of the ODT is to apply a similar algorithm in the same CTL module called `segmented_spline_c9_fwd()`. 

In the new SSTS system these two steps have been combined into one, the "RRT+ODT", which could theoretically handle all display output scenarios. However at this time only HDR display outputs use this system.

The included presets are loyal to the OCIO config and should match 1 to 1. Please report any issues you might notice! There may still be bugs.

If you want to play around with the SSTS parameters for SDR output, they are exposed and available. I have included a few different contrast presets to get you started. Note this is for interest and learning, not for production use, and it will not match the official AMPAS CTL!

For the SDR display presets, the SSTS is bypassed. Its parameters are not active. This is also the case when the use SegmentedSpline_c9 checkbox is active.



## ACES 1.0.3 OutputTransform
![ACES 1.0.3 OutputTransform](/images/ACES_103_OutputTransform.png)

The ACES_103_OutputTransform node applies the ACES output transform, matching the older ACES v1.0.3. An Inverse OutputTransform node is also supplied.

This node is the same idea as the ACES_OutputTransform but matches the ACES 1.0.3 config. It has a more limited set of HDR output transforms, and does not use the SSTS algorithm. It is provided for compatibility.


## RGB to XYZ
![RGBtoXYZ](/images/RGBtoXYZ.png)

Calculates a 3x3 matrix for converting from a source colorspace to CIE XYZ or the inverse. The source colorspace is specified by supplying xy chromaticity coordinates for the R, G, and B primaries as well as the whitepoint. A number of common colorspaces are included in the presets, but you could theoretically make your own!

I coded this based on the AMPAS CTL for purposes of learning. It is similar to the `PrimariesToXYZ` tool that comes with Alex Fry's [ParametricOutputTransform](https://github.com/alexfry/PureNukeACES/blob/master/Transforms/ACES_ODT_ParametricPrototype.nk) node, but rewritten without python callbacks and based on the CTL C++ code instead.



## Chromatic Adaptation
![ChromaticAdaptation](/images/ChromaticAdaptation.png)

Chromatic adaptation is the ability of the human eye to achieve constant color appearance under different illumination conditions. A Chromatic Adaptation (CAT) function tries to simulate this behavior by shifting colors to perceptually match under a new color of light.

This node calculates a 3x3 CAT matrix given a source and target whitepoint as xy chromaticity coordinates. A number of different chromatic adaptation methods are provided, such as Bradford, Cat02, CmcCat2000, Sharp, and vonKries.

The node also supports calculating an xy coordinate from a blackbody color temperature on the planckian locus, and also sampling an arbitrary color from an input image. (Hopefully something resembling a neutral color or your results may vary!)



## Chromaticity Converter
![Chromaticity Converter](/images/ChromaticityConverter.png)

Similar to RGBtoXYZ, but supports an arbitrary output color gamut and chromatic adaptation to convert between different whitepoints. 

ChromaticityConverter calculates a 3x3 matrix given the xy chromaticity coordinates of the R G and B primaries and whitepoints of a source and target color gamut. It also provides the option of calculating a chromatic adaptation transform. Basically the above two tools in one. Many common colorspaces are provided as presets but you can enter your own chromaticity coordinates if you have a colorspace that is missing.



## Plot Chromaticity
![PlotChromaticity UI](/images/PlotChromaticity_ui.png)

PlotChromaticity is a tool for plotting the chromaticities or hues of an image on a chromaticity diagram. There are two diagrams supported: The CIE 1931 xy Chromaticity Diagram, and the CIE 1976 u'v' Chromaticity Diagram.

![Plot Chromaticity](/images/PlotChromaticity_awg_xy.jpg)

There are quite a few options on the node:
- input gamut - You have to tell the node what the gamut of the input image is so that it can correctly map the colors into CIE Yxy colorspace and plot the color values accurately.
- diagram - let's you choose between the CIE 1931 xy Chromaticity Diagram and the CIE 1976 u'v' Uniform Chromaticity Scale Diagram. The [McAdam ellipses](https://www.tftcentral.co.uk/articles/pointers_gamut.htm#_Toc379132046) indicate that the 1931 xy diagram is not perceptually uniform, especially in greens. The 1976 u'v' diagram tries to improve on perceptual uniformity. 
![PlotChromaticity UI](/images/PlotChromaticity_pointers_uv.jpg) ![PlotChromaticity UI](/images/PlotChromaticity_pointers_xy.jpg)
- Plot Dimensions allows you to adjust how much of the plot you see. This may be necessary to expand for bigger color gamuts with imaginary primaries like RedWideGamutRGB.
- format is the size of the output image. 
- resample input will down-res the input for faster processing.
- Coordinate system and spectral locus should be pretty self-explanatory. 
- Gamut overlay allows you to plot another gamut as an overlay. There are a few different styles: boundary, dots, or grid. The distribution of the grid can be set, for example to allow the grid to be biased more towards perceptual uniformity.
- Pointer's gamut is a colorspace that attempts to quantify the color of real-world objects. Enabling this plots the locus of the pointer's gamut. The samples can also be plotted.
- Colorizing: the Spectral locus, the gamut overlay, and the pointer's gamut overlay can all be colorized. This means a constant color will be used instead of the XYZ color values that are default. 

A lot of the techniques and ideas in this tool were inspired by the excellent work in [Matthias Scharfenberg's post on ACESCentral](https://acescentral.com/t/simplistic-gamut-mapping-approaches-in-nuke/2679?u=jedsmith). 



## Plot Waveform
![PlotWaveform UI](/images/PlotWaveform_ui.png)

PlotWaveform is a tool to plot a waveform representation of the input image. The waveform graphs the input pixels, keeping horizontal position, but transforming vertical position into brightness. So in simple terms it shows the distribution of pixels by brightness.

![PlotWaveform UI](/images/PlotWaveform_plot.png)




## Matrix Tools
![Matrix Tools](/images/MatrixTools_ui.png)

MatrixTools is a utility node that allows you to combine two or more 3x3 ColorMatrix nodes into one. It can also calculate the inverse of a single matrix. It can also pop up a window with the matrix in different formats, which is useful for pasting the matrix into an OCIO config for example. Better than copying the values from each cell individually! You can also save and load spimtx format files.



## Log2 Shaper
![Log2Shaper](/images/Log2Shaper_ui.png)

A node implementation of the log2 function used for the shaper in the ACES OCIO configs. Allows you to set the middle gray value, and the stops above and below middle grey to preserve in the shaper space, the range between 0 and 1. 

A note of interest: the `48nits shaper acescc` preset is the new shaper used in the ACES 1.2 OCIO config. The older 48nits shaper clipped at a very low value! This change was introduced to improve that situation.



## DolbyPQ Shaper
![DolbyPQ Shaper](/images/DolbyPQShaper_ui.png)

A node implementation of the alternative Dolby PQ / ST.2084 log shaper function, which can be used in the ACES OCIO configs. 


## Misc Conversions
![Misc Conversins](/images/cie_conversions.png)

A few node implmentations for miscelaneous colorspace conversions. CIE XYZ to CIE Yxy to CIE Luv and back are now possible!
