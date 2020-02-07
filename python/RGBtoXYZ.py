import nuke
float2 = nuke.math.Vector2
float3 = nuke.math.Vector3
float3x3 = nuke.math.Matrix3
float4x4 = nuke.math.Matrix4


def get_primaries(node, dst=False):
    # get xy coordinates from node
    dst_pri = ['drxy', 'dgxy', 'dbxy', 'dwxy']
    pri = ['rxy', 'gxy', 'bxy', 'wxy']
    d = {}
    for i, p in enumerate(pri):
        if dst:
            d[p] = float2(node[dst_pri[i]].getValue()[0], node[dst_pri[i]].getValue()[1])
        else:
            d[p] = float2(node[p].getValue()[0], node[p].getValue()[1])
    return d


def RGBtoXYZ(xy, Y=1.0, inverse=False):
    # given r g b chromaticities and whitepoint
    # convert RGB colors to XYZ 
    # based on CtlColorSpace.cpp from the CTL source code
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
        return M.inverse()
    else:
        return M


def start():
    node = nuke.thisNode()
    
    invert = node['invert'].getValue()
    label = node['label']
    
    if invert:
        # Convert from XYZ colorspace to Src RGB
        mtx = RGBtoXYZ(get_primaries(node), inverse=True)
        label.setValue('XYZ to {0}'.format(node['src_colorspace_name'].getValue()))
    else:
        # Convert from Src RGB colorspace to XYZ
        mtx = RGBtoXYZ(get_primaries(node))
        label.setValue('{0} to XYZ'.format(node['src_colorspace_name'].getValue()))

    node['matrix'].setValue((mtx))
    
   

if __name__=='__main__':
    start()