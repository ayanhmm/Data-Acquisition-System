import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import time
import math
import logging
from time import gmtime, strftime
from datetime import datetime
import csv
import numpy as np


#----------------------------------------------Configure logging----------------------------------------------
# logging.basicConfig(filename='data.log', level=logging.INFO, format='%(asctime)s %(message)s')
#to conserve primary memory of dashboard screen,data is logged diectly at pit
data_to_append = [['Time','Motor Temperature','Motor Controller Temperature','ERPM','Speed','Throttle','AC Current','DC Current','Pack Voltage','LV Voltage','State of charge','High Temperarture','Low Temperature','MC FAULTS','BMS FAULTS']]
# file = open(r"/home/pi/Downloads/datalog/logfile.csv", 'a', newline='')
# writer = csv.writer(file)
# writer.writerows(data_to_append)
# file.close()
file_path = "/home/harsh/Music/"
file_name = file_path + time.ctime()
file_name = file_name + '.csv'
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_append)
    file.close()

# ----------------------------------------------Create the root window----------------------------------------------
root = tk.Tk()
#root.title("TDR - SDC")
#root.attributes('-fullscreen', True)

#----------------------------------------------bg of root window----------------------------------------------

# Get the screen width and height
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# screen_height = int(round((screen_height*2)/7, 0))
# screen_width = int(round((screen_width*5)/15, 0))
#print(screen_width, screen_height)

root.geometry("%dx%d" % (screen_width, screen_height))

#make bg dimentions equal to window
# flash_image = Image.open("flash image 3.png")
# if flash_image.size != (screen_width, screen_height):
#     flash_image = flash_image.resize((screen_width, screen_height), Image.ANTIALIAS)
# flash_image = ImageTk.PhotoImage(flash_image)

#Adding background image in form of a label
#removed since adding blinking caution button is easiar in canvas
# flash_image_label = ttk.Label(root, image = flash_image)
# flash_image_label.place(relx=0, rely=0, anchor="nw")
# flash_image_label.image = flash_image

root.attributes('-fullscreen', True)
# root.after(100)

#----------------------------------------------bg of main canvas window----------------------------------------------
#make bg dimentions equal to window
bg_image_pg1 = Image.open("/home/harsh/Music/new_dash.png")
# if bg_image_pg1.size != (screen_width, screen_height):
#     bg_image_pg1 = bg_image_pg1.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image_pg1 = ImageTk.PhotoImage(bg_image_pg1)
#Adding background image in form of a canvas
bg_canvas_pg1 = tk.Canvas(root, width=screen_width, height=screen_height,bg="black")
bg_canvas_pg1.place(relx=1, rely=1, anchor="se")
bg_canvas_pg1.create_image(0, 0, anchor="nw", image=bg_image_pg1)


#----------------------------------------------make canvas for throttle bar----------------------------------------------
throttle_canvas = tk.Canvas(root, width=screen_width, height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
throttle_canvas.place(relx=1, rely=0, anchor="ne")

# throttle_canvas_outer_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="throttle_outline")
# throttle_canvas_inner_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="throttle_outline")

# throttle_bar_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="throttle_outline")

throttle_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="THROTTLE ::", font=("areal black", int(round((screen_height * 1)/100, 0))), fill="white",anchor="ne" )

def create_gradient_throttle(current, total):
            speedometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            speedometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = speedometer_bg_outer_gradient_colour
            r2, g2, b2 = speedometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_throttle(100-i,100)
    throttle_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="throttle_outline")

#----------------------------------------------make canvas for soc----------------------------------------------
soc_canvas = tk.Canvas(root, width=screen_width, height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
soc_canvas.place(relx=1, rely=(0.025 + (int(round((screen_height * 1)/20, 0)))/screen_height), anchor="ne")

# soc_canvas_outer_outline_rectangle = soc_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="soc_outline")
# soc_canvas_inner_outline_rectangle = soc_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="soc_outline")

# soc_bar_outline_rectangle = soc_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="soc_outline")

soc_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="SOC ::", font=("areal black", int(round((screen_height * 1)/100, 0))), fill="white",anchor="ne" )

def create_gradient_soc(current, total):
            speedometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            speedometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = speedometer_bg_outer_gradient_colour
            r2, g2, b2 = speedometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_soc(100-i,100)
    soc_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="soc_outline")

#----------------------------------------------make canvas for speed----------------------------------------------
speed_canvas = tk.Canvas(root, width=screen_width, height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
speed_canvas.place(relx=1, rely=(0.025 + (int(round((screen_height * 1)/20, 0)))/screen_height)*2, anchor="ne")

# speed_canvas_outer_outline_rectangle = speed_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="speed_outline")
# speed_canvas_inner_outline_rectangle = speed_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="speed_outline")

# speed_bar_outline_rectangle = speed_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="speed_outline")

speed_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="SPEED ::", font=("areal black", int(round((screen_height * 1)/100, 0))), fill="white",anchor="ne" )

def create_gradient_speed(current, total):
            speedometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            speedometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = speedometer_bg_outer_gradient_colour
            r2, g2, b2 = speedometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_speed(100-i,100)
    speed_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="speed_outline")
    

#----------------------------------------------make canvas for lv_voltage----------------------------------------------
lv_voltage_canvas = tk.Canvas(root, width=screen_width, height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
lv_voltage_canvas.place(relx=1, rely=(0.025 + (int(round((screen_height * 1)/20, 0)))/screen_height)*3, anchor="ne")

# lv_voltage_canvas_outer_outline_rectangle = lv_voltage_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="lv_voltage_outline")
# lv_voltage_canvas_inner_outline_rectangle = lv_voltage_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="lv_voltage_outline")

# lv_voltage_bar_outline_rectangle = lv_voltage_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="lv_voltage_outline")

lv_voltage_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="LV VOLTAGE ::", font=("areal black", int(round((screen_height * 1)/100, 0))), fill="white",anchor="ne" )

def create_gradient_lv_voltage(current, total):
            lv_voltageometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            lv_voltageometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = lv_voltageometer_bg_outer_gradient_colour
            r2, g2, b2 = lv_voltageometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_lv_voltage(100-i,100)
    lv_voltage_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="lv_voltage_outline")

#----------------------------------------------make canvas for pack_voltage----------------------------------------------
pack_voltage_canvas = tk.Canvas(root, width=screen_width, height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
pack_voltage_canvas.place(relx=1, rely=(0.025 + (int(round((screen_height * 1)/20, 0)))/screen_height)*4, anchor="ne")

# pack_voltage_canvas_outer_outline_rectangle = pack_voltage_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="pack_voltage_outline")
# pack_voltage_canvas_inner_outline_rectangle = pack_voltage_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="pack_voltage_outline")

# pack_voltage_bar_outline_rectangle = pack_voltage_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="pack_voltage_outline")

pack_voltage_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="PACK VOLTAGE ::", font=("areal black", int(round((screen_height * 1)/100, 0))), fill="white",anchor="ne" )

def create_gradient_pack_voltage(current, total):
            pack_voltageometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            pack_voltageometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = pack_voltageometer_bg_outer_gradient_colour
            r2, g2, b2 = pack_voltageometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_pack_voltage(100-i,100)
    pack_voltage_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="pack_voltage_outline")


#----------------------------------------------CREATE DATA DISPLAY LABELS for circular display----------------------------------------------
#declare font parameters
display_labels_font_style = "RACE SPACE REGULAR"
circular_display_labels_font_color = "Orange Red"
list_display_labels_font_color = "Orange Red"
circular_display_labels_font_size = int(round((screen_width * 1)/100, 0))

#----------------------------------------------CREATE DATA DISPLAY LABELS for throttle canvas----------------------------------------------
label_data_throttle = tk.Label(throttle_canvas, text="tht", font=(display_labels_font_style, int(round((screen_width * 1)/150, 0))), bg="black", fg=list_display_labels_font_color)
label_data_throttle.place(relx=0.05, rely=0.5, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for soc canvas----------------------------------------------
label_data_soc = tk.Label(soc_canvas, text="SOC", font=(display_labels_font_style, int(round((screen_width * 1)/150, 0))), bg="black", fg=list_display_labels_font_color)
label_data_soc.place(relx=0.05, rely=0.5, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for speed canvas----------------------------------------------
label_data_speed = tk.Label(speed_canvas, text="SPD", font=(display_labels_font_style, int(round((screen_width * 1)/150, 0))), bg="black", fg=list_display_labels_font_color)
label_data_speed.place(relx=0.05, rely=0.5, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for lv_voltage canvas----------------------------------------------
label_data_lv_voltage = tk.Label(lv_voltage_canvas, text="LV", font=(display_labels_font_style, int(round((screen_width * 1)/150, 0))), bg="black", fg=list_display_labels_font_color)
label_data_lv_voltage.place(relx=0.05, rely=0.5, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for pack_voltage canvas----------------------------------------------
label_data_pack_voltage = tk.Label(pack_voltage_canvas, text="PV", font=(display_labels_font_style, int(round((screen_width * 1)/150, 0))), bg="black", fg=list_display_labels_font_color)
label_data_pack_voltage.place(relx=0.05, rely=0.5, anchor="center")


#----------------------------------------------CREATE Fault DISPLAY LABELS----------------------------------------------
# Create label to display MOTOR controller faults
label_data_motor_controller_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, int(round((screen_width * 1)/100, 0))), bg="black", fg=list_display_labels_font_color)
label_data_motor_controller_fault.place(relx=0.14, rely=0.82, anchor="center")
# Create label to display bms faults
label_data_bms_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, int(round((screen_width * 1)/100, 0))), bg="black", fg=list_display_labels_font_color)
label_data_bms_fault.place(relx=0.64, rely=0.82, anchor="center")

#----------------------------------------------Open serial connection to Arduino----------------------------------------------
#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/ttyACM0',460800)

bms_fault_mapping = {0: "Discharge Limit Enforcement Fault", 1: "Charger Safety Relay Fault", 2: "Internal Hardware Fault", 3: "Internal Heatsink Thermistor Fault", 4: "Internal Software Fault", 5: "Highest Cell Voltage Too High", 6: "Lowest Cell Voltage Too Low", 7: "Pack Too Hot Fault",
                    8: "Internal Communication Fault", 9: "Cell Balancing Stuck Off Fault", 10: "Weak Cell Fault", 11: "Low Cell Voltage Fault", 12: "Open Wiring Fault", 13: "Current Sensor Fault", 14: "Highest Cell Voltage Over 5V Fault", 15: "Cell ASIC Fault",
                    16: "Weak Pack Fault", 17: "Fan Monitor Fault", 18: "Thermistor Fault", 19: "External Communication Fault", 20: "Redundant Power Supply Fault", 21: "High Voltage Isolation Fault", 22: "Input Power Supply Fault", 23: "Charge Limit Enforcement Fault"}

mc_fault_mapping = {0: "No Mc Fault", 1: "Overvoltage Error", 2: "Undervoltage Error", 3: "DRV error", 4: "ABS. Overtemp.", 5: "Controller Overtemp.",
                    6: "Motor Overtemp.", 7: "Sensor Wire error", 8: "Sensor General Error", 9: "CAN command error", 10: "Analog input error"}

def update_data():
    #obtain raw data from arduino
    raw_data  = ser.readline()
    print(raw_data)
    try:
        raw_data = raw_data.decode()
        print(raw_data)
        # data = raw_data.split("\"")
    # Process the decoded data here
    except UnicodeDecodeError:
    # Handle the case when the data cannot be decoded
        root.after(1, update_data)
    #raw_data = '000,100,2000,30,40.00,500,600,700,800,900,1000,110,120,no mc fault a :no mc fault b:no mc fault c:no mc fault d; no bms fault a : no bms fault b: no bms fault c: no bms fault d'
    #print(raw_data)
    #split raw data into list of datas from different sensor

    data = raw_data.split(",")

    
    #prevent decoding error when "connection with arduino established" is the data recieved from arduino
    if len(data) == 13:
        
        #print(data)
        
        #converting faults to a more organised form
        bms_faults_list = []
        bms_fault_number = data[12].split("\n")
        bms_fault_number = bms_fault_number[0]
        for i in range(24):
            if int(bms_fault_number[i]) == 1:
                bms_faults_list.append(bms_fault_mapping[i])

        if len(bms_faults_list) == 0:
            bms_faults_list.append("No BMS Fault")

        bms_faults_string_arranged = '\n'.join(bms_faults_list)
        mc_fault = mc_fault_mapping[int(data[11])]
        #----------------------------------------------data loggging----------------------------------------------
        file = open(file_name, 'a', newline='')
        writer = csv.writer(file)
        data_to_append = []
        finaldatalist = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        for i in range(11):
            finaldatalist.append(data[i])
        finaldatalist.append(mc_fault)
        finaldatalist.append(bms_faults_list)
        data_to_append.append(finaldatalist)
                
        writer.writerows(data_to_append)
        file.close()

        
        #label_data_speed.config(text = current_vehicle_calculated_speed)
        speed = float(data[2])*0.1*2*3.14159*2.54*9*0.00001*60
        # label_data_speed.config(text = speed)
        
        throttle = float(data[3])
        soc = float(data[8])
        lv_voltage = float(data[7])
        pack_voltage = float(data[6])
    
        
        label_data_throttle.config(text = throttle)
        label_data_soc.config(text = soc)
        label_data_speed.config(text = speed)
        label_data_lv_voltage.config(text = lv_voltage)
        label_data_pack_voltage.config(text = pack_voltage)

        lv_voltage_percent = (int(float((float(lv_voltage)/14))))*200
        pack_voltage_percent = (int(float(float(pack_voltage)/3)))*2
        throttle_percent = (throttle)*2
        soc_percent = (soc)*2
        speed_percent = (speed)*2
        #----------------------------------------------display faults update----------------------------------------------
        label_data_motor_controller_fault.config(text = mc_fault)
        label_data_bms_fault.config(text = bms_faults_string_arranged)
        
        def update_throttle_bar():
            throttle_canvas.delete("throttle_black_fill")
            throttle_canvas.create_rectangle(int(round((screen_width* (((throttle_percent)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="throttle_black_fill")
        
        def update_soc_bar():
            soc_canvas.delete("soc_black_fill")
            soc_canvas.create_rectangle(int(round((screen_width * (((soc_percent)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="soc_black_fill")
        
        def update_speed_bar():
            speed_canvas.delete("speed_black_fill")
            speed_canvas.create_rectangle(int(round((screen_width * (((speed_percent)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="speed_black_fill")
            
        def update_lv_voltage_bar():
            lv_voltage_canvas.delete("lv_voltage_black_fill")
            lv_voltage_canvas.create_rectangle(int(round((screen_width * (((lv_voltage_percent)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="lv_voltage_black_fill")
            
        def update_pack_voltage_bar():
            pack_voltage_canvas.delete("pack_voltage_black_fill")
            pack_voltage_canvas.create_rectangle(int(round((screen_width * (((pack_voltage_percent)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/173600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="pack_voltage_black_fill")
        
        update_throttle_bar()
        update_soc_bar()
        update_speed_bar()
        update_lv_voltage_bar()
        update_pack_voltage_bar()

    
    #----------------------------------------------repead the update data function after 100ms----------------------------------------------   
    root.after(1, update_data) 
    # start_time = time.time()
    # while (time.time() - start_time) < 0.0005:
    #     update_data()

#----------------------------------------------start data updation on main window----------------------------------------------
root.after(1, update_data) 
#update_data()
root.mainloop()