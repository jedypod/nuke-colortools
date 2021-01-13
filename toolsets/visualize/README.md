# Visualization Tools

- [Visualization Tools](#visualization-tools)
  - [Plot Chromaticity](#plot-chromaticity)
  - [Plot Waveform](#plot-waveform)
  - [Plot Slice](#plot-slice)

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


## Plot Slice

Plots the pixel values of a slice through the image.