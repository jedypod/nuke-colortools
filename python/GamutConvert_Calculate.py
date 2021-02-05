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


def calc_npm(chr):
    # Calculate a normalized primaries matrix from the specified chromaticity coordinates,
    # given 2x4 list of xy chromaticity coordinates: red, green, blue, and white
    def xy_to_xyz(xy):
        return float3(xy[0], xy[1], 1.0 - xy[0] - xy[1])
    rxyz, gxyz, bxyz, wxyz = map(xy_to_xyz, chr)
    wy = chr[3][1]
    wxyz = float3(wxyz.x / wy, wxyz.y / wy, wxyz.z / wy)
    np_mtx = float3x3(rxyz[0], gxyz[0], bxyz[0],
                      rxyz[1], gxyz[1], bxyz[1],
                      rxyz[2], gxyz[2], bxyz[2])
    wscale = np_mtx.inverse() * wxyz 
    np_mtx = transpose(np_mtx * diag(wscale))
    return np_mtx


def start():
    node = nuke.thisNode()
    
    identity_mtx = float3x3()
    identity_mtx.makeIdentity()

    invert = node['invert'].getValue()
    cat_method = node['cat_method'].value()

    src_chr = [node[k].getValue() for k in ['rxy', 'gxy', 'bxy', 'wxy']]
    dst_chr = [node[k].getValue() for k in ['drxy', 'dgxy', 'dbxy', 'dwxy']]

    rgb_to_xyz = calc_npm(src_chr)
    xyz_to_rgb = calc_npm(dst_chr).inverse()       

    cat_mtx = calc_cat(src_chr[3], dst_chr[3], cat_method)

    mtx = (rgb_to_xyz * cat_mtx) * xyz_to_rgb

    if invert:
        mtx = mtx.inverse()

    node['matrix'].setValue(mtx)


if __name__=='__main__':
    start()