'''
ATTENTION USER
When you run this code, on the timer control display, there's a label Current Year | Timer:
default: here you enter the current year, default year is 2021
auto: here you can it is recommmended you leave it as it is - it uses the epoch timing for the countdown; and if need be, 
you enter the total time in minutes to round up the current year.
'''
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
get_auto_timer_once = True
get_manual_timer_once = True
def get_timer_value():
    epochTime = time.time()
    realTime = time.gmtime(epochTime)

    _hr = (realTime[3] + 1) * 60 * 60
    _min = realTime[4] * 60
    _sec = realTime[5]

    curr_time_in_secs = _hr + _min + _sec
    
    _timer = ((24 * 60 * 60) - curr_time_in_secs)
    
    return _timer

#WINDOW 1 - CONTROL WINDOW: TIME INPUT, ACTIVITY INPUT, SET/RESET BUTTON, START BUTTON
window_1 = tk.Tk()
window_1.title("RubyCodes - New Year Countdown Timer (c) 2021")
window_1.iconbitmap("clock.ico")
window_1.geometry("780x540+300+25")
window_1.minsize(780, 540)
window_1.configure(bg = "#000000")
window_1.resizable(False, False)
#window_1.lift()


# ********WINDOW 2 - COUNTDOWN DISPLAY & ACTIVITY DISPLAY ****************** #
window_2 = tk.Toplevel(window_1)
window_2.title("Countdown Timer - RubyCodes(c)")
window_2.iconbitmap("clock.ico")
window_2.minsize(720, 640)
window_2.configure(bg = bg_colour)

screenWidth = window_2.winfo_screenwidth()
screenHeight = window_2.winfo_screenheight()

#window_2.geometry("600x480+0+0")    #FOR SINGLE SCREEN, NOT EXTENDING

control_win_frm = tk.Frame(window_1, bg="#ffffff")
control_win_frm.pack(fill = tk.BOTH, expand = True)

# ********* FOR USING AN EXTENDED SCREEN **********
#window_2.geometry(str(screenWidth) + "x" + str(screenHeight) + "+" + str(screenWidth) + "+0")
window_2.geometry(f"{screenWidth}x{screenHeight}+{screenWidth}+0")  #FOR USING AN EXTENDED SCREEN:
                                                                                            #MOVES THE WINDOW TO AN EXTENDED SCREEN BY A SPECIFIED WIDTH
window_2.overrideredirect(1) #REMOVES THE TOP BADGE OF THE WINDOW - NO DRAGGING, NO BUTTONS, HIDES TASKBAR

#********* ****************

# ********* FOR FULL SCREEN/MAXIMIZING WINDOW **********
#maximize_window()
#window_2.attributes("-fullscreen", True)

# ********* ****************

#window_2.lower(window_1)  #THIS WOULD NOT ALLOW THE GEOMETRY POSITION [+screenWidth+50] OF THE WINDOW [window_2] WORK
#window_1.protocol("WM_DELETE_WINDOW", closewindows()) #DOESN'T WORK YET

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
timer_type = "default | auto"
timerType_ = f"{timer_type}"
current_year = 2021
inputTimePlaceholder = timerType_
## FLAGS
alarm_flag = 0    # NO NEED FOR CHANGING - DO NOT CHANGE
blinker_flag = 0  # NO NEED FOR CHANGING - DO NOT CHANGE
continuous = 5    # THE ALARM SOUNDS THE NUMBER OF INTEGER GIVEN OR CONTINUOUSLY IF True, NO ALARM IF False
timeup = False   # THIS DECIDES WETHER THE TIMER SHOULD RUN OR  NOT, TO BE ABLE TO STOP RECURSIVE LOOP THAT OCCURS OF CLICKING 'START' WHEN TIME'S UP

newYearText = f"HAPPY\nNEW YEAR\n==\n{current_year + 1}"
newYearLabel = f"Welcome to {current_year + 1}"
timeupText = newYearText #"TIME'S UP"

timer_reset = False
showColourWarning = True   #set_timer_colour() flag, to control showing Warning message if its cancel button or set button
#label = ""

def get_current_year_and_timer():
    global current_year, ctd_Time, newYearLabel
    
    _inputs = ent_Time.get().split("|")
    if _inputs[0].strip() == "default":
        current_year = current_year
    else:
        current_year = int(_inputs[0])
    

    if _inputs[-1].strip() == "auto":
        ctd_Time = get_timer_value()

    else:
        ctd_Time = convertTo_Seconds(_inputs[-1]) #USER INPUT TIME
        
        
    
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

def reset_notif(event=None):
    messagebox.showinfo(message="Time's Up! Reset Time")

#CUSTOMIZED TIME'S UP TEXT
def customizedText(userInput):
    global timeupText
    output = newYearText
    if "!" in userInput:
        userInput = userInput[0:label.index("!")]
            
    if "#" in userInput:
        output = userInput[userInput.index("#"):]  
        if len(output) > 8:
            messagebox.showinfo(message="Maximum Length of 8 characters for time up exceeded.")
            timeupText = newYearText
        else:
            timeupText = output
    else:
        timeupText = newYearText

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
timer_is_running = False  # TIMER LOOP FLAG


def showWidgets():
    lbl_new_year.grid(row=0, column=0, sticky = "w")
    ent_Time.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0)
    ent_activity.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)
    btn_setCtd.grid(row = 0, column = 0, rowspan = 2)
    btn_start.grid(row = 0, column = 1, rowspan = 2)

def setCtdTime(event=None):
    global timer_is_running, ctd_Time, delayTime, alarm_flag, label, get_auto_timer_once, get_manual_timer_once, timer_type, current_year, newYearLabel, newYearText#, prevCount
    timer_type = ent_Time.get()
    get_auto_timer_once, get_manual_timer_once = True, True
    delayTime = 1000
    alarm_flag = 0
    btn_start["command"] = start    # RETURNS start FUNCTION BACK TO ITS BUTTON, IT WAS CHANGED WHILE ON TIME'S UP
    window_1.bind("<Return>", start)
    
    
    get_current_year_and_timer()
    newYearText = f"HAPPY\nNEW YEAR\n_______________\n\::. {current_year + 1} .::/\n**************"
    newYearLabel = f"Welcome to {current_year + 1}"
    ent_activity.delete(0, tk.END)
    ent_activity.insert(0, f"We're ending {current_year} in...")
    lbl_activity["text"] = newYearLabel.upper()
    lbl_activityWin1["text"] = newYearLabel.upper()

    label = getLabel(ent_activity.get())
    label_length_exceeded = False
    #timeup = False  #TIME IS BEEN SET
    #timer_reset = True
    #maximize_window()
    
    customizedText(label)
    customizedColour(label)
    set_timer_colour()
    if timer_is_running:   #IF TIMER IS RUNNING ALREADY AND 'CANCEL->[SET/RESET]' BUTTON IS CLICKED
        control_win_frm.after_cancel(loop)     # THIS WILL ALSO CANCEL THE BLINKER IF 'TIME'S UP' IS BLINKING   
        showWidgets()
        btn_setCtd["text"] = "Reset"
        btn_setCtd["bg"] = "#FFAD00"
    
        
    prevCount = ctd_Time
    
    if len(label) > 30:
            messagebox.showinfo(message="Maximum Length of 30 characters for label exceeded.\n(Remove trailing whitespaces if any).")
            lbl_activityWin1["text"] = ""
            lbl_activity["text"] == ""
            label_length_exceeded = not(False)
    else:
        lbl_activity["text"] = label.upper() #USER INPUT ACTIVITY
        lbl_activityWin1["text"] = label.upper() #FOR WINDOW 1 - CONTROL WINDOW
        
    lbl_timeWin1["font"] = (timerFont, 80, "bold")

    
    if label_length_exceeded:
        #lbl_activity["bg"] = Timer_bgColour
        lbl_activity.pack_forget()
        lbl_activityWin1["text"] = "LABEL COULD NOT BE DISPLAYED"
    else:
        #lbl_activity["bg"] = actLabel_bg
        lbl_activity.pack(side = tk.TOP, fill = tk.X)
    lbl_time["text"] = TimerValue(ctd_Time)
    lbl_timeWin1["text"] = TimerValue(ctd_Time)  #FOR CONTROL WINDOW
    lbl_time["font"] = (timerFont, 350, "bold")     #THE FONT SIZE IS IN PIXELS AND HOW BIG IT IS (IN SIZE) DEPENDS ON THE SIZE OF THE COMPUTER IT'S RUNNING ON
    #lbl_time["fg"] = Timer_fgColour
    lbl_time.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True, pady = 0)
    #EXTRA TIME LABEL
    lbl_extratime.pack_forget()

    
#TIMER START FUNCTION

def start(event=None):    
    global delayTime, ctd_Time, loop, timer_is_running, timeupText, showColourWarning, get_auto_timer_once, get_manual_timer_once, timer_type, newYearLabel, current_year

    if timer_type == "default | auto":
        if get_auto_timer_once:
            label = getLabel(ent_activity.get())
            ctd_Time = get_timer_value()
            get_auto_timer_once = False
    else:
        _inputs = ent_Time.get().split("|")
        if get_manual_timer_once:
            ctd_Time = convertTo_Seconds(_inputs[-1])
            get_manual_timer_once = False
        
    loop = control_win_frm.after(delayTime, start)  #COUNTER 1000 MS (1.0 x 10^-3 Secs)
    #if not(timer_is_running):
        #lbl_activityWin1["text"] = "NO LABEL ENTERED FOR THIS TIMER"
    timer_is_running = True
    if lbl_activity["text"] == "":
        #lbl_activity["bg"] = Timer_bgColour
        lbl_activity.pack_forget()
        lbl_activityWin1["text"] = "NO TIMER LABEL"
    else:
        #lbl_activity["bg"] = actLabel_bg
        lbl_activity.pack(side = tk.TOP, fill = tk.X)
        
        
    if ctd_Time < 0:
        delayTime = 500  #REDUCE THIS TO INCREASE THE SPEED OF BLINKING
                        #ORIGINAL DELAY TIME = 1000 --> LINE 78 & 291
        #KEY BINDINGS/UNBINDINGS
        btn_start["command"] = reset_notif #THIS IS NECESSARY FOR BOTH RESET WARNUNG AND AVOIDING RECURSIVE LOOP OF 'start' FUNCTION
        window_1.bind("<Return>", reset_notif)
        lbl_activity["text"] = newYearLabel.upper()
        lbl_activityWin1["text"] = newYearLabel.upper()
        ent_activity.delete(0, tk.END)
        ent_activity.insert(0, newYearLabel)
        
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
        
        if ctd_Time <= -10800:   # 3600 == 60 MINUTES (WOULD BE REDUCED LATER TO 30 MINUTES --> 5 LINES FROM HERE (CHECK LINE 382)
            control_win_frm.after_cancel(loop)  # REMOVE THIS LINE AND REFER TO THE LAST LINE OF 'else:' BLOCK BELOW
                                    # TO KNOW THE ADDITIONAL TIME USED AFTER TIME'S UP,
        #EXTRA TIME USED
        xtime = int(abs(ctd_Time/2))    # THE DIVISOR (2) HERE IS NOT A BUG - RECALL (LINE 355) THE COUNTDOWN TIME WAS REDUCED TO 0.5 SECONDS - SO 2x0.5 GIVES 1SEC
        mins_ = xtime // 60             # PAY ATTENTION TO THE OPERATOR USED HERE (INTEGER DIVISION)
        secs_ = xtime % 60              # THE ctd_Time VARIABLE WAS DIVIDED BY 2 AND TYPECASTED, SO [1sec = int(0.5)sec = 0sec] AT THE SPEED OF 0.5 SECS
        xtimeTxt0 = ""
        txt0 = f"{current_year} ended"#with previous " + str(prevCount)
        if mins_ >= 60:
            xtimeTxt0 = "More than\n"
        #FOR MINUTES ONLY
        if mins_ < 2:
            xtimeTxt1 = xtimeTxt0 + str(mins_) + " min "   #SINGULAR min
        else:
            xtimeTxt1 = xtimeTxt0 + str(mins_) + " mins "   #PLURAL mins
        
        lbl_extratime["text"] = f"{txt0}\n{xtimeTxt1} {secs_} secs\nago"
        lbl_wmark.pack_forget()
        lbl_extratime.pack(side = tk.TOP, fill = tk.X, pady = 15)
        lbl_wmark.pack(side = tk.BOTTOM, pady = 15)
        
    else:
        window_1.unbind("<Return>")
        window_1.focus()#btn_setCtd.focus() TO AVOID ADDING EXTRA UNECESSSARY WHITESPACE TO THE LAST TEXTBOX EDITED BEFORE STARTING THE TIMER
        #window_1.bind("<space>", setCtdTime)
        
        lbl_time["text"] = TimerValue(ctd_Time)  #MAIN COUNTDOWN DISPLAY WINDOW
        lbl_timeWin1["text"] = TimerValue(ctd_Time)  #FOR CONTROL WINDOW
        lbl_time["font"] = (timerFont, 350, "bold")
        lbl_new_year.grid_forget()
        ent_Time.grid_forget()
        ent_activity.grid_forget()
        btn_start.grid_forget()
        #EXTRA TIME USED
        lbl_extratime.pack_forget()

        showColourWarning = False     #set_timer_colour() flag, to control showing Warning message if its cancel button or set button
        btn_setCtd["text"] = "Cancel"
        btn_setCtd["bg"] = "#C3C3C3"
            
    ctd_Time -= 1    #COUNTDOWN BY 1 SECOND - TAKE THIS LINE OUTSIDE THE 'else:' BLOCK [AND REFER TO THE LAST BUT FIRST LINE OF THE THIRD 'if:' BLOCK ABOVE]
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
fontsize = 320 #percentage(screenWidth, 25.62)
lbl_time = tk.Label(frm_count, text = TimerValue(get_timer_value()), bg = Timer_bgColour, fg = Timer_fgColour, font = (timerFont, fontsize, "bold"))
lbl_time.pack(fill = tk.BOTH, expand = True, pady = 0)

#///////////////*** WINDOW 1 ***///////////////////#

ctrl_win_width = 80

#FRAME (GENERAL CONTAINER) FOR CONTROL COUNTDOWN TIME INPUT, ACTIVITY, SET/RESET BUTTON, START BUTTON
frm_win1CtrlWidgets = tk.Frame(control_win_frm, width = ctrl_win_width, relief = tk.GROOVE, borderwidth = 5, bg = bg_colour)
frm_win1CtrlWidgets.pack(fill = None)

# >>> TITLES

frm_title = tk.Frame(frm_win1CtrlWidgets, )#relief = tk.RAISED, borderwidth = 3, bg = "#CCEEFF")
frm_title.pack()


lbl_titleA = tk.Label(frm_title, text = "CONTROLS", height = 2, width = ctrl_win_width // 2, bg = title_bgColour, fg = title_fgColour, font=(title_font, 16, "bold"))
lbl_titleA.pack(side=tk.LEFT, fill = tk.X, expand = True)

lbl_titleB = tk.Label(frm_title, text = "YEAR COUNTDOWN", height = 2, width = ctrl_win_width // 2, bg = title_bgColour, fg = title_fgColour, font=(title_font, 16, "bold"))
lbl_titleB.pack(side=tk.RIGHT, fill = tk.X, expand = True)

#--- END OF TITLES

#<>>>>>>>>><>| FRAME A |<>>>>><|*CONTROLS*|>>>>>>>><>
#A***FRAME (CONTAINER) FOR CONTROL/PROCESSES - INPUT & BUTTONS

frm_control = tk.Frame(frm_win1CtrlWidgets, width = 31, bg = "#DEDEDE")
frm_control.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

#A1***FRAME FOR INPUTS
frm_input = tk.Frame(frm_control, width = ctrl_win_width // 2, bg = "#C3C3C3")
frm_input.pack(side = tk.TOP,)# fill = tk.BOTH, expand = True)

#YEARLABEL
lbl_new_year = tk.Label(frm_input, text="::. Current Year | Timer  <>", bg = "#C3C3C3", font = (font1, 15))
lbl_new_year.grid(row=0, column=0, sticky = "w")
#TIME INPUT
ent_Time = tk.Entry(frm_input, width = 11, bg = "#FAFFFF", font = (font1, 18))
ent_Time.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0)
ent_Time.insert(0, inputTimePlaceholder) #USER INPUT TIME PLACEHOLDER


#ACIVITY INPUT
ent_activity = tk.Entry(frm_input, width = 27, bg = "#FEFFFE", font = (font1, 20, "italic"))
ent_activity.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)
ent_activity.insert(0, f"We're ending {current_year} in...")#"Your screen Resolution is: " + str(screenWidth) + " X " + str(screenHeight))

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
window_1.bind("<Return>", start)
window_1.bind("<space>", setCtdTime)

#<>>>>>>>>><>| FRAME B |<>>>>><|*TIMER*|>>>>>>>><>
#B***FRAME (CONTAINER) FOR COUNTDOWN ****

frm_countdown = tk.Frame(frm_win1CtrlWidgets, width = ctrl_win_width // 2, bg = Timer_bgColour)#bg_colour)
frm_countdown.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

#COUNTDOWN TIME DISPLAY (WINDOW 1)
lbl_activityWin1 = tk.Label(frm_countdown, text = "WE'RE ROUNDING UP 2021 IN...", fg = "#000000", bg = Timer_bgColour, font = (font1, 15, "normal"))
lbl_activityWin1.pack(ipady = 7)

lbl_timeWin1 = tk.Label(frm_countdown, text = TimerValue(get_timer_value()), width = 10, height = 5,
                        bg = Timer_bgColour, fg = Timer_fgColour, font = (timerFont, 80, "bold"))
lbl_timeWin1.pack()#fill = tk.BOTH, expand = True)

window_1.mainloop()
