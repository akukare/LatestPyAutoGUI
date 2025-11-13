import pyautogui
import subprocess
import time
import os, sys


sys.path.append(os.path.dirname(os.path.dirname(__file__))
                
CREO_PATH = r"C:\Program Files\PTC\Creo 12.4.0.0\Parametric\bin\parametric.exe"

class windchill:
    def __init__(self):
        pyautogui.FAILSAFE = True  # Enable fail-safe
        pyautogui.PAUSE = 1   