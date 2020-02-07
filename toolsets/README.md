## ACES OutputTransform
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_OutputTransform.png)
The ACES_OutputTransform node applies the ACES output transform, matching the latest [ACES version (v1.2_rc1)](https://github.com/ampas/aces-dev/releases). 

An Inverse OutputTransform node is also supplied, which reverses the output transform back into scene linear. Note that data may be lost depending on the dynamic range and gamut of the display device.
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_OutputTransform_graph.png)


## ACES 1.0.3 OutputTransform
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ACES_103_OutputTransform.png)
The ACES_103_OutputTransform node applies the ACES output transform, matching ACES v1.0.3. 

An Inverse OutputTransform node is also supplied.

## RGBtoXYZ
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/RGBtoXYZ.png)
Calculates a 3x3 matrix for converting from a source colorspace to CIE XYZ or the inverse. The source colorspace is specified by supplying xy chromaticity coordinates for the R, G, and B primaries as well as the whitepoint. A number of common colorspaces are included as presets.


## ChromaticAdaptationMatrix
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ChromaticAdaptationMatrix.png)
Calculates a chromatic adaptation matrix given a source and target whitepoint as xy chromaticity coordinates. A number of different chromatic adaptation methods are provided, such as Bradford, Cat02, CmcCat2000, Sharp, and vonKries Hunter-Point-Estevez D65 Normalized.

## Chromaticity Converter
![ACES OutputTransform UI](https://raw.githubusercontent.com/jedypod/nuke-colortools/master/images/screenshots/ChromaticityConverter.png)
Calculates a 3x3 matrix for converting from a source to a target colorspace given the xy chromaticity coordinates of the R G and B primaries and whitepoints. Also provides the option of calculating a chromatic adaptation transform. Basically the above two tools in one. Many common colorspaces are provided as presets but you can enter your own chromaticity coordinates if you have a colorspace that is missing.




