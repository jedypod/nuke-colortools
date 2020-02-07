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


def transpose(mtx):
    # transpose (swap rows to columns) of a 3x3 matrix
    order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    omtx = float3x3()
    for i in xrange(9):
        omtx[i] = mtx[order[i]]
    return omtx

def mult_f33_f33(A, B):
    # Calculate multiplication of 3x3 matrix A and 3x3 matrix B
    C = float3x3()
    C.makeIdentity()

    # Row 1
    C[0] = (A[0]*B[0] + A[1]*B[3] + A[2]*B[6])
    C[1] = (A[0]*B[1] + A[1]*B[4] + A[2]*B[7])
    C[2] = (A[0]*B[2] + A[1]*B[5] + A[2]*B[8])
    # Row 2
    C[3] = (A[3]*B[0] + A[4]*B[3] + A[5]*B[6])
    C[4] = (A[3]*B[1] + A[4]*B[4] + A[5]*B[7])
    C[5] = (A[3]*B[2] + A[4]*B[5] + A[5]*B[8])
    # Row 3
    C[6] = (A[6]*B[0] + A[7]*B[3] + A[8]*B[6])
    C[7] = (A[6]*B[1] + A[7]*B[4] + A[8]*B[7])
    C[8] = (A[6]*B[2] + A[7]*B[5] + A[8]*B[8])

    return C;


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


def RGBtoXYZ(xy, Y=1.0, inverse=False):
    # given r g b chromaticities and whitepoint, convert RGB colors to XYZ
    # based on CtlColorSpace.cpp from the CTL source code : 77
    # param: xy - dict of chromaticity xy coordinates: rxy: float2(x, y) etc
    # param: Y - luminance of "white" - defaults to 1.0
    # param: inverse - calculate XYZ to RGB instead
    r = xy['rxy']
    g = xy['gxy']
    b = xy['bxy']
    w = xy['wxy']

    X = w.x * Y / w.y
    Z = (1 - w.x - w.y) * Y / w.y

    # Scale factors for matrix rows
    d = r.x * (b.y - g.y) + b.x * (g.y - r.y) + g.x * (r.y - b.y)

    Sr =    (X * (b.y - g.y) -      \
            g.x * (Y * (b.y - 1) +  \
            b.y  * (X + Z)) +       \
            b.x  * (Y * (g.y - 1) + \
            g.y * (X + Z))) / d
    
    Sg =    (X * (r.y - b.y) +      \
            r.x * (Y * (b.y - 1) +  \
            b.y * (X + Z)) -        \
            b.x * (Y * (r.y - 1) +  \
            r.y * (X + Z))) / d

    Sb =    (X * (g.y - r.y) -      \
            r.x * (Y * (g.y - 1) +  \
            g.y * (X + Z)) +        \
            g.x * (Y * (r.y - 1) +  \
            r.y * (X + Z))) / d

    # Assemble the matrix
    M = float3x3()
    M.set(  Sr * r.x, Sr * r.y, Sr * (1 - r.x - r.y),
            Sg * g.x, Sg * g.y, Sg * (1 - g.x - g.y),
            Sb * b.x, Sb * b.y, Sb * (1 - b.x - b.y))
    if inverse:
        M = M.inverse()
        return M
    else:
        return M


def get_primaries(node, dst=False):
    # get colorspace chromaticities xy coordinates from node
    dst_pri = ['drxy', 'dgxy', 'dbxy', 'dwxy']
    pri = ['rxy', 'gxy', 'bxy', 'wxy']
    d = {}
    for i, p in enumerate(pri):
        if dst:
            d[p] = float2(node[dst_pri[i]].getValue()[0], node[dst_pri[i]].getValue()[1])
        else:
            d[p] = float2(node[p].getValue()[0], node[p].getValue()[1])
    return d



def start():
    node = nuke.thisNode()
    
    identity_mtx = float3x3()
    identity_mtx.makeIdentity()

    invert = node['invert'].getValue()
    label = node['label']
    cat_method = node['cat_method'].value()
    src_primaries = get_primaries(node)
    dst_primaries = get_primaries(node, dst=True)
    src_colorspace_name = node['src_colorspace_name'].getValue()
    dst_colorspace_name = node['dst_colorspace_name'].getValue()
    
    # Check for XYZ on src / destination
    enable_src = (src_colorspace_name != 'XYZ')
    enable_dst = (dst_colorspace_name != 'XYZ')
    whitepoint_changed = (src_primaries['wxy'][0] != dst_primaries['wxy'][0] or src_primaries['wxy'][1] != dst_primaries['wxy'][1])

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
        coneRespMat = identity_mtx
        whitepoint_changed = False

    # Set label
    if invert:
        label.setValue('{1} to {0}'.format(node['src_colorspace_name'].getValue(), node['dst_colorspace_name'].getValue()))
    else:
        label.setValue('{0} to {1}'.format(node['src_colorspace_name'].getValue(), node['dst_colorspace_name'].getValue()))

    if enable_src:
        # Calculate Source RGB to XYZ matrix
        src_rgb_to_xyz_mtx = RGBtoXYZ(src_primaries)

    if enable_dst:
        # Calculate Destination XYZ to RGB matrix
        dst_xyz_to_rgb_mtx = RGBtoXYZ(dst_primaries, inverse=True)

    if enable_src and not enable_dst:
        # Convert from Source RGB to XYZ only
        mtx = src_rgb_to_xyz_mtx

    if enable_dst and not enable_src:
        # Convert from XYZ to Destination RGB only
        mtx = dst_xyz_to_rgb_mtx

    if enable_src and enable_dst:
        if whitepoint_changed:
            # Calculate chromatic adaptation matrix
            cat_mtx = calculate_cat_matrix(src_primaries['wxy'], dst_primaries['wxy'], coneRespMat=coneRespMat)
            # We will use our own matrix multiplication algorithm since there seems to be precision issues with the nuke.math module :/
            # mtx = (cat_mtx * src_rgb_to_xyz_mtx) * dst_xyz_to_rgb_mtx
            mtx = mult_f33_f33(dst_xyz_to_rgb_mtx, mult_f33_f33(cat_mtx, src_rgb_to_xyz_mtx))
        else:
            mtx = mult_f33_f33(dst_xyz_to_rgb_mtx, src_rgb_to_xyz_mtx)

    if invert:
        mtx = mtx.inverse()

    node['matrix'].setValue(mtx)

    return True


if __name__=='__main__':
    start()