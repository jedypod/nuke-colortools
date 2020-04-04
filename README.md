# Nuke Color Tools
A collection of tools for Nuke related to color science and the Academy Color Encoding System (ACES). 
- **[ACES Output Transform](/toolsets/ACES_OutputTransform.nk)** - A Nuke node to apply the [ACES](https://github.com/ampas/aces-dev) output transform, matching ACES v1.2.
- **[ACES 103 Output Transform](/toolsets/ACES_103_OutputTransform.nk)** - A Nuke node to apply the ACES output transform matching ACES v1.0.3.
- **[Chromatic Adaptation](/toolsets/ChromaticAdaptation.nk)** - Calculate a chromatic adaptation matrix given a source and a destination whitepoint as CIE xy chromaticity coordinates. Supports blackbody color temperature and input image sampling.
- **[RGB to XYZ](/toolsets/RGBtoXYZ.nk)** - Calculate a 3x3 matrix to convert an RGB colorspace to CIE XYZ, given the chromaticies of the color gamut - (the primaries and whitepoint as xy coordinates).
- **[Chromaticity Converter](/toolsets/ChromaticityConverter.nk)** - Calculate a 3x3 matrix to convert from one colorspace to another, given the chromaticity coordinates of the source and destination colorspaces, and a chromatic adapaptation method if the whitepoints are different.
- **[Plot Chromaticity](/toolsets/PlotChromaticity.nk)** - A tool for plotting an image on a chromaticity diagram. Supports overlays for the spectral locus, pointer's gamut, and a specified rgb gamut.
- **[segmented_spline_c5_c9](/toolsets/segmented_spline_c5_c9_nuke_only.nk)** - A pure Nuke node implementation (no BlinkScript) of the segmented_spline_c5 and segmented_spline_c9 algorithms.

For more specific information on each tool go to the [toolsets folder](/toolsets) and check out the README.


## Resources
- Alex Fry's [PureNukeAces](https://github.com/alexfry/PureNukeACES) nodes
- The [AcesCentral Forums](https://acescentral.com)
- The [ACES Central Gamut Mapping Virtual Working Group](https://acescentral.com/c/aces-development-acesnext/vwg-aces-gamut-mapping-working-group/80)
- The [excellent information](https://colour.readthedocs.io/en/v0.3.10/colour.models.rgb.html) that comes with the [Colour python package](https://colour.readthedocs.io/en/v0.3.15/index.html).
- [Cinematic Color 2: Color for Motion Pictures and Games](https://nick-shaw.github.io/cinematiccolor/cinematic-color.html#color-science.html)
- Zach Lewis' [ACES Output Transform](https://gist.github.com/zachlewis/786c0be941868644c993fde1c3515c2c)


# OCIO Configs
I also made some [OCIO Configs](https://github.com/jedypod/colortools) and other color pipeline tools which might be of interest.
