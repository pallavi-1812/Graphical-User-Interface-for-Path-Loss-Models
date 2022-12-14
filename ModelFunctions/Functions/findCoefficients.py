import math
import customtkinter as ctk
from tkinter import ttk
from tkinter import *
from scipy import io
import numpy as np


def power_computation(coefficients, n, current_root, power):
    pow_level = []
    sum_of_pow = 0
    pw = float(power)
    for i in range(0, n):
        p = pw * abs(coefficients[i])
        pow_level.append(p)
    for p in pow_level:
        sum_of_pow += p
    avg_pow = sum_of_pow / n
    pow_in_dbm = 10*math.log(avg_pow, 10) + 30
    avg_pow_text = "Average Power: " + str(round(pow_in_dbm, 2)) + " dBm"
    avg_pow_label = ctk.CTkButton(current_root, text=avg_pow_text, fg_color="#C3F8FF", text_color="#400D51",
                                  hover_color="#C3F8FF", text_font=("Helvetica", 12))
    avg_pow_label.pack(pady=7)


def rate_computation(coefficients, n, current_root, power):
    bandwidth = 1  # in MHz
    p = float(power)
    sigma_sq = math.pow(10, -11)
    rate = []
    sum_of_rate = 0
    for i in range(0, n):
        r = bandwidth * math.log(1 + (p * abs(coefficients[i]) / sigma_sq), 2)
        rate.append(r)
    for r in rate:
        sum_of_rate += r
    avg_rate = sum_of_rate / n
    avg_rate_text = "Average Rate: " + str(round(avg_rate, 2)) + " mbps"
    avg_rate_label = ctk.CTkButton(current_root, text=avg_rate_text, fg_color="#C3F8FF", text_color="#400D51",
                                   hover_color="#C3F8FF", text_font=("Helvetica", 12))
    avg_rate_label.pack(pady=10)


def run_click(current_root, num, variance, file_name, power):
    runs = int(num)
    np.random.seed(0)
    channel_coefficients = []
    for i in range(1, runs + 1):
        h = math.sqrt(variance) * complex(np.random.randn(1, 1), np.conj(np.random.randn(1, 1)))
        channel_coefficients.append(h)
    coefficients_note = "Channel Coefficients have been downloaded \ninto a matlab file in your system"
    coefficients_note_label = ctk.CTkButton(current_root, fg_color="#FFE15D", text_color="#DC3535",
                                            hover_color="#FFE15D",
                                            height=25, text_font=("Ariel", 11, "bold"), text=coefficients_note)
    coefficients_note_label.pack(pady=10)
    filename = "channel_coefficients_" + file_name + "_loss.mat"
    io.savemat(filename, {"channel_coefficients": channel_coefficients})
    rate_computation(channel_coefficients, runs, current_root, power)
    power_computation(channel_coefficients, runs, current_root, power)


def calculatePathLossAndCoefficients(loss, scenario_name, path_loss_root):
    path_loss = round(loss, 2)
    variance = math.pow(10, -1 * (path_loss / 10))
    path_loss_text = "Path Loss: " + str(path_loss) + " dB"
    path_loss_label = ctk.CTkButton(path_loss_root, text=path_loss_text, fg_color="#C3F8FF", text_color="#400D51",
                                    hover_color="#C3F8FF", text_font=("Helvetica", 12))
    path_loss_label.pack(pady=10)
    power_label = ctk.CTkLabel(path_loss_root, text="Enter input power in watts:", text_font=("Helvetica", 12))
    power_label.pack()
    input_power = ttk.Entry(path_loss_root, textvariable=DoubleVar)
    input_power.pack()
    run_label = ctk.CTkLabel(path_loss_root, text="Please select number of monte-carlo runs:",
                             text_font=("Helvetica", 12))
    run_combo = ttk.Entry(path_loss_root, textvariable=DoubleVar)
    run_label.pack()
    run_combo.pack()
    button = ctk.CTkButton(path_loss_root, text="Calculate channel coefficients, power and rate levels",
                           fg_color="#FF577F", hover_color="#FF577F", text_color="white",
                           command=lambda: run_click(current_root=path_loss_root, num=run_combo.get(),
                                                     variance=variance, file_name=scenario_name,
                                                     power=input_power.get()))
    button.pack(pady=15)
