import numpy as np
import math
import random
from gaussian import Gaussian, plotGaussian

def c_w_detection(x, y, alpha_deg):
    """
    Distance/angle detection model product in [0,1].
    Inputs are scalars. Angle is in degrees (pass math.degrees(alpha_rad) if needed).
    """
    distance = math.hypot(x, y)

    # Distance contribution
    if distance < 10:
        x_val = 0.001
    elif distance < 15:
        x_val = (distance - 10) / 5.0
    elif distance < 40:
        x_val = 0.999
    elif distance < 45:
        x_val = 1.0 - (distance - 40) / 5.0
    else:
        x_val = 0.001

    # Angle contribution (degrees)
    a = alpha_deg
    if a < -45:
        alpha_val = 0.001
    elif a < -35:
        alpha_val = (a + 45) / 10.0
    elif a < 35:
        alpha_val = 0.999
    elif a < 45:
        alpha_val = 1.0 - (a - 35) / 10.0
    else:
        alpha_val = 0.001

    print("x_val:", x_val)
    print("alpha_val:", alpha_val)

    return float(x_val) * float(alpha_val)
    
def c_w_Model(x, y, alpha, x_measured, y_measured, alpha_measured):
    """Simple Gaussian-like likelihood around the true (x,y,alpha).
    Uses relative scale 1% of the magnitude (with a floor to avoid divide-by-zero).
    Returns a scalar probability-like value in (0,1].
    """
    # Avoid divide-by-zero with small epsilon scales
    sx = 0.01 * max(abs(x), 1.0)
    sy = 0.01 * max(abs(y), 1.0)
    sa = 0.01 * max(abs(alpha), 1.0)

    dx = (x_measured - x) / sx
    dy = (y_measured - y) / sy
    da = (alpha_measured - alpha) / sa

    deviation_sq = dx*dx + dy*dy + da*da
    p = math.exp(-0.5 * deviation_sq)
    return p
def Wall_Cubes_model(x, y, alpha_deg, x_measured, y_measured, alpha_measured):
    p_cube = c_w_detection(x, y, alpha_deg)
    value = random.uniform(0, 1)
    if value < p_cube:
        p_sensor = c_w_Model(x, y, alpha_deg, x_measured, y_measured, alpha_measured)
        return True, p_sensor
    else:
        return False, 0.0

def cliff_model(height, reflectivity):
    """Scalar-safe piecewise model using if/elif.
    height in the same units as your thresholds (1 and 1.5), reflectivity with thresholds 10 and 50.
    Returns probability in [0,1].
    """
    # Height contribution
    if height < 1:
        p_height = 0.001
    elif height < 1.5:
        # Linearly increase from ~0.001 at 1.0 to ~0.999 at 1.5
        t = (height - 1.0) / 0.5  # in [0,1)
        p_height = 0.001 + 0.998 * t
    else:
        p_height = 0.999

    # Reflectivity contribution
    if reflectivity < 10:
        p_reflectivity = 0.999
    elif reflectivity < 50:
        p_reflectivity = 1.0 - (reflectivity - 10.0) / 40.0
    else:
        p_reflectivity = 0.001

    return float(p_height) * float(p_reflectivity)


detected, likelihood = Wall_Cubes_model(20, 0, 0, 20, 0, 0)
print("Detected:", detected)
print("Likelihood Cube:", likelihood)

likelihood = cliff_model(4, 5)
print("Likelihood Cliff:", likelihood)
