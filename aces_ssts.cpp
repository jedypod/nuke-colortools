kernel AcesSSTSKernel : public ImageComputationKernel<ePixelWise>
{
  Image<eRead, eAccessPoint, eEdgeClamped> src;
  Image<eWrite> dst;

param:
  // each point has 
  // x = luminance (ACES), y = stops, z = percentages
  float3 minPt, midPt, maxPt;

local:
  float2 lumLow;    // luminance
  float2 stopsLow;  // stops
  float2 pctsLow;   // percentages
  float2 lumHigh;
  float2 stopsHigh;
  float2 pctsHigh;
  float expShift;
  float pctLow;
  float pctHigh;
  int N_KNOTS_LOW;
  int N_KNOTS_HIGH;
  float3x3 M;
  float knotIncLow;
  float knotIncHigh;
  float coefsLow[5];
  float coefsHigh[5];

  // 1d linear interpolation of two 1x2 arrays at pos x
  float interp1d(float2 xvals, float2 yvals, float x) {
      return yvals[0] + (yvals[1] - yvals[0]) / (xvals[1] - 
          xvals[0]) * (x - xvals[0]);
  }

  // multiply a float3 by a matrix3x3
  float3 mult_f3_f33( float3 src, float3x3 mtx) {
      return float3(mtx[0][0] * src.x + mtx[0][1] * src.y + 
      mtx[0][2] * src.z, mtx[1][0] * src.x + mtx[1][1] * src.y + 
      mtx[1][2] * src.z, mtx[2][0] * src.x + mtx[2][1] * src.y + 
      mtx[2][2] * src.z);
  }

  // dot product of two 1x3 matrices
  float dot_f3_f3( float3 A, float3 B) {
    return (A.x*B.x)+(A.y*B.y)+(A.z*B.z);
  }

  // Set up constant variables
  void init() {
    lumLow = float2(log10(float(0.0001)), log10(float(0.02)));
    stopsLow = float2(-15.0, -6.5);
    pctsLow = float2(0.14, 0.35);

    lumHigh = float2(log10(float(48)), log10(float(10000)));
    stopsHigh = float2(6.5, 18.0);
    pctsHigh = float2(0.89, 0.91);
    
    expShift = 0.0;

    float Marray[] = {0.5, -1.0, 0.5, -1.0, 1.0, 0.0, 0.5, 0.5, 0.0};
    M.setArray(Marray);

    N_KNOTS_LOW = 4;
    N_KNOTS_HIGH = 4;

    pctLow = interp1d(stopsLow, pctsLow, log2(float(minPt.x)/0.18));
    pctHigh = interp1d(stopsHigh, pctsHigh, log2(float(maxPt.x)/0.18));


    // initcoefsLow_wPct( minPt, midPt, pctLow)
    knotIncLow = (log10(float(midPt.x)) - log10(float(minPt.x))) / 3.;
    coefsLow[0] = (minPt.z * (log10(float(minPt.x))-0.5*knotIncLow)) + 
      (log10(float(minPt.y)) - minPt.z * log10(float(minPt.x)));
    coefsLow[1] = (minPt.z * (log10(float(minPt.x))+0.5*knotIncLow)) + 
      (log10(float(minPt.y)) - minPt.z * log10(float(minPt.x)));
    coefsLow[3] = (midPt.z * (log10(float(midPt.x))-0.5*knotIncLow)) + 
      (log10(float(midPt.y)) - midPt.z * log10(float(midPt.x)));
    coefsLow[4] = (midPt.z * (log10(float(midPt.x))+0.5*knotIncLow)) + 
      (log10(float(midPt.y)) - midPt.z * log10(float(midPt.x)));    
    coefsLow[2] = log10(float(minPt.y)) + pctLow*(log10(float(midPt.y))
       - log10(float(minPt.y)));

    // initcoefsHigh_wPct( midPt, maxPt, pctHigh)
    knotIncHigh = (log10(float(maxPt.x)) - log10(float(midPt.x))) / 3.;
    coefsHigh[0] = (midPt.z * (log10(float(midPt.x))-0.5*knotIncHigh)) + 
      ( log10(float(midPt.y)) - midPt.z * log10(float(midPt.x)));
    coefsHigh[1] = (midPt.z * (log10(float(midPt.x))+0.5*knotIncHigh)) + 
      ( log10(float(midPt.y)) - midPt.z * log10(float(midPt.x)));
    coefsHigh[3] = (maxPt.z * (log10(float(maxPt.x))-0.5*knotIncHigh)) + 
      ( log10(float(maxPt.y)) - maxPt.z * log10(float(maxPt.x)));
    coefsHigh[4] = (maxPt.z * (log10(float(maxPt.x))+0.5*knotIncHigh)) + 
      ( log10(float(maxPt.y)) - maxPt.z * log10(float(maxPt.x)));
    coefsHigh[2] = log10(float(midPt.y)) + pctHigh*(log10(float(maxPt.y)) 
        - log10(float(midPt.y)));
  }


  float ssts(float xIn) {
    // ACES Single Stage Tone Scale

    // Take the log: clamp min to HALF_MIN
    float logx = log10(max(xIn, 5.96046448e-08));
    float logy;

    // Calculate values for linear extension in shadows
    if (logx <= log10(float(minPt.x))) {
      logy = logx * minPt.z + (log10(float(minPt.y))) - 
        minPt.z * log10(float(minPt.x));
      // logy = logx;
    }
    // Calculate values for lower half of S-curve, shadows 
    if (( logx > log10(float(minPt.x)) ) && ( logx < log10(float(midPt.x)) )) {
      float knot_coord = (N_KNOTS_LOW-1) * (logx-log10(float(minPt.x)))/
        (log10(float(midPt.x))-log10(float(minPt.x)));
      int j = knot_coord;
      float t = knot_coord - j;
      float3 cf = float3(coefsLow[j], coefsLow[j + 1], coefsLow[j + 2]);
      float3 monomials = float3(t * t, t, 1.);
      logy = dot_f3_f3(monomials, mult_f3_f33(cf, M));
      // logy = logx;
    }
    // Calculate values for upper half of S-curve, highlights
    if (( logx >= log10(float(midPt.x)) ) && ( logx < log10(float(maxPt.x)) )) {
      float knot_coord = (N_KNOTS_HIGH-1) * (logx-log10(float(midPt.x)))/
        (log10(float(maxPt.x))-log10(float(midPt.x)));
      int j = knot_coord;
      float t = knot_coord - j;
      float3 cf = float3(coefsHigh[j], coefsHigh[j + 1], coefsHigh[j + 2]); 
      float3 monomials = float3(t * t, t, 1.);
      logy = dot_f3_f3(monomials, mult_f3_f33(cf, M));
      // logy = N_KNOTS_HIGH;
    }
    // Calculate values for linear extension in highlights
    if ( logx >= log10(float(maxPt.x)) ) {
      logy = logx * maxPt.z + ( log10(float(maxPt.y)) - maxPt.z * log10(float(maxPt.x)) );
      // logy = logx;
    }

    logy = pow(float(10),logy);
    return logy;
  }

  void process() {
    dst() = float4(ssts(src().x), ssts(src().y), ssts(src().z), src().w);
  }
};