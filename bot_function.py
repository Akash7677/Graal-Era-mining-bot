import ctypes
import random
import time

import pyautogui

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))




def drill(trigger, total_time):
    count = 0
    time_div = round(total_time / 3)
    while count < 3:
        try:
            check_ok_button()
            print("Drilling...")
            PressKey(trigger)
            time.sleep(2)
            ReleaseKey(trigger)
            # click_ok_button()
            time.sleep(random.randint(time_div-1,time_div+2))
            count += 1
        except KeyboardInterrupt as e:
            print(e)
            break
def move(inp,wall_side):
    PressKey(inp)
    print("moving...")
    time.sleep(0.1)
    ReleaseKey(inp)
    time.sleep(0.1)
    PressKey(wall_side)
    time.sleep(0.1)
    ReleaseKey(wall_side)
    # time.sleep(0.1)

def switch_corner(inp):
    PressKey(inp)
    print("Switched corner...")
    time.sleep(0.05)
    ReleaseKey(inp)
    time.sleep(0.05)

def check_ok_button():
    try:
        ok_button_location = pyautogui.locateOnScreen('button.png', confidence=0.7)
        time.sleep(1)
        if ok_button_location:
            ok_button_center = pyautogui.center(ok_button_location)
            pyautogui.click(ok_button_center)
            print("Pop up message detected.... OK pressed, exiting....")
            exit()
    except pyautogui.ImageNotFoundException:
        pass  # Continue with the program if the image is not found


