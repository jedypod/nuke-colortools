import nuke
float3 = nuke.math.Vector3
float3x3 = nuke.math.Matrix3

def transpose(m):
    # Transpose (swap rows and columns) of a nuke.math.Matrix3
    return float3x3(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8])

def set_matrix(m):
    # Populate a nuke.math.Matrix3 with a 3x3 python list (either 3x3 or 1x9)
    if len(m) is 3 and [isinstance(r, list) for r in m]:
        m = sum(m, [])
    o = float3x3(m[0], m[3], m[6], m[1], m[4], m[7], m[2], m[5], m[8])
    return o

def diag(v):
    # Create a diagonal 3x3 matrix from a 1x3 vector
    return float3x3(v[0], 0, 0, 0, v[1], 0, 0, 0, v[2])


def xyY_to_XYZ(xyY):
    # Convert an xyY chromaticity value to XYZ
    x = xyY[0]
    y = xyY[1]
    if len(xyY) is 2:
        # Assume an xy chromaticity coordinate, use default Y
        Y = 1.0
    else:
        Y = xyY[2]
    XYZ = float3(x * Y / max(y, 1e-10), Y, (1.0 - x - y) * Y / max(y, 1e-10))
    return XYZ


def calc_cat(src_xy, dst_xy, cat_method='cat02'):
    # Calculate Von Kries chromatic adaptation transform matrix,
    # given a source and destination illuminant and CAT method.
    # Illuminant is given as xy chromaticity coordinates. 
    # CAT method is the name of one of the below cone response matrices.

    crmtxs = {
        "bianco": [[0.8752, 0.2787, -0.1539], [-0.8904, 1.8709, 0.0195], [-0.0061, 0.0162, 0.9899]],
        "bianco_pc": [[0.6489, 0.3915, -0.0404], [-0.3775, 1.3055, 0.072], [-0.0271, 0.0888, 0.9383]],
        "bradford": [[0.8951, 0.2664, -0.1614], [-0.7502, 1.7135, 0.0367], [0.0389, -0.0685, 1.0296]],
        "cat02": [[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.003, 0.0136, 0.9834]],
        "cat02_brill_cat": [[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0, 0.0, 1.0]],
        "cmccat2000": [[0.7982, 0.3389, -0.1371], [-0.5918, 1.5512, 0.0406], [0.0008, 0.0239, 0.9753]],
        "cmccat97": [[0.8951, -0.7502, 0.0389], [0.2664, 1.7135, 0.0685], [-0.1614, 0.0367, 1.0296]],
        "fairchild": [[0.8562, 0.3372, -0.1934], [-0.836, 1.8327, 0.0033], [0.0357, -0.0469, 1.0112]],
        "sharp": [[1.2694, -0.0988, -0.1706], [-0.8364, 1.8006, 0.0357], [0.0297, -0.0315, 1.0018]],
        "von_kries": [[0.40024, 0.7076, -0.08081], [-0.2263, 1.16532, 0.0457], [0.0, 0.0, 0.91822]],
        "xyz_scaling": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    }
    
    cat_method = cat_method.lower().replace(' ', '_')
    # Return identity matrix if no match
    if cat_method not in crmtxs.keys():
        m = float3x3()
        m.makeIdentity()
        return m

    crmtx = set_matrix(crmtxs[cat_method])

    # Get XYZ values from xy chromaticity coordinates
    src_XYZ = xyY_to_XYZ(src_xy)
    dst_XYZ = xyY_to_XYZ(dst_xy)

    # Calculate source and destination cone response matrices
    src_crmtx = transpose(crmtx) * src_XYZ
    dst_crmtx = transpose(crmtx) * dst_XYZ

    von_kries_matrix = diag(dst_crmtx / src_crmtx)
    cat_mtx = float3x3()
    cat_mtx = crmtx * (von_kries_matrix * crmtx.inverse())
    return cat_mtx


def start():
    node = nuke.thisNode()
    
    invert = node['invert'].getValue()
    cat_method = node['method'].value()
    src_xy = float2(node['src_xy'].getValue()[0], node['src_xy'].getValue()[1])
    dst_xy = float2(node['dst_xy'].getValue()[0], node['dst_xy'].getValue()[1])

    mtx = calc_cat(src_xy, dst_xy, cat_method)

    if invert:
        mtx = mtx.inverse()

    node['matrix'].setValue(mtx)


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