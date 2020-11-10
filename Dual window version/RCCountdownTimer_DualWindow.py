try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import Tkinter.ttk as ttk
from tkinter import messagebox
import time
import winsound

#from pynput.keyboard import Key, Controller 

#DIFFERENT FROM BUT MOST LIKELY THE SAME WITH - Timer_bgColour
bg_colour = "#FFFFFF" #BACKGROUND COLOUR FOR ALL FRAMES AND TIME LABEL

"""
def maximize_window():
    kb = Controller()
    with kb.pressed(Key.cmd):
        kb.press(Key.up)
        kb.release(Key.up)
"""

#WINDOW 1 - TIME INPUT, ACTIVITY INPUT, SET/RESET BUTTON, START BUTTON
window_1 = tk.Tk()
window_1.title("RubyCodes - Countdown Timer (c) 2020")
window_1.iconbitmap("clock.ico")
window_1.geometry("600x480+300+25")
window_1.minsize(780, 520)
window_1.configure(bg = "#000000")
window_1.resizable(False, False)
#window_1.lift()

screenWidth = window_1.winfo_screenwidth()
screenHeight = window_1.winfo_screenheight()

# ********WINDOW 2 - COUNTDOWN DISPLAY & ACTIVITY DISPLAY ****************** #
window_2 = tk.Toplevel(window_1)
window_2.title("Countdown Timer - RubyCodes(c)")
window_2.iconbitmap("clock.ico")
window_2.minsize(720, 640)
window_2.configure(bg = bg_colour)

#window_2.geometry("600x480+0+0")    #FOR SINGLE SCREEN, NOT EXTENDING

# ********* FOR USING AN EXTENDED SCREEN **********
window_2.geometry(str(screenWidth) + "x" + str(screenHeight) + "+" + str(screenWidth) + "+0")  #FOR USING AN EXTENDED SCREEN:
                                                                                            #MOVES THE WINDOW TO AN EXTENDED SCREEN BY A SPECIFIED WIDTH
window_2.overrideredirect(1) #REMOVES THE TOP BADGE OF THE WINDOW - NO DRAGGING, NO BUTTONS, HIDES TASKBAR

#********* ****************

# ********* FOR FULL SCREEN/MAXIMIZING WINDOW **********
#maximize_window()
#window_2.attributes("-fullscreen", True)

# ********* ****************

#****** FONTS ***********
timerFont = "Jester"
font1 = "Cambria" #"DFGothic-EB"#
btnFont = "Jester"
title_font = "Cambria" #helvetica"


#********* COLOURS *************
Timer_fgColour = "#FF0000"
Timer_bgColour = "#FFFFFF"
actLabel_bg = Timer_bgColour#"#F0FFFF"  #ACTIVITY LABEL BACKGROUND COLOUR - SLIGTHLY DIFERENT FROM [Timer_bgColour] SAME COLOUR CAN BE USED
title_bgColour = "#0B00FF"
title_fgColour = "#FFFFFF"


## TIME
delayTime = 1000        # DO NOT CHANGE FOR NORMAL TIMER 1sec (1000 milliseconds, ) delay for the timer
inputTimePlaceholder = "10.30"
## FLAGS
alarm_flag = 0    # NO NEED FOR CHANGING - DO NOT CHANGE
blinker_flag = 0  # NO NEED FOR CHANGING - DO NOT CHANGE
continuous = 5    # THE ALARM SOUNDS THE NUMBER OF INTEGER GIVEN OR CONTINUOUSLY IF True, NO ALARM IF False
timeup = False   # THIS DECIDES WETHER THE TIMER SHOULD RUN OR  NOT, TO BE ABLE TO STOP RECURSIVE LOOP THAT OCCURS OF CLICKING 'START' WHEN TIME'S UP
timeupText = "TIME'S UP"
timer_reset = False
showColourWarning = True   #set_timer_colour() flag, to control showing Warning message if its cancel button or set button
#label = ""

def percentage(value, percent, text):
    percent = percent / 100
    val = int(round((percent * value), 0))
    valN = int((7 * val) / len(text))
    return valN

def twoDigits(dgt):
    if len(dgt) == 1:
        return "0" + dgt
    else:
        return dgt

def reset_notif():
    messagebox.showinfo(message="Time's Up! Reset Time")

#CUSTOMIZED TIME'S UP TEXT
def customizedText(userInput):
    global timeupText
    output = "TIME'S UP"
    if "!" in userInput:
        userInput = userInput[0:label.index("!")]
            
    if "#" in userInput:
        output = userInput[userInput.index("#"):]  
        if len(output) > 8:
            messagebox.showinfo(message="Maximum Length of 8 characters for time up exceeded.")
            timeupText = "TIME'S UP"
        else:
            timeupText = output
    else:
        timeupText = "TIME'S UP"

#CUSTOMIZED TIMER COLOUR
# @bg="#FAFAFD"
#'''
def customizedColour(userinput):
    global user_bg, user_fg, Timer_bgColour, Timer_fgColour
    #user_bg, user_fg = bg, fg
    Timer_fgColour = "#FF0000"
    Timer_bgColour = "#FFFFFF"
    user_bg = Timer_bgColour
    user_fg = Timer_fgColour
    if "@" in userinput:
        i = userinput.index("@")
        sample = userinput[i:]
        
        if len(sample) >= 9:
            sampleList = sample.split("@")
            if len(sampleList) >= 2:
                a = sampleList[1]
                b = a
                if "bg" in a:
                    user_bg = a.split("\"")[1]
                    
                elif "fg" in a:
                    user_fg = a.split("\"")[1]
                    
                if len(sampleList) > 2:
                    b = sampleList[2]
                    if "bg" in b:
                        user_bg = b.split("\"")[1]
                    elif "fg" in b:
                        user_fg = b.split("\"")[1]
    else:
        Timer_fgColour = "#FF0000"
        Timer_bgColour = "#FFFFFF"
                
                
                
            
      
#'''

#GETS TIMER LABEL/ACTIVITY   
def getLabel(label):
    if "!" in label:
        label = label[0:label.index("!")]
        
    if "#" in label:
        return label[0:label.index("#")]
    else:
        return label
    
        
#TIME'S UP ALARM
def alarm(continuous = True):
    global alarm_flag
    alarm_flag += 1
    frequency = 2020
    milliseconds = 120
    if type(continuous) == bool:   #THE ALARM SOUNDS CONTINUOUSLY OR NOT AT ALL
        if continuous:
            return winsound.Beep(frequency, milliseconds)
        else:
            pass
    elif type(continuous) == int:   #THE ALARM SOUNDS THE NUMBER OF TIMES INPUTED
        if alarm_flag - 1 >= continuous:
            pass
        else:
            return winsound.Beep(frequency, milliseconds)

def set_timer_colour():
    global showColourWarning, user_bg, user_fg, Timer_bgColour, Timer_fgColour
    Timer_fgColour = user_fg
    Timer_bgColour = user_bg
    if Timer_fgColour.upper() == Timer_bgColour.upper():
        messagebox.showinfo(message="Fg colour and Bg colour can not be the same.")
        Timer_fgColour = "#FF0000"
        Timer_bgColour = "#FFFFFF"
    #customizedColour(userinput)
    try:
        lbl_time["fg"] = Timer_fgColour
        lbl_time["bg"] = Timer_bgColour
        frm_count["bg"] = Timer_bgColour
        lbl_timeWin1["fg"] = Timer_fgColour
        lbl_timeWin1["bg"] = Timer_bgColour
        
        lbl_activity["bg"] = Timer_bgColour
        lbl_activity["fg"] = Timer_fgColour
    except:
        lbl_time["fg"] = Timer_fgColour
        lbl_time["bg"] = Timer_bgColour
        frm_count["bg"] = Timer_bgColour
        lbl_timeWin1["fg"] = Timer_fgColour
        lbl_timeWin1["bg"] = Timer_bgColour
        
        lbl_activity["bg"] = Timer_bgColour
        lbl_activity["fg"] = Timer_fgColour
        if showColourWarning:
            messagebox.showinfo(message="Invalid colour string.\nDefault colour is set!")
        

    

def blinker(txt, blink = True):
    global blinker_flag
    if blink:
        if blinker_flag == 0:
            blinker_flag = 1
            output = txt
            #winsound.Beep(32767, 204)  #ALERT SOUND
            set_timer_colour()
            
        else:         
            blinker_flag = 0
            output = txt#""
            #lbl_activity["text"] == "":
            lbl_time["fg"] = Timer_bgColour
            lbl_time["bg"] = Timer_fgColour
            frm_count["bg"] = Timer_fgColour
            lbl_timeWin1["fg"] = Timer_bgColour
            lbl_timeWin1["bg"] = Timer_fgColour

            lbl_activity["bg"] = Timer_fgColour
            lbl_activity["fg"] = Timer_bgColour
            
            alarm(continuous) #ALERT SOUND MAX FREQUENCY-32767 DURATION-THIS ALSO WORKS IN PLACE OF 'delayTime'
            
        return output
    else:
        return txt
    
def TimerValue(secs):
    try:
        minutes = str(secs // 60)
        seconds = str(secs % 60)            
        return twoDigits(minutes) + ":" + twoDigits(seconds)
    except(TypeError):
        pass #  return twoDigits(str(10)) + ":" + twoDigits(str(0))
    

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
        return 600


ctd_Time = convertTo_Seconds(inputTimePlaceholder)
loop = ""
timer_flag = False  # TIMER LOOP FLAG


def showWidgets():
    ent_Time.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0)
    ent_activity.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)
    btn_setCtd.grid(row = 0, column = 0, rowspan = 2)
    btn_start.grid(row = 0, column = 1, rowspan = 2)

def setCtdTime():
    global timer_flag, ctd_Time, delayTime, alarm_flag, label, prevCount
    delayTime = 1000
    alarm_flag = 0
    btn_start["command"] = start
    label = ent_activity.get()
    
    #timeup = False  #TIME IS BEEN SET
    #timer_reset = True
    #maximize_window()
    
    customizedText(label)
    customizedColour(label)
    set_timer_colour()
    if timer_flag:   #IF TIMER IS RUNNING ALREADY AND 'CANCEL->[START]' BUTTON IS CLICKED
        window_1.after_cancel(loop)     # THIS WILL ALSO CANCEL THE BLINKER IF 'TIME'S UP' IS BLINKING   
        showWidgets()
        btn_setCtd["text"] = "Reset"
        btn_setCtd["bg"] = "#FFAD00"        
  
    ctd_Time = convertTo_Seconds(ent_Time.get()) #USER INPUT TIME
    prevCount = ctd_Time
    lbl_activity["text"] = getLabel(label).upper() #USER INPUT ACTIVITY
    lbl_activityWin1["text"] = getLabel(label).upper() #FOR WINDOW 1 - CONTROL WINDOW
    if len(lbl_activityWin1["text"]) > 30:
            messagebox.showinfo(message="Maximum Length of 30 characters for label exceeded.")
            lbl_activityWin1["text"] = ""
    lbl_timeWin1["font"] = (timerFont, 80, "bold")

    
    if lbl_activity["text"] == "":
        #lbl_activity["bg"] = Timer_bgColour
        lbl_activity.pack_forget()
        lbl_activityWin1["text"] = "NO LABEL ENTERED FOR THIS TIMER"
    else:
        #lbl_activity["bg"] = actLabel_bg
        lbl_activity.pack(side = tk.TOP, fill = tk.X)
    lbl_time["text"] = TimerValue(ctd_Time)
    lbl_timeWin1["text"] = TimerValue(ctd_Time)  #FOR CONTROL WINDOW
    lbl_time["font"] = (timerFont, 350, "bold")
    #lbl_time["fg"] = Timer_fgColour
    lbl_time.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True, pady = 0)
    #EXTRA TIME LABEL
    lbl_extratime.pack_forget()

    
#TIMER START FUNCTION

def start():    
    global delayTime, ctd_Time, loop, timer_flag, timeupText, showColourWarning
    

    loop = window_1.after(delayTime, start)  #COUNTER 1000 MS (1.0 x 10^-3 Secs)
    #if not(timer_flag):
        #lbl_activityWin1["text"] = "NO LABEL ENTERED FOR THIS TIMER"
    timer_flag = True
    if lbl_activity["text"] == "":
        #lbl_activity["bg"] = Timer_bgColour
        lbl_activity.pack_forget()
        lbl_activityWin1["text"] = "NO LABEL ENTERED FOR THIS TIMER"
    else:
        #lbl_activity["bg"] = actLabel_bg
        lbl_activity.pack(side = tk.TOP, fill = tk.X)
        
        
    if ctd_Time < 0:
        delayTime = 500  #REDUCE THIS TO INCREASE THE SPEED OF BLINKING
            
        btn_start["command"] = reset_notif #THIS IS NECESSARY FOR BOTH RESET WARNUNG AND AVOIDING RECURSIVE LOOP OF 'start' FUNCTION 
        blinkText = blinker(timeupText)
        #FOR DISPLAY WINDOW
        #fs_2 = percentage(screenWidth, 15.37, timeupText)
        lbl_time["text"] = blinkText                #MAIN COUNTDOWN DISPLAY WINDOW
        lbl_time["font"] = (timerFont, 200, "bold")
        #FOR CONTROL WINDOW
        #fs_1 = percentage(screenWidth, 4.03, timeupText)
        lbl_timeWin1["text"] = blinkText                #FOR CONTROL WINDOW
        lbl_timeWin1["font"] = (timerFont, 55, "bold")
        
        #lbl_time["fg"] = Timer_fgColour  
        lbl_time.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True, pady = 90)
            
        showWidgets()

        showColourWarning = True  #set_timer_colour() flag, to control showing Warning message if its cancel button or set button  
        btn_setCtd["text"] = "Reset"
        btn_setCtd["bg"] = "#FFAD00"
        
        if ctd_Time <= -1800:   
            window_1.after_cancel(loop)  # REMOVE THIS LINE AND REFER TO THE LAST LINE OF 'else:' BLOCK
                                    # TO KNOW THE ADDITIONAL TIME USED AFTER TIME'S UP,
        #EXTRA TIME USED
        xtime = int(abs(ctd_Time/2))
        mins_ = xtime // 60
        secs_ = xtime % 60
        xtimeTxt0 = ""
        txt0 = "\nadditional time used."#with previous " + str(prevCount)
        if mins_ >= 30:
            xtimeTxt0 = "More than\n"
        #FOR MINUTES ONLY
        if mins_ < 2:
            xtimeTxt1 = xtimeTxt0 + str(mins_) + " min "   #SINGULAR min
        else:
            xtimeTxt1 = xtimeTxt0 + str(mins_) + " mins "   #PLURAL mins
        
        lbl_extratime["text"] = xtimeTxt1 + str(secs_) + " secs" + txt0
        lbl_wmark.pack_forget()
        lbl_extratime.pack(side = tk.TOP, fill = tk.X, pady = 15)
        lbl_wmark.pack(side = tk.BOTTOM, pady = 15)
        
    else:
        lbl_time["text"] = TimerValue(ctd_Time)  #MAIN COUNTDOWN DISPLAY WINDOW
        lbl_timeWin1["text"] = TimerValue(ctd_Time)  #FOR CONTROL WINDOW
        lbl_time["font"] = (timerFont, 350, "bold")
        ent_Time.grid_forget()
        ent_activity.grid_forget()
        btn_start.grid_forget()
        #EXTRA TIME USED
        lbl_extratime.pack_forget()

        showColourWarning = False     #set_timer_colour() flag, to control showing Warning message if its cancel button or set button
        btn_setCtd["text"] = "Cancel"
        btn_setCtd["bg"] = "#C3C3C3"
            
    ctd_Time -= 1    #COUNTDOWN BY 1 SECOND - TAKE THIS LINE OUTSIDE THE 'else:' BLOCK [AND REFER TO THE LAST LINE OF THE 'if:' BLOCK]
                    #TO KNOW THE ADDITIONAL TIME USED AFTER TIME'S UP
        
        

#///////////////*** WINDOW 2 ***///////////////////#
#COUNTDOWN TIME DISPLAY FRAME

#FRAMES - ACTIVITY & COUNTDOWN
frm_count = tk.Frame(window_2, bg = Timer_bgColour)
frm_count.pack(fill = tk.BOTH, expand = True)
        
#COUNTDOWN TIME ACTIVITY LABEL   
lbl_activity = tk.Label(frm_count, text = "", bg = actLabel_bg, relief = tk.GROOVE, borderwidth = 0, fg = Timer_fgColour, font = (font1, 45, "normal"))
lbl_activity.pack(fill = tk.X)

#COUNTDOWN TIME DISPLAY MAIN WINDOW (WINDOW 2)
fontsize = 350 #percentage(screenWidth, 25.62)
lbl_time = tk.Label(frm_count, text = TimerValue(ctd_Time), bg = Timer_bgColour, fg = Timer_fgColour, font = (timerFont, fontsize, "bold"))
lbl_time.pack(fill = tk.BOTH, expand = True, pady = 0)

#///////////////*** WINDOW 1 ***///////////////////#

ctrl_win_width = 64

#FRAME (GENERAL CONTAINER) FOR CONTROL COUNTDOWN TIME INPUT, ACTIVITY, SET/RESET BUTTON, START BUTTON
frm_win1CtrlWidgets = tk.Frame(window_1, width = ctrl_win_width, relief = tk.GROOVE, borderwidth = 5, bg = bg_colour)
frm_win1CtrlWidgets.pack(fill = None)

# >>> TITLES

frm_title = tk.Frame(frm_win1CtrlWidgets, )#relief = tk.RAISED, borderwidth = 3, bg = "#CCEEFF")
frm_title.pack()


lbl_titleA = tk.Label(frm_title, text = "CONTROLS", height = 2, width = ctrl_win_width // 2, bg = title_bgColour, fg = title_fgColour, font=(title_font, 16, "bold"))
lbl_titleA.pack(side=tk.LEFT, fill = tk.X, expand = True)

lbl_titleB = tk.Label(frm_title, text = "COUNTDOWN", height = 2, width = ctrl_win_width // 2, bg = title_bgColour, fg = title_fgColour, font=(title_font, 16, "bold"))
lbl_titleB.pack(side=tk.RIGHT, fill = tk.X, expand = True)

#--- END OF TITLES

#<>>>>>>>>><>| FRAME A |<>>>>><|*CONTROLS*|>>>>>>>><>
#A***FRAME (CONTAINER) FOR CONTROL/PROCESSES - INPUT & BUTTONS

frm_control = tk.Frame(frm_win1CtrlWidgets, width = 31, bg = "#DEDEDE")
frm_control.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

#A1***FRAME FOR INPUTS
frm_input = tk.Frame(frm_control, width = ctrl_win_width // 2, bg = "#C3C3C3")
frm_input.pack(side = tk.TOP,)# fill = tk.BOTH, expand = True)

#TIME INPUT
ent_Time = tk.Entry(frm_input, width = 5, bg = "#FAFFFF", font = (font1, 24))
ent_Time.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0)
ent_Time.insert(0, inputTimePlaceholder) #USER INPUT TIME PLACEHOLDER


#ACIVITY INPUT
ent_activity = tk.Entry(frm_input, width = 27, bg = "#FEFFFE", font = (font1, 20, "italic"))
ent_activity.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)
ent_activity.insert(0, "label")#"Your screen Resolution is: " + str(screenWidth) + " X " + str(screenHeight))

'''#PROGRESS BAR
progress_bar = ttk.Progressbar(frm_control, orient = "horizontal", length = 250, mode = "determinate", maximum = maxBar, value = progress_val)
progress_bar.pack(ipady = 8, expand=True)
#progress_bar.step(amount = 0.05)
'''
#FRAME FOR WATERMARK AND EXTRA TIME USED -- waex 
waexbg = "#C3C3C3"
frm_waex = tk.Frame(frm_control, bg = waexbg)
frm_waex.pack(fill = tk.BOTH, expand = True)

#EXTRA TIME USED
# "#FFFF0F" -- another option for fg
lbl_extratime = tk.Label(frm_waex, text = "", font = ("Calibri", 20, "normal"), bg = waexbg, fg = "#FFFF0F")
lbl_extratime.pack(side = tk.TOP, fill = tk.X, pady = 15)

#WATERMARK
info = "Email: rubycodes14@gmail.com\nTwitter: @_rubytech\n@rubycodes14"
lbl_wmark = tk.Label(frm_waex, text = info, font = (font1, 17, "normal"), bg = waexbg, fg = "#DADADA")
lbl_wmark.pack(side = tk.BOTTOM, pady = 15)

#A2***FRAME FOR SET/RESET AND START BUTTON
frm_process = tk.Frame(frm_control, bg = "#EDEDED")
frm_process.pack(side = tk.BOTTOM, fill = tk.BOTH,)

#SET/RESET BUTTON
# "#FFFF0F" "#FFAD00"
btn_setCtd = tk.Button(frm_process, text = "Set", bg = "#FFAD00", font = (btnFont, 30), command = setCtdTime)
btn_setCtd.grid(row = 0, column = 0, sticky = "s")# rowspan = 2)

#START BUTTON
btn_start = tk.Button(frm_process, text = "Start", bg = "#FF0000", font = (btnFont, 30), command = start)
btn_start.grid(row = 0, column = 1, sticky = "s")# rowspan = 2)

# BINDING THE ENTER KEY TO THE start FUNCTION/BUTTON
#window_1.bind('<Return>', start)  #NOT YET WORKING, THINK I HAVE TO CHANGE TO PURE OOP
                                  #GIVES ERROR: TypeError: start() takes 0 positional arguments but 1 was given



#<>>>>>>>>><>| FRAME B |<>>>>><|*TIMER*|>>>>>>>><>
#B***FRAME (CONTAINER) FOR COUNTDOWN ****

frm_countdown = tk.Frame(frm_win1CtrlWidgets, width = ctrl_win_width // 2, bg = Timer_bgColour)#bg_colour)
frm_countdown.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

#COUNTDOWN TIME DISPLAY (WINDOW 1)
lbl_activityWin1 = tk.Label(frm_countdown, text = "Your label will appear here!", fg = "#000000", bg = Timer_bgColour, font = (font1, 15, "normal"))
lbl_activityWin1.pack(ipady = 7)

lbl_timeWin1 = tk.Label(frm_countdown, text = TimerValue(ctd_Time), width = 10, height = 5, bg = Timer_bgColour, fg = Timer_fgColour, font = (timerFont, 80, "bold"))
lbl_timeWin1.pack()#fill = tk.BOTH, expand = True)

window_1.mainloop()
