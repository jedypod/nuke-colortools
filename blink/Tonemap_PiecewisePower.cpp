// John Hable Filmic Tonemap
// http://filmicworlds.com/blog/filmic-tonemapping-with-piecewise-power-curves/

kernel FilmicTonemap : public ImageComputationKernel<ePixelWise> {
  Image<eRead, eAccessPoint, eEdgeClamped> src;
  Image<eWrite> dst;

  param:
    float2 pt;
    float2 ps;
    float2 white;
    float2 black;
    bool invert;

  local:
    float m; 
    float b;
    float A_t;
    float B_t;
    float A_s;
    float B_s;

  float2 as_slope_intercept(float x0, float x1, float y0, float y1) {
    float m, b;
    float dy = (y1-y0);
    float dx = (x1-x0);
    if (dx == 0)
      m = 1.0f;
    else
      m = dy/dx;
    b = y0 - x0*m;  
    return float2(m, b);
  }

  float2 solve_ab(float x0, float y0, float m) {
    float B = (m*x0)/y0;
    float lnA = log(y0) - B*log(x0);
    return float2(lnA, B);
  }

  void init() {
    // Set up static variables from input point positions
    float2 tmp; // for passing float2 vals

    tmp = as_slope_intercept(pt.x, ps.x, pt.y, ps.y);
    m = tmp.x;
    b = tmp.y;
    
    tmp = solve_ab(pt.x - black.x, pt.y - black.y, m);
    A_t = tmp.x;
    B_t = tmp.y;

    float x0 = white.x - ps.x;
    float y0 = white.y - ps.y;
    
    tmp = solve_ab(x0, y0, m);
    A_s = tmp.x;
    B_s = tmp.y;
  }


  float curve_segment_eval(float x, float m_lnA, float m_B, float m_offsetX, float m_offsetY, float m_scaleX, float m_scaleY) {
    float x0 = (x - m_offsetX)*m_scaleX;
    float y0 = 0.0f;
    if (x0 > 0.0f) {
      y0 = exp(m_lnA + m_B*log(x0));
    }
    return y0*m_scaleY + m_offsetY;
  }

  float curve_segment_eval_inv(float y, float m_lnA, float m_B, float m_offsetX, float m_offsetY, float m_scaleX, float m_scaleY) {
    float y0 = (y-m_offsetY)/m_scaleY;
    float x0 = 0.0f;
    if (y0 > 0.0f) {
      x0 = exp((log(y0) - m_lnA)/m_B);
    }
    return x0/m_scaleX + m_offsetX;
  }

  float curve(float x) {
    float y, linear_segment, toe_segment, shoulder_segment;
    linear_segment = curve_segment_eval(x, log(m), 1.0f, -(b/m), 0, 1.0f, 1.0f);
    toe_segment = curve_segment_eval(x, A_t, B_t, black.x, black.y, 1.0f, 1.0f);
    shoulder_segment = curve_segment_eval(x, A_s, B_s, white.x, white.y, -1.0f, -1.0f);

    if (x <= pt.x) {
      y = toe_segment;
    } else if (x > pt.x && x < ps.x) {
      y = linear_segment;
    } else if (x >= ps.x) {
      y = shoulder_segment;
    }
    return y;
  }

  float curve_inv(float x) {
    float y, linear_segment, toe_segment, shoulder_segment;
    linear_segment = curve_segment_eval_inv(x, log(m), 1.0f, -(b/m), 0, 1.0f, 1.0f);
    toe_segment = curve_segment_eval_inv(x, A_t, B_t, black.x, black.y, 1.0f, 1.0f);
    shoulder_segment = curve_segment_eval_inv(x, A_s, B_s, white.x, white.y, -1.0f, -1.0f);

    if (x <= pt.y) {
      y = toe_segment;
    } else if (x > pt.y && x < ps.y) {
      y = linear_segment;
    } else if (x >= ps.y) {
      y = shoulder_segment;
    }

    return y;
  }

  void process() {
    SampleType(src) rgba = src();
    if (invert) {
      dst() = float4(curve_inv(rgba.x), curve_inv(rgba.y), curve_inv(rgba.z), rgba.w);
    } else {
      dst() = float4(curve(rgba.x), curve(rgba.y), curve(rgba.z), rgba.w);
    }
  }
};
