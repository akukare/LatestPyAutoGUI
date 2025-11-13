"""sample  creo launch and redirected to web """

import os
import sys
import time
import logging
import subprocess
from pathlib import Path

try:
    import pyautogui
    HAVE_PYAUTOGUI = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.2
except Exception:
    HAVE_PYAUTOGUI = False

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


#CONFIG 
APP_PATH = r"C:\Users\60165\Downloads\MED-100WIN-CD-490_12-4-0-0_Win64\setup.exe"
WINDCHILL_HOST = "plmtvdr3.plmtestlab.com"  
CHROMEDRIVER_PATH = r"C:\Tools\drivers\chromedriver.exe"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("creo_setup_to_windchill.log", mode="w"), logging.StreamHandler(sys.stdout)],
)


def open_application(app_path: str) -> subprocess.Popen:
    exe = Path(app_path)
    if not exe.exists():
        raise FileNotFoundError(f"Executable not found: {exe}")
    logging.info(f"Launching application: {exe}")
    # Use list form (no shell) so spaces in path are safe
    proc = subprocess.Popen([str(exe)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
    return proc

def close_window(proc: subprocess.Popen, use_alt_f4: bool = True, kill_after: float = 5.0) -> None:
    """
    Try to close the foreground window via Alt+F4 (if available), then ensure the process exits.
    """
    if use_alt_f4 and HAVE_PYAUTOGUI:
        logging.info("Closing window via Alt+F4…")
   
        time.sleep(0.4)
        try:
            pyautogui.hotkey("alt", "f4")
        except Exception as e:
            logging.warning(f"Alt+F4 failed: {e}")

    
    if proc and proc.poll() is None:
        logging.info("Terminating launcher process…")
        proc.terminate()
        try:
            proc.wait(timeout=kill_after)
        except subprocess.TimeoutExpired:
            logging.warning("Force-killing process…")
            proc.kill()

def make_driver() -> webdriver.Chrome:
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    opts.add_argument("--start-maximized")  
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    driver.set_page_load_timeout(60)
    return driver

def to_url(host: str) -> str:
    host = host.strip()
    if host.startswith("http://") or host.startswith("https://"):
        return host
    
    return f"https://{host}"


def run():
    if os.name != "nt":
        logging.warning("This script targets Windows; paths/closing may need changes on other OSes.")

    # Launcher
    proc = open_application(APP_PATH)

    logging.info("Waiting 5 seconds for installer window…")
    time.sleep(5)

    close_window(proc, use_alt_f4=True, kill_after=5)
    url = to_url(WINDCHILL_HOST)
    logging.info(f"Opening Windchill: {url}")
    driver = make_driver()
    try:
        driver.get(url)
  
        time.sleep(5)
    finally:
        driver.quit()
        logging.info("Done.")

if __name__ == "__main__":
    run()
