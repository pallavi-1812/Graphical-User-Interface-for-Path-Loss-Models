import customtkinter as ctk
import math


def rate_computation(coefficients, n, current_root):
    bandwidth = 1  # in MHz
    power = 1  # in W
    sigma_sq = math.pow(10, -11)
    rate = []
    sum_of_rate = 0
    for i in range(0, n):
        r = bandwidth * math.log(1 + (power * abs(coefficients[i]) / sigma_sq), 2)
        rate.append(r)
        r_label = ctk.CTkLabel(current_root, text="R(" + str(i+1) + "): " + str(r) + " bps")  # bits per second
        r_label.pack()
    for r in rate:
        sum_of_rate += r
    avg_rate = sum_of_rate / n
    avg_rate_text = "Average Rate: " + str(avg_rate) + " bps"
    avg_rate_label = ctk.CTkLabel(current_root, text=avg_rate_text)
    avg_rate_label.pack()