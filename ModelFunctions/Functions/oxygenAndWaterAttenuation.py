import math

gamma_oxygen = 0


def find_phi_val(rp, rt, a, b, c, d):
    return math.pow(rp, a) * math.pow(rt, b) * math.exp(c * (1 - rp) + d * (1 - rt))


def find_oxygen_attenuation(f, t, p_total):
    global gamma_oxygen
    rt = 288 / (273 + t)
    rp = p_total / 1013
    del_val = -0.00306 * find_phi_val(rp, rt, 3.211, -14.94, 1.583, -16.37)
    gamma_66 = 1.908 * find_phi_val(rp, rt, 2.0717, -4.1404, 0.4910, -4.8718)
    gamma_64 = 6.819 * find_phi_val(rp, rt, 1.4320, 0.6258, 0.3177, -0.5914)
    gamma_62 = 14.28 * find_phi_val(rp, rt, 0.9886, 3.4176, 0.1827, 1.3429)
    gamma_60 = 15 * find_phi_val(rp, rt, 0.9003, 4.1335, 0.0427, 1.6088)
    gamma_58 = 12.59 * find_phi_val(rp, rt, 1.0045, 3.5610, 0.1588, 1.2834)
    gamma_54 = 2.192 * find_phi_val(rp, rt, 1.8286, 1.9487, 0.4051, 2.8509)
    eta_7 = find_phi_val(rp, rt, -0.1883, 6.5589, -0.2402, 6.131)
    eta_6 = find_phi_val(rp, rt, 0.2445, 5.9191, 0.0422, 8.0719)
    eta_5 = find_phi_val(rp, rt, 0.2705, 2.7192, 0.3016, 4.1033)
    eta_4 = find_phi_val(rp, rt, -0.0112, 0.0092, -0.1033, -0.0009)
    eta_3 = find_phi_val(rp, rt, 0.3414, 6.5851, 0.2130, 8.5854)
    eta_2 = find_phi_val(rp, rt, 0.5146, 4.6368, 0.1921, 5.7416)
    eta_1 = find_phi_val(rp, rt, 0.0717, 1.8132, 0.0156, 1.6515)
    if f <= 54:
        gamma_oxygen = math.pow(f, 2) * math.pow(rp, 2) * math.pow(10, -3) * (
                7.2 * math.pow(rt, 2.8) / (math.pow(f, 2) + 0.34 * math.pow(rp, 2) * math.pow(rt, 1.6)) +
                0.62 * eta_3 / (math.pow(54 - f, 1.61 * eta_1) + 0.83 * eta_2))
    elif 54 < f <= 60:
        gamma_oxygen = math.exp(
            (f - 58) * (f - 60) * math.log(gamma_54, math.e) / 24 - (f - 54) * (f - 60) * math.log(gamma_58,
                                                                                                   math.e) / 8 + (
                    f - 58) * (f - 64) * math.log(gamma_60, math.e) / 12)
    elif 60 < f <= 62:
        gamma_oxygen = gamma_60 + (gamma_62 - gamma_60) * (f - 60) / 2
    elif 62 < f <= 66:
        gamma_oxygen = math.exp(
            (f - 64) * (f - 66) * math.log(gamma_62, math.e) / 8 - (f - 62) * (f - 66) * math.log(gamma_64,
                                                                                                  math.e) / 4 + (
                    f - 62) * (f - 64) * math.log(gamma_66, math.e) / 8)
    elif 66 < f <= 120:
        gamma_oxygen = math.pow(f, 2) * math.pow(rp, 2) * math.pow(10, -3) * (
                3.02 * math.pow(10, -4) * math.pow(rt, 3.5) +
                0.283 * math.pow(rt, 3.8) / (math.pow(f - 118.75, 2) + 2.91 * math.pow(rp, 2) * math.pow(rt, 1.6)) +
                0.502 * eta_6 * (1 - 0.0163 * eta_7 * (f - 66)) / (math.pow(f - 66, 1.4346 * eta_4) + 1.15 * eta_5))
    elif 120 < f <= 350:
        gamma_oxygen = del_val + math.pow(f, 2) * math.pow(rp, 2) * math.pow(rt, 3.5) * math.pow(10, -3) * (
                3.02 * math.pow(10, -4) / (1 + 1.9 * math.pow(10, -5) * math.pow(f, 1.5)) + 0.283 * math.pow(rt,
                                                                                                             0.3) / (
                        math.pow(f - 118.75, 2) + 2.91 * math.pow(rp, 2) * math.pow(rt, 1.6)))
    return gamma_oxygen


def g_func(f, fi):
    return 1 + math.pow((f - fi) / (f + fi), 2)


def find_water_attenuation(f, t, p_total, ro):
    rt = 288 / (273 + t)
    rp = p_total / 1013
    eta_1 = 0.955 * rp * math.pow(rt, 0.68) + 0.006 * ro
    eta_2 = 0.735 * rp * math.pow(rt, 0.5) + 0.0353 * math.pow(rt, 4) * ro
    term_1 = 3.98 * eta_1 * math.exp(2.23 * (1 - rt)) * g_func(f, 22) / (
            math.pow((f - 22.235), 2) + 9.42 * math.pow(eta_1, 2))
    term_2 = 11.96 * eta_1 * math.exp(0.7 * (1 - rt)) / (math.pow(f - 183.31, 2) + 11.14 * math.pow(eta_1, 2))
    term_3 = 0.08 * eta_1 * math.exp(6.44 * (1 - rt)) / (math.pow(f - 321.226, 2) + 6.29 * math.pow(eta_1, 2))
    term_4 = 3.66 * eta_1 * math.exp(1.6 * (1 - rt)) / (math.pow(f - 325.153, 2) + 9.22 * math.pow(eta_1, 2))
    term_5 = 25.37 * eta_1 * math.exp(1.09 * (1 - rt)) / (math.pow(f - 380, 2))
    term_6 = 17.4 * eta_1 * math.exp(1.46 * (1 - rt)) / math.pow(f - 448, 2)
    term_7 = 844.6 * eta_1 * math.exp(0.17 * (1 - rt)) * g_func(f, 557) / math.pow(f - 557, 2)
    term_8 = 290 * eta_1 * math.exp(0.41 * (1 - rt)) * g_func(f, 752) / math.pow(f - 752, 2)
    term_9 = 8.3328 * math.pow(10, 4) * eta_2 * math.exp(0.99 * (1 - rt)) * g_func(f, 1780) / math.pow(f - 1780, 2)
    return math.pow(f, 2) * math.pow(rt, 2.5) * ro * math.pow(10, -4) * (
            term_9 + term_8 + term_7 + term_6 + term_5 + term_4 + term_3 + term_2 + term_1)
