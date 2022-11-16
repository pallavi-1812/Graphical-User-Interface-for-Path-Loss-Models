import customtkinter
from GUIs.ModelFunctions.IndoorTransmissionLossFunction import indoor_transmission
from GUIs.ModelFunctions.SiteGeneralAboveRooftopFunction import site_general_above_rooftop
from GUIs.ModelFunctions.SiteGeneralBelowRooftopFunction import site_general_below_rooftop
from GUIs.ModelFunctions.SiteGeneralBelowRooftopToStreetFunction import site_general_below_rooftop_to_street
from GUIs.ModelFunctions.SiteSpecificBelowRooftopLoSFunction import site_specific_below_rooftop_LoS
from GUIs.ModelFunctions.SiteSpecificBelowRooftopNLoSFunction import site_specific_below_rooftop_NLoS
from GUIs.ModelFunctions.SiteSpecificAboveRooftopUrbanFunction import site_specific_above_rooftop_urban
from GUIs.ModelFunctions.SiteSpecificAboveRooftopSuburbanFunction import site_specific_above_rooftop_suburban
from GUIs.ModelFunctions.SiteSpecificBelowRooftopToStreetLoSFunction import site_specific_below_rooftop_to_street_LoS
from GUIs.ModelFunctions.SiteSpecificBelowRooftopToStreetNLoS1TurnFunction \
    import site_specific_below_rooftop_to_street_1_turn_NLoS
from GUIs.ModelFunctions.SiteSpecificBelowRooftopToStreetNLoS2TurnFunction \
    import site_specific_below_rooftop_to_street_2_turn_NLoS
from GUIs.ModelFunctions.SiteSpecificResidentialFunction import site_specific_residential

root = customtkinter.CTk()
root.geometry("900x500")
root.title("Scenarios for Path Loss Models")
root.config(bg="#DEF5E5")

scenario = customtkinter.CTkButton(root, fg_color="#FFE15D", text_color="#DC3535", hover_color="#FFE15D",
                                   text="SELECT SCENARIO FOR CALCULATING PATH LOSS", height=35, width=200)
scenario.grid(row=0, column=1, pady=20)

button_1 = customtkinter.CTkButton(root, fg_color="#242F9B", text_color="white", hover_color="#352F9B", width=200,
                                   height=45,
                                   text="Indoor Transmission Loss Model", command=indoor_transmission)
button_1.grid(row=1, column=0, padx=60, pady=70)

button_2 = customtkinter.CTkButton(root, fg_color="#711A75", text_color="white", hover_color="#821A75", width=200,
                                   height=45,
                                   text="Site General Model for above rooftop", command=site_general_above_rooftop)
button_2.grid(row=2, column=0, padx=60, pady=70)

button_3 = customtkinter.CTkButton(root, fg_color="#A760FF", text_color="white", hover_color="#B860FF", width=200,
                                   height=45,
                                   text="Site General Model for below rooftop", command=site_general_below_rooftop)
button_3.grid(row=3, column=0, padx=60, pady=70)

button_4 = customtkinter.CTkButton(root, fg_color="#F10086", text_color="white", hover_color="#F21086", width=200,
                                   height=45,
                                   text="Site General Model from below rooftop to street level",
                                   command=site_general_below_rooftop_to_street)
button_4.grid(row=4, column=0, padx=60, pady=70)

button_5 = customtkinter.CTkButton(root, fg_color="#764AF1", text_color="white", hover_color="#874AF1", width=200,
                                   height=45,
                                   text="Site Specific Model for below rooftop LoS",
                                   command=site_specific_below_rooftop_LoS)
button_5.grid(row=1, column=1, padx=50, pady=70)

button_6 = customtkinter.CTkButton(root, fg_color="#242F9B", text_color="white", hover_color="#352F9B", width=200,
                                   height=45,
                                   text="Site Specific Model for below rooftop NLoS",
                                   command=site_specific_below_rooftop_NLoS)
button_6.grid(row=2, column=1, padx=50, pady=70)

button_7 = customtkinter.CTkButton(root, fg_color="#711A75", text_color="white", hover_color="#821A75", width=200,
                                   height=45,
                                   text="Site Specific Model for above rooftop in Urban Scenario",
                                   command=site_specific_above_rooftop_urban)
button_7.grid(row=3, column=1, padx=50, pady=70)

button_8 = customtkinter.CTkButton(root, fg_color="#A760FF", text_color="white", hover_color="#B860FF", width=200,
                                   height=45,
                                   text="Site Specific Model for above rooftop in Suburban Scenario",
                                   command=site_specific_above_rooftop_suburban)
button_8.grid(row=4, column=1, padx=50, pady=70)

button_9 = customtkinter.CTkButton(root, fg_color="#F10086", text_color="white", hover_color="#F21086", width=200,
                                   height=45,
                                   text="Site Specific Model from below rooftop to street level LoS",
                                   command=site_specific_below_rooftop_to_street_LoS)
button_9.grid(row=1, column=2, padx=50, pady=70)

button_10 = customtkinter.CTkButton(root, fg_color="#764AF1", text_color="white", hover_color="#874AF1", width=200,
                                    height=45,
                                    text="Site Specific Model from below rooftop to street level for 1 turn NLoS "
                                         "propagation",
                                    command=site_specific_below_rooftop_to_street_1_turn_NLoS)
button_10.grid(row=2, column=2, padx=50, pady=70)

button_11 = customtkinter.CTkButton(root, fg_color="#242F9B", text_color="white", hover_color="#352F9B", width=200,
                                    height=45,
                                    text="Site Specific Model from below rooftop to street level for 2 turn NLoS "
                                         "propagation", command=site_specific_below_rooftop_to_street_2_turn_NLoS)
button_11.grid(row=3, column=2, padx=50, pady=70)

button_12 = customtkinter.CTkButton(root, fg_color="#711A75", text_color="white", hover_color="#821A75", width=200,
                                    height=45,
                                    text="Site Specific Model in residential environments",
                                    command=site_specific_residential)
button_12.grid(row=4, column=2, padx=50, pady=70)

root.mainloop()
