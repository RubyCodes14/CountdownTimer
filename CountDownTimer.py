try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import Tkinter.ttk as ttk
from tkinter import messagebox

#import time
import winsound

bg_colour = "#FFFFFF" #BACKGROUND COLOUR FOR ALL FRAMES AND TIME LABEL

window = tk.Tk()
window.title("Countdown Timer - RubyCodes(c)")
window.iconbitmap("clock.ico")
window.geometry("1080x680+125+11")
window.minsize(720, 620)
window.configure(bg = bg_colour)

fontFamily = "Jester"
actLabel_bg = "#F0FFFF"  #ACTIVITY LABEL BACKGROUND COLOUR

default_time = 600
maximum_time = 5999

fulscrn = False

class _Window_:
    def __init__(self, window, fulscrn):
        self.window = window
        self.fulscrn = fulscrn
        
            
    def close_window(self, window):
        self.window.destroy()
        
    def fullscreen(self, window):
        if self.fulscrn:
            self.fulscrn = False
            
        else:
            self.fulscrn = True
        self.window.wm_attributes("-fullscreen", self.fulscrn)
        

        
win = _Window_(window, fulscrn)
        
window.bind("<Escape>", win.close_window)
window.bind("<Double-Button-1>", win.fullscreen)

def reset_notif():
    messagebox.showinfo(message="Maximum time limit exceeded! Timer will be set to maximum [99:59] time allowed.")

def timeLimit(time):
    # max-99 minutes : 59 seconds <-> 5999 seconds
    # due to width; 3 figures  minutes cuts off at the edge of screen
    if time <= 5999:
        return time
    else:
        reset_notif()
        return maximum_time

def twoDigits(dgt):
    if len(dgt) == 1:
        return "0" + dgt
    else:
        return dgt
    
def TimerValue(secs):
    try:
        minutes = str(secs // 60)
        seconds = str(secs % 60)            
        return twoDigits(minutes) + ":" + twoDigits(seconds)
    except(TypeError):
        pass#return twoDigits(str(10)) + ":" + twoDigits(str(0))
    

def convertTo_Seconds(minutes):
    minutes = str(minutes)
    try:
        if "." in minutes:
            if minutes.index(".") == 0:
                timeSecs = int(minutes[1:])
            else:
                min_And_Secs = minutes.split(".")
                timeSecs = (int(min_And_Secs[0]) * 60) + int(min_And_Secs[-1])
        else:
            timeSecs = int(minutes) * 60
        
        return timeSecs
    except(TypeError, ValueError):
        return default_time


ctd_Time = timeLimit(convertTo_Seconds(10))
loop = ""
flag = False

def showWidgets():
    ent_Time.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0)
    ent_activity.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)
    btn_setCtd.grid(row = 0, column = 1, rowspan = 2)
    btn_start.grid(row = 0, column = 2, rowspan = 2)

def setCtdTime():
    global flag, ctd_Time
    if flag:
        window.after_cancel(loop)        
        showWidgets()
        btn_setCtd["text"] = "Reset"
        btn_setCtd["bg"] = "#FFAD00"
  
    ctd_Time = timeLimit(convertTo_Seconds(ent_Time.get())) #USER INPUT TIME
    lbl_activity["text"] = ent_activity.get().upper() #USER INPUT ACTIVITY
    if lbl_activity["text"] == "":
        lbl_activity["bg"] = bg_colour
    else:
        lbl_activity["bg"] = actLabel_bg
    lbl_time["text"] = TimerValue(ctd_Time)
    lbl_time["font"] = (fontFamily, 350, "bold")
    lbl_time["fg"] = "#111111"
    lbl_time.pack(fill = tk.BOTH, expand = True, pady = 0)
    
#TIMER START FUNCTION    
def start():    
    global ctd_Time, loop, flag
    
        
    loop = window.after(1000, start)  #COUNTER 1000 MS (1.0 x 10^-3 Secs)
    flag = True
    #ctd_Time -= 1    #COUNTDOWN BY 1 SECOND
    btn_setCtd["text"] = "Cancel"
    btn_setCtd["bg"] = "#C3C3C3"

    if lbl_activity["text"] == "":
        lbl_activity["bg"] = bg_colour
    else:
        lbl_activity["bg"] = actLabel_bg
        
    if ctd_Time < 0:
        lbl_time["text"] = "TIME'S UP"
        lbl_time["font"] = (fontFamily, 200, "bold")
        lbl_time["fg"] = "#FF0000"   
        lbl_time.pack(fill = tk.BOTH, expand = True, pady = 90)
        
        showWidgets()
        
        btn_setCtd["text"] = "Reset"
        btn_setCtd["bg"] = "#FFAD00"
        
        window.after_cancel(loop)  # REMOVE THIS LINE AND REFER TO THE LAST LINE OF 'else:' BLOCK
                                    # TO KNOW THE ADDITIONAL TIME USED AFTER TIME'S UP,
        
    else:
        lbl_time["text"] = TimerValue(ctd_Time)
        lbl_time["font"] = (fontFamily, 350, "bold")
        ent_Time.grid_forget()
        ent_activity.grid_forget()
        btn_start.grid_forget()

        ctd_Time -= 1    #COUNTDOWN BY 1 SECOND - TAKE THIS LINE OUTSIDE THE 'else:' BLOCK [AND REFER TO THE LAST LINE OF THE 'if:' BLOCK]
                         #TO KNOW THE ADDITIONAL TIME USED AFTER TIME'S UP
        
#COUNTDOWN TIME ACTIVITY LABEL   
lbl_activity = tk.Label(window, text = "", bg = actLabel_bg, fg = "#000000", font = (fontFamily, 35, "normal"))
lbl_activity.pack()#fill = tk.BOTH, expand = True)

#COUNTDOWN TIME DISPLAY
lbl_time = tk.Label(window, text = TimerValue(ctd_Time), bg = bg_colour, font = (fontFamily, 350, "bold"))
lbl_time.pack(fill = tk.BOTH, expand = True)

#FRAME (CONTAINER) FOR COUNTDOWN TIME INPUT, ACTIVITY, SET/RESET BUTTON, START BUTTON
frm_prompt = tk.Frame(window, bg = bg_colour)
frm_prompt.pack()#expand = True)

#TIME INPUT
ent_Time = tk.Entry(frm_prompt, width = 4, bg = "#DBDBDB", font = (fontFamily, 24))
ent_Time.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0)
ent_Time.insert(0, "10") #USER INPUT TIME PLACEHOLDER
#ctd_Time = int(ent_Time.get())

#ACIVITY INPUT
ent_activity = tk.Entry(frm_prompt, width = 10, bg = "#DBDBDB", font = (fontFamily, 20, "italic"))
ent_activity.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)
ent_activity.insert(1, "Label")

#SET/RESET BUTTON
btn_setCtd = tk.Button(frm_prompt, text = "Set", bg = "#FFAD00", font = (fontFamily, 30), command = setCtdTime)#lambda: start(ctd_Time))
btn_setCtd.grid(row = 0, column = 1, rowspan = 2)

#START BUTTON
btn_start = tk.Button(frm_prompt, text = "Start", bg = "#FF0000", font = (fontFamily, 30), command = lambda: [start(), _Window_(window, fulscrn).fullscreen(window)])#lambda: start(ctd_Time))
btn_start.grid(row = 0, column = 2, rowspan = 2)


window.mainloop()
