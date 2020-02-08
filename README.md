# Nuke Color Tools
A collection of tools for Nuke related to color science and the Academy Color Encoding System (ACES). 
- **ACES_OutputTransform** - A Nuke node to apply the [ACES](https://github.com/ampas/aces-dev) output transform, matching ACES v1.2rc1.
- **ACES_103_OutputTransform** - A Nuke node to apply the ACES output transform matching ACES v1.0.3.
- **ChromaticAdaptationMatrix** - Calculate a chromatic adaptation matrix given a source and a destination whitepoint as xy coordinates.
- **RGBtoXYZ** - Calculate a matrix to convert from an RGB colorspace given RGB primaries and Whitepoint as xy chromaticity coordinates to XYZ or the inverse.
- **ChromaticityConverter** - Calculate a matrix to convert from one colorspace to another, given the chromaticity coordinates of the source and destination colorspaces, and a chromatic adapaptation method if the whitepoints are different.
- **segmented_spline_c5_c9** - a Nuke node implementation of the segmented_spline_c5 and segmented_spline_c9 algorithms. 

For more specific information on each tool go to the [toolsets folder](https://github.com/jedypod/nuke-colortools/tree/master/toolsets) and check out the README.


## Resources
I couldn't have made this withouth the following resources:
- Alex Fry's [PureNukeAces](https://github.com/alexfry/PureNukeACES) nodes
- The [AcesCentral Forums](https://acescentral.com)
- The [excellent information](https://colour.readthedocs.io/en/v0.3.10/colour.models.rgb.html) that comes with the [Colour python package](https://colour.readthedocs.io/en/v0.3.15/index.html).
- [Cinematic Color 2: Color for Motion Pictures and Games](https://nick-shaw.github.io/cinematiccolor/cinematic-color.html#color-science.html)
- Zach Lewis' [ACES Output Transform](https://gist.github.com/zachlewis/786c0be941868644c993fde1c3515c2c)
