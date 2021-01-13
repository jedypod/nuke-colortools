# Transfer Function Tools

Contains many tools to apply or inverse luminance transfer functions. A Transfer function is the component of a colorspace that determines how the luminance of an image will be transformed from the reference space. For camera encoding colorspaces, a log transfer function is common. 

- [Transfer Function Tools](#transfer-function-tools)
  - [Log2 Shaper](#log2-shaper)
  - [DolbyPQ Shaper](#dolbypq-shaper)


## Log2 Shaper
![Log2Shaper](/images/Log2Shaper_ui.png)

A node implementation of the log2 function used for the shaper in the ACES OCIO configs. Allows you to set the middle gray value, and the stops above and below middle grey to preserve in the shaper space, the range between 0 and 1. 

A note of interest: the `48nits shaper acescc` preset is the new shaper used in the ACES 1.2 OCIO config. The older 48nits shaper clipped at a very low value! This change was introduced to improve that situation.

Additionally this tool includes the option to add a linear extension to the log function at an arbitrary cut point. A linear extension allows the log curve to more gracefully handle encoding of negative values in scene-linear. There is [a plot](https://www.desmos.com/calculator/on4cq2xj9g) on [desmos](https://www.desmos.com/calculator) if you would like to investigate the math.



## DolbyPQ Shaper
![DolbyPQ Shaper](/images/DolbyPQShaper_ui.png)

An implementation of the Dolby PQ / ST.2084 log shaper function, which can be enabled as an alternative shaper function in the ACES OCIO configs.