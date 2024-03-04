# Nuke Color Tools
A collection of Nuke tools related to color science and the Academy Color Encoding System (ACES).
- **[ACES Output Transform v1.2](/toolsets/ACES/ACES_OutputTransform_v1.2.nk)** - A Nuke node to apply [ACES](https://github.com/ampas/aces-dev) output transforms, matching ACES v1.2 CTL. This node is compatible with Nuke Non-Commercial. There is also [a blinkscript version](toolsets/ACES/ACES_OutputTransform_v1.2_blink.nk).
- **[ACES Output Transform v1.0.3](/toolsets/ACES/ACES_OutputTransform_v1.0.3.nk)** - A Nuke node to apply [ACES](https://github.com/ampas/aces-dev) output transforms, matching ACES v1.0.3 CTL. This node is compatible with Nuke Non-Commercial. There is also [a blinkscript version](toolsets/ACES/ACES_OutputTransform_v1.0.3_blink.nk).
- **ACES Inverse Output Transforms** are also available as separate nodes: [ACES_InvOutputTransform_v1.0.3](/toolsets/ACES/ACES_InvOutputTransform_v1.0.3.nk) (with [blink version](/toolsets/ACES/ACES_InvOutputTransform_v1.0.3_blink.nk)), [ACES_InvOutputTransform_v1.2](/toolsets/ACES/ACES_InvOutputTransform_v1.2.nk) (with [blink version](/toolsets/ACES/ACES_InvOutputTransform_v1.2_blink.nk)).
- **[ACES expression nodes](/toolsets/ACES/ACES_expression_nodes.nk)** - A Nuke node implementation of rrt algorithms: segmented_spline_c5, segmented_spline_c9, ssts, glow_module, red_modifier. No blinkscript, compatible with Nuke Non-Commercial.
- **[Gamut Convert](/toolsets/chromaticity/GamutConvert.nk)** - Calculate a 3x3 matrix to convert from one colorspace to another, given the chromaticity coordinates of the source and destination colorspaces, and a chromatic adapaptation method if the whitepoints are different. 
- **[Whitepoint](/toolsets/chromaticity/Whitepoint.nk)** - Calculate a chromatic adaptation matrix given a source and a destination whitepoint as CIE xy chromaticity coordinates. Supports blackbody color temperature and input image sampling.
- **[Gamut to XYZ](/toolsets/chromaticity/GamutToXYZ.nk)** - Calculate a 3x3 matrix to convert an RGB colorspace to CIE XYZ, given the chromaticities of the color gamut - (the rgb primaries and whitepoint as xy coordinates).
- **[Plot Chromaticity](/toolsets/visualize/PlotChromaticity.nk)** - A blinkscript tool for plotting an image on a chromaticity diagram. Supports overlays for the spectral locus, the planckian locus, pointer's gamut, a macbeth chart, and 3 rgb gamuts.
- **[Plot Chromaticity Points](/toolsets/visualize/PlotChromaticity_Points.nk)** - Same as PlotChromaticity above, but uses a Nuke 3D PositionToPoints method instead of blinkscript. Works in Nuke Non-Commercial, and is useful if you want to view the 3 dimensional gamut volume.
- **[Plot Waveform](/toolsets/visualize/PlotWaveform.nk)** - Blinkscript tool to plot the waveform of an input image.
- **[Plot Slice](/toolsets/visualize/PlotSlice.nk)** - Blinkscript tool to plot a graph of the pixel values through a slice of the input image. Similar to the venerable [SliceTool](http://www.nukepedia.com/gizmos/other/slicetool) written by [Frank Reuter](https://www.ohufx.com), but with antialiasing.

For more specific information on each tool go to the [toolsets folder](/toolsets) and check out the README.


## Resources
- Alex Fry's [PureNukeAces](https://github.com/alexfry/PureNukeACES) nodes
- The [AcesCentral Forums](https://acescentral.com)
- The [ACES Central Gamut Mapping Virtual Working Group](https://acescentral.com/c/aces-development-acesnext/vwg-aces-gamut-mapping-working-group/80)
- The [excellent information](https://colour.readthedocs.io/en/v0.3.10/colour.models.rgb.html) that comes with the [Colour python package](https://colour.readthedocs.io/en/v0.3.15/index.html).
- [Colour](https://github.com/colour-science/colour/): [color matching functions](https://nbviewer.jupyter.org/github/colour-science/colour-ipython/blob/master/notebooks/colorimetry/cmfs.ipynb).
- [Colour and Vision Research Labratory](http://www.cvrl.org) - Great resource for datasets related to human visual perception. Including the [CIE 1931 color matching functions](http://cvrl.ioo.ucl.ac.uk/cie.htm), and the newer [CIE 2006 color matching functions](http://www.cvrl.org/ciexyzpr.htm).
- [Useful article](https://www.tftcentral.co.uk/articles/pointers_gamut.htm) on Pointer's Gamut and wide gamut display devices.
- [Cinematic Color 2: Color for Motion Pictures and Games](https://nick-shaw.github.io/cinematiccolor/cinematic-color.html#color-science.html)
- Zach Lewis' [ACES Output Transform](https://gist.github.com/zachlewis/786c0be941868644c993fde1c3515c2c)


# OCIO Configs
I also made some [OCIO Configs](https://github.com/jedypod/colortools) and other color pipeline tools which might be of interest.
