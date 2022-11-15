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
        p_label = ctk.CTkLabel(current_root, text="P(" + str(i+1) + "): " + str(p) + " W")
        p_label.pack()
    for p in pow_level:
        sum_of_pow += p
    avg_pow = sum_of_pow / n
    avg_pow_text = "Average Power: " + str(avg_pow) + " W"
    avg_pow_label = ctk.CTkLabel(current_root, text=avg_pow_text)
    avg_pow_label.pack()


def rate_computation(coefficients, n, current_root, power):
    bandwidth = 1  # in MHz
    p = float(power)
    sigma_sq = math.pow(10, -11)
    rate = []
    sum_of_rate = 0
    for i in range(0, n):
        r = bandwidth * math.log(1 + (p * abs(coefficients[i]) / sigma_sq), 2)
        rate.append(r)
        r_label = ctk.CTkLabel(current_root, text="R(" + str(i+1) + "): " + str(r) + " bps")  # bits per second
        r_label.pack()
    for r in rate:
        sum_of_rate += r
    avg_rate = sum_of_rate / n
    avg_rate_text = "Average Rate: " + str(avg_rate) + " bps"
    avg_rate_label = ctk.CTkLabel(current_root, text=avg_rate_text)
    avg_rate_label.pack()


def run_click(current_root, num, variance, file_name, power):
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
    filename = "channel_coefficients_" + file_name + "_loss.mat"
    io.savemat(filename, {"channel_coefficients": channel_coefficients})
    rate_computation(channel_coefficients, runs, current_root, power)
    power_computation(channel_coefficients, runs, current_root, power)


def calculatePathLossAndCoefficients(path_loss, scenario_name, path_loss_root):
    variance = math.pow(10, -1 * (path_loss / 10))
    path_loss_text = "Path Loss: " + str(path_loss) + " dB"
    path_loss_label = ctk.CTkLabel(path_loss_root, text=path_loss_text)
    path_loss_label.pack()
    power_label = ctk.CTkLabel(path_loss_root, text="Enter input power in watts:")
    power_label.pack()
    input_power = ttk.Entry(path_loss_root, textvariable=DoubleVar)
    input_power.pack()
    run_label = ctk.CTkLabel(path_loss_root, text="Please select number of monte-carlo runs:")
    run_combo = ttk.Entry(path_loss_root, textvariable=DoubleVar)
    run_label.pack()
    run_combo.pack()
    button = ctk.CTkButton(path_loss_root, text="Calculate channel coefficients, power and rate levels",
                           command=lambda: run_click(current_root=path_loss_root, num=run_combo.get(),
                                                     variance=variance, file_name=scenario_name, power=input_power.get()))
    button.pack(pady=10)



