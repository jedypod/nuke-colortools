import nuke
float2 = nuke.math.Vector2
float3 = nuke.math.Vector3
float3x3 = nuke.math.Matrix3

CONE_RESP_MAT_BRADFORD = float3x3()
CONE_RESP_MAT_CAT02 = float3x3()
CONE_RESP_MAT_VONKRIES = float3x3()
CONE_RESP_MAT_SHARP = float3x3()
CONE_RESP_MAT_CMCCAT2000 = float3x3()

# From ACESlib.Utilities_Color : 166
CONE_RESP_MAT_BRADFORD.set(0.89510, -0.75020,  0.03890, 0.26640,  1.71350, -0.06850, -0.16140,  0.03670,  1.02960)
CONE_RESP_MAT_CAT02.set(0.73280, -0.70360,  0.00300, 0.42960,  1.69750,  0.01360, -0.16240, 0.00610, 0.98340)

# https://web.stanford.edu/~sujason/ColorBalancing/adaptation.html
# from S. Bianco. "Two New von Kries Based Chromatic Adapatation Transforms Found by Numerical Optimization."
CONE_RESP_MAT_VONKRIES.set(0.40024, -0.2263, 0, 0.7076, 1.16532, 0, -0.08081, 0.0457, 0.91822)
CONE_RESP_MAT_SHARP.set(1.2694, -0.8364, 0.0297, -0.0988, 1.8006, -0.0315, -0.1706, 0.0357, 1.0018)
CONE_RESP_MAT_CMCCAT2000.set(0.7982, -0.5918, 0.0008, 0.3389, 1.5512, 0.239, -0.1371, 0.0406, 0.9753)



def mult_f3_f33(src, mtx):
    return float3(mtx[0] * src[0] + mtx[1] * src[1] + 
    mtx[2] * src[2], mtx[3] * src[0] + mtx[4] * src[1] + 
    mtx[5] * src[2], mtx[6] * src[0] + mtx[7] * src[1] + 
    mtx[8] * src[2])

def XYZ_2_xyY(XYZ):
    xyY = float3()
    divisor = (XYZ[0] + XYZ[1] + XYZ[2])
    if (divisor == 0.):
        divisor = 1e-10
    xyY.set(XYZ[0] / divisor, XYZ[1] / divisor, XYZ[1])
    return xyY

def xyY_2_XYZ(xyY):
    XYZ = float3()
    XYZ.set(
        xyY[0] * xyY[2] / max( xyY[1], 1e-10), \
        xyY[2], \
        (1.0 - xyY[0] - xyY[1]) * xyY[2] / max( xyY[1], 1e-10)
        )
    return XYZ


def calculate_cat_matrix(src_xy, des_xy, coneRespMat=CONE_RESP_MAT_BRADFORD):
    # Calculates and returns a 3x3 Von Kries chromatic adaptation transform 
    # from src_xy to des_xy using the cone response primaries defined 
    # by coneRespMat. By default, coneRespMat is set to CONE_RESP_MAT_BRADFORD. 
    # The default coneRespMat can be overridden at runtime. 

    src_xyY = float3(src_xy[0], src_xy[1], 1.0)
    des_xyY = float3(des_xy[0], des_xy[1], 1.0)

    src_XYZ = xyY_2_XYZ( src_xyY )
    des_XYZ = xyY_2_XYZ( des_xyY )

    src_coneResp = mult_f3_f33(src_XYZ, coneRespMat)
    des_coneResp = mult_f3_f33(des_XYZ, coneRespMat)

    vkMat = float3x3()
    vkMat.set(
        des_coneResp[0] / src_coneResp[0], 0.0, 0.0,
        0.0, des_coneResp[1] / src_coneResp[1], 0.0,
        0.0, 0.0, des_coneResp[2] / src_coneResp[2]
        )

    cat_matrix = float3x3()
    coneRespMatInv = coneRespMat.inverse()
    cat_matrix = coneRespMat * ( vkMat * coneRespMatInv)
    
    return cat_matrix



def start():
    node = nuke.thisNode()
    
    invert = node['invert'].getValue()
    cat_method = node['method'].value()
    src_xy = float2(node['src_xy'].getValue()[0], node['src_xy'].getValue()[1])
    dst_xy = float2(node['dst_xy'].getValue()[0], node['dst_xy'].getValue()[1])

    # Get chromatic adaptation method
    if cat_method == 'Bradford':
        coneRespMat = CONE_RESP_MAT_BRADFORD
    elif cat_method == 'cat02':
        coneRespMat = CONE_RESP_MAT_CAT02
    elif cat_method == 'vonKries Hunt-Pointer-Estevez D65-Normalized':
        coneRespMat = CONE_RESP_MAT_VONKRIES
    elif cat_method == 'cmccat2000':
        coneRespMat = CONE_RESP_MAT_CMCCAT2000
    elif cat_method == 'sharp':
        coneRespMat = CONE_RESP_MAT_SHARP
    elif cat_method == 'None':
        coneRespMat = float3x3()
        coneRespMat.makeIdentity()

    mtx = calculate_cat_matrix(src_xy, dst_xy, coneRespMat=coneRespMat)

    if invert:
        mtx = mtx.inverse()

    node['matrix'].setValue(mtx)

    node['label'].setValue('CAT: {0}\n {1} to {2}'.format(node['method'].value(), node['src_wp_name'].getValue(), node['dst_wp_name'].getValue()))

if __name__=='__main__':
    start()






# References for different xyY whitepoints of different Standard Illuminants
# http://brucelindbloom.com/index.html?Eqn_ChromAdapt.html
# https://www.mathworks.com/help/images/ref/whitepoint.html
# https://rdrr.io/cran/spacesXYZ/man/standardXYZ.html
# https://en.wikipedia.org/wiki/Standard_illuminant

# XYZ 
# A   1.09850 1.00000 0.35585     Simulates typical, domestic, tungsten-filament lighting with correlated color temperature of 2856 K. 
# B   0.99072 1.00000 0.85223     Simulates average or north sky daylight with correlated color temperature of 6774 K. Deprecated by CIE.
# C   0.98074 1.00000 1.18232     Useful as a theoretical reference.
# D50 0.96422 1.00000 0.82521     Simulates warm daylight at sunrise or sunset with correlated color temperature of 5003 K. Also known as horizon light.
# D55 0.95682 1.00000 0.92149     Simulates mid-morning or mid-afternoon daylight with correlated color temperature of 5500 K.  
# D60 0.95230 1.00000 1.00859     
# D65 0.95047 1.00000 1.08883     Simulates noon daylight with correlated color temperature of 6504 K. 
# D75 0.94972 1.00000 1.22638
# E   1.00000 1.00000 1.00000
# F2  0.99186 1.00000 0.67393
# F7  0.95041 1.00000 1.08747
# F11 1.00962 1.00000 0.64350


# xy
# name        CIE 1931 2deg         kelvin (cct)
# A           0.44757 0.40745     2856            Incandescent / Tungsten
# B           0.34842 0.35161     4874            {obsolete} Direct sunlight at noon
# C           0.31006 0.31616     6774            {obsolete} Average / North sky Daylight
# D50         0.34567 0.35850     5003            Horizon Light. ICC profile PCS
# D55         0.33242 0.34743     5503            Mid-morning / Mid-afternoon Daylight
# D60         0.32163 0.33774
# D60.ACES    0.32168 0.33767
# D65         0.31271 0.32902     6504            Noon Daylight: Television, sRGB color space
# D75         0.29902 0.31485     7504            North sky Daylight
# E           1/3 1/3 1/3 1/3     5454            Equal energy
# F1          0.31310 0.33727     6430            Daylight Fluorescent
# F2          0.37208 0.37529     4230            Cool White Fluorescent
# F3          0.40910 0.39430     3450            White Fluorescent
# F4          0.44018 0.40329     2940            Warm White Fluorescent
# F5          0.31379 0.34531     6350            Daylight Fluorescent
# F6          0.37790 0.38835     4150            Lite White Fluorescent
# F7          0.31292 0.32933     6500            D65 simulator, Daylight simulator
# F8          0.34588 0.35875     5000            D50 simulator, Sylvania F40 Design 50
# F9          0.37417 0.37281     4150            Cool White Deluxe Fluorescent
# F10         0.34609 0.35986     5000            Philips TL85, Ultralume 50
# F11         0.38052 0.37713     4000            Philips TL84, Ultralume 40
# F12         0.43695 0.40441     3000            Philips TL83, Ultralume 30
# LED-B1      0.4560  0.4078      2733            phosphor-converted blue
# LED-B2      0.4357  0.4012      2998            phosphor-converted blue
# LED-B3      0.3756  0.3723      4103            phosphor-converted blue
# LED-B4      0.3422  0.3502      5109            phosphor-converted blue
# LED-B5      0.3118  0.3236      6598            phosphor-converted blue
# LED-BH1     0.4474  0.4066      2851            mixing of phosphor-converted blue LED and red LED (blue-hybrid)
# LED-RGB1    0.4557  0.4211      2840            mixing of red, green, and blue LEDs
# LED-V1      0.4560  0.4548      2724            phosphor-converted violet
# LED-V2      0.3781  0.3775      4070            phosphor-converted violet