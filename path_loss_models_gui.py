from tkinter import ttk
from tkinter import *
import customtkinter as ctk
from scipy import io
from statistics import NormalDist
from oxygenAndWaterAttenuation import find_oxygen_attenuation
from oxygenAndWaterAttenuation import find_water_attenuation
import math
import numpy as np
from time import sleep

root = ctk.CTk()
root.geometry("900x500")
root.title("Path Loss Models")

scenarios_options = [
    "Indoor Transmission Loss Model",  # 0
    "Site General Model for above rooftop",  # 1
    "Site General Model for below rooftop",  # 2
    "Site General Model from below rooftop to street level",  # 3
    "Site Specific Model for below rooftop LoS",  # 4
    "Site Specific Model for below rooftop NLoS",  # 5
    "Site Specific Model for above rooftop in Urban Scenario",  # 6
    "Site Specific Model for above rooftop in Suburban Scenario",  # 7
    "Site Specific Model from below rooftop to street level LoS",  # 8
    "Site Specific Model from below rooftop to street level for 1 turn NLoS propagation",  # 9
    "Site Specific Model from below rooftop to street level for 2 turn NLoS propagation",  # 10
    "Site Specific Model in residential environments"  # 11
]

area_options = [
    "Residential",
    "Office",
    "Commercial"
]

building_shapes = [
    "wedge-shaped",
    "chamfered-shape"
]

frequency_ranges = [
    "UHF propagation",
    "SHF propagation",
    "EHF propagation (Millimeter Wave)"
]

environment_options = []

env_options = [
    "Urban environment",
    "Residential environment"
]

is_UHF_propagation = False
is_SHF_propagation = False
is_EHF_propagation = False

alpha = 0
beta = 0
gamma = 0
standard_deviation = 0

road_distances = []
path_loss_along_road = 0

power_loss_coefficient = 0
floor_penetration_loss_factor = 0
curr_path_loss = 0
path_loss = 0
variance = 0

street_orientation_factor = 0

l_urban = 0

breakpoint_distance = -1
effective_road_height = -1
path_loss_exponent = 0
freq = 0
l_c = 0
l_att = 0

curr = 0
l_los = 0
turn_distances = []


def delete_labels():
    note_label_3.pack_forget()
    angle_2_label.pack_forget()
    corner_angle.pack_forget()
    sidewalk_label.pack_forget()
    sidewalk.pack_forget()
    street_width_label.pack_forget()
    street_width.pack_forget()
    length_label.pack_forget()
    length.pack_forget()
    avg_b_label.pack_forget()
    avg_b.pack_forget()
    avg_height_label.pack_forget()
    avg_height_combo.pack_forget()
    note_label.pack_forget()
    env_label.pack_forget()
    env_combo.pack_forget()
    b_label.pack_forget()
    b_combo.pack_forget()
    distance_label_1.pack_forget()
    distance_1.pack_forget()
    distance_label_2.pack_forget()
    distance_2.pack_forget()
    street_width_label_1.pack_forget()
    street_width_1.pack_forget()
    street_width_label_2.pack_forget()
    street_width_2.pack_forget()
    f_1_combo.pack_forget()
    traffic_label.pack_forget()
    traffic_combo.pack_forget()
    d_2_label.pack_forget()
    d_3_label.pack_forget()
    d_label.pack_forget()
    d_combo.pack_forget()
    f_label.pack_forget()
    f_combo.pack_forget()
    p_total_label.pack_forget()
    p_total.pack_forget()
    density_label.pack_forget()
    density.pack_forget()
    temp_label.pack_forget()
    temp.pack_forget()
    wavelength_label.pack_forget()
    wavelength.pack_forget()
    corner_angle_label.pack_forget()
    corner_angle.pack_forget()
    height_label_1.pack_forget()
    height_1.pack_forget()
    height_label_2.pack_forget()
    height_2.pack_forget()
    range_label.pack_forget()
    range_combo.pack_forget()
    fr_label.pack_forget()
    percentage_label.pack_forget()
    percentage_combo.pack_forget()
    path_loss_button.pack_forget()
    e_label.pack_forget()
    e_combo.pack_forget()
    area_label.pack_forget()
    area_combo.pack_forget()
    num_label.pack_forget()
    num_combo.pack_forget()
    street_width_first.pack_forget()
    x_1_label.pack_forget()
    x_1_combo.pack_forget()
    x_2_label.pack_forget()
    x_2_combo.pack_forget()
    note_label_2.pack_forget()
    num_of_corners_label.pack_forget()
    num_of_corners.pack_forget()
    num_of_corners_label_1.pack_forget()
    h_b_tx_label.pack_forget()
    h_b_tx_combo.pack_forget()
    h_b_rx_label.pack_forget()
    h_b_rx_combo.pack_forget()
    h_rx_label.pack_forget()
    h_rx_combo.pack_forget()
    h_tx_label.pack_forget()
    h_tx_combo.pack_forget()
    a_label.pack_forget()
    a_combo.pack_forget()
    b_label.pack_forget()
    b_combo.pack_forget()
    c_label.pack_forget()
    c_combo.pack_forget()
    b_d_label.pack_forget()
    b_d_input.pack_forget()
    avg_building_h_label.pack_forget()
    avg_building_h_input.pack_forget()
    corner_combo.pack_forget()
    corner_label.pack_forget()


def scenario_click(event):
    scenario = scenario_combo.get()
    global environment_options, alpha, beta, gamma, standard_deviation
    if scenario == scenarios_options[0]:
        delete_labels()
        area_label.pack(pady=2)
        area_combo.pack()
        num_label.pack(pady=2)
        num_combo.pack()
        d_combo.config(values=list(range(1, 101)))
    elif scenario == scenarios_options[1]:
        delete_labels()
        environment_options = [
            "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS"
        ]
        alpha = 2.29
        beta = 28.6
        gamma = 1.96
        standard_deviation = 3.48
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options)
        e_combo.bind("<<ComboboxSelected>>", e_above_rooftop_click)
        e_combo.pack()
    elif scenario == scenarios_options[2]:
        delete_labels()
        environment_options = [
            "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS", "Urban low-rise/NLoS"
        ]
        alpha = 2.12
        beta = 29.2
        gamma = 2.11
        standard_deviation = 5.06
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options)
        e_combo.bind("<<ComboboxSelected>>", e_below_rooftop_click)
        e_combo.pack()
    elif scenario == scenarios_options[3]:
        delete_labels()
        environment_options = [
            "urban", "suburban", "dense urban/high-rise"
        ]
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options)
        e_combo.bind("<<ComboboxSelected>>", e_below_rooftop_to_street_click)
        e_combo.pack()
        percentage_label.pack()
        percentage_combo.pack()
    elif scenario == scenarios_options[4] or scenario == scenarios_options[8]:
        delete_labels()
        range_label.pack()
        range_combo.pack()
        height_label_1.pack()
        height_1.config(values=list(range(1, 11)))
        height_1.current(0)
        height_1.pack()
        height_label_2.pack()
        height_2.config(values=list(range(1, 11)))
        height_2.current(0)
        height_2.pack()
        corner_angle_label.pack()
        corner_angle.pack()
        d_2_label.pack()
        d_combo.config(values=list(range(1, 1001)))
        d_combo.pack()
    elif scenario == scenarios_options[5]:
        delete_labels()
        corner_angle_label.pack()
        corner_angle.pack()
        f_label.pack()
        f_1_combo.config(values=list(np.round(np.arange(0.8, 38.1, 0.1), 1)))
        f_1_combo.bind("<<ComboboxSelected>>", f_below_rooftop_click)
        f_1_combo.pack()
        street_width_label_1.pack()
        street_width_1.pack()
        street_width_label_2.pack()
        street_width_2.pack()
        distance_label_1.pack()
        distance_1.pack()
        distance_label_2.pack()
        distance_2.pack()
    elif scenario == scenarios_options[6]:
        delete_labels()
        note_label.pack()
        environment_options = [
            "medium sized city and suburban centers with medium tree density",
            "metropolitan centers"
        ]
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options, width=60)
        e_combo.pack()
        d_3_label.pack()
        d_combo.config(values=list(range(20, 1001)))
        d_combo.current(0)
        d_combo.pack()
        height_label_1.pack()
        height_1.config(values=list(range(4, 51)))
        height_1.current(0)
        height_1.pack()
        height_label_2.pack()
        height_2.config(values=list(range(1, 4)))
        height_2.current(0)
        height_2.pack()
        wavelength_label.pack()
        wavelength.pack()
        angle_2_label.pack()
        corner_angle.pack()
        sidewalk_label.pack()
        sidewalk.pack()
        street_width_label.pack()
        street_width.pack()
        length_label.pack()
        length.pack()
        avg_b_label.pack()
        avg_b.pack()
        avg_height_label.pack()
        avg_height_combo.set("Select average height of buildings")
        avg_height_combo.bind("<<ComboboxSelected>>", avg_height_click)
        avg_height_combo.pack()
    elif scenario == scenarios_options[7]:
        delete_labels()
        street_width_label.pack()
        street_width_first.current(0)
        street_width_first.pack()
        angle_2_label.pack()
        corner_angle.pack()
        wavelength_label.pack()
        wavelength.pack()
        height_label_1.pack()
        height_1.config(values=list(range(6, 111)))
        height_1.current(0)
        height_1.pack()
        height_label_2.pack()
        height_2.config(values=list(range(1, 17)))
        height_2.current(0)
        height_2.pack()
        avg_height_label.pack()
        avg_height_combo.config(values=list(range(11, 21)))
        avg_height_combo.current(0)
        avg_height_combo.pack()
        d_3_label.pack()
        d_combo.config(values=list(range(10, 1001)))
        d_combo.pack()
        f_label.pack()
        f_combo.config(values=list(np.round(np.arange(0.8, 38.1, 0.1), 1)))
        f_combo.pack()
        path_loss_button.pack(pady=10)
    elif scenario == scenarios_options[9]:
        delete_labels()
        alpha = 2.12
        beta = 29.2
        gamma = 2.11
        standard_deviation = 5.06
        environment_options = [
            "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS"
        ]
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options)
        e_combo.bind("<<ComboboxSelected>>", e_below_rooftop_to_street_1_turn_click)
        e_combo.pack()
    elif scenario == scenarios_options[10]:
        delete_labels()
        alpha = 2.12
        beta = 29.2
        gamma = 2.11
        standard_deviation = 5.06
        environment_options = [
            "Urban high-rise/LoS", "Urban low-rise/LoS", "Urban high-rise/NLoS"
        ]
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options)
        e_combo.bind("<<ComboboxSelected>>", e_below_rooftop_to_street_2_turn_click)
        e_combo.pack()
        num_of_corners_label.pack()
        num_of_corners.current(0)
        num_of_corners.pack()
        note_label_2.pack()
        range_label.pack()
        range_combo.config(values=["UHF propagation", "SHF propagation"])
        range_combo.pack()
        height_label_1.pack()
        height_1.config(values=list(range(1, 11)))
        height_1.current(0)
        height_1.pack()
        height_label_2.pack()
        height_2.config(values=list(range(1, 11)))
        height_2.current(0)
        height_2.pack()
    elif scenario == scenarios_options[11]:
        delete_labels()
        d_2_label.pack()
        d_combo.config(values=list(range(1, 1001)))
        d_combo.pack()
        f_label.pack()
        f_combo.config(values=list(range(2, 27)))
        f_combo.pack()
        wavelength_label.pack()
        wavelength.pack()
        h_b_tx_label.pack()
        h_b_tx_combo.current(0)
        h_b_tx_combo.pack()
        h_b_rx_label.pack()
        h_b_rx_combo.current(0)
        h_b_rx_combo.pack()
        h_rx_label.pack()
        h_rx_combo.current(0)
        h_rx_combo.pack()
        h_tx_label.pack()
        h_tx_combo.current(0)
        h_tx_combo.pack()
        a_label.pack()
        a_combo.current(0)
        a_combo.pack()
        b_label.pack()
        b_combo.current(0)
        b_combo.pack()
        c_label.pack()
        c_combo.current(0)
        c_combo.pack()
        b_d_label.pack()
        b_d_input.pack()
        avg_building_h_label.pack()
        avg_building_h_input.pack()
        corner_label.pack()
        corner_combo.current(0)
        corner_combo.bind("<<ComboboxSelected>>", corner_click)
        corner_combo.pack()
        path_loss_button.pack(pady=20)


def find_loss_around_corners(n, f):
    curr_sum = 0
    for dist in road_distances:
        theta = dist[0]
        x_1 = dist[1]
        x_2 = dist[2]
        curr_sum += ((7.18 * math.log(theta, 10) + 0.97 * math.log(f, 10) + 6.1) * (
                1 - math.exp(-3.72 * math.pow(10, -5) * theta * x_2 * x_1)))
    return curr_sum


def loss_before_corner():
    d = float(d_combo.get())
    wl = float(wavelength.get())
    return 20 * math.log(4 * math.pi * d / wl)


def corner_click(event):
    if corner_combo.get() == "after corner":
        path_loss_button.pack_forget()
        num_of_corners_label_1.pack()
        num_of_corners.pack()
        note_label_2.pack()
        path_loss_button.pack(pady=5)
    else:
        path_loss_button.pack_forget()
        num_of_corners_label_1.pack_forget()
        num_of_corners.pack_forget()
        note_label_2.pack_forget()
        path_loss_button.pack(pady=15)


def mean_visible_distance():
    n = float(b_d_input.get())
    m = float(avg_building_h_input.get())
    h_rx = float(h_rx_combo.get())
    curr_l = 6
    l3 = 12
    w_0 = 15
    alp = 0.55
    bt = 0.18
    gm = (l3 - h_rx) / (m - curr_l)
    dl = 1 + bt * (m - curr_l)
    del_sq = math.pow(dl, 2)
    w_p = 4 * w_0 * (1 - ((alp * (1 - math.exp(-dl * gm))) / (del_sq * (1 - math.exp(-gm)))) * math.exp(
        -bt * h_rx)) / math.pi
    return 1000 * gm * math.exp((h_rx - curr_l) / (m - curr_l)) / (n * w_p * (1 - math.exp(-gm)))


def find_over_roof_propagation_loss():
    h_b_rx = float(h_b_rx_combo.get())
    h_rx = float(h_rx_combo.get())
    h_b_tx = float(h_b_tx_combo.get())
    h_tx = float(h_tx_combo.get())
    wl = float(wavelength.get())
    a = float(a_combo.get())
    b = float(b_combo.get())
    c = float(c_combo.get())
    d = float(d_combo.get())
    v1 = (h_b_tx - h_tx) * math.sqrt((2 / wl) * (1 / a + 1 / b))
    v2 = (h_b_rx - h_rx) * math.sqrt((2 / wl) * (1 / c + 1 / b))
    l1 = 6.9 + 20 * math.log(math.sqrt(math.pow(v1 - 0.1, 2) + 1) + v1 - 0.1)
    l2 = 6.9 + 20 * math.log(math.sqrt(math.pow(v2 - 0.1, 2) + 1) + v2 - 0.1)
    return 20 * math.log(4 * math.pi * d / wl) + l1 + l2 + 10 * math.log((a + b) * (b + c) / (b * (a + b + c)))


def e_below_rooftop_to_street_2_turn_click(event):
    global alpha, beta, gamma, standard_deviation
    if e_combo.get() == "Urban high-rise/NLoS":
        alpha = 4.00
        beta = 10.2
        gamma = 2.36
        standard_deviation = 7.60


def e_below_rooftop_to_street_1_turn_click(event):
    global alpha, beta, gamma, standard_deviation
    # x1+x2 should be in given range
    if e_combo.get() == "Urban high-rise/LoS":
        x_1_combo.config(values=list(range(55, 1201)))
        x_1_combo.current(0)
        x_2_combo.config(values=list(range(55, 1201)))
        x_2_combo.current(0)
        f_combo.config(values=[2400, 3705, 4860])
        f_combo.current(0)
    elif e_combo.get() == "Urban low-rise/LoS":
        x_1_combo.config(values=list(range(55, 1201)))
        x_1_combo.current(0)
        x_2_combo.config(values=list(range(55, 1201)))
        x_2_combo.current(0)
        f_combo.config(values=[2400, 3705, 4860])
        f_combo.current(0)
    elif e_combo.get() == "Urban high-rise/NLoS":
        alpha = 4.00
        beta = 10.2
        gamma = 2.36
        standard_deviation = 7.60
        x_1_combo.config(values=list(range(260, 1201)))
        x_1_combo.current(0)
        x_2_combo.config(values=list(range(260, 1201)))
        x_2_combo.current(0)
        f_combo.config(values=[2400, 3705, 4860])
        f_combo.current(0)
    fr_label.pack()
    f_combo.pack()
    x_1_label.pack()
    x_1_combo.pack()
    x_2_label.pack()
    x_2_combo.pack()
    path_loss_button.pack(pady=10)


def avg_height_click(event):
    f_combo.pack_forget()
    fr_label.pack_forget()
    path_loss_button.pack_forget()
    h1 = float(height_1.get())
    hr = float(avg_height_combo.get())
    w2 = float(sidewalk.get())
    if h1 < hr and w2 < 10:
        f_combo.config(values=list(range(2000, 16001)))
    else:
        f_combo.config(values=list(range(800, 5001)))
    fr_label.pack()
    f_combo.pack()
    path_loss_button.pack(pady=10)


def f_below_rooftop_click(event):
    if float(f_1_combo.get()) > 2:
        path_loss_button.pack_forget()
        wavelength_label.pack_forget()
        wavelength.pack_forget()
        range_label.pack()
        range_combo.pack()
        height_label_1.pack()
        height_1.pack()
        height_label_2.pack()
        height_2.pack()
        b_label.pack()
        b_combo.pack()
        env_label.pack()
        env_combo.pack()
    else:
        range_label.pack_forget()
        range_combo.pack_forget()
        height_label_1.pack_forget()
        height_1.pack_forget()
        height_label_2.pack_forget()
        height_2.pack_forget()
        b_label.pack()
        b_combo.pack()
        env_label.pack_forget()
        env_combo.pack_forget()
        wavelength_label.pack()
        wavelength.pack()
        path_loss_button.pack(pady=10)


def range_click(event):
    global is_UHF_propagation, is_SHF_propagation, is_EHF_propagation
    global traffic_label, traffic_combo, environment_options
    scenario = scenario_combo.get()
    is_UHF_propagation = False
    is_SHF_propagation = False
    is_EHF_propagation = False
    if range_combo.get() == "UHF propagation":
        path_loss_button.pack_forget()
        p_total_label.pack_forget()
        p_total.pack_forget()
        density_label.pack_forget()
        density.pack_forget()
        temp_label.pack_forget()
        temp.pack_forget()
        e_label.pack_forget()
        e_combo.pack_forget()
        traffic_label.pack_forget()
        traffic_combo.pack_forget()
        is_UHF_propagation = True
        height_1.config(values=list(range(1, 11)))
        height_1.current(0)
        height_2.config(values=list(range(1, 11)))
        height_2.current(0)
        if scenario == "Site Specific Model for below rooftop LoS" or scenario == "Site Specific Model from below " \
                                                                                  "rooftop to street level LoS":
            f_combo.config(values=list(np.round(np.arange(0.3, 3.1, 0.1), 1)))
            f_combo.current(0)
            f_label.pack()
            f_combo.pack()
        elif scenario == scenarios_options[10]:
            f_combo.config(values=[2400])
            f_combo.current(0)
            fr_label.pack()
            f_combo.pack()
        wavelength_label.pack()
        wavelength.pack()
        path_loss_button.pack(pady=10)
    elif range_combo.get() == "SHF propagation":
        # The roadway is 27 m wide, including 6 m wide footpaths on either side
        fr_label.pack_forget()
        f_1_combo.pack_forget()
        f_label.pack_forget()
        f_combo.pack_forget()
        p_total_label.pack_forget()
        p_total.pack_forget()
        density_label.pack_forget()
        density.pack_forget()
        temp_label.pack_forget()
        temp.pack_forget()
        path_loss_button.pack_forget()
        e_label.pack_forget()
        e_combo.pack_forget()
        is_SHF_propagation = True
        if scenario == "Site Specific Model for below rooftop LoS" or scenario == "Site Specific Model from below " \
                                                                                  "rooftop to street level LoS":
            f_combo.config(values=[3.35, 8.45, 15.75])
            f_combo.current(0)
            f_label.pack()
            f_combo.pack()
        elif scenario == "Site Specific Model for below rooftop NLoS":
            f_1_combo.config(values=[3.35, 8.45, 15.75])
            f_1_combo.current(0)
            f_label.pack()
            f_1_combo.pack()
        elif scenario == scenarios_options[10]:
            f_combo.config(values=[3705, 4860])
            f_combo.current(0)
            fr_label.pack()
            f_combo.pack()
        traffic_label.pack()
        traffic_combo.pack()
        wavelength_label.pack()
        wavelength.pack()
        path_loss_button.pack(pady=10)
        height_1.config(values=[4, 8])
        height_1.current(0)
        height_2.config(values=[2.7, 1.6])
        height_2.current(0)
    elif range_combo.get() == "EHF propagation (Millimeter Wave)":
        f_1_combo.pack_forget()
        wavelength_label.pack_forget()
        wavelength.pack_forget()
        f_label.pack_forget()
        f_combo.pack_forget()
        traffic_label.pack_forget()
        traffic_combo.pack_forget()
        path_loss_button.pack_forget()
        height_1.config(values=list(range(1, 11)))
        height_1.current(0)
        height_2.config(values=list(range(1, 11)))
        height_2.current(0)
        is_EHF_propagation = True
        environment_options = [
            "Urban very high-rise with frequency 28 GHz",
            "Urban low-rise with frequency 28 GHz",
            "Urban low-rise with frequency 60 GHz"
        ]
        e_label.pack(pady=2)
        e_combo.set("Select environment")
        e_combo.config(values=environment_options, width=40)
        e_combo.bind("<<ComboboxSelected>>", e_below_rooftop_los_click)
        e_combo.pack()
        temp_label.pack()
        temp.pack()
        density_label.pack()
        density.pack()
        p_total_label.pack()
        p_total.pack()
        path_loss_button.pack(pady=10)


def area_click(event):
    global power_loss_coefficient, floor_penetration_loss_factor
    d_combo.current(0)
    if area_combo.get() == "Residential":
        num_combo.config(values=list(range(1, 10)))
        num_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(1.8, 2.1, 0.1), 1)))
        f_combo.current(0)
        power_loss_coefficient = 28
        floor_penetration_loss_factor = 4 * int(num_combo.get())
    elif area_combo.get() == "Office":
        num_combo.config(values=list(range(1, 4)))
        num_combo.current(0)
        f_options = list(np.round(np.arange(1.8, 2.1, 0.1), 1))
        f_options.insert(0, 0.9)
        f_combo.config(values=f_options)
        f_combo.current(0)
        if f_combo.get() == 0.9:
            power_loss_coefficient = 33
            if num_combo.get() == 1:
                floor_penetration_loss_factor = 9
            elif num_combo.get() == 2:
                floor_penetration_loss_factor = 19
            elif num_combo.get() == 3:
                floor_penetration_loss_factor = 24
        else:
            power_loss_coefficient = 30
            floor_penetration_loss_factor = 15 + 4 * (int(num_combo.get()) - 1)
    elif area_combo.get() == "Commercial":
        num_combo.config(values=list(range(1, 10)))
        num_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(1.8, 2.1, 0.1), 1)))
        f_combo.current(0)
        power_loss_coefficient = 22
        floor_penetration_loss_factor = 6 + 3 * (int(num_combo.get()) - 1)
    d_label.pack()
    d_combo.current(0)
    d_combo.pack()
    f_label.pack()
    f_combo.pack()
    path_loss_button.pack(pady=20)


def e_below_rooftop_los_click(event):
    global path_loss_exponent, freq
    if e_combo.get() == environment_options[0]:
        path_loss_exponent = 2.21
        freq = 28
    elif e_combo.get() == environment_options[1]:
        path_loss_exponent = 2.06
        freq = 28
    elif e_combo.get() == environment_options[2]:
        path_loss_exponent = 1.9
        freq = 60


def e_below_rooftop_to_street_click(event):
    global l_urban
    if e_combo.get() == "urban":
        l_urban = 0
    elif e_combo.get() == "suburban":
        l_urban = 6.8
    elif e_combo.get() == "dense urban/high-rise":
        l_urban = 2.3
    d_combo.config(values=list(range(1, 3001)))
    f_combo.config(values=list(range(300, 3001)))
    d_label.pack()
    d_combo.current(0)
    d_combo.pack()
    fr_label.pack()
    f_combo.current(0)
    f_combo.pack()
    percentage_combo.current(0)
    path_loss_button.pack(pady=20)


def e_below_rooftop_click(event):
    global alpha, beta, gamma, standard_deviation
    if e_combo.get() == "Urban high-rise/LoS" or e_combo.get() == "Urban low-rise/LoS":
        alpha = 2.12
        beta = 29.2
        gamma = 2.11
        standard_deviation = 5.06
        d_combo.config(values=list(range(5, 661)))
        d_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(0.8, 73.1, 0.1), 1)))
        f_combo.current(0)
    elif e_combo.get() == "Urban high-rise/NLoS":
        alpha = 4.00
        beta = 10.2
        gamma = 2.36
        standard_deviation = 7.60
        d_combo.config(values=list(range(30, 716)))
        d_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(0.8, 38.1, 0.1), 1)))
        f_combo.current(0)
    elif e_combo.get() == "Urban low-rise/NLoS":
        alpha = 5.06
        beta = -4.68
        gamma = 2.02
        standard_deviation = 9.33
        d_combo.config(values=list(range(30, 251)))
        d_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(10, 73.1, 0.1), 1)))
        f_combo.current(0)
    d_label.pack()
    d_combo.pack()
    f_label.pack()
    f_combo.pack()
    path_loss_button.pack(pady=20)


def e_above_rooftop_click(event):
    if e_combo.get() == "Urban high-rise/LoS" or e_combo.get() == "Urban low-rise/LoS":
        d_combo.config(values=list(range(55, 1201)))
        d_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(2.2, 73.1, 0.1), 1)))
        f_combo.current(0)
    elif e_combo.get() == "Urban high-rise/NLoS":
        global alpha, beta, gamma, standard_deviation
        alpha = 4.39
        beta = -6.27
        gamma = 2.30
        standard_deviation = 6.89
        d_combo.config(values=list(range(260, 1201)))
        d_combo.current(0)
        f_combo.config(values=list(np.round(np.arange(2.2, 66.6, 0.1), 1)))
        f_combo.current(0)
    d_label.pack()
    d_combo.pack()
    f_label.pack()
    f_combo.pack()
    path_loss_button.pack(pady=20)


def calculate_below_rooftop_LoS(d, fq):
    global breakpoint_distance, curr_path_loss
    curr_path_loss = -1
    h1 = float(height_1.get())
    h2 = float(height_2.get())
    f = 0
    if range_combo.get() != "EHF propagation (Millimeter Wave)":
        f = fq
    if is_UHF_propagation:
        wl = float(wavelength.get())
        breakpoint_distance = 4 * h1 * h2 / wl
        breakpoint_loss = abs(20 * math.log((math.pow(wl, 2) / (8 * math.pi * h1 * h2)), 10))
        if d < breakpoint_distance:
            curr_path_loss = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
        elif d == breakpoint_distance:
            curr_path_loss = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
        else:
            curr_path_loss = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
    elif is_SHF_propagation:
        global effective_road_height
        wl = float(wavelength.get())
        effective_road_height = -1
        if traffic_combo.get() == "Heavy Traffic":
            if f == 3.35:
                if h1 == 4:
                    if h2 == 2.7:
                        effective_road_height = 1.3
                else:
                    if h2 == 2.7:
                        effective_road_height = 1.6
            elif f == 8.45:
                if h1 == 4:
                    if h2 == 2.7:
                        effective_road_height = 1.6
                else:
                    if h2 == 2.7:
                        effective_road_height = 1.6
            else:
                if h1 == 4:
                    if h2 == 2.7:
                        effective_road_height = 1.4
                else:
                    if h2 == 2.7:
                        effective_road_height = 1000
        else:
            if f == 3.35:
                if h1 == 4:
                    if h2 == 2.7:
                        effective_road_height = 0.59
                    else:
                        effective_road_height = 0.23
            elif f == 8.45:
                if h1 == 4:
                    if h2 == 2.7:
                        effective_road_height = 1000
                    else:
                        effective_road_height = 0.43
                else:
                    if h2 == 2.7:
                        effective_road_height = 1000
            else:
                if h1 == 4:
                    if h2 == 2.7:
                        effective_road_height = 1000
                    else:
                        effective_road_height = 0.74
                else:
                    if h2 == 2.7:
                        effective_road_height = 1000
        # print(effective_road_height)
        if effective_road_height == -1:
            curr_path_loss = -1
        elif effective_road_height == 1000:
            breakpoint_distance = 4 * h1 * h2 / wl
        else:
            breakpoint_distance = 4 * (h1 - effective_road_height) * (h2 - effective_road_height) / wl
        if effective_road_height != -1 and h1 > effective_road_height and h2 > effective_road_height:
            r_s = 20  # experimentally derived
            if d < r_s:
                breakpoint_loss = abs(20 * math.log(
                    (math.pow(wl, 2) / (8 * math.pi * (h1 - effective_road_height) * (h2 - effective_road_height))),
                    10))
                if d < breakpoint_distance:
                    curr_path_loss = breakpoint_loss + 20 * math.log(d / breakpoint_distance, 10)
                elif d == breakpoint_distance:
                    curr_path_loss = breakpoint_loss + 6 + 20 * math.log(d / breakpoint_distance, 10)
                else:
                    curr_path_loss = breakpoint_loss + 20 + 40 * math.log(d / breakpoint_distance, 10)
            else:
                basic_propagations_loss = abs(20 * math.log(wl / 2 * math.pi * r_s, 10))
                curr_path_loss = basic_propagations_loss + 20 + 30 * math.log(d / r_s, 10)
    elif is_EHF_propagation:
        ro = float(density.get())
        t = float(temp.get())
        p_tot = float(p_total.get())
        path_loss_at_reference_distance = 20 * math.log(freq * 1000, 10) - 28
        attenuation_by_gases = find_oxygen_attenuation(freq, t, p_tot)
        attenuation_by_rain = find_water_attenuation(freq, t, p_tot, ro)
        curr_path_loss = path_loss_at_reference_distance + 10 * path_loss_exponent * math.log(
            d) + attenuation_by_gases + attenuation_by_rain
    return curr_path_loss


def settled_field_distance(d, wl, hr, h1):
    return wl * d * d / math.pow((h1 - hr), 2)


def l1_msd(f, d, h1, hr, b):
    ka = 0
    kf = 0
    del_h1 = h1 - hr
    if h1 > hr:
        l_bsh = -18 * math.log(1 + del_h1, 10)
    else:
        l_bsh = 0
    if h1 > hr and f > 2:
        ka = 71.4
    elif h1 <= hr and f > 2 and d >= 500:
        ka = 73 - 0.8 * del_h1
    elif h1 <= hr and f > 2 and d < 500:
        ka = 73 - 1.6 * del_h1 * d / 1000
    elif h1 > hr and f <= 2:
        ka = 54
    elif h1 <= hr and f <= 2 and d >= 500:
        ka = 54 - 0.8 * del_h1
    elif h1 <= hr and f <= 2 and d < 500:
        ka = 54 - 1.6 * h1 * d / 1000
    if h1 > hr:
        kd = 18
    else:
        kd = 18 - 15 * del_h1 / hr
    if f > 2:
        kf = -8
    elif e_combo.get() == environment_options[0] and f <= 2:
        kf = -4 + 0.7 * (f / 925 - 1)
    elif e_combo.get() == environment_options[1] and f <= 2:
        kf = -4 + 1.5 * (f / 925 - 1)
    return l_bsh + ka + kd * math.log(d / 1000, 10) + kf * math.log(f, 10) - 9 * math.log(b, 10)


def l2_msd(f, d, h1, hr, b, wl):
    del_h1 = h1 - hr
    ro = math.sqrt(math.pow(del_h1, 2) + math.pow(b, 2))
    del_hu = math.pow(10, -math.log(math.sqrt(b / wl), 10) - math.log(d, 10) / 9 + 10 * math.log(b / 2.35, 10) / 9)
    del_hl = (((0.00023 * b * b) - (0.1827 * b) - 9.4978) / (math.pow(math.log(f, 10), 2.938))) + 0.000718 * b + 0.06923
    theta = math.atan(del_h1 / b)
    qm = -1
    if h1 > hr + del_hu:
        qm = 2.35 * math.pow((del_h1 / d) * math.sqrt(b / wl), 0.9)
    elif hr + del_hu >= h1 >= hr + del_hl:
        qm = b / d
    elif h1 < hr + del_hl:
        qm = (b / (2 * math.pi * d)) * math.sqrt(wl / ro) * (1 / theta - 1 / (2 * math.pi + theta))
    return -10 * math.log(math.pow(qm, 2), 10)


def find_l_0_n(d, d_rd, phi, h1, h2, hr, w, wl, f):
    k = 0
    while True:
        d_k = find_d_k(k, phi, h1, h2, hr, w)
        d_k1 = find_d_k(k + 1, phi, h1, h2, hr, w)
        if d_k <= d < d_k1 < d_rd:
            l_dk = find_loss_dk(k, phi, h1, h2, hr, w, wl)
            l_dk1 = find_loss_dk(k + 1, phi, h1, h2, hr, w, wl)
            return l_dk + (l_dk1 - l_dk) * (d - d_k) / (d_k1 - d_k)
        elif d_k <= d < d_rd < d_k1:
            l_dk = find_loss_dk(k, phi, h1, h2, hr, w, wl)
            l_d_rd = find_loss_d_rd(k, f, phi, h1, h2, hr, w, wl)
            return l_dk + (l_d_rd - l_dk) * (d - d_k) / (d_rd - d_k)
        k += 1


def find_k(f, phi, h1, h2, hr, w):
    k = 0
    d_rd = find_d_rd(f, phi, h1, h2, hr, w)
    while True:
        d_k = find_d_k(k, phi, h1, h2, hr, w)
        d_k1 = find_d_k(k + 1, phi, h1, h2, hr, w)
        if d_k <= d_rd <= d_k1:
            return k
        k += 1


def find_loss_d_rd(k, f, phi, h1, h2, hr, w, wl):
    l_dk = find_loss_dk(k, phi, h1, h2, hr, w, wl)
    l_dk1 = find_loss_dk(k + 1, phi, h1, h2, hr, w, wl)
    dk = find_d_k(k, phi, h1, h2, hr, w)
    dk1 = find_d_k(k + 1, phi, h1, h2, hr, w)
    d_rd = find_d_rd(f, phi, h1, h2, hr, w)
    return l_dk + ((l_dk1 - l_dk) * (d_rd - dk) / (dk1 - dk))


def find_d_rd(f, phi, h1, h2, hr, w):
    d3 = find_d_kp(3, phi, h1, h2, hr, w)
    d4 = find_d_kp(4, phi, h1, h2, hr, w)
    d1 = find_d_kp(1, phi, h1, h2, hr, w)
    d2 = find_d_kp(2, phi, h1, h2, hr, w)
    return math.log(f, 10) * (
            0.25 * d3 + 0.25 * d4 - 0.16 * d1 - 0.35 * d2) + 0.25 * d1 + 0.56 * d2 + 0.10 * d3 + 0.10 * d4


def find_d_k(k, phi, h1, h2, hr, w):
    b_k = find_bk(k, h1, h2, hr, w)
    return math.sqrt(math.pow(b_k / math.sin(phi), 2) + math.pow((h1 - h2), 2))


def find_loss_dk(k, phi, h1, h2, hr, w, wl):
    d_kp = find_d_kp(k, phi, h1, h2, hr, w)
    return 20 * math.log((4 * math.pi * d_kp / (math.pow(0.4, k) * wl)), 10)


def find_d_kp(k, phi, h1, h2, hr, w):
    phi_k = find_phi_k(k, phi, h1, h2, hr, w)
    a_k = find_ak(k, h1, h2, hr, w)
    return math.sqrt(math.pow(a_k / math.sin(phi_k), 2) + math.pow((h1 - h2), 2))


def find_ak(k, h1, h2, hr, w):
    return w * (h1 - h2) * (2 * k + 1) / (2 * (hr - h2))


def find_bk(k, h1, h2, hr, w):
    return w * (h1 - h2) * (2 * k + 1) / (2 * (hr - h2)) - k * w


def find_phi_k(k, phi, h1, h2, hr, w):
    a_k = find_ak(k, h1, h2, hr, w)
    b_k = find_bk(k, h1, h2, hr, w)
    return math.atan(a_k * phi / b_k)


def find_l_los(d, f):
    # subtracting 10 for considering directivity of the tx antenna
    return 10 * alpha * math.log(d, 10) + beta + 10 * gamma * math.log(f, 10) + standard_deviation - 10


def find_l_los_1_turn(x1, x2, f):
    global l_los
    l_los = calculate_below_rooftop_LoS(x1 + x2, f)
    diff_parameter = 3.45 * math.pow(10, 4) * math.pow(f * math.pow(10, 6), -0.46)
    s_2 = math.pow(diff_parameter, 2)
    d_corner = 30
    if x2 > max(s_2, d_corner):
        return l_los + 10 * math.log((x1 * x2) / (x1 + x2), 10) - 20 * math.log(diff_parameter, 10)
    else:
        l_los_0 = calculate_below_rooftop_LoS(x1, f)
        l_los_max = calculate_below_rooftop_LoS(x1 + max(s_2, d_corner), f)
        return l_los_0 + (l_los_max - l_los_0) * x1 / max(s_2, d_corner)


def n_th_loss_list(turn_dist):
    loss_2_turn = []
    global curr
    curr = 0
    d_corner = 30
    f = float(f_combo.get())
    # print("freq: ", f)
    s_1 = 0.54 * math.pow(f * 1000, 0.076)
    s_2 = 3.45 * math.pow(10, 4) * math.pow(f * math.pow(10, 6), -0.46)
    max_d = max(math.pow(s_2, 2), d_corner)
    for d in turn_dist:
        x1 = d[0]
        x2 = d[1]
        x3 = d[2]
        # print("x1: ", x1, "x2: ", x2, "x3: ", x3)
        if x3 > max_d:
            curr = find_l_los(x1 + x2 + x3, f) + 10 * math.log(x1 * x2 * x3 / (x1 + x2 + x3), 10) - 20 * math.log(s_1,
                                                                                                                  10) - 20 * math.log(
                s_2, 10)
        else:
            l_los_0 = find_l_los_1_turn(x1 + x2, 0, f)
            l_los_max = find_l_los_1_turn(x1 + x2, max(math.pow(s_2, 2), d_corner), f)
            curr = l_los_0 + (l_los_max - l_los_0) * x1 / max_d
        loss_2_turn.append(curr)
    return loss_2_turn


def calculate_path_loss():
    scenario = scenario_combo.get()
    path_loss_root = ctk.CTkToplevel(root)
    path_loss_root.geometry("350x300")
    path_loss_root.title("Path Loss")
    global path_loss, variance, l_urban, breakpoint_distance, l_c, l_att
    if scenario == "Indoor Transmission Loss Model":
        if float(d_combo.get()) >= 5:
            path_loss = 20 * math.log(float(f_combo.get()), 10) + power_loss_coefficient * math.log(
                float(d_combo.get()),
                10) + floor_penetration_loss_factor - 28
        else:
            path_loss = 20 * math.log(float(f_combo.get()), 10) + power_loss_coefficient * math.log(
                float(d_combo.get()),
                10) + floor_penetration_loss_factor
    elif scenario == "Site General Model for above rooftop" or scenario == "Site General Model for below rooftop":
        path_loss = find_l_los(float(d_combo.get()), float(f_combo.get()))
    elif scenario == "Site General Model from below rooftop to street level":
        f = float(f_combo.get())
        d = float(d_combo.get())
        p = int(percentage_combo.get())
        sigma = 7
        w = 20
        l_los_median = 32.45 + 20 * math.log(f, 10) + 20 * math.log(d / 1000, 10)
        los_location_percentage = 1.5624 * sigma * (math.sqrt((-2) * math.log((1 - (p / 100)), 10)) - 1.1774)
        loss_los = l_los_median + los_location_percentage
        l_nlos_median = 9.5 + 45 * math.log(f, 10) + 40 * math.log(d / 1000, 10) + l_urban
        nlos_location_percentage = sigma * (NormalDist().inv_cdf(p / 100))
        loss_nlos = l_nlos_median + nlos_location_percentage
        if p < 45:
            d_los = 212 * (math.pow(math.log(p / 100, 10), 2)) - 64 * math.log(p / 100, 10)
        else:
            d_los = 79.2 - 70 * (p / 100)
        if d < d_los:
            path_loss = loss_los
        elif d > d_los + w:
            path_loss = loss_nlos
        else:
            path_loss = loss_los + (loss_nlos - loss_los) * (d - d_los) / w
    elif scenario == "Site Specific Model for below rooftop LoS" or scenario == "Site Specific Model from below " \
                                                                                "rooftop to street level LoS":
        if f_combo.get() == "Select frequency":
            path_loss = calculate_below_rooftop_LoS(float(d_combo.get()), freq)
        else:
            path_loss = calculate_below_rooftop_LoS(float(d_combo.get()), float(f_combo.get()))
    elif scenario == "Site Specific Model for below rooftop NLoS":
        w1 = float(street_width_1.get())
        w2 = float(street_width_2.get())
        x1 = float(distance_1.get())
        x2 = float(distance_2.get())
        f = float(f_1_combo.get())
        if 0.8 <= f <= 2:
            angle = float(corner_angle.get())
            wl = float(wavelength.get())
            reflection_path_loss = 20 * math.log(x1 + x2, 10) + x1 * x2 * (
                    3.86 / (math.pow(angle, 3.5) * (w1 * w2))) + 20 * math.log(4 * math.pi / wl, 10)
            # check pi and angles conversion
            diffraction_path_loss = 10 * math.log(x1 * x2 * (x1 + x2), 10) + 2 * 40 * (
                    math.atan(x2 / w2) + math.atan(x1 / w1) - math.pi / 2) / (2 * math.pi) - 0.1 * (
                                            90 - angle * (180 / math.pi)) + 20 * math.log(4 * math.pi / wl,
                                                                                          10)

            path_loss = -10 * math.log(
                (math.pow(10, -1 * reflection_path_loss / 10) + math.pow(10, -1 * diffraction_path_loss / 10)), 10)
        else:
            d_corner = 30
            l_corner = 20 if env_combo.get() == env_options[0] else 30
            bet = 6 if b_combo.get() == building_shapes[0] else 4.2 + (1.4 * math.log(f * 1000, 10) - 7.8) * (
                    0.8 * math.log(x1, 10) - 1.0)
            if w1 / 2 + 1 < x2 <= w1 / 2 + 1 + d_corner:
                l_c = l_corner * math.log((x2 - w1 / 2), 10) / math.log(1 + d_corner, 10)
            elif x2 > w1 / 2 + 1 + d_corner:
                l_c = l_corner
            if x2 > w1 / 2 + 1 + d_corner:
                l_att = 10 * bet * math.log(((x1 + x2) / (x1 + w1 / 2 + d_corner)), 10)
            else:
                l_att = 0
            los_loss = calculate_below_rooftop_LoS(float(distance_1.get()), float(f_1_combo.get()))
            path_loss = los_loss + l_c + l_att
    elif scenario == "Site Specific Model for above rooftop in Urban Scenario":
        f = float(f_combo.get())
        d = float(d_combo.get())
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        w1 = float(street_width.get())
        hr = float(avg_height_combo.get())
        wl = float(wavelength.get())
        ds = settled_field_distance(d, wl, hr, h1)
        l = float(length.get())
        b = float(avg_b.get())
        phi = float(corner_angle.get())
        global street_orientation_factor
        if 0 <= phi < 35:
            street_orientation_factor = -10 + 0.354 * phi
        elif 35 <= phi < 55:
            street_orientation_factor = 2.5 + 0.075 * (phi - 35)
        else:
            street_orientation_factor = 4.0 - 0.114 * (phi - 55)
        bf_loss = 32.4 + 20 * math.log(d / 1000, 10) + 20 * math.log(f, 10)
        rts_loss = -8.2 - (10 * math.log(w1, 10)) + (10 * math.log(f, 10)) + (
                20 * math.log((hr - h2), 10)) + street_orientation_factor
        msd_loss = 0
        d_bp = abs(hr - h1) * math.sqrt(1 / wl)
        l_upp = l1_msd(f, d_bp, h1, hr, b)
        l_low = l2_msd(f, d_bp, h1, hr, b, wl)
        l_mid = (l_low + l_upp) / 2
        v = 0.0417
        x = 0.1
        eta = (l_upp - l_low) * v
        d_h_bp = l_upp - l_low
        if l > ds and d_h_bp > 0:
            msd_loss = -math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / x) * (
                    l1_msd(f, d, h1, hr, b) - l_mid) + l_mid
        elif l <= ds and d_h_bp > 0:
            msd_loss = math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / x) * (
                    l2_msd(f, d, h1, hr, b, wl) - l_mid) + l_mid
        elif d_h_bp == 0:
            msd_loss = l2_msd(f, d, h1, hr, b, wl)
        elif l > ds and d_h_bp < 0:
            msd_loss = l1_msd(f, d, h1, hr, b) - math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / eta) * (
                    l_upp - l_mid) - l_upp + l_mid
        elif l <= ds and d_h_bp < 0:
            msd_loss = l2_msd(f, d, h1, hr, b, wl) - math.tanh((math.log(d, 10) - math.log(d_bp, 10)) / eta) * (
                    l_mid - l_low) - l_low + l_mid
        if rts_loss + msd_loss > 0:
            path_loss = bf_loss + rts_loss + msd_loss
        else:
            path_loss = bf_loss
    elif scenario == "Site Specific Model for above rooftop in Suburban Scenario":
        w = float(street_width_first.get())
        phi = float(corner_angle.get())
        wl = float(wavelength.get())
        hr = float(avg_height_combo.get())
        h1 = float(height_1.get())
        h2 = float(height_2.get())
        d = float(d_combo.get())
        f = float(f_combo.get())
        d0 = find_d_k(0, phi, h1, h2, hr, w)
        d_rd = find_d_rd(f, phi, h1, h2, hr, w)
        l_0_n = find_l_0_n(d, d_rd, phi, h1, h2, hr, w, wl, f)
        k_l_drd = find_k(f, phi, h1, h2, hr, w)
        if d < d0:
            path_loss = 20 * math.log((4 * math.pi * d / wl), 10)
        elif d0 <= d <= d_rd:
            path_loss = l_0_n
        elif d >= d_rd:
            path_loss = 32.1 * math.log(d / d_rd, 10) + find_loss_d_rd(k_l_drd, f, phi, h1, h2, hr, w, wl)
    elif scenario == scenarios_options[9]:
        f = float(f_combo.get())
        x1 = float(x_1_combo.get())
        x2 = float(x_2_combo.get())
        l_los = find_l_los(x1 + x2, f)
        diff_parameter = 3.45 * math.pow(10, 4) * math.pow(f * math.pow(10, 6), -0.46)
        s_2 = math.pow(diff_parameter, 2)
        d_corner = 30
        if x2 > max(s_2, d_corner):
            path_loss = l_los + 10 * math.log((x1 * x2) / (x1 + x2), 10) - 20 * math.log(diff_parameter, 10)
        else:
            l_los_0 = find_l_los(x1, f)
            l_los_max = find_l_los(x1 + max(s_2, d_corner), f)
            path_loss = l_los_0 + (l_los_max - l_los_0) * x1 / max(s_2, d_corner)
    elif scenario == scenarios_options[10]:
        global turn_distances
        n = int(num_of_corners.get())
        sleep(1)
        for i in range(1, n + 1):
            print("for "+str(i)+" corner: ")
            x_1 = input("Please enter the distance between first corner and Station 1 in meters:")
            x_2 = input("Please enter the distance between first corner and second corner in meters:")
            x_3 = input("Please enter the distance between second corner and Station 2 in meters:")
            x_dist = [float(x_1), float(x_2), float(x_3)]
            turn_distances.append(x_dist)

        curr_loss = n_th_loss_list(turn_distances)
        curr_sum = 0
        for val in curr_loss:
            # print('val', val)
            curr_sum += math.pow(math.pow(10, val / 10), -1)
            # print(curr_sum)
        path_loss = -10 * math.log(curr_sum, 10)
        print("Please go to GUI to check path loss and channel coefficients")
    elif scenario == scenarios_options[11]:
        global road_distances, path_loss_along_road
        f = float(f_combo.get())
        d = float(d_combo.get())
        wl = float(wavelength.get())
        r = mean_visible_distance()
        loss_between_houses = 20 * math.log(4 * math.pi * d / wl, 10) + 30.6 * math.log(d / r, 10) + 6.88 * math.log(f,
                                                                                                                     10) + 5.76
        loss_rbc = 20 * math.log(4 * math.pi * d / wl, 10)
        over_roof_propagation_loss = find_over_roof_propagation_loss()
        if corner_combo.get() == "before corner":
            path_loss_along_road = loss_rbc
        else:
            road_distances = []
            sleep(1)
            n = int(num_of_corners.get())
            for i in range(1, n + 1):
                print("for "+str(i)+" corner: ")
                road_angle = input("Select road angle of the corner in degrees")
                r_d_t = input("Select road distance from transmitter to the corner in meters")
                r_d_r = input("Select road distance from corner to the receiver in meters")
                curr_parameters = [float(road_angle), float(r_d_t), float(r_d_r)]
                road_distances.append(curr_parameters)
            loss_rac = loss_rbc + find_loss_around_corners(int(num_of_corners.get()), f)
            path_loss_along_road = loss_rac
            print("Please go to GUI to check path loss and channel coefficients")
        path_loss = -10 * math.log(
            1 / math.pow(10, path_loss_along_road / 10) + 1 / math.pow(10, loss_between_houses / 10) + 1 / math.pow(10,
                                                                                                                    over_roof_propagation_loss / 10))

    if path_loss == -1:
        note_label_3.pack()
        return
    variance = math.pow(10, -1 * (path_loss / 10))
    path_loss_text = "Path Loss: " + str(path_loss) + " dB"
    path_loss_label = ctk.CTkLabel(path_loss_root, text=path_loss_text)
    path_loss_label.pack()
    run_label = ctk.CTkLabel(path_loss_root, text="Please select number of monte-carlo runs:")
    run_combo = ttk.Combobox(path_loss_root, values=list(range(1, 10)))
    run_combo['state'] = 'readonly'
    run_combo.current(0)
    run_combo.bind("<<ComboboxSelected>>",
                   lambda event: run_click(event, current_root=path_loss_root, num=run_combo.get()))
    run_label.pack()
    run_combo.pack()


def run_click(event, current_root, num):
    runs = int(num)
    coefficients_label = ctk.CTkLabel(current_root, text="Channel Coefficients are: ")
    coefficients_label.pack()
    np.random.seed(0)
    channel_coefficients = []
    for i in range(1, runs + 1):
        h = math.sqrt(variance) * complex(np.random.randn(1, 1), np.conj(np.random.randn(1, 1)))
        channel_coefficients.append(h)
        h_label = ctk.CTkLabel(current_root, text="h(" + str(i) + "): " + str(h))
        h_label.pack()
    io.savemat('channel_coefficients.mat', {"channel_coefficients": channel_coefficients})


scenario_label = ctk.CTkLabel(root, text="Please select the scenario type:", text_font=("Roboto", 11))
scenario_label.pack(pady=2)
scenario_combo = ttk.Combobox(root, values=scenarios_options, width=70)
scenario_combo['state'] = 'readonly'
scenario_combo.set("Select scenario")
scenario_combo.bind("<<ComboboxSelected>>", scenario_click)
scenario_combo.pack()

e_label = ctk.CTkLabel(root, text="Please select environment type:", text_font=("Roboto", 11))
e_combo = ttk.Combobox(root, values=environment_options)
e_combo['state'] = 'readonly'

area_label = ctk.CTkLabel(root, text="Please select area:", text_font=("Roboto", 11))
area_combo = ttk.Combobox(root, values=area_options)
area_combo['state'] = 'readonly'
area_combo.set("Select area")
area_combo.bind("<<ComboboxSelected>>", area_click)

env_label = ctk.CTkLabel(root, text="Please select urban or residential environment:", text_font=("Roboto", 11))
env_combo = ttk.Combobox(root, values=env_options)
env_combo['state'] = 'readonly'
env_combo.current(0)

num_label = ctk.CTkLabel(root, text="Please select number of floors:", text_font=("Roboto", 11))
num_combo = ttk.Combobox(root, values=[""])
num_combo['state'] = 'readonly'
num_combo.set("Select number of floors")

d_label = ctk.CTkLabel(root, text="Please select separation distance between the BS-UE in meters:",
                       text_font=("Roboto", 11))
d_2_label = ctk.CTkLabel(root, text="Enter distance from Station 1 to Station 2 in meters: ", text_font=("Roboto", 11))
d_3_label = ctk.CTkLabel(root, text="Please select path length in meters:", text_font=("Roboto", 11))
d_combo = ttk.Combobox(root, values=list(range(1, 101)))
d_combo['state'] = 'readonly'
d_combo.set("Select distance")

f_label = ctk.CTkLabel(root, text="Please select frequency in GHz:", text_font=("Roboto", 11))
fr_label = ctk.CTkLabel(root, text="Please select frequency in MHz:", text_font=("Roboto", 11))
f_combo = ttk.Combobox(root, values=[""])
f_combo['state'] = 'readonly'
f_combo.set("Select frequency")
f_1_combo = ttk.Combobox(root, values=[""])
f_1_combo['state'] = 'readonly'
f_1_combo.set("Select frequency")

percentage_label = ctk.CTkLabel(root, text="Please select the required location percentage (%):",
                                text_font=("Roboto", 11))
percentage_combo = ttk.Combobox(root, values=list(range(1, 100)))
percentage_combo.current(0)
percentage_combo['state'] = 'readonly'

range_label = ctk.CTkLabel(root, text="Please select frequency range:", text_font=("Roboto", 11))
range_combo = ttk.Combobox(root, values=frequency_ranges)
range_combo['state'] = 'readonly'
range_combo.set("Select frequency range")
range_combo.bind("<<ComboboxSelected>>", range_click)

height_label_1 = ctk.CTkLabel(root, text="Enter height of Station 1 in meters: ", text_font=("Roboto", 11))
height_1 = ttk.Combobox(root, values=list(range(1, 11)))
height_1['state'] = 'readonly'
height_1.set("Select station 1 height")

height_label_2 = ctk.CTkLabel(root, text="Enter height of Station 2 in meters: ", text_font=("Roboto", 11))
height_2 = ttk.Combobox(root, values=list(range(1, 11)))
height_2['state'] = 'readonly'
height_2.set("Select station 2 height")

traffic_label = ctk.CTkLabel(root, text="Please select traffic conditions:", text_font=("Roboto", 11))
traffic_combo = ttk.Combobox(root, values=["Heavy Traffic", "Light Traffic"])
traffic_combo['state'] = 'readonly'
traffic_combo.current(0)

sidewalk_label = ctk.CTkLabel(root, text="Enter width of the sidewalk in meters: ", text_font=("Roboto", 11))
sidewalk = ttk.Entry(root, textvariable=DoubleVar)

street_width_label = ctk.CTkLabel(root, text="Enter width of the street in meters: ", text_font=("Roboto", 11))
street_width = ttk.Entry(root, textvariable=DoubleVar)
street_width_first = ttk.Combobox(root, values=list(range(10, 26)))
street_width_first['state'] = 'readonly'
street_width_first.set("Select width of the street")

length_label = ctk.CTkLabel(root, text="Enter length of the path covered by buildings in meters: ",
                            text_font=("Roboto", 11))
length = ttk.Entry(root, textvariable=DoubleVar)

avg_b_label = ctk.CTkLabel(root, text="Enter average separation of buildings in meters: ", text_font=("Roboto", 11))
avg_b = ttk.Entry(root, textvariable=DoubleVar)

avg_height_label = ctk.CTkLabel(root, text="Please select average height of buildings in meters:",
                                text_font=("Roboto", 11))
avg_height_combo = ttk.Combobox(root, values=list(range(1, 6)))
avg_height_combo['state'] = 'readonly'

angle_2_label = ctk.CTkLabel(root, text="Please select angle of orientation of the street in degrees:",
                             text_font=("Roboto", 11))
corner_angle_label = ctk.CTkLabel(root, text="Enter corner angle in radians: ", text_font=("Roboto", 11))
corner_angle = ttk.Entry(root, textvariable=DoubleVar)

wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Roboto", 11))
wavelength = ttk.Entry(root, textvariable=DoubleVar)

temp_label = ctk.CTkLabel(root, text="Enter mean temperature in celsius: ", text_font=("Roboto", 11))
temp = ttk.Entry(root, textvariable=DoubleVar)

density_label = ctk.CTkLabel(root, text="Enter water vapour density in g/m3: ", text_font=("Roboto", 11))
density = ttk.Entry(root, textvariable=DoubleVar)

p_total_label = ctk.CTkLabel(root, text="Enter total air pressure in hPa: ", text_font=("Roboto", 11))
p_total = ttk.Entry(root, textvariable=DoubleVar)

b_label = ctk.CTkLabel(root, text="Please select shape of building:", text_font=("Roboto", 11))
b_combo = ttk.Combobox(root, values=building_shapes)
b_combo['state'] = 'readonly'
b_combo.set("Select building shape")

street_width_label_1 = ctk.CTkLabel(root, text="Enter street width at position of Station 1 in meters: ",
                                    text_font=("Roboto", 11))
street_width_1 = ttk.Entry(root, textvariable=DoubleVar)

street_width_label_2 = ctk.CTkLabel(root, text="Enter street width at position of Station 2 in meters: ",
                                    text_font=("Roboto", 11))
street_width_2 = ttk.Entry(root, textvariable=DoubleVar)

distance_label_1 = ctk.CTkLabel(root, text="Enter distance from Station 1 to street crossing in meters: ",
                                text_font=("Roboto", 11))
distance_1 = ttk.Entry(root, textvariable=DoubleVar)

distance_label_2 = ctk.CTkLabel(root, text="Enter distance from Station 2 to street crossing in meters: ",
                                text_font=("Roboto", 11))
distance_2 = ttk.Entry(root, textvariable=DoubleVar)

note_label = ctk.CTkLabel(root, text="Height of station 2 should be less than the average height of buildings",
                          text_font=("Roboto", 9))
note_label_2 = ctk.CTkLabel(root, text="Please go to terminal for entering values of corner distances after clicking "
                                       "on path loss button", text_font=("Roboto", 11))
note_label_3 = ctk.CTkLabel(root, text="Invalid parameters", text_font=("Roboto", 11))

x_1_label = ctk.CTkLabel(root, text="Please select the distance between corner and Station 1 in meters:",
                         text_font=("Roboto", 11))
x_1_combo = ttk.Combobox(root, values=[""])
x_1_combo['state'] = 'readonly'

x_2_label = ctk.CTkLabel(root, text="Please select the distance between corner and Station 2 in meters:",
                         text_font=("Roboto", 11))
x_2_combo = ttk.Combobox(root, values=[""])
x_2_combo['state'] = 'readonly'

h_b_tx_label = ctk.CTkLabel(root,
                            text="Please select height of nearest building from transmitter in receiver direction in "
                                 "meters:",
                            text_font=("Roboto", 11))
h_b_tx_combo = ttk.Combobox(root, values=list(range(1, 101)))
h_b_tx_combo['state'] = 'readonly'

h_b_rx_label = ctk.CTkLabel(root,
                            text="Please select height of nearest building from receiver in transmitter direction in "
                                 "meters:",
                            text_font=("Roboto", 11))
h_b_rx_combo = ttk.Combobox(root, values=list(range(1, 101)))
h_b_rx_combo['state'] = 'readonly'

h_rx_label = ctk.CTkLabel(root, text="Please select receiver antenna height in meters:", text_font=("Roboto", 11))
h_rx_combo = ttk.Combobox(root, values=list(range(1, 101)))
h_rx_combo['state'] = 'readonly'

h_tx_label = ctk.CTkLabel(root, text="Please select transmitter antenna height in meters:", text_font=("Roboto", 11))
h_tx_combo = ttk.Combobox(root, values=list(range(1, 101)))
h_tx_combo['state'] = 'readonly'

a_label = ctk.CTkLabel(root,
                       text="Please select distance between transmitter and nearest building from transmitter in "
                            "meters:",
                       text_font=("Roboto", 11))
a_combo = ttk.Combobox(root, values=list(range(1, 101)))
a_combo['state'] = 'readonly'

b_label = ctk.CTkLabel(root,
                       text="Please select distance between nearest buildings from transmitter and receiver in meters:",
                       text_font=("Roboto", 11))
b_combo = ttk.Combobox(root, values=list(range(1, 101)))
b_combo['state'] = 'readonly'

c_label = ctk.CTkLabel(root,
                       text="Please select distance between receiver and nearest building from receiver in meters:",
                       text_font=("Roboto", 11))
c_combo = ttk.Combobox(root, values=list(range(1, 101)))
c_combo['state'] = 'readonly'

b_d_label = ctk.CTkLabel(root, text="Enter building density in buildings/km2: ", text_font=("Roboto", 11))
b_d_input = ttk.Entry(root, textvariable=DoubleVar)

avg_building_h_label = ctk.CTkLabel(root,
                                    text="Enter average building height of the buildings with less than 3 stories in "
                                         "meters: (less than 6 meters)", text_font=("Roboto", 11))
avg_building_h_input = ttk.Entry(root, textvariable=DoubleVar)

corner_label = ctk.CTkLabel(root, text="Select corner", text_font=("Roboto", 11))
corner_combo = ttk.Combobox(root, values=["before corner", "after corner"])
corner_combo['state'] = 'readonly'

num_of_corners_label = ctk.CTkLabel(root, text="Please select for how many 2-Turn route path, you want to calculate "
                                               "path loss:", text_font=("Roboto", 11))
num_of_corners_label_1 = ctk.CTkLabel(root, text="Please select number of corners", text_font=("Roboto", 11))
num_of_corners = ttk.Combobox(root, values=list(range(1, 5)))
num_of_corners['state'] = 'readonly'
num_of_corners.current(0)

path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                 command=calculate_path_loss)

root.mainloop()
