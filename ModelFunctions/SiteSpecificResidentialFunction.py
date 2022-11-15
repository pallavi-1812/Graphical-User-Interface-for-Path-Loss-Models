import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import math
from time import sleep
from scipy import io
import numpy as np
from GUIs.ModelFunctions.Functions.rateLevel import rate_computation


def site_specific_residential():
    root = ctk.CTk()
    root.geometry("700x700")
    root.title("Site Specific for residential environments")

    path_loss = 0
    variance = 0
    road_distances = []
    path_loss_along_road = 0

    def find_loss_around_corners(n, f):
        curr_sum = 0
        for dist in road_distances:
            theta = dist[0]
            x_1 = dist[1]
            x_2 = dist[2]
            curr_sum += ((7.18 * math.log(theta, 10) + 0.97 * math.log(f, 10) + 6.1) * (
                    1 - math.exp(-3.72 * math.pow(10, -5) * theta * x_2 * x_1)))
        return curr_sum

    def corner_click(event):
        path_loss_button.pack_forget()
        if corner_combo.get() == "after corner":
            num_of_corners_label_1.pack()
            num_of_corners.pack()
            note_label.pack()
        else:
            num_of_corners_label_1.pack_forget()
            num_of_corners.pack_forget()
            note_label.pack_forget()
        path_loss_button.pack(pady=5)

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

    def calculate_path_loss():
        path_loss_root = ctk.CTkToplevel(root)
        path_loss_root.geometry("500x400")
        path_loss_root.title("Path Loss")
        nonlocal path_loss, variance, path_loss_along_road, road_distances
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
            sleep(2)
            n = int(num_of_corners.get())
            for i in range(1, n + 1):
                print("for " + str(i) + " corner: ")
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
        io.savemat('../channel_coefficients_site_specific_residential_loss.mat',
                   {"channel_coefficients": channel_coefficients})
        rate_computation(channel_coefficients, runs, current_root)

    d_label = ctk.CTkLabel(root, text="Please select the distance between two terminals in meters:", text_font=("Roboto", 11))
    d_label.pack()
    d_combo = ttk.Combobox(root, values=list(range(1, 1001)))
    d_combo.current(0)
    d_combo['state'] = 'readonly'
    d_combo.pack()

    f_label = ctk.CTkLabel(root, text="Please select operating frequency in GHz:", text_font=("Roboto", 11))
    f_label.pack()
    f_combo = ttk.Combobox(root, values=list(range(2, 27)))
    f_combo.current(0)
    f_combo['state'] = 'readonly'
    f_combo.pack()

    wavelength_label = ctk.CTkLabel(root, text="Enter carrier wavelength in meters: ", text_font=("Roboto", 11))
    wavelength_label.pack()
    wavelength = ttk.Entry(root, textvariable=DoubleVar)
    wavelength.pack()

    h_b_tx_label = ctk.CTkLabel(root,
                                text="Please select height of nearest building from transmitter in receiver direction "
                                     "in "
                                     "meters:", text_font=("Roboto", 11))
    h_b_tx_label.pack()
    h_b_tx_combo = ttk.Entry(root, textvariable=DoubleVar)
    h_b_tx_combo.pack()

    h_b_rx_label = ctk.CTkLabel(root,
                                text="Please select height of nearest building from receiver in transmitter direction "
                                     "in "
                                     "meters:", text_font=("Roboto", 11))
    h_b_rx_label.pack()
    h_b_rx_combo = ttk.Entry(root, textvariable=DoubleVar)
    h_b_rx_combo.pack()

    h_rx_label = ctk.CTkLabel(root, text="Please select receiver antenna height in meters:", text_font=("Roboto", 11))
    h_rx_label.pack()
    h_rx_combo = ttk.Combobox(root, values=list(np.round(np.arange(1.2, 6.1, 0.1), 1)))
    h_rx_combo.current(0)
    h_rx_combo['state'] = 'readonly'
    h_rx_combo.pack()

    h_tx_label = ctk.CTkLabel(root, text="Please select transmitter antenna height in meters:", text_font=("Roboto", 11))
    h_tx_label.pack()
    h_tx_combo = ttk.Combobox(root, values=list(np.round(np.arange(1.2, 6.1, 0.1), 1)))
    h_tx_combo.current(0)
    h_tx_combo['state'] = 'readonly'
    h_tx_combo.pack()

    a_label = ctk.CTkLabel(root,
                           text="Please select distance between transmitter and nearest building from transmitter in "
                                "meters:", text_font=("Roboto", 11))
    a_label.pack()
    a_combo = ttk.Entry(root, textvariable=DoubleVar)
    a_combo.pack()

    b_label = ctk.CTkLabel(root,
                           text="Please select distance between nearest buildings from transmitter and receiver in "
                                "meters:", text_font=("Roboto", 11))
    b_label.pack()
    b_combo = ttk.Entry(root, textvariable=DoubleVar)
    b_combo.pack()

    c_label = ctk.CTkLabel(root,
                           text="Please select distance between receiver and nearest building from receiver in meters:", text_font=("Roboto", 11))
    c_label.pack()
    c_combo = ttk.Entry(root, textvariable=DoubleVar)
    c_combo.pack()

    b_d_label = ctk.CTkLabel(root, text="Enter building density in buildings/km2: ", text_font=("Roboto", 11))
    b_d_label.pack()
    b_d_input = ttk.Entry(root, textvariable=DoubleVar)
    b_d_input.pack()

    avg_building_h_label = ctk.CTkLabel(root,
                                        text="Enter average building height of the buildings with less than 3 stories "
                                             "in meters: (less than 6 meters)", text_font=("Roboto", 11))
    avg_building_h_label.pack()
    avg_building_h_input = ttk.Entry(root, textvariable=DoubleVar)
    avg_building_h_input.pack()

    corner_label = ctk.CTkLabel(root, text="Select corner", text_font=("Roboto", 11))
    corner_label.pack()
    corner_combo = ttk.Combobox(root, values=["before corner", "after corner"])
    corner_combo['state'] = 'readonly'
    corner_combo.current(0)
    corner_combo.bind("<<ComboboxSelected>>", corner_click)
    corner_combo.pack()

    num_of_corners_label_1 = ctk.CTkLabel(root, text="Please select number of corners", text_font=("Roboto", 11))
    num_of_corners = ttk.Combobox(root, values=list(range(1, 5)))
    num_of_corners['state'] = 'readonly'
    num_of_corners.current(0)

    note_label = ctk.CTkLabel(root,
                              text="Please go to terminal for entering values of corner distances after clicking on "
                                   "path loss button", text_font=("Roboto", 11))

    path_loss_button = ctk.CTkButton(root, text="Calculate Path Loss", border_width=2,
                                     command=calculate_path_loss)
    path_loss_button.pack(pady=20)

    root.mainloop()
