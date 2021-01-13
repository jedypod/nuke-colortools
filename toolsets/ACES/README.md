# ACES Tools

- [ACES Tools](#aces-tools)
  - [ACES Output Transform](#aces-output-transform)
  - [ACES 1.0.3 OutputTransform](#aces-103-outputtransform)

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

